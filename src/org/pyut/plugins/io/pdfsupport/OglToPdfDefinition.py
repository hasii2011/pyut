
from typing import cast
from typing import List
from typing import final

from logging import Logger
from logging import getLogger

from pdfdiagrams.Definitions import ClassDefinition
from pdfdiagrams.Definitions import ClassDefinitions
from pdfdiagrams.Definitions import DefinitionType
from pdfdiagrams.Definitions import MethodDefinition
from pdfdiagrams.Definitions import Methods
from pdfdiagrams.Definitions import ParameterDefinition
from pdfdiagrams.Definitions import Parameters
from pdfdiagrams.Definitions import Position
from pdfdiagrams.Definitions import Size
from pdfdiagrams.Definitions import UmlLineDefinition
from pdfdiagrams.Definitions import UmlLineDefinitions
from pdfdiagrams.Definitions import LineType

from pdfdiagrams.Diagram import Diagram

from org.pyut.MiniOgl.AnchorPoint import AnchorPoint

from org.pyut.model.PyutClass import PyutClass
from org.pyut.model.PyutLink import PyutLink
from org.pyut.model.PyutMethod import PyutMethod
from org.pyut.model.PyutVisibilityEnum import PyutVisibilityEnum

from org.pyut.ogl.OglClass import OglClass
from org.pyut.ogl.OglLink import OglLink

from org.pyut.enums.LinkType import LinkType


class OglToPdfDefinition:

    INHERITANCE_DESTINATION_POSITION_NUDGE_FACTOR: final = 1

    def __init__(self, fqFileName: str, dpi: int):

        self.logger:              Logger           = getLogger(__name__)
        self._classDefinitions:   ClassDefinitions = []
        self._umlLineDefinitions: UmlLineDefinitions = []
        self._diagram:            Diagram = Diagram(fileName=fqFileName, dpi=dpi)

    def toClassDefinitions(self, oglObjects: List[OglClass]):

        classDefinitions: ClassDefinitions = []

        for umlObject in oglObjects:

            umlObject: OglClass  = cast(OglClass, umlObject)
            if not isinstance(umlObject, OglClass):
                continue

            pyutClass: PyutClass = umlObject.getPyutObject()

            x, y = umlObject.GetPosition()
            w, h = umlObject.GetSize()
            position: Position = Position(x=x, y=y)
            size: Size = Size(width=int(w), height=int(h))
            classDefinition: ClassDefinition = ClassDefinition(name=pyutClass.name, position=position, size=size)
            self._addMethods(classDefinition=classDefinition, pyutClass=pyutClass)
            self._diagram.drawClass(classDefinition=classDefinition)
            classDefinitions.append(classDefinition)

        self._classDefinitions = classDefinitions

    def layoutLines(self, oglObjects: List[OglClass]):

        umlLineDefinitions: UmlLineDefinitions = []

        for umlObject in oglObjects:

            if not isinstance(umlObject, OglLink):
                continue
            oglLink: OglLink = cast(OglLink, umlObject)

            pyutLink:    PyutLink = oglLink.getPyutObject()
            umlLinkType: LinkType = pyutLink.linkType
            lineType:    LineType = self._toPdfLineType(umlLinkType)

            destinationPosition, sourcePosition = self._toPdfPositions(oglLink)
            self.logger.info(f'{lineType=} {sourcePosition=} {destinationPosition=}')
            line:    UmlLineDefinition = UmlLineDefinition(source=sourcePosition, destination=destinationPosition, lineType=lineType)

            self._diagram.drawUmlLine(lineDefinition=line)
            umlLineDefinitions.append(line)

        self._umlLineDefinitions = umlLineDefinitions

    def write(self):
        self._diagram.write()

    def _toPdfLineType(self, umlLinkType) -> LineType:

        if umlLinkType == LinkType.INHERITANCE:
            lineType: LineType = LineType.Inheritance
        elif umlLinkType == LinkType.COMPOSITION:
            lineType: LineType = LineType.Composition
        elif umlLinkType == LinkType.AGGREGATION:
            lineType: LineType = LineType.Aggregation
        else:
            lineType: LineType = LineType.Association   # This won't happen yet

        return lineType

    def _toPdfPositions(self, oglLink):

        srcAnchor:  AnchorPoint = oglLink.sourceAnchor
        destAnchor: AnchorPoint = oglLink.destinationAnchor

        srcX,  srcY  = srcAnchor.GetPosition()
        destX, destY = destAnchor.GetPosition()

        sourcePosition:      Position = Position(x=srcX, y=srcY)
        destinationPosition: Position = Position(x=destX, y=destY)

        return destinationPosition, sourcePosition

    def _addMethods(self, classDefinition: ClassDefinition, pyutClass: PyutClass) -> ClassDefinition:

        methods: Methods = []
        for pyutMethod in pyutClass.methods:

            pyutMethod: PyutMethod = cast(PyutMethod, pyutMethod)

            methodDef: MethodDefinition = MethodDefinition(name=pyutMethod.name)
            methodDef.visibility = self.__toDefinitionType(pyutMethod.visibility)
            methodDef.returnType = pyutMethod.returnType.value

            self.__addParameters(methodDefinition=methodDef, pyutMethod=pyutMethod)
            methods.append(methodDef)

        classDefinition.methods = methods
        return classDefinition

    def __addParameters(self, methodDefinition: MethodDefinition, pyutMethod: PyutMethod) -> MethodDefinition:

        parameters: Parameters = []
        for parameter in pyutMethod.parameters:

            paramDef: ParameterDefinition = ParameterDefinition(name=parameter.name)
            paramDef.parameterType = parameter.type.value
            paramDef.defaultValue  = parameter.defaultValue

            parameters.append(paramDef)

        methodDefinition.parameters = parameters
        self.logger.info(f'{methodDefinition.name=}  {parameters=}')
        return methodDefinition

    def __toDefinitionType(self, visibility: PyutVisibilityEnum) -> DefinitionType:

        if visibility == PyutVisibilityEnum.PUBLIC:
            return DefinitionType.Public

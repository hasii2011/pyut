
from typing import cast
from typing import List
from typing import final

from logging import Logger
from logging import getLogger

from time import localtime
from time import strftime

from pyumldiagrams.Definitions import ClassDefinition
from pyumldiagrams.Definitions import ClassDefinitions
from pyumldiagrams.Definitions import DefinitionType
from pyumldiagrams.Definitions import LinePositions
from pyumldiagrams.Definitions import MethodDefinition
from pyumldiagrams.Definitions import Methods
from pyumldiagrams.Definitions import ParameterDefinition
from pyumldiagrams.Definitions import Parameters
from pyumldiagrams.Definitions import Position
from pyumldiagrams.Definitions import Size
from pyumldiagrams.Definitions import UmlLineDefinition
from pyumldiagrams.Definitions import UmlLineDefinitions
from pyumldiagrams.Definitions import LineType

from pyumldiagrams.image.ImageDiagram import ImageDiagram

from pyumldiagrams.pdf.PdfDiagram import PdfDiagram

from org.pyut.MiniOgl.AnchorPoint import AnchorPoint
from org.pyut.MiniOgl.ControlPoint import ControlPoint

from org.pyut.model.PyutClass import PyutClass
from org.pyut.model.PyutLink import PyutLink
from org.pyut.model.PyutMethod import PyutMethod
from org.pyut.model.PyutVisibilityEnum import PyutVisibilityEnum

from org.pyut.ogl.OglClass import OglClass
from org.pyut.ogl.OglLink import OglLink

from org.pyut.enums.LinkType import LinkType

from org.pyut.plugins.io.pyumlsupport.ImageFormat import ImageFormat
from org.pyut.plugins.io.pyumlsupport.ImageOptions import ImageOptions


class OglToPyUmlDefinition:

    INHERITANCE_DESTINATION_POSITION_NUDGE_FACTOR: final = 1

    def __init__(self, imageOptions: ImageOptions, dpi: int = 0, pyutVersion: str = '', pluginVersion: str = ''):
        """

        Args:
            imageOptions: Lots of information on how to draw the diagram

            dpi:  Dots per inch;  Only used in PDF generation;  Image generation is in pixels

            pyutVersion:  Information for header

            pluginVersion:  Information for header
        """

        self.logger:              Logger             = getLogger(__name__)
        self._classDefinitions:   ClassDefinitions   = []
        self._umlLineDefinitions: UmlLineDefinitions = []

        today: str = strftime("%d %b %Y %H:%M:%S", localtime())
        headerText: str = f'Pyut Version {pyutVersion} Plugin Version {pluginVersion} - {today}'

        fqFileName:  str         = imageOptions.outputFileName
        imageFormat: ImageFormat = imageOptions.imageFormat
        if imageFormat == ImageFormat.PDF:
            self._diagram: PdfDiagram = PdfDiagram(fileName=fqFileName, dpi=dpi, headerText=headerText)
        else:
            self._diagram: ImageDiagram = ImageDiagram(fileName=fqFileName,
                                                       headerText=headerText   # TODO use image size from new method signature
                                                       )

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
            lineType:    LineType = self._toPyUmlLineType(umlLinkType)

            linePositions: LinePositions  = self._toPyUmlPositions(oglLink, umlLinkType)
            self.logger.info(f'{lineType=} {linePositions=}')

            line:    UmlLineDefinition = UmlLineDefinition(lineType=lineType, linePositions=linePositions)

            self._diagram.drawUmlLine(lineDefinition=line)
            umlLineDefinitions.append(line)

        self._umlLineDefinitions = umlLineDefinitions

    def write(self):
        self._diagram.write()

    def _toPyUmlLineType(self, umlLinkType) -> LineType:

        if umlLinkType == LinkType.INHERITANCE:
            lineType: LineType = LineType.Inheritance
        elif umlLinkType == LinkType.COMPOSITION:
            lineType: LineType = LineType.Composition
        elif umlLinkType == LinkType.AGGREGATION:
            lineType: LineType = LineType.Aggregation
        else:
            lineType: LineType = LineType.Association   # This won't happen yet

        return lineType

    def _toPyUmlPositions(self, oglLink, pyutLinkType: LinkType) -> LinePositions:

        if pyutLinkType == LinkType.INHERITANCE:
            srcAnchor:  AnchorPoint = oglLink.sourceAnchor
            destAnchor: AnchorPoint = oglLink.destinationAnchor
        else:
            srcAnchor:  AnchorPoint = oglLink.destinationAnchor
            destAnchor: AnchorPoint = oglLink.sourceAnchor

        srcX,  srcY  = srcAnchor.GetPosition()
        destX, destY = destAnchor.GetPosition()

        sourcePosition:      Position = Position(x=srcX, y=srcY)
        destinationPosition: Position = Position(x=destX, y=destY)

        bends: List[ControlPoint] = oglLink.GetControlPoints()
        if bends is None or len(bends) == 0:
            linePositions: LinePositions = [sourcePosition, destinationPosition]
        else:
            linePositions: LinePositions = [sourcePosition]
            for bend in bends:
                bend: ControlPoint = cast(ControlPoint, bend)
                self.logger.info(f'{bend:}')

                bendX, bendY = bend.GetPosition()
                bendPosition: Position = Position(x=bendX, y=bendY)
                linePositions.append(bendPosition)

            linePositions.append(destinationPosition)

        return linePositions

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

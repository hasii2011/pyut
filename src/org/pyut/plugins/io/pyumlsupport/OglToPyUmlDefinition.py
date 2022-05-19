
from typing import cast
from typing import List

from logging import Logger
from logging import getLogger

from time import localtime
from time import strftime

from pyumldiagrams.BaseDiagram import BaseDiagram
from pyumldiagrams.Definitions import ClassDefinition
from pyumldiagrams.Definitions import ClassDefinitions
from pyumldiagrams.Definitions import DefinitionType
from pyumldiagrams.Definitions import DisplayMethodParameters
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

from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutLink import PyutLink
from pyutmodel.PyutMethod import PyutMethod
from pyutmodel.PyutVisibilityEnum import PyutVisibilityEnum
from pyutmodel.PyutLinkType import PyutLinkType

from miniogl.AnchorPoint import AnchorPoint
from miniogl.ControlPoint import ControlPoint

from org.pyut.ogl.OglClass import OglClass
from org.pyut.ogl.OglLink import OglLink


from org.pyut.plugins.io.pyumlsupport.ImageFormat import ImageFormat
from org.pyut.plugins.io.pyumlsupport.ImageOptions import ImageOptions

from org.pyut.preferences.PyutPreferences import PyutPreferences


class OglToPyUmlDefinition:

    INHERITANCE_DESTINATION_POSITION_NUDGE_FACTOR: int = 1

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
        self._prefs:              PyutPreferences    = PyutPreferences()

        today: str = strftime("%d %b %Y %H:%M:%S", localtime())
        headerText: str = f'Pyut Version {pyutVersion} Plugin Version {pluginVersion} - {today}'

        fqFileName:  str         = imageOptions.outputFileName
        imageFormat: ImageFormat = imageOptions.imageFormat
        imageLibShowParameters: DisplayMethodParameters = self.__toImageLibraryEnum(self._prefs.showParameters)
        if imageFormat == ImageFormat.PDF:
            self._diagram: BaseDiagram = PdfDiagram(fileName=fqFileName, dpi=dpi, headerText=headerText, docDisplayMethodParameters=imageLibShowParameters)
        else:
            self._diagram = ImageDiagram(fileName=fqFileName, headerText=headerText)   # TODO use image size from new method signature)

    def toClassDefinitions(self, oglObjects: List[OglClass]):

        classDefinitions: ClassDefinitions = []

        for oglObject in oglObjects:

            umlObject: OglClass  = cast(OglClass, oglObject)
            if not isinstance(umlObject, OglClass):
                continue

            pyutClass: PyutClass = cast(PyutClass, umlObject.pyutObject)

            x, y = umlObject.GetPosition()
            w, h = umlObject.GetSize()
            position: Position = Position(x=x, y=y)
            size:     Size     = Size(width=int(w), height=int(h))

            classDefinition: ClassDefinition = ClassDefinition(name=pyutClass.name, position=position, size=size)

            if pyutClass.displayParameters is True:
                classDefinition.displayMethodParameters = DisplayMethodParameters.DISPLAY
            else:
                classDefinition.displayMethodParameters = DisplayMethodParameters.DO_NOT_DISPLAY

            classDefinition = self.__addClassDiagramDisplayPreferences(pyutClass=pyutClass, classDefinition=classDefinition)

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

            pyutLink:    PyutLink = oglLink.pyutObject
            umlLinkType: PyutLinkType = pyutLink.linkType
            lineType:    LineType = self._toPyUmlLineType(umlLinkType)

            linePositions: LinePositions  = self._toPyUmlPositions(oglLink, umlLinkType)
            self.logger.debug(f'{lineType=} {linePositions=}')

            line:    UmlLineDefinition = UmlLineDefinition(lineType=lineType, linePositions=linePositions)

            self._diagram.drawUmlLine(lineDefinition=line)
            umlLineDefinitions.append(line)

        self._umlLineDefinitions = umlLineDefinitions

    def write(self):
        self._diagram.write()

    def _toPyUmlLineType(self, umlLinkType) -> LineType:

        if umlLinkType == PyutLinkType.INHERITANCE:
            lineType: LineType = LineType.Inheritance
        elif umlLinkType == PyutLinkType.COMPOSITION:
            lineType = LineType.Composition
        elif umlLinkType == PyutLinkType.AGGREGATION:
            lineType = LineType.Aggregation
        else:
            lineType = LineType.Association   # This won't happen yet

        return lineType

    def _toPyUmlPositions(self, oglLink, pyutLinkType: PyutLinkType) -> LinePositions:

        if pyutLinkType == PyutLinkType.INHERITANCE:
            srcAnchor:  AnchorPoint = oglLink.sourceAnchor
            destAnchor: AnchorPoint = oglLink.destinationAnchor
        else:
            srcAnchor  = oglLink.destinationAnchor
            destAnchor = oglLink.sourceAnchor

        srcX,  srcY  = srcAnchor.GetPosition()
        destX, destY = destAnchor.GetPosition()

        sourcePosition:      Position = Position(x=srcX, y=srcY)
        destinationPosition: Position = Position(x=destX, y=destY)

        bends: List[ControlPoint] = oglLink.GetControlPoints()
        if bends is None or len(bends) == 0:
            linePositions: LinePositions = [sourcePosition, destinationPosition]
        else:
            linePositions = [sourcePosition]
            for cp in bends:
                bend: ControlPoint = cast(ControlPoint, cp)
                self.logger.debug(f'{bend:}')

                bendX, bendY = bend.GetPosition()
                bendPosition: Position = Position(x=bendX, y=bendY)
                linePositions.append(bendPosition)

            linePositions.append(destinationPosition)

        return linePositions

    def _addMethods(self, classDefinition: ClassDefinition, pyutClass: PyutClass) -> ClassDefinition:

        methods: Methods = []
        for method in pyutClass.methods:

            pyutMethod: PyutMethod = cast(PyutMethod, method)

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
        self.logger.debug(f'{methodDefinition.name=}  {parameters=}')
        return methodDefinition

    def __toDefinitionType(self, visibility: PyutVisibilityEnum) -> DefinitionType:

        if visibility == PyutVisibilityEnum.PUBLIC:
            return DefinitionType.Public

    def __addClassDiagramDisplayPreferences(self, pyutClass: PyutClass, classDefinition: ClassDefinition) -> ClassDefinition:

        classDefinition.displayMethods    = pyutClass.showMethods
        classDefinition.displayFields     = pyutClass.showFields

        return classDefinition

    def __toImageLibraryEnum(self, showParameters: bool) -> DisplayMethodParameters:

        if showParameters is True:
            return DisplayMethodParameters.DISPLAY
        else:
            return DisplayMethodParameters.DO_NOT_DISPLAY

from typing import Dict
from typing import cast
from typing import List

from logging import Logger
from logging import getLogger

from xmlschema import XMLSchema

from xmlschema.validators import XsdComplexType
from xmlschema.validators import XsdElement
from xmlschema.validators import XsdGroup
# from xmlschema.validators import XsdType
from xmlschema.validators import XsdAttributeGroup

from org.pyut.plugins.common.ElementTreeData import ElementTreeData

from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame

from org.pyut.ui.UmlClassDiagramsFrame import CreatedClassesType


class XSDParser:

    X_INCREMENT_VALUE:  float = 80.0
    Y_INCREMENT_VALUE:  float = 80.0
    INITIAL_Y_POSITION: float = 50.0
    INITIAL_X_POSITION: float = 50.0
    MAX_X_POSITION:     float = 800

    def __init__(self, filename: str, umlFrame: UmlClassDiagramsFrame):

        self.logger: Logger = getLogger(__name__)

        self._umlFrame: UmlClassDiagramsFrame = umlFrame

        self.schema: XMLSchema = XMLSchema(filename)

        self.position = self._positionGenerator()
        self._schemaTypeNames: List[str] = []
        self.classTree: Dict[str, ElementTreeData] = {}

    def process(self):

        self.logger.info(f'')
        self.logger.info(f'---------- Traverse Schema Types ------------')
        for schemaTypeName in self.schema.types:
            self.logger.info(f'schemaTypeName: {schemaTypeName}')
            self._schemaTypeNames.append(schemaTypeName)

        self._createClassTree()
            # schemaType: XsdType = self.schema.types[schemaTypeName]
            # if isinstance(schemaType, XsdComplexType):
            #     complexSchemaType: XsdComplexType = cast(XsdComplexType, schemaType)
            #     self._handleComplexTypes(complexSchemaType)

    def _createClassTree(self):

        for classname in self._schemaTypeNames:
            pos: Dict[str, float] = next(self.position)

            createdClasses: CreatedClassesType = self._umlFrame.createClasses(name=classname, x=pos['x'], y=pos['y'])

    def _positionGenerator(self):

        x = XSDParser.INITIAL_X_POSITION
        y = XSDParser.INITIAL_Y_POSITION
        while True:
            yield {'x': x, 'y': y}

            if x < XSDParser.MAX_X_POSITION:
                x += XSDParser.X_INCREMENT_VALUE
            else:
                x = XSDParser.INITIAL_X_POSITION
                y += XSDParser.Y_INCREMENT_VALUE

    def _displayComplexTypes(self, xsdComplexType: XsdComplexType):

        self.logger.info(f'--------- Start _displayComplexTypes ---------')
        isComplex:     bool = xsdComplexType.is_complex()
        isSimple:      bool = xsdComplexType.is_simple()
        localName:     str  = xsdComplexType.local_name
        isElementOnly: bool = xsdComplexType.is_element_only()
        self.logger.info(
            f'\txsdComplexType: localName: `{localName}` isComplex: `{isComplex}` isSimple: `{isSimple}` isElementOnly: `{isElementOnly}`')

        contentType: XsdGroup = xsdComplexType.content_type
        self.logger.info(f'_handleComplexTypes -- contentType: {contentType}')
        grp = contentType._group

        for xsdElement in grp:
            xsdElement: XsdElement = cast(XsdElement, xsdElement)
            self.logger.info(f'xsdElement: {xsdElement} {xsdElement.local_name} {xsdElement.type}')

        attrGroup: XsdAttributeGroup = xsdComplexType.attributes
        self.logger.info(f'attrGroup: {attrGroup}')

        self.logger.info(f'--------- End _displayComplexTypes ---------')

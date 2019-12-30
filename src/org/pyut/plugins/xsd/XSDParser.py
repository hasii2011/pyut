
from logging import Logger
from logging import getLogger
from typing import cast

from xmlschema import XMLSchema

from xmlschema.validators import XsdComplexType
from xmlschema.validators import XsdElement
from xmlschema.validators import XsdGroup
from xmlschema.validators import XsdType
from xmlschema.validators import XsdAttributeGroup

from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame
# from org.pyut.ui.UmlClassDiagramsFrame import CreatedClassesType


class XSDParser:

    def __init__(self, filename: str, umlFrame: UmlClassDiagramsFrame):

        self.logger: Logger = getLogger(__name__)

        self._umlFrame: UmlClassDiagramsFrame = umlFrame

        self.schema: XMLSchema = XMLSchema(filename)

    def process(self):

        self.logger.info(f'schema.types: {self.schema.types}')

        self.logger.info(f'')
        self.logger.info(f'---------- Traverse Schema Types ------------')
        for schemaTypeName in self.schema.types:
            self.logger.info(f'schemaTypeName: {schemaTypeName}')
            schemaType: XsdType = self.schema.types[schemaTypeName]
            if isinstance(schemaType, XsdComplexType):
                complexSchemaType: XsdComplexType = cast(XsdComplexType, schemaType)
                self._handleComplexTypes(complexSchemaType)

    def _handleComplexTypes(self, xsdComplexType: XsdComplexType):

        isComplex:     bool = xsdComplexType.is_complex()
        isSimple:      bool = xsdComplexType.is_simple()
        localName:     str  = xsdComplexType.local_name
        isElementOnly: bool = xsdComplexType.is_element_only()
        self.logger.info(
            f'\txsdComplexType: localName: `{localName}` isComplex: `{isComplex}` isSimple: `{isSimple}` isElementOnly: `{isElementOnly}`')

        # createdClasses: CreatedClassesType = self._umlFrame.createClasses(name=localName, x=0.0, y=0.0)

        contentType: XsdGroup = xsdComplexType.content_type
        self.logger.info(f'_handleComplexTypes -- contentType: {contentType}')
        grp = contentType._group

        for xsdElement in grp:
            xsdElement: XsdElement = cast(XsdElement, xsdElement)
            self.logger.info(f'_handleComplexTypes -- xsdElement: {xsdElement} {xsdElement.local_name} {xsdElement.type}')

        attrGroup: XsdAttributeGroup = xsdComplexType.attributes
        self.logger.info(f'_handleComplexTypes - attrGroup: {attrGroup}')

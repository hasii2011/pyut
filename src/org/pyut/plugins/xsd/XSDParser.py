from typing import Dict
from typing import cast
from typing import List

from logging import Logger
from logging import getLogger

from xmlschema import XMLSchema

from xmlschema.validators import XsdComplexType
from xmlschema.validators import XsdElement
from xmlschema.validators import XsdGroup

from xmlschema.validators import XsdType

from org.pyut.PyutClass import PyutClass
from org.pyut.PyutField import PyutField
from org.pyut.PyutVisibilityEnum import PyutVisibilityEnum
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
        self._generateClassFields()
        self._generateLinks()

    def _createClassTree(self):

        for classname in self._schemaTypeNames:
            pos: Dict[str, float] = next(self.position)

            createdClasses: CreatedClassesType = self._umlFrame.createClasses(name=classname, x=pos['x'], y=pos['y'])

            treeData: ElementTreeData = ElementTreeData(pyutClass=createdClasses[0], oglClass=createdClasses[1])
            self.classTree[classname] = treeData

    def _generateClassFields(self):

        for className in self.classTree.keys():
            self.logger.info(f'className: {className}')
            schemaType: XsdType = self.schema.types[className]

            if isinstance(schemaType, XsdComplexType):
                complexSchemaType: XsdComplexType = cast(XsdComplexType, schemaType)
                self._handleComplexTypes(complexSchemaType)

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

    def _handleComplexTypes(self, xsdComplexType: XsdComplexType):

        self.logger.info(f'--------- Start _handleComplexTypes ---------')
        localName:     str  = xsdComplexType.local_name
        isElementOnly: bool = xsdComplexType.is_element_only()

        self.logger.info(f'localName: `{localName}` isElementOnly: `{isElementOnly}` open_content: {xsdComplexType.open_content}')

        contentType: XsdGroup = xsdComplexType.content_type
        self.logger.info(f'contentType: {contentType}')
        grp: List[XsdElement] = contentType._group
        self._addFields(className=localName, content=grp)
        #
        # attrGroup: XsdAttributeGroup = xsdComplexType.attributes
        # self.logger.info(f'attrGroup: {attrGroup}')

        self.logger.info(f'--------- End _handleComplexTypes ---------')

    def _addFields(self, className: str, content: List[XsdElement]):
        """
        Has the side effect that it updates the classtree data with the class names of the children

        Args:
            className: The class name for which we are adding fields to
            content:  The list of xsd elements that represents the fields
        """
        classTreeData:  ElementTreeData = self.classTree[className]
        pyutClass: PyutClass       = classTreeData.pyutClass
        for xsdElement in content:
            xsdElement: XsdElement = cast(XsdElement, xsdElement)
            self.logger.info(f'xsdElement: {xsdElement} {xsdElement.local_name} {xsdElement.type}')

            defaultValue = xsdElement.default
            if defaultValue is None:
                defaultValue = ''
            else:
                self.logger.warning(f'Handle a real default value for a field')
            xsdType: XsdType = xsdElement.type
            childClassName: str = xsdElement.local_name

            pyutField: PyutField = PyutField(name=childClassName,
                                             theFieldType=xsdType.local_name, defaultValue=defaultValue, visibility=PyutVisibilityEnum.PUBLIC)

            #
            # SIDE EFFECT !!!!!
            #
            classTreeData.addChild(childClassName)
            pyutClass.addField(pyutField)

    def _generateLinks(self):
        pass

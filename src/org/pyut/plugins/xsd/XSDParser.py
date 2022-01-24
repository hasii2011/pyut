
from typing import Dict
from typing import cast
from typing import List

from logging import Logger
from logging import getLogger

from xmlschema import XMLSchema

from xmlschema.validators import XsdComplexType
from xmlschema.validators import XsdElement
from xmlschema.validators import XsdEnumerationFacets
from xmlschema.validators import XsdGroup
from xmlschema.validators import XsdAtomicRestriction

from xmlschema.validators import XsdType

from org.pyut.model.PyutClass import PyutClass
from org.pyut.model.PyutField import PyutField
from org.pyut.model.PyutLink import PyutLink
from org.pyut.model.PyutVisibilityEnum import PyutVisibilityEnum

from org.pyut.enums.LinkType import LinkType

from org.pyut.ogl.OglClass import OglClass
from org.pyut.plugins.common.ElementTreeData import ElementTreeData

from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame

from org.pyut.ui.UmlClassDiagramsFrame import CreatedClassesType


class XSDParser:

    X_INCREMENT_VALUE:  float = 80.0
    Y_INCREMENT_VALUE:  float = 80.0
    INITIAL_Y_POSITION: float = 50.0
    INITIAL_X_POSITION: float = 50.0
    MAX_X_POSITION:     float = 800

    ENUMERATION_STEREOTYPE: str = 'Enumeration'
    SUBCLASS_INDICATOR:     str = 'extension'

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
        self._generateAggregationLinks()
        self._generateInheritanceLinks()

    def _createClassTree(self):

        for className in self._schemaTypeNames:

            pos: Dict[str, float] = next(self.position)

            createdClasses: CreatedClassesType = self._umlFrame.createClasses(name=className, x=pos['x'], y=pos['y'])

            pyutClass:  PyutClass  = createdClasses[0]
            oglClass:   OglClass   = createdClasses[1]
            schemaType: XsdType    = self.schema.types[className]
            if schemaType.derivation == XSDParser.SUBCLASS_INDICATOR:
                baseType: XsdType = schemaType.base_type
                self.logger.debug(f'class: {className} is a subclass of: {baseType.local_name}')
                pyutClass.addParent(baseType.local_name)

            treeData: ElementTreeData = ElementTreeData(pyutClass=pyutClass, oglClass=oglClass)
            self.classTree[className] = treeData

    def _generateClassFields(self):

        for className in self.classTree.keys():
            self.logger.info(f'className: {className}')
            schemaType: XsdType = self.schema.types[className]

            if isinstance(schemaType, XsdComplexType):
                complexSchemaType: XsdComplexType = cast(XsdComplexType, schemaType)
                self._handleComplexTypes(complexSchemaType)
            elif isinstance(schemaType, XsdAtomicRestriction):
                xsdAtomRestriction: XsdAtomicRestriction = cast(XsdAtomicRestriction, schemaType)
                self.logger.info(f'{xsdAtomRestriction.local_name}')
                facets: XsdEnumerationFacets = xsdAtomRestriction.facets
                for facetName in facets:
                    facet: XsdEnumerationFacets = facets[facetName]
                    if isinstance(facet, XsdEnumerationFacets):
                        self.logger.info(f'enumeration facet element enumeration: {facet.enumeration}')
                        self._createEnumerationFields(self.classTree[className].pyutClass, facet.enumeration)

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
            # if defaultValue is None:
            #     defaultValue = ''
            # else:
            #     self.logger.warning(f'Handle a real default value for a field')
            xsdType: XsdType = xsdElement.type
            childClassName: str = xsdElement.local_name

            pyutField: PyutField = PyutField(name=childClassName,
                                             theFieldType=xsdType.local_name, defaultValue=defaultValue, visibility=PyutVisibilityEnum.PUBLIC)

            #
            # SIDE EFFECT !!!!!
            #
            self.updateChildTypes(classTreeData, xsdElement)
            pyutClass.addField(pyutField)
            oglClass: OglClass = classTreeData.oglClass
            oglClass.autoResize()

    def updateChildTypes(self, classTreeData: ElementTreeData, xsdElement: XsdElement):
        """

        Args:
            classTreeData:  our class tree data for this particular type
            xsdElement:  an xsd element that is contained by this class

        """
        childTypeName: str = xsdElement.type.local_name
        if not classTreeData.childElementNames.__contains__(childTypeName):
            classTreeData.addChild(childTypeName)

    def _generateAggregationLinks(self):

        for className in self.classTree.keys():
            parentTreeData: ElementTreeData = self.classTree[className]
            childrenNames = parentTreeData.getChildElementNames()
            for childName in childrenNames:
                self.logger.debug(f'Class {className} has child type: {childName}')

                parentOglClass: OglClass = parentTreeData.oglClass
                try:
                    childTreeData: ElementTreeData = self.classTree[childName]

                    childOglClass: OglClass = childTreeData.oglClass
                    link: PyutLink = self._umlFrame.createLink(parentOglClass, childOglClass, LinkType.AGGREGATION)
                    self._umlFrame.GetDiagram().AddShape(shape=link, withModelUpdate=True)
                except KeyError:
                    self.logger.info(f'No problem {childName} is not in this hierarchy')

    def _generateInheritanceLinks(self):

        for className in self.classTree.keys():
            childTreeData: ElementTreeData = self.classTree[className]
            pyutClass: PyutClass = childTreeData.pyutClass
            parents: List[str] = pyutClass.getParents()
            for parentName in parents:
                self.logger.info(f'class: {pyutClass.getName()} is a subclass of: {parentName}')
                parentTreeData: ElementTreeData = self.classTree[parentName]

                childOglClass:  OglClass = childTreeData.oglClass
                parentOglClass: OglClass = parentTreeData.oglClass

                link: PyutLink = self._umlFrame.createLink(parentOglClass, childOglClass, LinkType.INHERITANCE)
                self._umlFrame.GetDiagram().AddShape(shape=link, withModelUpdate=True)

    def _createEnumerationFields(self, pyutClass: PyutClass, enumValues: List[str]):
        """
        TODO:  Create a PyutEnumeration at some point
        For now simulate with a bunch of fields in a class that is `Stereotyped` as
        Enumeration

        """
        pyutClass.setStereotype(stereotype=XSDParser.ENUMERATION_STEREOTYPE)
        pyutClass.setShowStereotype(theNewValue=True)

        for val in enumValues:
            pyutField: PyutField = PyutField(name=val.upper(), defaultValue=val, visibility=PyutVisibilityEnum.PUBLIC)
            pyutClass.addField(pyutField)

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

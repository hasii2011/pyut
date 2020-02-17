
from typing import cast
from typing import Dict
from typing import Tuple

from typing import List

from typing import NewType

from logging import Logger
from logging import getLogger

from xml.parsers.expat import ParserCreate

from org.pyut.model.PyutVisibilityEnum import PyutVisibilityEnum
from org.pyut.model.PyutClass import PyutClass
from org.pyut.model.PyutField import PyutField
from org.pyut.model.PyutLink import PyutLink

from org.pyut.enums.OglLinkType import OglLinkType

from org.pyut.ogl.OglClass import OglClass
from org.pyut.plugins.dtd.DTDElementTypes import DTDElementTypes

from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame
from org.pyut.ui.UmlClassDiagramsFrame import CreatedClassesType

from org.pyut.plugins.dtd.DTDAttribute import DTDAttribute
from org.pyut.plugins.common.ElementTreeData import ElementTreeData


DTDElements        = NewType('DTDElements', Dict[str, Tuple])
DTDAttributes      = NewType('DTDAttributes', List[DTDAttribute])


class DTDParser:

    MODEL_CHILD_ELEMENT_TYPE_INDEX:                int = 0
    MODEL_CHILD_ELEMENT_NAME_INDEX:                int = 2
    MODEL_CHILD_ELEMENT_ADDITIONAL_ELEMENTS_INDEX: int = 3

    MODEL_CHILDREN_INDEX:           int = 3

    klsLogger: Logger = None
    classParser       = None

    elementTypes: DTDElements   = {}
    attributes:   DTDAttributes = []

    def __init__(self, umlFrame: UmlClassDiagramsFrame):
        """
        In order for all of this to work you actually have to instantiate the class in
        order to get the 'class' variables initialized;  Failure to do so will cause an
        ugly mess
        Also, I use the pycharm noinspection pragma because I cannot get the correct
        type imported for the parser; I think because the code is 'generated' with
        some kind of C language binder;

        """
        self.logger: Logger = getLogger(__name__)
        DTDParser.klsLogger = self.logger

        self.dtdParser = ParserCreate()
        DTDParser.classParser = self.dtdParser

        self._umlFrame: UmlClassDiagramsFrame      = umlFrame
        self.classTree: Dict[str, ElementTreeData] = {}

        self.dtdParser.StartDoctypeDeclHandler = DTDParser.startDocTypeHandler
        self.dtdParser.ElementDeclHandler      = DTDParser.elementHandler
        self.dtdParser.AttlistDeclHandler      = DTDParser.attributeListHandler
        self.dtdParser.EndDoctypeDeclHandler   = self.endDocTypeHandler   # DTDReader.endDocTypeHandler

    def open(self, filename: str) -> bool:
        """

        Args:
            filename:

        Returns:  'True' if opened and parsed correctly else 'False'

        """
        self.logger.info(f'filename: {filename}')

        with open(filename, "rb") as dataFile:
            dtdData: bytes = dataFile.read()
            self.dtdParser.Parse(dtdData)

        return True

    @staticmethod
    def startDocTypeHandler(doctypeName, sysId, pubId, hasInternalSubset):
        dbgStr: str = f'startDocTypeHandler - doctypeName: {doctypeName} sysId: {sysId} pubId: {pubId} hasInternalSubset: {hasInternalSubset}'
        DTDParser.klsLogger.info(dbgStr)

    @staticmethod
    def elementHandler(elementName: str, model):
        """

        Args:
            elementName:   Element name
            model:  The element content model in (sep,cont,mod) format, where cont is a list of (name,mod) and (sep,cont,mod) tuples.
            ANY content models are represented as None, and EMPTYs as ("",[],"").

            (name , descr , (attribute | attribute-group-ref)* , )

        Returns:

        """
        currentLineNumber: int = DTDParser.classParser.CurrentLineNumber
        DTDParser.klsLogger.debug(f'eltHndlr - {currentLineNumber:{2}} name: {elementName:{12}} model: {model}')

        DTDParser.elementTypes[elementName] = model

    @staticmethod
    def attributeListHandler(eltName, attrName, attrType, attrValue, valType: int):

        dtdAttribute: DTDAttribute = DTDAttribute()

        dtdAttribute.elementName    = eltName
        dtdAttribute.attributeName  = attrName
        dtdAttribute.attributeType  = attrType
        dtdAttribute.attributeValue = attrValue
        dtdAttribute.valueType      = valType

        DTDParser.klsLogger.debug(dtdAttribute)

        DTDParser.attributes.append(dtdAttribute)

    # @staticmethod
    def endDocTypeHandler(self):

        self.classTree = self._createClassTree()
        self.logger.debug(f'elmentsTree: {self.classTree}')
        self._addAttributesToClasses()
        self._addLinks()

        self.logger.info(f'attributes: {DTDParser.attributes}')

    def _createClassTree(self) -> Dict[str, ElementTreeData]:

        elementsTree: Dict[str, ElementTreeData] = {}
        x = 50.0
        y = 50.0

        for eltName in list(DTDParser.elementTypes.keys()):

            createdClasses: CreatedClassesType = self._umlFrame.createClasses(name=eltName, x=x, y=y)
            pyutClass: PyutClass = createdClasses[0]
            oglClass:  OglClass  = createdClasses[1]

            elementTreeData: ElementTreeData = ElementTreeData(pyutClass=pyutClass, oglClass=oglClass)

            model = DTDParser.elementTypes[eltName]
            chillunNames: List[str] = self._getChildElementNames(eltName=eltName, model=model)
            elementTreeData.childElementNames = chillunNames

            elementsTree[eltName] = elementTreeData

            # Carefully, update the graphics layout
            if x < 800:
                x += 80
            else:
                x = 80
                y += 80

        return elementsTree

    def _addLinks(self):

        for className in list(self.classTree.keys()):

            eltTreeData: ElementTreeData = self.classTree[className]

            for associatedClassName in eltTreeData.childElementNames:
                self.logger.info(f'{className} associated with {associatedClassName}')
                parent: OglClass = eltTreeData.oglClass
                destTreeData: ElementTreeData = self.classTree[associatedClassName]
                child: OglClass = destTreeData.oglClass

                link: PyutLink = self._umlFrame.createLink(parent, child, OglLinkType.OGL_AGGREGATION)
                self._umlFrame.GetDiagram().AddShape(shape=link, withModelUpdate=True)

    def _addAttributesToClasses(self):

        for classAttr in DTDParser.attributes:
            typedAttr: DTDAttribute   = cast(DTDAttribute, classAttr)
            className: str            = typedAttr.elementName
            treeData: ElementTreeData = self.classTree[className]
            attrName: str             = typedAttr.attributeName
            attrType: str             = typedAttr.attributeType
            attrValue: str            = typedAttr.attributeValue

            pyutField: PyutField = PyutField(name=attrName,
                                             theFieldType=attrType,
                                             defaultValue=attrValue,
                                             visibility=PyutVisibilityEnum.PUBLIC)

            self.logger.info(f'pyutField: {pyutField}')
            pyutClass: PyutClass = treeData.pyutClass
            pyutClass.addField(pyutField)

    def _getChildElementNames(self, eltName, model) -> List[str]:

        self.logger.debug(f'_getChildElementNames - eltName: {eltName:{12}}\n model[0]: `{model[0]}`\n model[1]: `{model[1]}`\n model[2]: `{model[2]}`\n model[3]" `{model[3]}`')

        children = model[DTDParser.MODEL_CHILDREN_INDEX]
        self.logger.info(f'children {children}')
        chillunNames: List[str] = []
        for child in children:

            self.logger.info(f'eltName: {eltName} - child Length {len(child)}')

            dtdElementType: DTDElementTypes = DTDElementTypes(child[DTDParser.MODEL_CHILD_ELEMENT_TYPE_INDEX])
            childName = child[DTDParser.MODEL_CHILD_ELEMENT_NAME_INDEX]
            self.logger.info(f'eltName: {eltName} child: `{child}` eltType: `{dtdElementType.__repr__()}` childName: `{childName}`')
            addlElts = child[DTDParser.MODEL_CHILD_ELEMENT_ADDITIONAL_ELEMENTS_INDEX]
            if len(addlElts) != 0:
                for additionChildren in addlElts:
                    addlChildName = additionChildren[DTDParser.MODEL_CHILD_ELEMENT_NAME_INDEX]
                    chillunNames.append(addlChildName)
            else:
                chillunNames.append(childName)

        self.logger.info(f'Children names: {chillunNames}')
        return chillunNames

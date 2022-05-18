
from typing import cast
from typing import Dict
from typing import Tuple
from typing import List
from typing import NewType

from logging import Logger
from logging import getLogger

from xml.parsers.expat import ParserCreate
from pyexpat import XMLParserType

from pyutmodel.PyutType import PyutType
from pyutmodel.PyutVisibilityEnum import PyutVisibilityEnum
from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutField import PyutField
from pyutmodel.PyutLink import PyutLink

from pyutmodel.PyutLinkType import PyutLinkType

from org.pyut.ogl.OglClass import OglClass

from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame
from org.pyut.ui.UmlClassDiagramsFrame import CreatedClassesType

from org.pyut.plugins.dtd.DTDAttribute import DTDAttribute
from org.pyut.plugins.dtd.DTDElementTypes import DTDElementTypes

from org.pyut.plugins.common.ElementTreeData import ElementTreeData
from org.pyut.plugins.common.Types import ClassTree


DTDElements   = NewType('DTDElements',   Dict[str, Tuple])
DTDAttributes = NewType('DTDAttributes', List[DTDAttribute])


class DTDParser:

    MODEL_CHILD_ELEMENT_TYPE_INDEX:                int = 0
    MODEL_CHILD_ELEMENT_NAME_INDEX:                int = 2
    MODEL_CHILD_ELEMENT_ADDITIONAL_ELEMENTS_INDEX: int = 3

    MODEL_CHILDREN_INDEX:           int = 3

    def __init__(self, umlFrame: UmlClassDiagramsFrame):
        """
        Also, I use the pycharm noinspection pragma because I cannot get the correct
        type imported for the parser; I think because the code is 'generated' with
        some kind of C language binder;

        """
        self.logger:    Logger                = getLogger(__name__)
        self._umlFrame: UmlClassDiagramsFrame = umlFrame

        self._elementTypes: DTDElements   = DTDElements({})
        self._attributes:   DTDAttributes = DTDAttributes([])
        self._classTree:    ClassTree     = ClassTree({})

        # noinspection SpellCheckingInspection
        """
        Due to limitations in the Expat library used by pyexpat, the xmlparser instance returned can
        only be used to parse a single XML document.Call ParserCreate for each document to provide unique
        parser instances.
        """
        self._dtdParser: XMLParserType = ParserCreate()

        # noinspection SpellCheckingInspection
        self._dtdParser.StartDoctypeDeclHandler = self.startDocumentTypeHandler
        # noinspection SpellCheckingInspection
        self._dtdParser.ElementDeclHandler      = self.elementHandler
        # noinspection SpellCheckingInspection
        self._dtdParser.AttlistDeclHandler      = self.attributeListHandler
        # noinspection SpellCheckingInspection
        self._dtdParser.EndDoctypeDeclHandler   = self.endDocumentTypeHandler

    def open(self, filename: str) -> bool:
        """

        Args:
            filename:

        Returns:  'True' if opened and parsed correctly else 'False'

        """
        self.logger.info(f'filename: {filename}')

        with open(filename, "r") as dataFile:
            dtdData: str = dataFile.read()
            self._dtdParser.Parse(dtdData)

        return True

    def startDocumentTypeHandler(self, docTypeName, sysId, pubId, hasInternalSubset):

        dbgStr: str = f'startDocTypeHandler - {docTypeName=} {sysId=} {pubId=} {hasInternalSubset=}'
        self.logger.info(dbgStr)

    def elementHandler(self, elementName: str, model):
        # noinspection SpellCheckingInspection
        """

        Args:
            elementName:   Element name
            model:  The element content model in (sep,cont,mod) format, where cont is a list of (name,mod) and (sep,cont,mod) tuples.
            ANY content models are represented as None, and EMPTYs as ("",[],"").

            (name , descr , (attribute | attribute-group-ref)*)
        """
        currentLineNumber: int = self._dtdParser.CurrentLineNumber
        self.logger.debug(f'elementHandler - {currentLineNumber:{2}} name: {elementName:{12}} model: {model}')

        self._elementTypes[elementName] = model

    def attributeListHandler(self, eltName, attrName, attrType, attrValue, valType: int):

        dtdAttribute: DTDAttribute = DTDAttribute()

        dtdAttribute.elementName    = eltName
        dtdAttribute.attributeName  = attrName
        dtdAttribute.attributeType  = attrType
        dtdAttribute.attributeValue = attrValue
        dtdAttribute.valueType      = valType

        self.logger.debug(dtdAttribute)

        self._attributes.append(dtdAttribute)

    def endDocumentTypeHandler(self):

        self._classTree = self._createClassTree()
        self.logger.debug(f'elementsTree: {self._classTree}')
        self._addAttributesToClasses()
        self._addLinks()

        self.logger.info(f'attributes: {self._attributes}')

    def _createClassTree(self) -> ClassTree:

        elementsTree: ClassTree = ClassTree({})
        x: int = 50
        y: int = 50

        for eltName in list(self._elementTypes.keys()):

            createdClasses: CreatedClassesType = self._umlFrame.createClasses(name=eltName, x=x, y=y)
            pyutClass: PyutClass = createdClasses.pyutClass
            oglClass:  OglClass  = createdClasses.oglClass

            elementTreeData: ElementTreeData = ElementTreeData(pyutClass=pyutClass, oglClass=oglClass)

            model = self._elementTypes[eltName]
            # noinspection SpellCheckingInspection
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

        for className in list(self._classTree.keys()):

            eltTreeData: ElementTreeData = self._classTree[className]

            for associatedClassName in eltTreeData.childElementNames:
                self.logger.info(f'{className} associated with {associatedClassName}')
                parent: OglClass = eltTreeData.oglClass
                destTreeData: ElementTreeData = self._classTree[associatedClassName]
                child: OglClass = destTreeData.oglClass

                link: PyutLink = self._umlFrame.createLink(parent, child, PyutLinkType.AGGREGATION)
                self._umlFrame.GetDiagram().AddShape(shape=link, withModelUpdate=True)

    def _addAttributesToClasses(self):

        for classAttr in self._attributes:
            typedAttr: DTDAttribute   = cast(DTDAttribute, classAttr)
            className: str            = typedAttr.elementName
            treeData: ElementTreeData = self._classTree[className]
            attrName: str             = typedAttr.attributeName
            attrType: str             = typedAttr.attributeType
            attrValue: str            = typedAttr.attributeValue

            pyutField: PyutField = PyutField(name=attrName,
                                             fieldType=PyutType(value=attrType),
                                             defaultValue=attrValue,
                                             visibility=PyutVisibilityEnum.PUBLIC)

            self.logger.info(f'pyutField: {pyutField}')
            pyutClass: PyutClass = treeData.pyutClass
            pyutClass.addField(pyutField)

    def _getChildElementNames(self, eltName, model) -> List[str]:

        self.logger.debug(f'_getChildElementNames - {eltName=}\n {model[0]=}\n {model[1]=}\n {model[2]=}\n {model[3]=}')

        children = model[DTDParser.MODEL_CHILDREN_INDEX]
        self.logger.info(f'children {children}')
        # noinspection SpellCheckingInspection
        chillunNames: List[str] = []
        for child in children:

            self.logger.info(f'eltName: {eltName} - child Length {len(child)}')

            dtdElementType: DTDElementTypes = DTDElementTypes(child[DTDParser.MODEL_CHILD_ELEMENT_TYPE_INDEX])
            childName = child[DTDParser.MODEL_CHILD_ELEMENT_NAME_INDEX]
            self.logger.info(f'eltName: {eltName} child: `{child}` eltType: `{dtdElementType.__repr__()}` childName: `{childName}`')
            additionalElements = child[DTDParser.MODEL_CHILD_ELEMENT_ADDITIONAL_ELEMENTS_INDEX]
            if len(additionalElements) != 0:
                for additionChildren in additionalElements:
                    additionalChildName = additionChildren[DTDParser.MODEL_CHILD_ELEMENT_NAME_INDEX]
                    chillunNames.append(additionalChildName)
            else:
                chillunNames.append(childName)

        self.logger.info(f'Children names: {chillunNames}')
        return chillunNames

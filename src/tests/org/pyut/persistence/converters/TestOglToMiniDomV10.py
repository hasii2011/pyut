
from typing import cast


from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from xml.dom.minidom import Document
from xml.dom.minidom import Element

from wx import App

from org.pyut.enums.DiagramType import DiagramType
from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutMethod import PyutMethod
from pyutmodel.PyutMethod import PyutModifiers
from pyutmodel.PyutMethod import SourceCode
from pyutmodel.PyutModifier import PyutModifier
from pyutmodel.PyutType import PyutType

from ogl.OglClass import OglClass

from org.pyut.persistence.converters.OglToMiniDomV10 import OglToMiniDom as OglToMiniDomV10
from org.pyut.persistence.converters.PyutXmlConstants import PyutXmlConstants

from org.pyut.preferences.PyutPreferences import PyutPreferences

from org.pyut.ui.UmlFrame import UmlObjects

from tests.TestBase import TestBase


class TestOglToMiniDomV10(TestBase):
    """
    """
    OGL_CLASSES_TO_CREATE: int = 1

    clsLogger: Logger = cast(Logger, None)
    clsCounter: int    = 0
    clsApp:     App    = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestOglToMiniDomV10.clsLogger = getLogger(__name__)
        PyutPreferences.determinePreferencesLocation()

        TestOglToMiniDomV10.clsApp    = App()

    def setUp(self):
        self.logger:       Logger          = TestOglToMiniDomV10.clsLogger
        self._preferences: PyutPreferences = PyutPreferences()

    def tearDown(self):
        pass

    def testBasicClass(self):
        from org.pyut.persistence.PyutXmlV10 import PyutXml

        xmlDoc: Document = Document()

        top = xmlDoc.createElement(PyutXmlConstants.TOP_LEVEL_ELEMENT)
        top.setAttribute(PyutXmlConstants.ATTR_VERSION, str(PyutXml.VERSION))
        top.setAttribute(PyutXmlConstants.ATTR_CODE_PATH, '/Users/humberto.a.sanchez.ii/PycharmProjects/PyUt/src')

        xmlDoc.appendChild(top)

        documentNode: Element = self._pyutDocumentToPyutXml(xmlDoc=xmlDoc)
        top.appendChild(documentNode)

        oglObjects: UmlObjects      = self._createTestOglObjects()
        toPyutXml:  OglToMiniDomV10 = OglToMiniDomV10()

        for oglObject in oglObjects:
            if isinstance(oglObject, OglClass):
                classElement: Element = toPyutXml.oglClassToXml(oglObject, xmlDoc)
                documentNode.appendChild(classElement)

        sourceCodeElements: Element = xmlDoc.getElementsByTagName(PyutXmlConstants.ELEMENT_MODEL_SOURCE_CODE)
        self.assertIsNotNone(sourceCodeElements, "We should create a source code element")

        # childNodes = sourceCodeElements[0].childNodes
        # noinspection PyUnresolvedReferences
        childNodes = sourceCodeElements.item(0).childNodes
        self.assertEqual(5, len(childNodes), 'Incorrect number of source code lines')
        text = xmlDoc.toprettyxml()
        self.logger.info(f'xml: {text}')

    def testName2(self):
        """Another test"""
        pass

    def _pyutDocumentToPyutXml(self, xmlDoc: Document) -> Element:

        documentNode = xmlDoc.createElement(PyutXmlConstants.ELEMENT_DOCUMENT)

        documentNode.setAttribute(PyutXmlConstants.ATTR_TYPE, DiagramType.CLASS_DIAGRAM.value)
        documentNode.setAttribute(PyutXmlConstants.ATTR_TITLE, 'UnitTest')

        documentNode.setAttribute(PyutXmlConstants.ATTR_SCROLL_POSITION_X, '100')
        documentNode.setAttribute(PyutXmlConstants.ATTR_SCROLL_POSITION_Y, '100')

        documentNode.setAttribute(PyutXmlConstants.ATTR_PIXELS_PER_UNIT_X, '1')
        documentNode.setAttribute(PyutXmlConstants.ATTR_PIXELS_PER_UNIT_Y, '1')

        return documentNode

    def _createTestOglObjects(self) -> UmlObjects:

        umlObjects: UmlObjects = UmlObjects([])
        for x in range(TestOglToMiniDomV10.OGL_CLASSES_TO_CREATE):
            umlObject: OglClass = self._createNewClass()
            umlObjects.append(umlObject)

        return umlObjects

    def _createNewClass(self) -> OglClass:
        """
        Create a new class

        Returns: the newly created OglClass
        """
        className: str       = f'{self._preferences.className}{TestOglToMiniDomV10.clsCounter}'
        pyutClass: PyutClass = PyutClass(className)
        pyutClass.addMethod(self._generateAMethod())
        pyutClass.fileName = '/Users/humberto.a.sanchez.ii/PycharmProjects/PyUt/src/UnitTest.py'
        oglClass:  OglClass  = OglClass(pyutClass)

        TestOglToMiniDomV10.clsCounter += 1

        return oglClass

    def _generateAMethod(self) -> PyutMethod:
        pyutMethod: PyutMethod    = PyutMethod(name='OzzeeElGatoDiablo')

        pyutMethod.sourceCode = SourceCode(
            [
                'weLeft:           bool = True',
                'isOzzeeAGoodGato: bool = False',
                'if weLeft is True:',
                '    isOzzeeAGoodGato = True',
                'return isOzzeeAGoodGato'
            ]
        )
        pyutMethod.modifiers = PyutModifiers([PyutModifier(modifierTypeName='static'), PyutModifier('bogus')])
        pyutMethod.returnType = PyutType('str')
        return pyutMethod


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestOglToMiniDomV10))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

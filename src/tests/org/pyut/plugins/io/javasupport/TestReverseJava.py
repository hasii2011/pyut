
from typing import List

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain
from unittest.mock import Mock

from pkg_resources import resource_filename

from wx import App

from org.pyut.ogl.OglClass import OglClass

from org.pyut.plugins.io.javasupport.ReverseJava import Extenders
from org.pyut.plugins.io.javasupport.ReverseJava import ReverseJava

from org.pyut.preferences.PyutPreferences import PyutPreferences

from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame

from tests.TestBase import TestBase

TEST_BASE_CLASS_NAME: str = 'BaseModel'


class TestReverseJava(TestBase):
    """
    You need to change the name of this class to Test`xxxx`
    Where `xxxx' is the name of the class that you want to test.

    See existing tests for more information.
    """
    clsLogger: Logger = None
    clsApp:    App    = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestReverseJava.clsLogger = getLogger(__name__)
        PyutPreferences.determinePreferencesLocation()

        TestReverseJava.clsApp = App()

    @classmethod
    def tearDownClass(cls):
        cls.clsApp.OnExit()
        del cls.clsApp

    def setUp(self):
        self.logger:     Logger = TestReverseJava.clsLogger
        self._mockFrame: Mock   = Mock(spec=UmlClassDiagramsFrame)

        self._app: App = TestReverseJava.clsApp

    def tearDown(self):
        pass

    def testBasicClass(self):
        # rj: ReverseJava = ReverseJava(cast(UmlClassDiagramsFrame, umlFrame))
        reverseJava: ReverseJava = ReverseJava(umlFrame=self._mockFrame)

        basicClassPath: str = resource_filename(TestBase.RESOURCES_TEST_JAVA_CLASSES_PACKAGE_NAME, 'Tenant.java')

        reverseJava.analyseFile(basicClassPath)

        self.assertEqual(1, len(reverseJava.reversedClasses))

    def testCorrectlyGeneratedSingleSubclassMap(self):

        reverseJava: ReverseJava = self._createReversedOglClasses()

        expectedLength: int = 1
        actualLength:   int = len(reverseJava._subClassMap)
        self.assertEqual(expectedLength, actualLength, "More than one base class")

    def testCorrectlyGeneratedSubClassEntry(self):

        reverseJava: ReverseJava = self._createReversedOglClasses()

        testBaseClass: OglClass = reverseJava.reversedClasses[TEST_BASE_CLASS_NAME]

        self.assertIn(testBaseClass, reverseJava._subClassMap, 'Not the correct base class')

    def testCorrectlyGeneratedSubClasses(self):

        reverseJava: ReverseJava = self._createReversedOglClasses()

        testBaseClass: OglClass = reverseJava.reversedClasses[TEST_BASE_CLASS_NAME]

        extenders: Extenders = reverseJava._subClassMap[testBaseClass]

        expectedLength: int = 2
        actualLength:   int = len(extenders)

        self.assertEqual(expectedLength, actualLength, "Incorrect number of subclasses")

    def _createReversedOglClasses(self) -> ReverseJava:

        fileNames: List[str] = [f'{TEST_BASE_CLASS_NAME}.java', 'Feature.java', 'ICreated.java',
                                'IModified.java', 'Tenancy.java', 'Tenant.java', 'User.java'
                                ]
        reverseJava: ReverseJava = ReverseJava(umlFrame=self._mockFrame)
        for fileName in fileNames:
            testFileName: str = resource_filename(TestBase.RESOURCES_TEST_JAVA_CLASSES_PACKAGE_NAME, fileName)
            reverseJava.analyseFile(testFileName)

        return reverseJava


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestReverseJava))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

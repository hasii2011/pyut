
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain
from unittest.mock import Mock

from pkg_resources import resource_filename
from wx import App

from org.pyut.miniogl.Diagram import Diagram
from org.pyut.plugins.io.javasupport.ReverseJava import ReverseJava
from org.pyut.preferences.PyutPreferences import PyutPreferences

from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame

from tests.TestBase import TestBase


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
        mockDiagram: Mock = Mock(spec=Diagram)
        # self._mockFrame.GetPanel().return_value =
        reverseJava.analyseFile(basicClassPath)

        self.assertEqual(1, len(reverseJava.reversedClasses))

    def testExtenderCorrectlySetup(self):
        """Another test"""
        pass


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestReverseJava))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

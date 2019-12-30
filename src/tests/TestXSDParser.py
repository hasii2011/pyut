
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain
from unittest.mock import MagicMock

from wx import App

from tests.TestBase import TestBase

from org.pyut.plugins.xsd.XSDParser import XSDParser


class TestXSDParser(TestBase):
    """
    You need to change the name of this class to Test`xxxx`
    Where `xxxx' is the name of the class that you want to test.

    See existing tests for more information.
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestXSDParser.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger:    Logger = TestXSDParser.clsLogger

        # For python 3 and wx 4.x we need to save it so it does not get GC'ed
        # Did this because could not figure out how to mock creation of Font
        # in the OglObject constructor
        self.app = App()

        self.mockFrame:  MagicMock = MagicMock()

    def tearDown(self):
        pass

    def testBasicInitialization(self):

        xsdParser: XSDParser = XSDParser(filename='testdata/SimpleSchema.xsd', umlFrame=self.mockFrame)
        self.assertIsNotNone(xsdParser, 'Basic creation works')

    def testProcessing(self):

        xsdParser: XSDParser = XSDParser(filename='testdata/SimpleSchema.xsd', umlFrame=self.mockFrame)

        xsdParser.process()


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestXSDParser))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

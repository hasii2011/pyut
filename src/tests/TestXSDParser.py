
from typing import Dict

from logging import Logger
from logging import getLogger

from os import sep as osSep

from unittest import TestSuite
from unittest import main as unitTestMain
from unittest.mock import MagicMock

from wx import App

from tests.TestBase import TestBase
from tests.TestBase import TEST_DIRECTORY

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

        self._schemaPath: str = f'{TEST_DIRECTORY}{osSep}testdata{osSep}SimpleSchema.xsd'

    def tearDown(self):
        pass

    def testPositionGeneratorInitialValues(self):

        xsdParser: XSDParser = XSDParser(filename=self._schemaPath, umlFrame=self.mockFrame)

        pos: Dict[str, float] = next(xsdParser.position)
        x: float = pos['x']
        y: float = pos['y']
        self.logger.info(f'Pos({x}, {y})')

        self.assertEqual(XSDParser.INITIAL_X_POSITION, x, 'Initial X value is incorrect')
        self.assertEqual(XSDParser.INITIAL_X_POSITION, y, 'Initial Y value is incorrect')

    def testPositionGeneratorIncrementValues(self):

        xsdParser: XSDParser = XSDParser(filename=self._schemaPath, umlFrame=self.mockFrame)

        pos: Dict[str, float] = next(xsdParser.position)
        initX: float = pos['x']
        initY: float = pos['y']

        pos = next(xsdParser.position)
        x: float = pos['x']
        y: float = pos['y']

        expectedX: float = initX + XSDParser.X_INCREMENT_VALUE
        expectedY: float = initY

        self.logger.info(f'Pos({x}, {y})')

        self.assertEqual(expectedX, x, 'Incremented X value is incorrect')
        self.assertEqual(expectedY, y, 'Non-incremented Y value is incorrect')

    def testPositionGeneratorIncrementYValue(self):

        xsdParser: XSDParser = XSDParser(filename=self._schemaPath, umlFrame=self.mockFrame)

        pos: Dict[str, float] = next(xsdParser.position)

        initY: float = pos['y']

        while True:
            nextPos: Dict[str, float] = next(xsdParser.position)
            currX: float = nextPos['x']
            currY: float = nextPos['y']
            self.logger.info(f'nextPos({currX}, {currY})')
            if currY != initY:
                self.assertEqual(XSDParser.INITIAL_X_POSITION, currX, 'We did not wrap around')
                expectedY: float = initY + XSDParser.Y_INCREMENT_VALUE
                self.assertEqual(expectedY, currY, 'Y position did not properly increment')
                break   # Test is done

    def testBasicInitialization(self):

        xsdParser: XSDParser = XSDParser(filename=self._schemaPath, umlFrame=self.mockFrame)
        self.assertIsNotNone(xsdParser, 'Basic creation works')

    def testProcessing(self):

        xsdParser: XSDParser = XSDParser(filename=self._schemaPath, umlFrame=self.mockFrame)

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


from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from tests.TestBase import TestBase

from org.pyut.plugins.orthogonal.CartesianConverter import CartesianConverter
from org.pyut.plugins.orthogonal.CartesianConverter import ScreenCoordinates


class TestCartesianConverter(TestBase):
    """
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestCartesianConverter.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestCartesianConverter.clsLogger

        self.maxCoordinates = (75, -91, 0)
        self.minCoordinates = (-225, -482, 0)

    def tearDown(self):
        pass

    def testCartesianToScreen(self):
        x: int = 0
        y: int = -91

        screenCoordinates: ScreenCoordinates = CartesianConverter.cartesianToScreen(x, y)
        self.logger.info(f'cartesianToScreen: ({x}, {y}) screenCoordinates - {screenCoordinates}')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestCartesianConverter))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

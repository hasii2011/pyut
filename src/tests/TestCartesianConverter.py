
from logging import Logger
from logging import getLogger
from typing import List

from unittest import TestSuite
from unittest import main as unitTestMain

from tests.TestBase import TestBase

from org.pyut.plugins.orthogonal.CartesianConverter import CartesianConverter
from org.pyut.plugins.orthogonal.CartesianConverter import CartesianCoordinates
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

    def testCartesianToScreenBasic(self):

        cartesianCoordinates: CartesianCoordinates = CartesianCoordinates(0, -91)
        actualCoordinates:    ScreenCoordinates    = CartesianConverter.cartesianToScreen(cartesianCoordinates)
        self.logger.info(f'cartesianToScreen: ({cartesianCoordinates} actualCoordinates - {actualCoordinates}')

        expectedCoordinates: ScreenCoordinates = ScreenCoordinates(375, 600)
        self.assertEqual(expectedCoordinates, actualCoordinates, 'Something Changed')

    def testSimpleTranslationGraph(self):

        node0Coordinates: CartesianCoordinates = CartesianCoordinates(0, 0)

        cartesianNodeCoordinates: List[CartesianCoordinates] [
            CartesianCoordinates(0, 0)
        ]

        actualCoordinates: ScreenCoordinates   = CartesianConverter.cartesianToScreen(node0Coordinates)
        self.logger.info(f'cartesianToScreen: ({node0Coordinates}) actualCoordinates - {actualCoordinates}')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestCartesianConverter))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

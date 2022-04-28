
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from org.pyut.ogl.OglPosition import OglPosition
from org.pyut.preferences.PyutPreferences import PyutPreferences

from org.pyut.ogl.OglUtils import OglUtils

from tests.TestBase import TestBase


class TestOglUtils(TestBase):
    """
    """
    TEST_GRID_INTERVAL: int = 25

    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestOglUtils.clsLogger = getLogger(__name__)
        PyutPreferences.determinePreferencesLocation()

    def setUp(self):
        self.logger: Logger = TestOglUtils.clsLogger

    def tearDown(self):
        pass

    def testComputeMidPointNorthSouth(self):

        srcPosition: OglPosition = OglPosition(0, 100)
        dstPosition: OglPosition = OglPosition(0, 400)

        midPoint: OglPosition = OglUtils.computeMidPoint(srcPosition=srcPosition, dstPosition=dstPosition)

        self.assertEqual(0.0,   midPoint.x, 'X coordinate is not correct')
        self.assertEqual(250.0, midPoint.y, 'Y coordinate is not correct')

        self.logger.info(f'midPoint: {midPoint}')

    def testComputeMidPointSouthNorth(self):

        srcPosition: OglPosition = OglPosition(0, 400)
        dstPosition: OglPosition = OglPosition(0, 100)

        midPoint: OglPosition = OglUtils.computeMidPoint(srcPosition=srcPosition, dstPosition=dstPosition)
        self.assertEqual(0.0,   midPoint.x, 'X coordinate is not correct')
        self.assertEqual(250.0, midPoint.y, 'Y coordinate is not correct')

        self.logger.info(f'midPoint: {midPoint}')

    def testComputeMidPointEastWest(self):

        srcPosition: OglPosition = OglPosition(200, 400)
        dstPosition: OglPosition = OglPosition(200, 800)

        midPoint: OglPosition = OglUtils.computeMidPoint(srcPosition=srcPosition, dstPosition=dstPosition)
        self.assertEqual(200.0, midPoint.x, 'X coordinate is not correct')
        self.assertEqual(600.0, midPoint.y, 'Y coordinate is not correct')

        self.logger.info(f'midPoint: {midPoint}')

    def testComputeMidPointWestEast(self):

        srcPosition: OglPosition = OglPosition(200, 800)
        dstPosition: OglPosition = OglPosition(200, 400)

        midPoint: OglPosition = OglUtils.computeMidPoint(srcPosition=srcPosition, dstPosition=dstPosition)
        self.assertEqual(200.0, midPoint.x, 'X coordinate is not correct')
        self.assertEqual(600.0, midPoint.y, 'Y coordinate is not correct')

        self.logger.info(f'midPoint: {midPoint}')

    def testComputeMidPointNorthEastToSouthWest(self):

        srcPosition: OglPosition = OglPosition(8000, 8000)
        dstPosition: OglPosition = OglPosition(4000, 4000)

        midPoint: OglPosition = OglUtils.computeMidPoint(srcPosition=srcPosition, dstPosition=dstPosition)
        self.assertEqual(6000.0, midPoint.x, 'X coordinate is not correct')
        self.assertEqual(6000.0, midPoint.y, 'Y coordinate is not correct')

        self.logger.info(f'midPoint: {midPoint}')

    def testComputeMidPointNorthWestToSouthEast(self):

        srcPosition: OglPosition = OglPosition(1024, 1024)
        dstPosition: OglPosition = OglPosition(8092, 8092)

        midPoint: OglPosition = OglUtils.computeMidPoint(srcPosition=srcPosition, dstPosition=dstPosition)
        self.assertEqual(4558.0, midPoint.x, 'X coordinate is not correct')
        self.assertEqual(4558.0, midPoint.y, 'Y coordinate is not correct')

        self.logger.info(f'midPoint: {midPoint}')

    def testSnapCoordinatesToGrid(self):

        gridInterval: int = TestOglUtils.TEST_GRID_INTERVAL
        x: int = 335
        y: int = 142

        snappedX, snappedY = OglUtils.snapCoordinatesToGrid(x=x, y=y, gridInterval=gridInterval)

        expectedX: int = 325
        expectedY: int = 125

        self.assertEqual(expectedX, snappedX, 'X coordinate not correctly snapped')
        self.assertEqual(expectedY, snappedY, 'Y coordinate not correctly snapped')

    def testSnapCoordinatesToGridNoSnapping(self):
        gridInterval: int = TestOglUtils.TEST_GRID_INTERVAL
        x: int = 300
        y: int = 200

        snappedX, snappedY = OglUtils.snapCoordinatesToGrid(x=x, y=y, gridInterval=gridInterval)

        expectedX: int = 300
        expectedY: int = 200

        self.assertEqual(expectedX, snappedX, 'X coordinate not correctly snapped')
        self.assertEqual(expectedY, snappedY, 'Y coordinate not correctly snapped')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestOglUtils))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

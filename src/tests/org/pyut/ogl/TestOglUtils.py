
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from org.pyut.ogl.OglPosition import OglPosition
from org.pyut.preferences.PyutPreferences import PyutPreferences

from tests.TestBase import TestBase

from org.pyut.ogl.OglUtils import OglUtils


class TestOglUtils(TestBase):
    """
    """
    clsLogger: Logger = None

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

        srcPosition:  OglPosition = OglPosition(0, 100)
        destPosition: OglPosition = OglPosition(0, 400)

        midPoint: OglPosition = OglUtils.computeMidPoint(srcPosition=srcPosition, destPosition=destPosition)

        self.assertEqual(0.0,   midPoint.x, 'X coordinate is not correct')
        self.assertEqual(250.0, midPoint.y, 'Y coordinate is not correct')

        self.logger.info(f'midPoint: {midPoint}')

    def testComputeMidPointSouthNorth(self):

        srcPosition:  OglPosition = OglPosition(0, 400)
        destPosition: OglPosition = OglPosition(0, 100)

        midPoint: OglPosition = OglUtils.computeMidPoint(srcPosition=srcPosition, destPosition=destPosition)
        self.assertEqual(0.0,   midPoint.x, 'X coordinate is not correct')
        self.assertEqual(250.0, midPoint.y, 'Y coordinate is not correct')

        self.logger.info(f'midPoint: {midPoint}')

    def testComputeMidPointEastWest(self):

        srcPosition:  OglPosition = OglPosition(200, 400)
        destPosition: OglPosition = OglPosition(200, 800)

        midPoint: OglPosition = OglUtils.computeMidPoint(srcPosition=srcPosition, destPosition=destPosition)
        self.assertEqual(200.0, midPoint.x, 'X coordinate is not correct')
        self.assertEqual(600.0, midPoint.y, 'Y coordinate is not correct')

        self.logger.info(f'midPoint: {midPoint}')

    def testComputeMidPointWestEast(self):

        srcPosition:  OglPosition = OglPosition(200, 800)
        destPosition: OglPosition = OglPosition(200, 400)

        midPoint: OglPosition = OglUtils.computeMidPoint(srcPosition=srcPosition, destPosition=destPosition)
        self.assertEqual(200.0, midPoint.x, 'X coordinate is not correct')
        self.assertEqual(600.0, midPoint.y, 'Y coordinate is not correct')

        self.logger.info(f'midPoint: {midPoint}')

    def testComputeMidPointNorthEastToSouthWest(self):

        srcPosition:  OglPosition = OglPosition(8000, 8000)
        destPosition: OglPosition = OglPosition(4000, 4000)

        midPoint: OglPosition = OglUtils.computeMidPoint(srcPosition=srcPosition, destPosition=destPosition)
        self.assertEqual(6000.0, midPoint.x, 'X coordinate is not correct')
        self.assertEqual(6000.0, midPoint.y, 'Y coordinate is not correct')

        self.logger.info(f'midPoint: {midPoint}')

    def testComputeMidPointNorthWestToSouthEast(self):

        srcPosition:  OglPosition = OglPosition(1024, 1024)
        destPosition: OglPosition = OglPosition(8092, 8092)

        midPoint: OglPosition = OglUtils.computeMidPoint(srcPosition=srcPosition, destPosition=destPosition)
        self.assertEqual(4558.0, midPoint.x, 'X coordinate is not correct')
        self.assertEqual(4558.0, midPoint.y, 'Y coordinate is not correct')

        self.logger.info(f'midPoint: {midPoint}')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestOglUtils))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

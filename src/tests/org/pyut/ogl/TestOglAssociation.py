
from logging import Logger
from logging import getLogger
from unittest import TestSuite
from unittest import main as unitTestMain

from tests.TestBase import TestBase

from org.pyut.ogl.OglAssociation import OglAssociation
from org.pyut.ogl.OglPosition import OglPosition


class TestOglAssociation(TestBase):
    """
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestOglAssociation.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestOglAssociation.clsLogger

    def tearDown(self):
        pass

    def testComputeMidPointNorthSouth(self):

        srcPosition:  OglPosition = OglPosition(0, 100)
        destPosition: OglPosition = OglPosition(0, 400)

        midPoint = OglAssociation._computeMidPoint(srcPosition=srcPosition, destPosition=destPosition)
        self.assertEqual(0.0,   midPoint[0], 'X coordinate is not correct')
        self.assertEqual(250.0, midPoint[1], 'Y coordinate is not correct')
        self.logger.info(f'midPoint: {midPoint}')

    def testComputeMidPointSouthNorth(self):

        srcPosition:  OglPosition = OglPosition(0, 400)
        destPosition: OglPosition = OglPosition(0, 100)

        midPoint = OglAssociation._computeMidPoint(srcPosition=srcPosition, destPosition=destPosition)
        self.assertEqual(0.0,   midPoint[0], 'X coordinate is not correct')
        self.assertEqual(250.0, midPoint[1], 'Y coordinate is not correct')
        self.logger.info(f'midPoint: {midPoint}')

    def testComputeMidPointEastWest(self):

        srcPosition:  OglPosition = OglPosition(200, 400)
        destPosition: OglPosition = OglPosition(200, 800)

        midPoint = OglAssociation._computeMidPoint(srcPosition=srcPosition, destPosition=destPosition)
        self.assertEqual(200.0, midPoint[0], 'X coordinate is not correct')
        self.assertEqual(600.0, midPoint[1], 'Y coordinate is not correct')
        self.logger.info(f'midPoint: {midPoint}')

    def testComputeMidPointWestEast(self):

        srcPosition:  OglPosition = OglPosition(200, 800)
        destPosition: OglPosition = OglPosition(200, 400)

        midPoint = OglAssociation._computeMidPoint(srcPosition=srcPosition, destPosition=destPosition)
        self.assertEqual(200.0, midPoint[0], 'X coordinate is not correct')
        self.assertEqual(600.0, midPoint[1], 'Y coordinate is not correct')
        self.logger.info(f'midPoint: {midPoint}')

    def testComputeMidPointNorthEastToSouthWest(self):

        srcPosition:  OglPosition = OglPosition(8000, 8000)
        destPosition: OglPosition = OglPosition(4000, 4000)

        midPoint = OglAssociation._computeMidPoint(srcPosition=srcPosition, destPosition=destPosition)
        self.assertEqual(6000.0, midPoint[0], 'X coordinate is not correct')
        self.assertEqual(6000.0, midPoint[1], 'Y coordinate is not correct')
        self.logger.info(f'midPoint: {midPoint}')

    def testComputeMidPointNorthWestToSouthEast(self):

        srcPosition:  OglPosition = OglPosition(1024, 1024)
        destPosition: OglPosition = OglPosition(8092, 8092)

        midPoint = OglAssociation._computeMidPoint(srcPosition=srcPosition, destPosition=destPosition)
        self.assertEqual(4558.0, midPoint[0], 'X coordinate is not correct')
        self.assertEqual(4558.0, midPoint[1], 'Y coordinate is not correct')
        self.logger.info(f'midPoint: {midPoint}')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestOglAssociation))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

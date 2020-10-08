
from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from unittest import TestSuite
from unittest import main as unitTestMain

from tests.TestBase import TestBase

from org.pyut.miniogl.Common import Common


@dataclass
class Point:

    x: float = 0.0
    y: float = 0.0


@dataclass
class TestLine:

    start: Point = Point(0, 0)
    end:   Point = Point(0, 0)


class TestMiniOglCommon(TestBase):
    """
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestMiniOglCommon.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger:   Logger   = TestMiniOglCommon.clsLogger
        self.common:   Common   = Common()
        self.testLine: TestLine = TestLine(start=Point(100, 100), end=Point(100, 200))

    def tearDown(self):
        pass

    def testInsideSegment(self):

        clickPointX: float = 101.0
        clickPointY: float = 150.0

        x1: float = self.testLine.start.x
        y1: float = self.testLine.start.y
        x2: float = self.testLine.end.x
        y2: float = self.testLine.end.y

        diffX: float = x2 - x1
        diffY: float = y2 - y1

        clickDiffStartX: float = clickPointX - x1     # x - x1
        clickDiffStartY: float = clickPointY - y1     # y - y1

        isIt: bool = self.common.insideSegment(clickDiffStartX=clickDiffStartX, clickDiffStartY=clickDiffStartY, diffX=diffX, diffY=diffY)

        self.assertTrue(isIt, 'But, but it IS inside the segment')

    def testInsideSegmentFail(self):

        clickPointX: float = 100 + Common.CLICK_TOLERANCE + 1.0
        clickPointY: float = 150

        x1: float = self.testLine.start.x
        y1: float = self.testLine.start.y
        x2: float = self.testLine.end.x
        y2: float = self.testLine.end.y

        diffX: float = x2 - x1
        diffY: float = y2 - y1

        clickDiffStartX: float = clickPointX - x1     # x - x1
        clickDiffStartY: float = clickPointY - y1     # y - y1

        isIt: bool = self.common.insideSegment(clickDiffStartX=clickDiffStartX, clickDiffStartY=clickDiffStartY, diffX=diffX, diffY=diffY)

        self.assertFalse(isIt, 'But, but it IS NOT inside the segment')

    def testInsideBoundingBox(self):
        clickPointX: float = 101.0
        clickPointY: float = 150.0

        x1: float = self.testLine.start.x
        y1: float = self.testLine.start.y
        x2: float = self.testLine.end.x
        y2: float = self.testLine.end.y

        diffX: float = x2 - x1
        diffY: float = y2 - y1

        clickDiffStartX: float = clickPointX - x1     # x - x1
        clickDiffStartY: float = clickPointY - y1     # y - y1

        isIt: bool = self.common.insideBoundingBox(clickDiffStartX, clickDiffStartY, diffX, diffY)

        self.assertTrue(isIt, 'But, but it IS inside the bounding box')

    def testInsideBoundingBoxFalse(self):
        clickPointX: float = 100.0 + Common.CLICK_TOLERANCE
        clickPointY: float = 150.0

        x1: float = self.testLine.start.x
        y1: float = self.testLine.start.y
        x2: float = self.testLine.end.x
        y2: float = self.testLine.end.y

        diffX: float = x2 - x1
        diffY: float = y2 - y1

        clickDiffStartX: float = clickPointX - x1     # x - x1
        clickDiffStartY: float = clickPointY - y1     # y - y1

        isIt: bool = self.common.insideBoundingBox(clickDiffStartX, clickDiffStartY, diffX, diffY)

        self.assertFalse(isIt, 'But, but it IS NOT inside the bounding box')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestMiniOglCommon))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

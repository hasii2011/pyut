
from typing import cast
from typing import List

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from unittest.mock import Mock

from wx import App

from tests.TestBase import TestBase

from org.pyut.general.LineSplitter import LineSplitter


class TestLineSplitter(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):

        TestBase.setUpLogging()
        TestLineSplitter.clsLogger = getLogger(__name__)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.logger:       Logger       = TestLineSplitter.clsLogger
        self.app:          App          = App()
        self.lineSplitter: LineSplitter = LineSplitter()

    def tearDown(self):
        self.app.OnExit()
        del self.app

    def testNoSplit(self):

        shortLine: str       = 'Short line'
        mockedDC:  Mock = Mock()
        mockedDC.GetTextExtent = self.mockGetTextExtent
        textWidth: int       = 120
        newLines: List[str] = self.lineSplitter.split(text=shortLine, dc=mockedDC, textWidth=textWidth)

        expectedLength: int = 1
        actualLength:   int = len(newLines)
        self.assertEqual(expectedLength, actualLength, 'Split incorrectly')

    def testBasicSplit(self):
        longLine: str = '12345678 12345678 12345678'
        mockedDC:  Mock = Mock()
        mockedDC.GetTextExtent = self.mockGetTextExtent
        textWidth: int       = 45

        newLines: List[str] = self.lineSplitter.split(text=longLine, dc=mockedDC, textWidth=textWidth)

        expectedLength: int = 3
        actualLength:   int = len(newLines)
        self.assertEqual(expectedLength, actualLength, 'Split incorrectly')

    def testFancySplit(self):

        longLine: str = 'Where oh where do you want to split me along party lines or maybe not'
        mockedDC:  Mock = Mock()
        mockedDC.GetTextExtent = self.mockGetTextExtent
        textWidth: int       = 50

        newLines: List[str] = self.lineSplitter.split(text=longLine, dc=mockedDC, textWidth=textWidth)

        expectedLength: int = 8
        actualLength:   int = len(newLines)
        self.assertEqual(expectedLength, actualLength, 'Split incorrectly')

    def mockGetTextExtent(self, textToMeasure: str):

        noSpaces: str = textToMeasure.strip(' ')
        height:   int = 10
        width:    int = noSpaces.__len__() * 5

        width += 2  # account for space at end that was stripped

        return width, height


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestLineSplitter))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

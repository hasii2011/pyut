
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from wx import App
from wx import Colour

from org.pyut.miniogl.PyutColorEnum import PyutColorEnum

from tests.TestBase import TestBase


class TestPyutColorEnum(TestBase):
    """
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestPyutColorEnum.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestPyutColorEnum.clsLogger
        self.app = App()

    def tearDown(self):
        del self.app

    def testBlack(self):
        c: Colour = PyutColorEnum.toWxColor(PyutColorEnum.BLACK)
        self.assertTrue(c.IsOk(), 'Wah, wah.  Black should be a valid color')

    def testLightGrey(self):
        c: Colour = PyutColorEnum.toWxColor(PyutColorEnum.LIGHT_GREY)
        self.assertTrue(c.IsOk(), 'Wah, wah.  Light Grey should be a valid color')

    def testCornFlowerBlue(self):
        c: Colour = PyutColorEnum.toWxColor(PyutColorEnum.CORNFLOWER_BLUE)
        self.assertTrue(c.IsOk(), 'Wah, wah.  Corn Flower Blue should be a valid color')

    def testYellow(self):
        c: Colour = PyutColorEnum.toWxColor(PyutColorEnum.YELLOW)
        self.assertTrue(c.IsOk(), 'Wah, wah.  Yellow should be a valid color')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestPyutColorEnum))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

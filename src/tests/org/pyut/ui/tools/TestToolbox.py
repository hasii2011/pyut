
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from wx import Size

from org.pyut.preferences.PyutPreferences import PyutPreferences
from org.pyut.preferences.ToolBarIconSize import ToolBarIconSize

from tests.TestBase import TestBase

from org.pyut.ui.tools.Toolbox2 import Toolbox


class TestToolbox(TestBase):
    """
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestToolbox.clsLogger = getLogger(__name__)
        PyutPreferences.determinePreferencesLocation()

    def setUp(self):
        self.logger: Logger = TestToolbox.clsLogger
        self._preferences: PyutPreferences = PyutPreferences()

    def tearDown(self):
        pass

    def testComputeToolboxNumberRows(self):

        actualRowCount:   int = Toolbox.computeToolboxNumberRows(toolCount=21, numColumns=3)
        expectedRowCount: int = 7

        self.assertEqual(expectedRowCount, actualRowCount, 'Incorrect row count')

    def testComputeToolboxNumberRowsForceCeiling(self):

        actualRowCount:   int = Toolbox.computeToolboxNumberRows(toolCount=35, numColumns=6)
        expectedRowCount: int = 6

        self.assertEqual(expectedRowCount, actualRowCount, 'Incorrect row count')

    def testComputeSizeBasedOnRowColumnsSmallIcons(self):

        iconSize:     int = int(ToolBarIconSize.SIZE_16.value)
        actualSize:   Size = Toolbox.computeSizeBasedOnRowColumns(numColumns=3, numRows=6, iconSize=iconSize)
        expectedSize: Size = Size(54, 108)
        self.logger.debug(f'Small Icons Window Size: {actualSize}')

        self.assertEqual(expectedSize, actualSize, 'Size computation changed for small icons')

    def testComputeSizeBasedOnRowColumnsLargeIcons(self):

        iconSize:   int = int(ToolBarIconSize.SIZE_32.value)
        actualSize: Size = Toolbox.computeSizeBasedOnRowColumns(numColumns=3, numRows=6, iconSize=iconSize)
        expectedSize: Size = Size(102, 204)
        self.logger.debug(f'Large Icons Window Size: {actualSize}')

        self.assertEqual(expectedSize, actualSize, 'Size computation changed for large icons')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestToolbox))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

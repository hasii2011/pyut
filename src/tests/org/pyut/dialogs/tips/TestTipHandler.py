
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from org.pyut.PyutUtils import PyutUtils

from org.pyut.preferences.PyutPreferences import PyutPreferences

from tests.TestBase import TestBase

from org.pyut.dialogs.tips.DlgTips import DlgTips
from org.pyut.dialogs.tips.TipHandler import TipHandler


class TestTipHandler(TestBase):
    """
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestTipHandler.clsLogger = getLogger(__name__)
        PyutPreferences.determinePreferencesLocation()

    def setUp(self):
        self.logger: Logger = TestTipHandler.clsLogger
        self._tipsFileName: str = PyutUtils.retrieveResourcePath(f'{DlgTips.TIPS_FILENAME}')

    def tearDown(self):
        pass

    def testInitialization(self):

        tipHandler: TipHandler = TipHandler(fqFileName=self._tipsFileName)

        self.assertTrue(len(tipHandler._tipLines) > 0)

    def testComputeTipCount(self):
        """Another test"""
        pass

        tipHandler: TipHandler = TipHandler(fqFileName=self._tipsFileName)
        self.assertTrue(tipHandler._tipCount > 0)

    def testSafelyRetrieveCurrentTipNumber(self):

        tipHandler: TipHandler = TipHandler(fqFileName=self._tipsFileName)

        self.assertIsNotNone(tipHandler._currentTipNumber)

        self.assertTrue(tipHandler._currentTipNumber >= 0)

    def testGetCurrentTipText(self):

        tipHandler: TipHandler = TipHandler(fqFileName=self._tipsFileName)

        expectedTip: str = tipHandler._tipLines[tipHandler._currentTipNumber]
        actualTip:   str = tipHandler.getCurrentTipText()

        self.assertEqual(expectedTip, actualTip, 'Uh, our white box test did not work')

    def testIncrementTipNumber(self):

        tipHandler: TipHandler = TipHandler(fqFileName=self._tipsFileName)

        prevTipNumber: int = tipHandler._currentTipNumber
        tipHandler.incrementTipNumber(1)

        self.assertEqual(prevTipNumber + 1, tipHandler._currentTipNumber, 'We did not increment by 1')


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestTipHandler))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

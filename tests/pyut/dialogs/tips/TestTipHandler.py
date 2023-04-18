
from unittest import TestSuite
from unittest import main as unitTestMain

from hasiihelper.ResourceManager import ResourceManager
from hasiihelper.UnitTestBase import UnitTestBase

from pyut.general.Globals import BASE_RESOURCES_PACKAGE
from pyut.general.Globals import BASE_RESOURCE_PATH

from pyut.preferences.PreferencesCommon import PreferencesCommon

from pyut.uiv2.dialogs.tips.DlgTips import DlgTips
from pyut.uiv2.dialogs.tips.TipHandler import TipHandler

from tests.TestBase import TestBase


class TestTipHandler(TestBase):
    """
    """
    @classmethod
    def setUpClass(cls):
        UnitTestBase.setUpClass()
        PreferencesCommon.determinePreferencesLocation()

    def setUp(self):
        super().setUp()
        self._tipsFileName: str = ResourceManager.retrieveResourcePath(bareFileName=f'{DlgTips.TIPS_FILENAME}',
                                                                       packageName=f'{BASE_RESOURCES_PACKAGE}',
                                                                       resourcePath=f'{BASE_RESOURCE_PATH}')

    def tearDown(self):
        super().tearDown()

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

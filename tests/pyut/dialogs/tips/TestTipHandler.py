
from unittest import TestSuite
from unittest import main as unitTestMain

from codeallybasic.ResourceManager import ResourceManager
from codeallybasic.UnitTestBase import UnitTestBase

from pyut.PyutConstants import PyutConstants

from pyut.uiv2.dialogs.tips.TipHandler import TipHandler

from tests.ProjectTestBase import ProjectTestBase


class TestTipHandler(ProjectTestBase):
    """
    """
    @classmethod
    def setUpClass(cls):
        UnitTestBase.setUpClass()

    def setUp(self):
        super().setUp()
        self._tipsFileName: str = ResourceManager.retrieveResourcePath(bareFileName=f'{PyutConstants.TIPS_FILENAME}',
                                                                       packageName=f'{PyutConstants.BASE_RESOURCES_PACKAGE}',
                                                                       resourcePath=f'{PyutConstants.BASE_RESOURCE_PATH}')

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

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestTipHandler))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

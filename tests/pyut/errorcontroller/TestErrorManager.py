
from unittest import TestCase
from unittest import main as unitTestMain
from unittest import TestSuite

from os import linesep as osLineSep

from pathlib import Path

from pyut.PyutConstants import PyutConstants
from pyut.errorcontroller.ErrorViewType import ErrorViewType
from pyut.errorcontroller.IErrorView import IErrorView
from pyut.errorcontroller.TextErrorView import TextErrorView
from pyut.preferences.PyutPreferences import PyutPreferences

from pyut.errorcontroller.ErrorManager import ErrorManager

EXPECTED_TEST_OUTPUT: str = (
    f'ERROR: ErrorManager: --------------------------------------------------------------------{osLineSep}'
    f'ERROR: ErrorManager: A Test Log Entry Title - This is only a test error message{osLineSep}'
)

TEST_LOG_FILE_NAME: str   = '/tmp/testErrorManager.log'
TEST_LOG_FILE_PATH: Path  = Path(TEST_LOG_FILE_NAME)


class TestErrorManager(TestCase):
    """
    Subclass from basic TestCase so we can set up our own logging
    """

    def setUp(self):

        super().setUp()
        preferences: PyutPreferences = PyutPreferences()
        self._saveErrorViewType: ErrorViewType = preferences.errorViewType

    def tearDown(self):

        super().tearDown()
        preferences: PyutPreferences = PyutPreferences()
        preferences.errorViewType = self._saveErrorViewType

    def testAddToLogFile(self):

        self._setupAddToLogFileTest()
        ErrorManager.addToLogFile(title='A Test Log Entry Title', msg='This is only a test error message')

        actualTestOutput: str = TEST_LOG_FILE_PATH.read_text()

        self.assertEqual(EXPECTED_TEST_OUTPUT, actualTestOutput, 'Our test did not generated good stuff')

    def testChangingViewType(self):
        errorManger: ErrorManager = ErrorManager()

        errorManger.errorViewType = ErrorViewType.RAISE_ERROR_VIEW

        self.assertEqual(ErrorViewType.RAISE_ERROR_VIEW, errorManger.errorViewType, 'Incorrect error type')

    def testCorrectViewSet(self):

        errorManger: ErrorManager = ErrorManager()

        errorManger.errorViewType = ErrorViewType.TEXT_ERROR_VIEW

        view: IErrorView = errorManger._errorView

        self.assertTrue(isinstance(view, TextErrorView))

    def _setupAddToLogFileTest(self):
        from logging import getLogger
        from logging import FileHandler
        from logging import Formatter
        from logging import Logger
        from logging import DEBUG

        # noinspection SpellCheckingInspection
        logger:    Logger      = getLogger(PyutConstants.MAIN_LOGGING_NAME)
        fh:        FileHandler = FileHandler(TEST_LOG_FILE_NAME, mode='w')
        formatter: Formatter   = Formatter('%(levelname)s: %(module)s: %(message)s')

        logger.setLevel(DEBUG)

        fh.setLevel(DEBUG)

        fh.setFormatter(formatter)

        logger.addHandler(fh)


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestErrorManager))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

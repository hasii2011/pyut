
from unittest import main as unitTestMain
from unittest import TestSuite

from pyut.errorcontroller.ErrorViewTypes import ErrorViewTypes
from pyut.errorcontroller.IErrorView import IErrorView
from pyut.errorcontroller.TextErrorView import TextErrorView

from tests.ProjectTestBase import ProjectTestBase

from pyut.errorcontroller.ErrorManager import ErrorManager


class TestErrorManager(ProjectTestBase):
    """
    """

    def setUp(self):
        super().setUp()

    def testAddToLogFile(self):

        ErrorManager.addToLogFile(title='A Test Log Entry Title', msg='This is only a test error message')

    def testChangingViewType(self):
        errorManger: ErrorManager = ErrorManager()

        errorManger.errorViewType = ErrorViewTypes.RAISE_ERROR_VIEW

        self.assertEqual(ErrorViewTypes.RAISE_ERROR_VIEW, errorManger.errorViewType, 'Incorrect error type')

    def testCorrectViewSet(self):

        errorManger: ErrorManager = ErrorManager()

        errorManger.errorViewType = ErrorViewTypes.TEXT_ERROR_VIEW

        view: IErrorView = errorManger._errorView

        self.assertTrue(isinstance(view, TextErrorView))


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestErrorManager))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

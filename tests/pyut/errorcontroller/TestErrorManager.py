
from unittest import main as unitTestMain
from unittest import TestSuite

from tests.TestBase import TestBase

from pyut.errorcontroller.ErrorManager import ErrorManager


class TestErrorManager(TestBase):
    """
    """

    def setUp(self):
        super().setUp()

    def testAddToLogFile(self):
        ErrorManager.addToLogFile(title='A Test Log Entry Title', msg='This is only a test error message')


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestErrorManager))

    return testSuite


if __name__ == '__main__':
    unitTestMain()


from typing import cast

from logging import Logger
from logging import getLogger

from unittest import main as unitTestMain
from unittest import TestSuite

from tests.TestBase import TestBase

from pyut.errorcontroller.ErrorManager import ErrorManager


class TestErrorManager(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestErrorManager.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestErrorManager.clsLogger

    def testAddToLogFile(self):
        ErrorManager.addToLogFile(title='A Test Log Entry Title', msg='This is only a test error message')


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestErrorManager))

    return testSuite


if __name__ == '__main__':
    unitTestMain()


from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from org.pyut.preferences.PyutPreferences import PyutPreferences
from tests.TestBase import TestBase


class TestCreateOglClassCommand(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestCreateOglClassCommand.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger          = TestCreateOglClassCommand.clsLogger
        self.prefs:  PyutPreferences = PyutPreferences()

    def tearDown(self):
        pass

    def testPass(self):
        pass


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestCreateOglClassCommand))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

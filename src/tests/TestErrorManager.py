
from logging import Logger
from logging import getLogger

from unittest import main as unitTestMain

from tests.TestBase import TestBase

from org.pyut.errorcontroller.ErrorManager import ErrorManager
from org.pyut.errorcontroller.ErrorManager import addToLogFile


class TestErrorManager(TestBase):
    """
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestErrorManager.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestErrorManager.clsLogger

    def testAddToLogFile(self):
        addToLogFile(title='A Test Log Entry Title', msg='This is only a test error message')


if __name__ == '__main__':
    unitTestMain()

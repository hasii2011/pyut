
from logging import Logger
from logging import getLogger

from unittest import main as unitTestMain

from tests.TestBase import TestBase

from org.pyut.persistence.IoFile import IoFile


class TestIoFile(TestBase):
    """
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestIoFile.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestIoFile.clsLogger
        ioFile: IoFile = IoFile()

    def tearDown(self):
        pass

    def testName1(self):
        pass

    def testName2(self):
        pass


if __name__ == '__main__':
    unitTestMain()

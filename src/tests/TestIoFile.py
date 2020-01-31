
from logging import Logger
from logging import getLogger
from os import chdir
from os import getcwd

from unittest import main as unitTestMain
from unittest import TestSuite

from unittest.mock import patch
from unittest.mock import MagicMock

from org.pyut.ui.FileHandling import FileHandling
from tests.TestBase import TestBase

from org.pyut.general.Mediator import Mediator
from org.pyut.persistence.IoFile import IoFile


class TestIoFile(TestBase):
    """
    PyutClasses (datamodel) and OglClasses UI are intermixed in the PyutXml code;  Extremely, hard to unit
    test that the data model has been built correct
    But, I did learn a bit about Python mocking !!
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestIoFile.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestIoFile.clsLogger
        self.ioFile: IoFile = IoFile()

        self.mockFrame:    MagicMock = MagicMock()
        self.mockTree:     MagicMock = MagicMock()
        self.mockTreeRoot: MagicMock = MagicMock()
        self.fileHandling: FileHandling = MagicMock()

        oldPath: str = getcwd()
        # Assume we are at src/tests
        chdir('../..')
        newAppPath: str = getcwd()
        chdir(oldPath)

        self.mediator = Mediator()      # It's a Singleon, I can do this
        self.mediator.registerAppPath(newAppPath)
        self.mediator.registerFileHandling(self.fileHandling)

    def tearDown(self):
        pass

    @patch('wx.Dialog')
    @patch('wx.Gauge')
    @patch('org.pyut.general.Mediator')
    @patch('org.pyut.persistence.FileHandling.FileHandling')
    def testIoFileOpenV8(self, mockFileHandling, mockMediator, wxGauge, wxDialog):

        with patch('org.pyut.PyutProject.PyutProject') as mockPyutProject:
            self.ioFile.open(filename='testdata/BaseSave_V8.put', project=mockPyutProject)

    def testName2(self):
        pass


def suite() -> TestSuite:

    import unittest

    testSuite: unittest.TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestIoFile))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

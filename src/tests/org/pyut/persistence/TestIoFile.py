
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import main as unitTestMain
from unittest import TestSuite

from unittest.mock import patch
from unittest.mock import MagicMock

from pkg_resources import resource_filename
from wx import App

from org.pyut.ui.PyutUI import PyutUI
from tests.TestBase import TestBase

from org.pyut.ui.Mediator import Mediator
from org.pyut.persistence.IoFile import IoFile


class TestIoFile(TestBase):
    """
    PyutClasses (data model) and OglClasses UI are intermixed in the PyutXml code;  Extremely, hard to unit
    test that the data model has been built correctly
    But, I did learn a bit about Python mocking !!
    """
    clsLogger: Logger = cast(Logger, None)

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
        self.fileHandling: PyutUI    = MagicMock()

        self.mediator = Mediator()      # It's a Singleton, I can do this
        self.mediator.registerAppPath('./')
        self.mediator.registerFileHandling(self.fileHandling)

        self.app: App = App()

    def tearDown(self):
        self.app.OnExit()

    # noinspection PyUnusedLocal
    @patch('wx.Dialog')
    @patch('wx.Gauge')
    @patch('org.pyut.ui.TreeNotebookHandler.TreeNotebookHandler')
    def testIoFileOpenV10(self, mockFileHandling, wxGauge, wxDialog):
        fqFileName = resource_filename(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, 'IoFileTest.put')

        with patch('org.pyut.ui.PyutProject.PyutProject') as mockPyutProject:
            self.ioFile.open(filename=fqFileName, project=mockPyutProject)


def suite() -> TestSuite:

    import unittest

    testSuite: unittest.TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestIoFile))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

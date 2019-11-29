from typing import List

from logging import Logger
from logging import getLogger

from os import chdir
from os import getcwd


from unittest import main as unitTestMain

from org.pyut.PyutUtils import PyutUtils
from tests.TestBase import TestBase

from org.pyut.plugins.PluginManager import PluginManager


class TestPluginManager(TestBase):
    """
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestPluginManager.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestPluginManager.clsLogger

        # Assume we are in src/tests
        savePath: str = getcwd()
        chdir('../..')
        newBasePath: str = getcwd()
        PyutUtils.setBasePath(newBasePath)
        chdir(savePath)

        self.pluginManager: PluginManager = PluginManager()

    def testBasicLoad(self):

        infoStrings: List[str] = self.pluginManager.getPluginsInfo()
        self.assertIsNotNone(infoStrings, 'I should get lots of these')

        for info in infoStrings:
            self.logger.info(info)


if __name__ == '__main__':
    unitTestMain()

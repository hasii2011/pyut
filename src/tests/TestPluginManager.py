
from typing import List

from logging import Logger
from logging import getLogger

from unittest import main as unitTestMain

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
        self.pluginManager: PluginManager = PluginManager()

    def testBasicLoad(self):

        infoStrings: List[str] = self.pluginManager.getPluginsInfo()
        self.assertIsNotNone(infoStrings, 'I should get lots of these')

        for info in infoStrings:
            self.logger.info(info)


if __name__ == '__main__':
    unitTestMain()


from typing import List

from logging import Logger
from logging import getLogger

from os import chdir
from os import getcwd

from unittest import main as unitTestMain
from unittest import TestSuite

from org.pyut.PyutUtils import PyutUtils

from org.pyut.ui.tools.SharedTypes import PluginMap

from tests.TestBase import TestBase

from org.pyut.plugins.PluginManager import PluginManager


class TestPluginManager(TestBase):

    EXPECTED_TOOL_COUNT:          int = 9
    EXPECTED_IMPORT_PLUGIN_COUNT: int = 8
    EXPECTED_EXPORT_PLUGIN_COUNT: int = 9
    """
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestPluginManager.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestPluginManager.clsLogger

        # Assume we are in src
        savePath: str = getcwd()

        newBasePath: str = getcwd()
        PyutUtils.setBasePath(newBasePath)
        chdir(savePath)

        self.pluginManager: PluginManager = PluginManager()

    def testBasicLoad(self):

        infoStrings: List[str] = self.pluginManager.getPluginsInfo()
        self.assertIsNotNone(infoStrings, 'I should get lots of these')

        for info in infoStrings:
            self.logger.info(info)

    def testMapWxIdsToToolPlugins(self):

        toolPluginMap: PluginMap = self.pluginManager.mapWxIdsToToolPlugins()
        self.assertEqual(TestPluginManager.EXPECTED_TOOL_COUNT, len(toolPluginMap), 'Incorrect tool count')

    def testMapWxIdsToImportPlugins(self):

        importPluginMap: PluginMap = self.pluginManager.mapWxIdsToImportPlugins()
        self.assertEqual(TestPluginManager.EXPECTED_IMPORT_PLUGIN_COUNT, len(importPluginMap), 'Incorrect import plugin count')

    def testMapWxIdsToExportPlugins(self):

        exportPluginMap: PluginMap = self.pluginManager.mapWxIdsToExportPlugins()
        self.assertEqual(TestPluginManager.EXPECTED_EXPORT_PLUGIN_COUNT, len(exportPluginMap), 'Incorrect export plugin count')


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestPluginManager))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

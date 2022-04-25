
from typing import cast

from logging import Logger
from logging import getLogger
import logging
import logging.config

import json

from os import remove as osRemove
from os import path as osPath

from shutil import copyfile

from pkg_resources import resource_filename

from unittest import TestCase

from unittest import TestSuite
from unittest import main as unitTestMain

from org.pyut.ogl.OglDimensions import OglDimensions
from tests.TestBase import TestBase

from org.pyut.ogl.preferences.OglPreferences import OglPreferences

JSON_LOGGING_CONFIG_FILENAME: str = "testLoggingConfig.json"
TEST_DIRECTORY:               str = 'tests'


class TestOglPreferences(TestCase):
    """
    """
    BACKUP_SUFFIX: str = '.backup'

    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpLogging(cls):
        """"""

        loggingConfigFilename: str = cls.findLoggingConfig()

        with open(loggingConfigFilename, 'r') as loggingConfigurationFile:
            configurationDictionary = json.load(loggingConfigurationFile)

        logging.config.dictConfig(configurationDictionary)
        logging.logProcesses = False
        logging.logThreads = False

    @classmethod
    def findLoggingConfig(cls) -> str:

        fqFileName = resource_filename(TestBase.RESOURCES_PACKAGE_NAME, JSON_LOGGING_CONFIG_FILENAME)

        return fqFileName

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestOglPreferences.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestOglPreferences.clsLogger
        self.oglPreferences: OglPreferences = OglPreferences()

        self._backupPrefs()

    def tearDown(self):
        self._restoreBackup()

    def testNewOglPreferences(self):

        oglPreferences: OglPreferences = OglPreferences()
        self.assertIsNotNone(oglPreferences, 'For some reason instantiation did not work')

    def testChangeNoteText(self):

        self.oglPreferences.noteText = 'I changed it'
        actualNoteText: str = self.oglPreferences.noteText
        self.assertEqual('I changed it', actualNoteText, 'Hmm did not change')

    def testChangeClassDimensions(self):
        self.oglPreferences.classDimensions = OglDimensions(width=100, height=100)
        actualDimensions: OglDimensions = self.oglPreferences.classDimensions
        self.assertEqual(OglDimensions(100, 100), actualDimensions, 'Ouch did not change')

    def testChangeDefaultMethodName(self):
        self.oglPreferences.methodName = 'I changed you'
        actualName: str = self.oglPreferences.methodName
        self.assertEqual('I changed you', actualName, 'The default method name did not change')

    def _backupPrefs(self):

        prefsFileName: str = self.oglPreferences._preferencesFileName
        source: str = prefsFileName
        target: str = f"{prefsFileName}{TestOglPreferences.BACKUP_SUFFIX}"
        if osPath.exists(source):
            try:
                copyfile(source, target)
            except IOError as e:
                self.logger.error(f"Unable to copy file. {e}")

    def _restoreBackup(self):

        prefsFileName: str = self.oglPreferences._preferencesFileName
        source: str = f"{prefsFileName}{TestOglPreferences.BACKUP_SUFFIX}"
        target: str = prefsFileName
        if osPath.exists(source):
            try:
                copyfile(source, target)
            except IOError as e:
                self.logger.error(f"Unable to copy file. {e}")

            osRemove(source)
        else:
            osRemove(target)


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestOglPreferences))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

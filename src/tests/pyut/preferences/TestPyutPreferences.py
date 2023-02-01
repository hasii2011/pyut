
from typing import cast

from logging import Logger
from logging import getLogger

from os import remove as osRemove
from os import path as osPath

from shutil import copyfile

from unittest import main as unitTestMain
from unittest import TestSuite

from tests.TestBase import TestBase

from pyut.preferences.PyutPreferences import PyutPreferences


class TestPyutPreferences(TestBase):
    """
    """
    BACKUP_SUFFIX: str = '.backup'

    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestPyutPreferences.clsLogger = getLogger(__name__)
        PyutPreferences.determinePreferencesLocation()

    def setUp(self):
        """
        Remove any existing prefs file.

        Instantiate a prefs (Singleton class) and fill it.
        """
        self.logger: Logger = TestPyutPreferences.clsLogger

        self._backupPrefs()
        self.prefs: PyutPreferences = PyutPreferences()
        self._emptyPrefs()

    def tearDown(self):
        self._restoreBackup()

    def testAutoResizeOptionIsTrue(self):

        self.prefs.init()  # reload default prefs

        self.prefs.autoResizeShapesOnEdit = True

        autoResize: bool = self.prefs.autoResizeShapesOnEdit
        self.assertEqual(autoResize, True, 'What !! I set it to boolean `True`')
        self.logger.info(f'{autoResize}')

    def testAutoResizeOptionIsFalse(self):

        self.prefs.init()  # reload default prefs

        self.prefs.autoResizeShapesOnEdit = False

        autoResize: bool = self.prefs.autoResizeShapesOnEdit

        self.assertEqual(autoResize, False, 'What !! I set it to the boolean `False`')
        self.logger.info(f'{autoResize}')

    def _backupPrefs(self):

        prefsFileName: str = PyutPreferences.getPreferencesLocation()
        source: str = prefsFileName
        target: str = f"{prefsFileName}{TestPyutPreferences.BACKUP_SUFFIX}"
        if osPath.exists(source):
            try:
                copyfile(source, target)
            except IOError as e:
                self.logger.error(f"Unable to copy file. {e}")

    def _restoreBackup(self):

        prefsFileName: str = PyutPreferences.getPreferencesLocation()
        source: str = f"{prefsFileName}{TestPyutPreferences.BACKUP_SUFFIX}"
        target: str = prefsFileName
        if osPath.exists(source):
            try:
                copyfile(source, target)
            except IOError as e:
                self.logger.error(f"Unable to copy file. {e}")

            osRemove(source)
        else:
            osRemove(target)

    def _emptyPrefs(self):

        self.prefs = PyutPreferences()
        self.prefs._createEmptyPreferences()
        self.prefs._preferencesCommon.saveConfig()


def suite() -> TestSuite:

    import unittest

    testSuite: unittest.TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestPyutPreferences))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

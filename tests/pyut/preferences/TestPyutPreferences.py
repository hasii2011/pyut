
from pathlib import Path

from shutil import copyfile

from unittest import main as unitTestMain
from unittest import TestSuite

from codeallybasic.UnitTestBase import UnitTestBase

from pyut.preferences.PreferencesCommon import PreferencesCommon
from pyut.preferences.PyutPreferences import PyutPreferences

from tests.TestBase import TestBase


class TestPyutPreferences(TestBase):
    """
    """
    BACKUP_SUFFIX: str = '.backup'

    @classmethod
    def setUpClass(cls):
        UnitTestBase.setUpClass()
        PreferencesCommon.determinePreferencesLocation()

    def setUp(self):
        """
        Remove any existing prefs file.

        Instantiate a prefs (Singleton class) and fill it.
        """
        super().setUp()
        self._backupPrefs()
        self.prefs: PyutPreferences = PyutPreferences()
        self._emptyPrefs()

    def tearDown(self):
        super().tearDown()
        self._restoreBackup()

    def testAutoResizeOptionIsTrue(self):

        self.prefs.init()  # reload default prefs

        self.prefs.autoResizeShapesOnEdit = True

        autoResize: bool = self.prefs.autoResizeShapesOnEdit
        self.assertEqual(autoResize, True, 'What !! I set it to boolean `True`')
        # self.logger.info(f'{autoResize}')   does not work;  How does inheritance work with class variables

    def testAutoResizeOptionIsFalse(self):

        self.prefs.init()  # reload default prefs

        self.prefs.autoResizeShapesOnEdit = False

        autoResize: bool = self.prefs.autoResizeShapesOnEdit

        self.assertEqual(autoResize, False, 'What !! I set it to the boolean `False`')
        # self.logger.info(f'{autoResize}')   does not work;  How does inheritance work with class variables

    def _backupPrefs(self):

        prefsPath:     Path = Path(PyutPreferences.getPreferencesLocation())
        targetPath:    Path = Path(f'{prefsPath}{TestPyutPreferences.BACKUP_SUFFIX}')
        if prefsPath.exists() is True and prefsPath.is_file() is True:
            try:
                copyfile(prefsPath, targetPath)
            except IOError as e:
                self.logger.error(f"Unable to copy file. {e}")

    def _restoreBackup(self):
        targetPath:       Path = Path(PyutPreferences.getPreferencesLocation())
        backupPrefsPath:  Path = Path(f'{targetPath}{TestPyutPreferences.BACKUP_SUFFIX}')

        if backupPrefsPath.exists() is True and backupPrefsPath.is_file() is True:
            try:
                copyfile(backupPrefsPath, targetPath)
            except IOError as e:
                self.logger.error(f"Unable to copy file. {e}")

            backupPrefsPath.unlink()

    def _emptyPrefs(self):

        self.prefs = PyutPreferences()
        self.prefs._createEmptyPreferences()
        self.prefs._preferencesCommon.saveConfig()


def suite() -> TestSuite:

    import unittest

    testSuite: unittest.TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestPyutPreferences))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

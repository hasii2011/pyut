
from logging import Logger
from logging import getLogger

from os import remove as osRemove

from shutil import copyfile

from unittest import main as unitTestMain
from unittest import TestSuite

from tests.TestBase import TestBase

from org.pyut.PyutPreferences import PyutPreferences


class TestPyutPreferences(TestBase):
    """
    """
    BACKUP_SUFFIX: str = '.backup'

    clsLogger: Logger = None

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

        self.testPrefs = {
            "test_int": 12,
            "test_double": 12.12,
            "test_string": "salut",
            "test_tuple": ("salut", "les", "amis"),
            "test_list": ["comment", "allez", "vous"],
        }
        self.prefs: PyutPreferences = PyutPreferences()
        self._backupPrefs()
        self._emptyPrefs()

        # fill the prefs
        for item, value in list(self.testPrefs.items()):
            self.prefs[item] = value

    def tearDown(self):
        self._restoreBackup()

    def testValues(self):
        """
        Test that the prefs contain the good values.
        """
        for item, value in list(self.testPrefs.items()):
            found = self.prefs[item]
            self.assertTrue(found == str(value), "Wrong value for %s. Want %s, got %s" % (item, value, found))

    def testSpaceInName(self):
        """
        Test what happened with a space in the name of a pref.
        """
        try:
            self.prefs["salut les amis"] = str(3)
        except TypeError:
            pass  # that's OK
        else:
            self.fail("A name without spaces has not raised an exception")

    def testLoadSave(self):
        """
        Test that load and save work correctly.
        """
        # now, prefs is already loaded, add some values that are automatically
        # saved
        self.prefs["new_pref"] = str(10)
        self.prefs.init()  # reinit the object (that's the only way since it's a singleton
        self.assertTrue(self.prefs["new_pref"] == "10", "Value doesn't exist")

    def testGetUnknownPref(self):
        """
        What happens with an unknown pref.
        """
        try:
            self.assertTrue(self.prefs["unknown"] is None)
        except (ValueError, Exception) as e:
            self.fail(f"Should not raise an exception {e}")

    def testGetUnknownPrefWhenEmpty(self):
        """
        What happens with an unknown section.

        All is now in `emptyPrefs`.
        """
        self._emptyPrefs()

    def testLastOpenedFiles(self):
        """
        Test the last opened files management.
        """
        files = [
            "un", "deux", "trois", "quatre", "cinq", "six"
        ]
        self.prefs.setNbLOF(len(files) - 1)
        self.prefs.init()  # reload prefs
        self.assertTrue(self.prefs.getNbLOF() == len(files) - 1, "wrong nbLOF")
        for file in files:
            self.prefs.addNewLastOpenedFilesEntry(file)
        self.prefs.init()
        files.reverse()  # because it's a last in first out
        files.pop()      # remove last one which should have been dropped
        for i in range(len(files) - 1):
            self.assertTrue(self.prefs.getLastOpenedFilesList()[i] == files[i], "wrong file name")

    def testNoAutoResizeOption(self):
        autoResize = self.prefs['auto_resize']
        self.assertTrue(autoResize is None, 'Should not have received an option')
        self.logger.info(f'{autoResize}')

    def testAutoResizeOptionIsTrue(self):

        self.prefs[PyutPreferences.AUTO_RESIZE_SHAPE_ON_EDIT] = 'True'
        autoResize: str = self.prefs[PyutPreferences.AUTO_RESIZE_SHAPE_ON_EDIT]
        self.assertEqual(autoResize, 'True', 'What !! I set it to string `True`')
        self.logger.info(f'{autoResize}')

    def testAutoResizeOptionIsFalse(self):

        self.prefs[PyutPreferences.AUTO_RESIZE_SHAPE_ON_EDIT] = 'False'
        autoResize: str = self.prefs[PyutPreferences.AUTO_RESIZE_SHAPE_ON_EDIT]
        self.assertEqual(autoResize, 'False', 'What !! I set it to the string `False`')
        self.logger.info(f'{autoResize}')

    def _backupPrefs(self):

        prefsFileName: str = PyutPreferences.getPreferencesLocation()
        source: str = prefsFileName
        target: str = f"{prefsFileName}{TestPyutPreferences.BACKUP_SUFFIX}"
        try:
            copyfile(source, target)
        except IOError as e:
            self.logger.error(f"Unable to copy file. {e}")

    def _restoreBackup(self):

        prefsFileName: str = PyutPreferences.getPreferencesLocation()
        source: str = f"{prefsFileName}{TestPyutPreferences.BACKUP_SUFFIX}"
        target: str = prefsFileName
        try:
            copyfile(source, target)
        except IOError as e:
            self.logger.error(f"Unable to copy file. {e}")

        osRemove(source)

    def _emptyPrefs(self):
        osRemove(PyutPreferences.getPreferencesLocation())
        self.prefs.init()
        # test that it's empty
        try:
            self.assertTrue(self.prefs[list(self.testPrefs.keys())[0]] is None)
        except (ValueError, Exception) as e:
            self.fail(f"Should not raise an exception;  {e}")


def suite() -> TestSuite:

    import unittest

    testSuite: unittest.TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestPyutPreferences))

    return testSuite


if __name__ == '__main__':
    unitTestMain()


from logging import Logger
from logging import getLogger

from os import remove as osRemove
from os import path as osPath

from shutil import copyfile

from unittest import main as unitTestMain
from unittest import TestSuite

from org.pyut.preferences.DiagramPreferences import BackgroundPreferences
from tests.TestBase import TestBase

from org.pyut.preferences.PyutPreferences import PyutPreferences


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

        self._backupPrefs()
        self.prefs: PyutPreferences = PyutPreferences()
        self._emptyPrefs()

    def tearDown(self):
        self._restoreBackup()

    def testLastOpenedFiles(self):
        """
        Test the last opened files management.
        """
        files = [
            "uno", "dos", "tres", "quattro", "cinco", "seis"
        ]
        self.prefs.init()  # reload prefs
        self.prefs.setNbLOF(len(files) - 1)
        self.assertTrue(self.prefs.getNbLOF() == len(files) - 1, "wrong nbLOF")
        for file in files:
            self.prefs.addNewLastOpenedFilesEntry(file)
        files.reverse()  # because it's a last in first out
        files.pop()      # remove last one which should have been dropped
        for i in range(len(files) - 1):
            self.assertTrue(self.prefs.getLastOpenedFilesList()[i] == files[i], "wrong file name")

    def testAutoResizeOptionIsTrue(self):

        self.prefs.autoResizeShapesOnEdit = True

        autoResize: bool = self.prefs.autoResizeShapesOnEdit
        self.assertEqual(autoResize, True, 'What !! I set it to boolean `True`')
        self.logger.info(f'{autoResize}')

    def testAutoResizeOptionIsFalse(self):

        self.prefs.autoResizeShapesOnEdit = False

        autoResize: bool = self.prefs.autoResizeShapesOnEdit

        self.assertEqual(autoResize, False, 'What !! I set it to the boolean `False`')
        self.logger.info(f'{autoResize}')

    def testUseDebugTempFileLocationTrue(self):
        self.prefs.init()  # reload prefs
        self.prefs.useDebugTempFileLocation = True
        self.assertTrue(self.prefs.useDebugTempFileLocation, 'Syntactic sugar not working')

    def testUseDebugTempFileLocationFalse(self):
        self.prefs.init()  # reload prefs
        self.prefs.useDebugTempFileLocation = False
        self.assertFalse(self.prefs.useDebugTempFileLocation, 'Syntactic sugar not working')

    def testDebugBasicShapeTrue(self):
        self.prefs.init()  # reload prefs
        self.prefs.debugBasicShape = True
        self.assertTrue(self.prefs.debugBasicShape, 'Syntactic sugar not working')

    def testDebugBasicShapeFalse(self):
        self.prefs.init()  # reload prefs
        self.prefs.debugBasicShape = False
        self.assertFalse(self.prefs.debugBasicShape, 'Syntactic sugar not working')

    def testTwoColorValue(self):

        self.prefs.init()  # reload prefs
        expectedColor: str = BackgroundPreferences.DEFAULT_GRID_LINE_COLOR
        actualColor:   str = self.prefs.gridLineColor.value

        self.assertEqual(expectedColor, actualColor, 'Default must have change')

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

        self.prefs: PyutPreferences = PyutPreferences()
        self.prefs.init()       # it is a singleton so init only runs the first time
        self.prefs._createEmptyPreferences()


def suite() -> TestSuite:

    import unittest

    testSuite: unittest.TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestPyutPreferences))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

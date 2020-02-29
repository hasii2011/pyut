
from typing import Dict
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

import sys
import os

from configparser import *

from org.pyut.general.Singleton import Singleton

from org.pyut.general.exceptions.PreferencesLocationNotSet import PreferencesLocationNotSet


PREFS_NAME_VALUES = NewType('PREFS_NAME_VALUES', Dict[str, str])


class PyutPreferences(Singleton):

    DEFAULT_NB_LOF: int = 5         # Number of last opened files, by default
    FILE_KEY:       str = "File"

    OPENED_FILES_SECTION:       str = "RecentlyOpenedFiles"
    NUMBER_OF_ENTRIES:          str = "Number_of_Recently_Opened_Files"

    MAIN_SECTION:               str = 'Main'

    ORG_DIRECTORY:              str = 'orgDirectory'
    LAST_DIRECTORY:             str = 'LastDirectory'
    STARTUP_DIRECTORY:          str = 'Startup_Directory'
    SHOW_TIPS_ON_STARTUP:       str = 'Show_Tips_On_Startup'
    AUTO_RESIZE_SHAPE_ON_EDIT:  str = 'Auto_Resize_Shape_On_Edit'
    SHOW_PARAMETERS:            str = 'Show_Parameters'
    FULL_SCREEN:                str = 'Full_Screen'
    I18N:                       str = 'I18N'
    CURRENT_TIP:                str = 'Current_Tip'
    EDITOR:                     str = 'Editor'

    MAIN_PREFERENCES: PREFS_NAME_VALUES = cast(PREFS_NAME_VALUES, {
        STARTUP_DIRECTORY:          '.',
        SHOW_TIPS_ON_STARTUP:       'False',
        AUTO_RESIZE_SHAPE_ON_EDIT:  'False',
        SHOW_PARAMETERS:            'False',
        FULL_SCREEN:                'False',
        I18N:                       'en',       # TODO: I think this should be 'English' if I look at the preferences dialog Close code
        CURRENT_TIP:                '0',
        EDITOR:                     'brackets'
    })

    preferencesFileLocationAndName: str = None

    """
    The goal of this class is to handle Pyut Preferences, to load them and save
    them from/to a file.
    To use it :
      - instantiate a PyutPreferences object :
        myPP=PyutPreferences()
      - to get a pyut' preference :
        myPref=myPP["ma_preference"]
      - to set a pyut' preference :
        myPP["ma_preference"]=xxx

      - To change the number of last opened files, use :
        myPP.setNbLOF(x)
      - To get the number of last opened files, use :
        myPP.getNbLOF()
      - To get the list of Last Opened files, use :
        myPP.getLastOpenedFilesList()
      - To add a file to the Last Opened Files list, use :
        myPP.addNewLastOpenedFilesEntry(filename)

    The preferences are loaded on the first instantiation of this
    class and are auto-saved when a value is added or changed.

    """
    def init(self):
        """
        """
        self.logger:  Logger = getLogger(__name__)
        self._emptyPrefs()
        self.__loadConfig()

    @staticmethod
    def determinePreferencesLocation():
        if sys.platform == "linux2" or sys.platform == "linux" or sys.platform == 'darwin':
            PyutPreferences.preferencesFileLocationAndName = os.getenv("HOME") + "/.PyutPrefs.dat"
        else:
            PyutPreferences.preferencesFileLocationAndName = "PyutPrefs.dat"

    @staticmethod
    def getPreferencesLocation():
        if PyutPreferences.preferencesFileLocationAndName is None:
            raise PreferencesLocationNotSet()
        else:
            return PyutPreferences.preferencesFileLocationAndName

    def getNbLOF(self) -> int:
        """

        Returns:  the number of last opened files to keep

        """
        ans: int = self._config.get(PyutPreferences.OPENED_FILES_SECTION, PyutPreferences.NUMBER_OF_ENTRIES)
        return int(ans)

    def setNbLOF(self, nbLOF: int):
        """
        Set the number of last opened files
        Args:
            nbLOF:  The new value for the number or last opened files to remember
        """
        self._config.set(PyutPreferences.OPENED_FILES_SECTION, PyutPreferences.NUMBER_OF_ENTRIES, str(max(nbLOF, 0)))
        self.__saveConfig()

    def getLastOpenedFilesList(self):
        """
        Return the list of files"

        @return list Last Opened files list
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        lstFiles = []

        # Read data
        for index in range(self.getNbLOF()):
            fileNameKey: str = f'{PyutPreferences.FILE_KEY}{str(index+1)}'
            lstFiles.append(self._config.get(PyutPreferences.OPENED_FILES_SECTION, fileNameKey))
        return lstFiles

    def addNewLastOpenedFilesEntry(self, filename):
        """
        Add a file to the list of last opened files

        @param String filename : filename to be added
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        # Get list
        lstFiles = self.getLastOpenedFilesList()

        # Already in list ? => remove
        if filename in lstFiles:
            lstFiles.remove(filename)

        # Insert on top of the list
        lstFiles = [filename]+lstFiles

        # Save
        for idx in range(PyutPreferences.DEFAULT_NB_LOF):
            fileNameKey: str = f'{PyutPreferences.FILE_KEY}{str(idx+1)}'
            self._config.set(PyutPreferences.OPENED_FILES_SECTION, fileNameKey, lstFiles[idx])
        self.__saveConfig()

    def showTipsOnStartup(self) -> bool:
        showTips: bool = self._config.getboolean(PyutPreferences.MAIN_SECTION, PyutPreferences.SHOW_TIPS_ON_STARTUP)
        return showTips

    def autoResizeShapesOnEdit(self) -> bool:
        resizeOrNot: bool = self._config.getboolean(PyutPreferences.MAIN_SECTION, PyutPreferences.AUTO_RESIZE_SHAPE_ON_EDIT)
        return resizeOrNot

    def fullScreen(self) -> bool:
        fullScreenOrNot: bool = self._config.getboolean(PyutPreferences.MAIN_SECTION, PyutPreferences.FULL_SCREEN)
        return fullScreenOrNot

    def __saveConfig(self):
        """
        Save data to config file

        @since 1.1.2.5
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        f = open(PyutPreferences.getPreferencesLocation(), "w")
        self._config.write(f)
        f.close()

    def __loadConfig(self):
        """
        Load preferences from configuration file
        """
        # Make sure that the configuration file exists
        # noinspection PyUnusedLocal
        try:
            f = open(PyutPreferences.getPreferencesLocation(), "r")
            f.close()
        except (ValueError, Exception) as e:
            try:
                f = open(PyutPreferences.getPreferencesLocation(), "w")
                f.write("")
                f.close()
                self.logger.warning(f'Preferences file re-created')
            except (ValueError, Exception) as e:
                self.logger.error(f"Error: {e}")
                return

        # Read data
        self._config = ConfigParser()
        self._config.read(PyutPreferences.getPreferencesLocation())

        # Create a "LastOpenedFiles" structure ?
        hasSection: bool = self._config.has_section(PyutPreferences.OPENED_FILES_SECTION)
        self.logger.debug(f'hasSection: {hasSection}')
        if hasSection is False:
            self.__addOpenedFilesSection()

        self.__addAnyMissingMainPreferences()

    def __addOpenedFilesSection(self):

        self._config.add_section(PyutPreferences.OPENED_FILES_SECTION)
        # Set last opened files
        self._config.set(PyutPreferences.OPENED_FILES_SECTION, PyutPreferences.NUMBER_OF_ENTRIES, str(PyutPreferences.DEFAULT_NB_LOF))
        for idx in range(PyutPreferences.DEFAULT_NB_LOF):
            fileNameKey: str = f'{PyutPreferences.FILE_KEY}{str(idx+1)}'
            self._config.set(PyutPreferences.OPENED_FILES_SECTION, fileNameKey, "")
        self.__saveConfig()

    def __addAnyMissingMainPreferences(self):

        try:
            if self._config.has_section(PyutPreferences.MAIN_SECTION) is False:
                self._config.add_section(PyutPreferences.MAIN_SECTION)

            for prefName in PyutPreferences.MAIN_PREFERENCES.keys():
                if self._config.has_option(PyutPreferences.MAIN_SECTION, prefName) is False:
                    self.__addMissingMainPreference(prefName, PyutPreferences.MAIN_PREFERENCES[prefName])

        except (ValueError, Exception) as e:
            self.logger.error(f"Error: {e}")

    def __addMissingMainPreference(self, preferenceName, value: str):
        self.__addMissingPreference(PyutPreferences.MAIN_SECTION, preferenceName, value)

    def __addMissingPreference(self, sectionName: str, preferenceName, value: str):
        self._config.set(sectionName, preferenceName, value)
        self.__saveConfig()

    def _emptyPrefs(self):
        self._config: ConfigParser = ConfigParser()

    def __getitem__(self, name: str) -> str:
        """
        Magic method
        Return the pyut preferences for the given item

        Args:
            name:
                Name of the item for which we return a value
        Returns:
            value of the preference, or None if it is not defined
        """
        if not self._config.has_section(PyutPreferences.MAIN_SECTION):
            return cast(str, None)

        try:
            return self._config.get(PyutPreferences.MAIN_SECTION, name)
        except NoOptionError:
            return cast(str, None)

    def __setitem__(self, name: str, value: str):
        """
        Return the pyut preferences for the given item

        @param String name : Name of the item WITHOUT SPACES
        @param String value : Value for the given name
        @raises TypeError : if the name contains spaces
        @since 1.1.2.7
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        # Add 'Main' section ?
        if not self._config.has_section("Main"):
            self._config.add_section("Main")

        if " " in list(name):
            raise TypeError("Name cannot contain a space")

        # Save
        self._config.set("Main", name, str(value))
        self.__saveConfig()

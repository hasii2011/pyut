
from logging import Logger
from logging import getLogger

import sys
import os

from org.pyut.general.Singleton import Singleton
from configparser import *


# Set the Preferences filename
if sys.platform == "linux2" or sys.platform == "linux" or sys.platform == 'darwin':
    PREFS_FILENAME = os.getenv("HOME") + "/.PyutPrefs.dat"
else:
    PREFS_FILENAME = "PyutPrefs.dat"

DEFAULT_NB_LOF  = 5    # Number of last opened files, by default

MAIN_SECTION:             str = 'Main'
OPENED_FILES_SECTION:     str = "LastOpenedFiles"
SHOW_TIPS_ON_STARTUP_KEY: str = 'ShowTipsOnStartup'


class PyutPreferences(Singleton):
    """
    The goal of this class is to handle Pyut Preferences, to load them and save
    them from/to a file.
    To use it :
      - instantiate a PyutPreferences object :
        myPP=PyutPreferences()
      - to get a pyut' preference :
        mypref=myPP["ma_preference"]
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

    The preferences are automatically loaded on the first instanciation of this
    class and are saved when a value is added or changed automatically, too.
    ---
    @since 1.0
    """
    def init(self):
        """
        Constructor

        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self.logger: Logger = getLogger(__name__)

        self._config = None
        self.__loadConfig()

    def __getitem__(self, name):
        """
        Return the pyut preferences for the given item

        @param String name : Name of the item for which we return a value
        @return String : value of the pref, or None if inexistant
        @since 1.1.2.7
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        if not self._config.has_section("Main"):
            return None

        try:
            return self._config.get("Main", name)
        except NoOptionError:
            return None

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

    def __saveConfig(self):
        """
        Save data to config file

        @since 1.1.2.5
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        f = open(PREFS_FILENAME, "w")
        self._config.write(f)
        f.close()

    def __loadConfig(self):
        """
        Load data from config file

        @since 1.1.2.5
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        # Make sure that the configuration file exist
        try:
            f = open(PREFS_FILENAME, "r")
            f.close()
        except (ValueError, Exception) as e:
            try:
                f = open(PREFS_FILENAME, "w")
                f.write("")
                f.close()
                self.logger.warning(f'Prefs file re-created')
            except (ValueError, Exception) as e:
                self.logger.error(f"Error: {e}")
                return

        # Read data
        self._config = ConfigParser()
        self._config.read(PREFS_FILENAME)

        # Create a "LastOpenedFiles" structure ?
        hasSection: bool = self._config.has_section(OPENED_FILES_SECTION)
        self.logger.debug(f'hasSection: {hasSection}')
        if hasSection is False:
            # Add section
            self._config = ConfigParser()
            self._config.add_section(OPENED_FILES_SECTION)

            # Set last opened files
            self._config.set(OPENED_FILES_SECTION, "NbEntries", str(DEFAULT_NB_LOF))
            for i in range(DEFAULT_NB_LOF):
                self._config.set(OPENED_FILES_SECTION, "File" + str(i + 1), "")
            self.__saveConfig()
        else:
            self.logger.debug(f'Found all my preferences sections.')

    def getNbLOF(self):
        """
        Return the number of last opened files

        @return Number of last opened files
        @since 1.Config0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        ans: int = self._config.get("LastOpenedFiles", "NbEntries")
        return int(ans)

    def setNbLOF(self, nbLOF):
        """
        Set the number of last opened files

        @param int nbLOF : Number or last opened files
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._config.set("LastOpenedFiles", "NbEntries", str(max(nbLOF, 0)))
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
            lstFiles.append(self._config.get("LastOpenedFiles", "File" + str(index+1)))
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
        for i in range(DEFAULT_NB_LOF):
            self._config.set("LastOpenedFiles", "File" + str(i+1), lstFiles[i])
        self.__saveConfig()

    def showTipsOnStartup(self) -> bool:

        showTips: bool = self._config.getboolean('Main', SHOW_TIPS_ON_STARTUP_KEY)
        return showTips

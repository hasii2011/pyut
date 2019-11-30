
from os import chdir
from os import getcwd
from sys import path as sysPath
from sys import argv

import json

from logging import Logger
from logging import getLogger

import logging.config

from org.pyut.PyutUtils import PyutUtils
from org.pyut.PyutPreferences import PyutPreferences

from org.pyut.ui.PyutApp import PyutApp

from org.pyut.enums.ResourceTextType import ResourceTextType

from org.pyut.general.Lang import importLanguage as setupPyutLanguage
from org.pyut.general.PyutVersion import PyutVersion


class Pyut2:

    JSON_LOGGING_CONFIG_FILENAME: str = "loggingConfiguration.json"
    MADE_UP_PRETTY_MAIN_NAME:     str = "Pyut"

    def __init__(self):
        self._setupSystemLogging()
        self.logger: Logger = getLogger('Pyut2')
        setupPyutLanguage()

        self._exePath:  str = self._getExePath()
        self._userPath: str = getcwd()      # where the user launched pyut from
        PyutUtils.setBasePath(self._exePath)

    def getUserPath(self) -> str:
        return self._userPath

    def setUserPath(self, theNewValue: str):
        self._userPath = theNewValue

    userPath = property(getUserPath, setUserPath)

    def _setupSystemLogging(self):

        with open(Pyut2.JSON_LOGGING_CONFIG_FILENAME, 'r') as loggingConfigurationFile:
            configurationDictionary = json.load(loggingConfigurationFile)

        logging.config.dictConfig(configurationDictionary)
        logging.logProcesses = False
        logging.logThreads = False

    def startApp(self):
        self._setOurSysPath()
        self._updateOurDirectoryPreferences()
        self._displayIntro()
        app: PyutApp = PyutApp(redirect=False)
        app.MainLoop()

    def _getExePath(self) -> str:
        """
        Return the absolute path currently used
        """
        absPath = sysPath[0]
        return absPath

    def _setOurSysPath(self):
        try:
            sysPath.append(self._exePath)
            chdir(self._exePath)
        except OSError as msg:
            self.logger.error(f"Error while setting path: {msg}")

    def _updateOurDirectoryPreferences(self):
        """
        Define last open directory ?
            - default is current directory
            - last opened directory for developers (pyut/src present)
        """
        prefs: PyutPreferences = PyutPreferences()    # Prefs handler
        prefs["orgDirectory"] = getcwd()
        if (self._userPath.find('pyut/src') == -1) and (self._userPath.find('pyut2/src') == -1):

            self.logger.debug(f'self._userPath: {self._userPath}')
            prefs["LastDirectory"] = self._userPath
            self.logger.debug(f'prefs: {prefs}')

    def _displayIntro(self):

        introText: str = PyutUtils.retrieveResourceText(ResourceTextType.INTRODUCTION_TEXT_TYPE)
        print(introText)
        self.displayVersionInformation()

    def displayVersionInformation(self):
        import wx
        import sys
        import platform

        print("Versions: ")
        print(f"PyUt:     {PyutVersion.getPyUtVersion()}")
        print(f'Platform: {platform.platform()}')
        print(f'    System:       {platform.system()}')
        print(f'    Version:      {platform.version()}')
        print(f'    Release:      {platform.release()}')

        print(f'WxPython: {wx.__version__}')
        print(f'Python:   {sys.version.split(" ")[0]}')


def handleCommandLineArguments(pyut: Pyut2) -> bool:
    """
    Handle command line arguments, display help, ...

    @return True if arguments were found and handled (means no startup)
    """
    # Exit if no arguments
    if len(argv) < 2:
        return False

    # Treat command line arguments
    if argv[1] == "--version":
        pyut.displayVersionInformation()
        return True
    elif argv[1] == "--help":
        print(f"PyUt, version {PyutVersion.getPyUtVersion()}")
        helpText: str = PyutUtils.retrieveResourceText(ResourceTextType.HELP_TEXT_TYPE)
        print(helpText)
        return True
    for param in argv[1:]:
        if param[:18] == "--start_directory=":
            print(f'Starting with default directory: {param[18:]}')
            pyut.setUserPath(param[18:])
    return False


# Program entry point
if __name__ == "__main__":

    # setupSystemLogging()
    print(f"Starting {Pyut2.MADE_UP_PRETTY_MAIN_NAME}")

    pyut2: Pyut2 = Pyut2()

    # Launch pyut
    if handleCommandLineArguments(pyut=pyut2) is not True:
        pyut2.startApp()

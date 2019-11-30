
from typing import cast

from os import chdir
from os import getcwd
from sys import path as sysPath
from sys import argv

import json

from logging import Logger
from logging import getLogger

import logging.config

from pkg_resources import resource_filename

from org.pyut.ui.PyutApp import PyutApp
from org.pyut.PyutUtils import PyutUtils

from org.pyut.general.PyutVersion import PyutVersion
from org.pyut.PyutPreferences import PyutPreferences

from org.pyut.general.Lang import importLanguage as setupPyutLanguage

JSON_LOGGING_CONFIG_FILENAME = "loggingConfiguration.json"
MADE_UP_PRETTY_MAIN_NAME     = "Pyut"

moduleLogger: Logger = cast(Logger, None)


# def setupSystemLogging():
#
#     global moduleLogger
#
#     with open(JSON_LOGGING_CONFIG_FILENAME, 'r') as loggingConfigurationFile:
#         configurationDictionary = json.load(loggingConfigurationFile)
#
#     logging.config.dictConfig(configurationDictionary)
#     logging.logProcesses = False
#     logging.logThreads   = False
#
#     moduleLogger = getLogger(MADE_UP_PRETTY_MAIN_NAME)


class Pyut2:
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

        with open(JSON_LOGGING_CONFIG_FILENAME, 'r') as loggingConfigurationFile:
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

        fileName = resource_filename('org.pyut.resources', 'Kilroy-Pyut.txt')
        self.logger.debug(f'Intro text filename: {fileName}')
        objRead = open(fileName, 'r')
        introText: str = objRead.read()
        print(introText)

        print("Versions found : ")
        import wx
        import sys
        print("WX     ", wx.__version__)
        print("Python ", sys.version.split(" ")[0])
        print(" =============================================================================")


def handlCommandLineArguments(pyut: Pyut2) -> bool:
    """
    Handle command line arguments, display help, ...

    @return True if arguments were found and handled (means no startup)
    """
    # Exit if no arguments
    if len(argv) < 2:
        return False

    # Treat command line arguments
    if argv[1] == "--version":
        print(f"PyUt version {PyutVersion.getPyUtVersion()}")
        print()
        return True
    elif argv[1] == "--help":
        print(f"PyUt, version {PyutVersion.getPyUtVersion()}")
        print("Syntax : pyut.pyw [filename] [--version] [--help] [--start_directory=xxx] file1 file2 ...")
        print()
        print("i.e. :    pyut.pyw --version             display version number")
        print("          pyut.pyw --help                display this help")
        print("          pyut.pyw file1 file2           load files")
        print("          pyut.pyw --start_directory=/   start with '/' as")
        print("                                         default directory")
        print()
        return True
    for param in argv[1:]:
        if param[:18] == "--start_directory=":
            print(f'Starting with default directory: {param[18:]}')
            pyut.setUserPath(param[18:])
    return False


# Program entry point
if __name__ == "__main__":

    # setupSystemLogging()
    print(f"Starting {MADE_UP_PRETTY_MAIN_NAME}")

    pyut2: Pyut2 = Pyut2()

    # Launch pyut
    if handlCommandLineArguments(pyut=pyut2) is not True:
        pyut2.startApp()

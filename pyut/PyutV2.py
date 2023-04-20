
from os import chdir
from os import getcwd
from os import environ

from sys import path as sysPath
from sys import argv

from logging import Logger
from logging import getLogger

import logging.config

from json import load as jsonLoad

from pyut.PyutConstants import PyutConstants
from pyut.PyutUtils import PyutUtils
from pyut.preferences.PyutPreferences import PyutPreferences

from pyut.uiv2.PyutAppV2 import PyutAppV2

from pyut.enums.ResourceTextType import ResourceTextType

from pyut.general.PyutVersion import PyutVersion


class PyutV2:

    JSON_LOGGING_CONFIG_FILENAME: str = "loggingConfiguration.json"

    def __init__(self):
        self._setupSystemLogging()
        self.logger: Logger = getLogger(PyutConstants.MAIN_LOGGING_NAME)
        PyutPreferences.determinePreferencesLocation()
        # Lang.importLanguage()

        self._exePath:  str = self._getExePath()
        self._userPath: str = getcwd()      # where the user launched pyut from
        PyutUtils.setBasePath(self._exePath)

        self._cmdLineArgsHandled: bool = False
        """
        If `True` then we handled some command line arguments that do not require the
        full startup of Pyut.  Examples of this are `--help` or `--version`.
        TODO:  Perhaps rename this to `_startupUI` or `_fullStartup` or `_startUI`
        """
        self.handleCommandLineArguments()

        optimize: str | None = environ.get(f'{PyutConstants.PYTHON_OPTIMIZE}')
        self.logger.info(f'{PyutConstants.PYTHON_OPTIMIZE}=`{optimize}`')

    @property
    def userPath(self) -> str:
        return self._userPath

    @userPath.setter
    def userPath(self, theNewValue: str):
        self._userPath = theNewValue
        prefs: PyutPreferences = PyutPreferences()
        prefs.userDirectory = theNewValue

    @property
    def cmdLineArgsHandled(self) -> bool:
        return self._cmdLineArgsHandled

    @cmdLineArgsHandled.setter
    def cmdLineArgsHandled(self, theNewValue: bool):
        self._cmdLineArgsHandled = theNewValue

    def _setupSystemLogging(self):

        configFilePath: str = PyutUtils.retrieveResourcePath(PyutV2.JSON_LOGGING_CONFIG_FILENAME)

        with open(configFilePath, 'r') as loggingConfigurationFile:
            configurationDictionary = jsonLoad(loggingConfigurationFile)

        logging.config.dictConfig(configurationDictionary)
        logging.logProcesses = False
        logging.logThreads   = False

    def startApp(self):
        # self._setOurSysPath()
        self._updateOurDirectoryPreferences()
        self._displayIntro()
        app: PyutAppV2 = PyutAppV2(redirect=False)

        pyutV2.displaySystemMetrics()

        app.MainLoop()

    def _getExePath(self) -> str:
        """
        Return the absolute path currently used
        """
        absPath = sysPath[0]
        return absPath

    def _setOurSysPath(self):
        appMode: str | None = environ.get(f'{PyutConstants.APP_MODE}')
        self.logger.info(f'{PyutConstants.APP_MODE}=`{appMode}`  {self._exePath=}')
        if appMode != 'True':
            try:
                sysPath.append(self._exePath)
                chdir(self._exePath)
            except OSError as msg:
                self.logger.error(f"_setOurSysPath - Error while setting path: {msg}")

    def _updateOurDirectoryPreferences(self):
        """
        Define last open directory ?
            - default is current directory
            - last opened directory for developers (pyut/src present)
        """
        prefs: PyutPreferences = PyutPreferences()    # Prefs handler
        prefs.orgDirectory = getcwd()

        if (self._userPath.find('PyUt/src') == -1) and (self._userPath.find('PyUt2/src') == -1):

            self.logger.debug(f'{self._userPath=}')

            prefs.lastOpenedDirectory = self._userPath
            self.logger.debug(f'{prefs.lastOpenedDirectory=}')

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

    def displaySystemMetrics(self):
        from wx import ScreenDC
        from wx import DisplaySize
        from wx import Size

        size: Size = ScreenDC().GetPPI()
        print('')
        print(f'Display Size: {DisplaySize()}')
        print(f'x-DPI: {size.GetWidth()} y-DPI: {size.GetHeight()}')
        print(f'toolBarIconSize: {PyutPreferences().toolBarIconSize.value}')

        # noinspection PyUnreachableCode
        if __debug__:
            self.logger.info("Assertions are turned on")
        else:
            self.logger.info("Assertions are turned off")

    def handleCommandLineArguments(self):
        """
        Handle command line arguments, display help, ...

        @return True if arguments were found and handled (means no startup)
        """

        if len(argv) < 2:
            self.cmdLineArgsHandled = False
            return
        # Process command line arguments
        if argv[1] == "--version":
            self.displayVersionInformation()
            self.cmdLineArgsHandled = True
            return
        elif argv[1] == "--help":
            print(f"PyUt, version {PyutVersion.getPyUtVersion()}")
            helpText: str = PyutUtils.retrieveResourceText(ResourceTextType.HELP_TEXT_TYPE)
            print(helpText)
            self.cmdLineArgsHandled = True
            return

        for param in argv[1:]:
            if param[:18] == "--start_directory=":
                print(f'Starting with default directory: {param[18:]}')
                self.userPath = param[18:]
        self.cmdLineArgsHandled = False


if __name__ == "__main__":

    print(f'Starting Pyut')

    pyutV2: PyutV2 = PyutV2()

    # Launch pyut
    if pyutV2.cmdLineArgsHandled is False:
        pyutV2.startApp()

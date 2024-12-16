
from logging import Logger
from logging import getLogger

import logging.config

from json import load as jsonLoad

from os import environ

from sys import argv

from pyut import __version__ as pyutVersion

from pyut.PyutConstants import PyutConstants
from pyut.PyutUtils import PyutUtils
from pyut.preferences.PyutPreferences import PyutPreferences

from pyut.ui.main.PyutApp import PyutApp

from pyut.enums.ResourceTextType import ResourceTextType


class Pyut:

    JSON_LOGGING_CONFIG_FILENAME: str = "loggingConfiguration.json"

    def __init__(self):
        self._setupApplicationLogging()

        self.logger: Logger = getLogger(PyutConstants.MAIN_LOGGING_NAME)

        self._cmdLineArgsHandled: bool = False
        """
        If `True` then we handled some command line arguments that do not require the
        full startup of Pyut.  Examples of this are `--help` or `--version`.
        """
        self._handleCommandLineArguments()

        optimize: str | None = environ.get(f'{PyutConstants.PYTHON_OPTIMIZE}')
        self.logger.info(f'{PyutConstants.PYTHON_OPTIMIZE}=`{optimize}`')

    @property
    def cmdLineArgsHandled(self) -> bool:
        return self._cmdLineArgsHandled

    @cmdLineArgsHandled.setter
    def cmdLineArgsHandled(self, theNewValue: bool):
        self._cmdLineArgsHandled = theNewValue

    def _setupApplicationLogging(self):

        configFilePath: str = PyutUtils.retrieveResourcePath(Pyut.JSON_LOGGING_CONFIG_FILENAME)

        with open(configFilePath, 'r') as loggingConfigurationFile:
            configurationDictionary = jsonLoad(loggingConfigurationFile)

        logging.config.dictConfig(configurationDictionary)
        logging.logProcesses = False
        logging.logThreads   = False

    def startApplication(self):
        self._displayIntroduction()
        app: PyutApp = PyutApp(redirect=False)

        pyut._displaySystemMetrics()

        app.MainLoop()

    def _displayIntroduction(self):

        introText: str = PyutUtils.retrieveResourceText(ResourceTextType.INTRODUCTION_TEXT_TYPE)
        print(introText)
        self._displayVersionInformation()

    def _displayVersionInformation(self):
        import wx
        import sys
        import platform

        from ogl import __version__ as oglVersion
        # noinspection PyPackageRequirements
        from untanglepyut import __version__ as untanglePyutVersion
        from oglio import __version__ as oglioVersion
        from pyutplugins import __version__ as pluginVersion

        print("Versions: ")
        print(f"PyUt:     {pyutVersion}")
        print(f'Platform: {platform.platform()}')
        print(f'    System:       {platform.system()}')
        print(f'    Version:      {platform.version()}')
        print(f'    Release:      {platform.release()}')

        print(f'WxPython: {wx.__version__}')
        print(f'')
        print(f'Pyut Packages')
        print(f'    Ogl:             {oglVersion}')
        print(f'    Untangle Pyut:   {untanglePyutVersion}')
        print(f'    OglIO:           {oglioVersion}')
        print(f'    Plugin Platform: {pluginVersion}')

        print(f'')
        print(f'Python:   {sys.version.split(" ")[0]}')

    def _displaySystemMetrics(self):
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

    def _handleCommandLineArguments(self):
        """
        Handle command line arguments, display help, and version

        Returns:  if arguments were found and handled (means no startup)
        """
        if len(argv) < 2:
            self.cmdLineArgsHandled = False
            return
        # Process command line arguments
        if argv[1] == "--version":
            self._displayVersionInformation()
            self.cmdLineArgsHandled = True
            return
        elif argv[1] == "--help":
            print(f"PyUt, version {pyutVersion}")
            helpText: str = PyutUtils.retrieveResourceText(ResourceTextType.HELP_TEXT_TYPE)
            print(helpText)
            self.cmdLineArgsHandled = True
            return
        else:
            self.logger.info(f'If these are files;  Will be loaded by PyutApp startup')
        self.cmdLineArgsHandled = False


if __name__ == "__main__":

    print(f'Starting Pyut')

    pyut: Pyut = Pyut()

    # Launch pyut
    if pyut.cmdLineArgsHandled is False:
        pyut.startApplication()

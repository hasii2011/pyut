
from logging import Logger
from logging import getLogger

import logging.config

from json import load as jsonLoad

from os import environ

from sys import argv

from pyut import START_STOP_MARKER
from pyut import __version__ as pyutVersion
from pyut.PyutConstants import PyutConstants

from pyut.general.Version import Version
from pyut.general.PyutSystemMetrics import PyutSystemMetrics

from pyut.PyutUtils import PyutUtils

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
        self.logger.debug(f'{PyutConstants.PYTHON_OPTIMIZE}=`{optimize}`')

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

        self.logger.info(f'Pyut startup complete.')
        app.MainLoop()

    def _displayIntroduction(self):

        introText: str = PyutUtils.retrieveResourceText(ResourceTextType.INTRODUCTION_TEXT_TYPE)
        print(introText)
        self._displayVersionInformation()

    def _displayVersionInformation(self):
        import platform

        version: Version = Version()
        print("Versions: ")
        print(f"Pyut:     {version.applicationVersion}")
        print(f'Platform: {version.platform}')
        print(f'    System:       {platform.system()}')
        print(f'    Version:      {platform.version()}')
        print(f'    Release:      {platform.release()}')

        print(f'WxPython: {version.wxPythonVersion}')
        print(f'')
        print(f'Pyut Packages')
        print(f'    Ogl:             {version.oglVersion}')
        print(f'    Untangle Pyut:   {version.untanglePyutVersion}')
        print(f'    OglIO:           {version.oglioVersion}')
        print(f'    Plugin Platform: {version.pyutPluginsVersion}')

        print(f'')
        print(f'Python:   {version.pythonVersion}')

    def _displaySystemMetrics(self):

        from wx import Size

        metrics: PyutSystemMetrics = PyutSystemMetrics()
        size:    Size              = metrics.screenResolution
        print('')
        print(f'Display Size: {metrics.displaySize}')
        print(f'x-DPI: {size.GetWidth()} y-DPI: {size.GetHeight()}')
        print(f'toolBarIconSize: {metrics.toolBarIconSize}')

        # noinspection PyUnreachableCode
        if __debug__:
            self.logger.debug("Assertions are turned on")
        else:
            self.logger.debug("Assertions are turned off")

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
            self.logger.debug(f'If these are files, the will be loaded by PyutApp startup')
        self.cmdLineArgsHandled = False


if __name__ == "__main__":

    print(f'Starting Pyut')

    pyut: Pyut = Pyut()
    pyut.logger.info(START_STOP_MARKER)
    pyut.logger.info(f'Pyut Version {pyutVersion} starting')

    # Launch pyut
    if pyut.cmdLineArgsHandled is False:
        pyut.startApplication()


from logging import Logger
from logging import getLogger

from os import sep as osSeparator
from os import environ as osEnviron

from codeallybasic.SingletonV3 import SingletonV3

from pyut.preferences.PyutPreferencesV2 import PyutPreferencesV2


class CurrentDirectoryHandler(metaclass=SingletonV3):

    HOME_ENV_VAR:            str = 'HOME'
    DIAGRAMS_DIRECTORY_NAME: str = ''

    def __init__(self):

        self.logger:            Logger            = getLogger(__name__)
        self._preferences:      PyutPreferencesV2 = PyutPreferencesV2()
        self._currentDirectory: str               = ''

        if self._preferences.diagramsDirectory == '':
            if CurrentDirectoryHandler.HOME_ENV_VAR in osEnviron:
                self._currentDirectory              = osEnviron[CurrentDirectoryHandler.HOME_ENV_VAR]
                self._preferences.diagramsDirectory = osEnviron[CurrentDirectoryHandler.HOME_ENV_VAR]
        else:
            self._currentDirectory = self._preferences.diagramsDirectory

    @property
    def currentDirectory(self):

        return self._currentDirectory

    @currentDirectory.setter
    def currentDirectory(self, fullPath: str):
        """
        Set the current working directory.
        We'll strip off the filename

        Args:
            fullPath:   Full path, with filename
        """
        self._currentDirectory = fullPath[:fullPath.rindex(osSeparator)]

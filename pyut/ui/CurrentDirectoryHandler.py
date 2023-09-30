
from logging import Logger
from logging import getLogger

from os import sep as osSeparator
from os import environ as osEnviron

from codeallybasic.Singleton import Singleton

from pyut.preferences.PyutPreferences import PyutPreferences


class CurrentDirectoryHandler(Singleton):

    HOME_ENV_VAR:            str = 'HOME'
    DIAGRAMS_DIRECTORY_NAME: str = ''

    # noinspection PyAttributeOutsideInit
    def init(self):

        self.logger:            Logger          = getLogger(__name__)
        self._preferences:      PyutPreferences = PyutPreferences()
        self._currentDirectory: str             = ''

        if self._preferences.diagramsDirectory == '':
            if CurrentDirectoryHandler.HOME_ENV_VAR in osEnviron:
                self._currentDirectory              = osEnviron[CurrentDirectoryHandler.HOME_ENV_VAR]
                self._preferences.diagramsDirectory = osEnviron[CurrentDirectoryHandler.HOME_ENV_VAR]

    @property
    def currentDirectory(self):

        return self._currentDirectory

    @currentDirectory.setter
    def currentDirectory(self, fullPath: str):
        """
        Set current working directory.

        Args:
            fullPath:   Full path, with filename
        """
        # noinspection PyAttributeOutsideInit
        self._currentDirectory = fullPath[:fullPath.rindex(osSeparator)]

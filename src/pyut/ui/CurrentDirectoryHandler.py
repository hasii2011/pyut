
from logging import Logger
from logging import getLogger

from os import getcwd
from os import sep as osSeparator

from pyut.general.Singleton import Singleton
from pyut.preferences.PyutPreferences import PyutPreferences


class CurrentDirectoryHandler(Singleton):

    def init(self):

        self.logger: Logger = getLogger(__name__)

        self._preferences: PyutPreferences = PyutPreferences()

        self._lastDir = getcwd()

    @property
    def currentDirectory(self):

        return self._lastDir

    @currentDirectory.setter
    def currentDirectory(self, fullPath: str):
        """
        Set current working directory.

        Args:
            fullPath:   Full path, with filename
        """
        self._lastDir = fullPath[:fullPath.rindex(osSeparator)]

        self._preferences.lastOpenedDirectory = self._lastDir

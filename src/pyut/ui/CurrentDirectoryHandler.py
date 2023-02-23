
from logging import Logger
from logging import getLogger

from os import getcwd
from os import sep as osSeparator

from hasiicommon.Singleton import Singleton

from pyut.preferences.PyutPreferences import PyutPreferences


class CurrentDirectoryHandler(Singleton):

    # noinspection PyAttributeOutsideInit
    def init(self):

        self.logger:       Logger          = getLogger(__name__)
        self._preferences: PyutPreferences = PyutPreferences()
        self._lastDir:     str             = getcwd()

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
        # noinspection PyAttributeOutsideInit
        self._lastDir = fullPath[:fullPath.rindex(osSeparator)]

        self._preferences.lastOpenedDirectory = self._lastDir

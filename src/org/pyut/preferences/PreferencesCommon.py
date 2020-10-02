
from typing import Dict

import sys

import os

from configparser import ConfigParser

from org.pyut.PyutConstants import PyutConstants
from org.pyut.general.Singleton import Singleton
from org.pyut.general.exceptions.PreferencesLocationNotSet import PreferencesLocationNotSet

PREFS_NAME_VALUES = Dict[str, str]


class PreferencesCommon(Singleton):

    preferencesFileLocationAndName: str = None

    def init(self, theMasterParser: ConfigParser):

        self._config = theMasterParser

    @staticmethod
    def determinePreferencesLocation():
        """
        This method MUST (I repeat MUST) be called before attempting to instantiate the preferences Singleton
        """
        if sys.platform == "linux2" or sys.platform == "linux" or sys.platform == PyutConstants.THE_GREAT_MAC_PLATFORM:
            PreferencesCommon.preferencesFileLocationAndName = os.getenv("HOME") + "/.PyutPrefs.dat"
        else:
            PreferencesCommon.preferencesFileLocationAndName = "PyutPrefs.dat"

    @staticmethod
    def getPreferencesLocation():
        if PreferencesCommon.preferencesFileLocationAndName is None:
            raise PreferencesLocationNotSet()
        else:
            return PreferencesCommon.preferencesFileLocationAndName

    def addMissingPreference(self, sectionName: str, preferenceName: str, value: str):
        self._config.set(sectionName, preferenceName, value)
        self.saveConfig()

    def saveConfig(self):
        """
        Save data to the preferences file
        """
        f = open(PreferencesCommon.getPreferencesLocation(), "w")
        self._config.write(f)
        f.close()

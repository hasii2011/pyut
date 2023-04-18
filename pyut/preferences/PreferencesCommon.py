
from typing import Dict
from typing import Optional
from typing import cast

import sys

import os

from pyut.PyutConstants import PyutConstants
from pyut.general.exceptions.PreferencesLocationNotSet import PreferencesLocationNotSet
from pyut.preferences.BaseSubPreference import BaseSubPreference

PREFS_NAME_VALUES = Dict[str, str]


class PreferencesCommon(BaseSubPreference):

    PREFERENCES_FILENAME: str = 'pyut.ini'

    preferencesFileLocationAndName: str = cast(str, None)

    def init(self, *args, **kwargs):

        BaseSubPreference.init(self, *args, **kwargs)

    @staticmethod
    def determinePreferencesLocation():
        """
        This method MUST (I repeat MUST) be called before attempting to instantiate the preferences Singleton
        """
        if sys.platform == "linux2" or sys.platform == "linux" or sys.platform == PyutConstants.THE_GREAT_MAC_PLATFORM:
            homeDir:  Optional[str] = os.getenv('HOME')
            fullName: str = f'{homeDir}/{PreferencesCommon.PREFERENCES_FILENAME}'
            PreferencesCommon.preferencesFileLocationAndName = fullName
        else:
            PreferencesCommon.preferencesFileLocationAndName = PreferencesCommon.PREFERENCES_FILENAME

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
        with open(PreferencesCommon.getPreferencesLocation(), "w") as fd:
            self._config.write(fd)

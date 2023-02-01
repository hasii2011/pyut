
from logging import Logger
from logging import getLogger

from pyut.preferences.BaseSubPreference import BaseSubPreference

from pyut.preferences.PreferencesCommon import PREFS_NAME_VALUES
from pyut.preferences.PreferencesCommon import PreferencesCommon


class DebugPreferences(BaseSubPreference):

    DEBUG_SECTION:   str = 'Debug'

    DEBUG_ERROR_VIEWS:             str = 'debug_error_views'              # If true allows testing of the error views through Pyut

    DEBUG_PREFERENCES:  PREFS_NAME_VALUES = {
        DEBUG_ERROR_VIEWS:              'False'
    }

    def init(self, *args, **kwargs):

        self.logger:  Logger       = getLogger(__name__)

        BaseSubPreference.init(self, *args, **kwargs)

        self._preferencesCommon: PreferencesCommon = PreferencesCommon(self._config)

    def addAnyMissingDebugPreferences(self):

        try:
            if self._config.has_section(DebugPreferences.DEBUG_SECTION) is False:
                self._config.add_section(DebugPreferences.DEBUG_SECTION)

            for prefName in DebugPreferences.DEBUG_PREFERENCES.keys():
                if self._config.has_option(DebugPreferences.DEBUG_SECTION, prefName) is False:
                    self.__addMissingDebugPreference(prefName, DebugPreferences.DEBUG_PREFERENCES[prefName])

        except (ValueError, Exception) as e:
            self.logger.error(f"Error: {e}")

    @property
    def debugErrorViews(self):
        ans: bool = self._config.getboolean(DebugPreferences.DEBUG_SECTION, DebugPreferences.DEBUG_ERROR_VIEWS)
        return ans

    @debugErrorViews.setter
    def debugErrorViews(self, theNewValue: bool):
        self._config.set(DebugPreferences.DEBUG_SECTION, DebugPreferences.DEBUG_ERROR_VIEWS, str(theNewValue))
        self._preferencesCommon.saveConfig()

    def __addMissingDebugPreference(self, preferenceName, value):
        self._preferencesCommon.addMissingPreference(DebugPreferences.DEBUG_SECTION, preferenceName, value)

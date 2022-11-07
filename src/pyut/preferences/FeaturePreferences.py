
from logging import Logger
from logging import getLogger

from pyut.preferences.BaseSubPreference import BaseSubPreference
from pyut.preferences.PreferencesCommon import PREFS_NAME_VALUES
from pyut.preferences.PreferencesCommon import PreferencesCommon


class FeaturePreferences(BaseSubPreference):
    """
    These are the Pyut Feature flags
    """

    FEATURE_SECTION: str = 'Features'
    USE_V2_UI:      str = 'use_v2_ui'

    FEATURE_PREFERENCES:  PREFS_NAME_VALUES = {
        USE_V2_UI: 'True',

    }

    def init(self, *args, **kwargs):

        self.logger: Logger = getLogger(__name__)

        BaseSubPreference.init(self, *args, **kwargs)

        self._preferencesCommon: PreferencesCommon = PreferencesCommon(self._config)

    @property
    def usev2ui(self) -> bool:
        ans: bool = self._config.getboolean(FeaturePreferences.FEATURE_SECTION, FeaturePreferences.USE_V2_UI)
        return ans

    @usev2ui.setter
    def usev2ui(self, newValue: bool):
        self._config.set(FeaturePreferences.FEATURE_SECTION, FeaturePreferences.USE_V2_UI, str(newValue))
        self._preferencesCommon.saveConfig()

    def addAnyMissingFeaturePreferences(self):

        try:
            if self._config.has_section(FeaturePreferences.FEATURE_SECTION) is False:
                self._config.add_section(FeaturePreferences.FEATURE_SECTION)

            for prefName in FeaturePreferences.FEATURE_PREFERENCES.keys():
                if self._config.has_option(FeaturePreferences.FEATURE_SECTION, prefName) is False:
                    self.__addMissingDebugPreference(prefName, FeaturePreferences.FEATURE_PREFERENCES[prefName])

        except (ValueError, Exception) as e:
            self.logger.error(f"Error: {e}")

    def __addMissingDebugPreference(self, preferenceName, value):
        self._preferencesCommon.addMissingPreference(FeaturePreferences.FEATURE_SECTION, preferenceName, value)

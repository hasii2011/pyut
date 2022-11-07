
from logging import Logger
from logging import getLogger

from pyut.preferences.BaseSubPreference import BaseSubPreference

from pyut.preferences.PreferencesCommon import PREFS_NAME_VALUES
from pyut.preferences.PreferencesCommon import PreferencesCommon


class DebugPreferences(BaseSubPreference):

    DEBUG_SECTION:   str = 'Debug'

    DEBUG_TEMP_FILE_LOCATION:      str = 'debug_temp_file_location'       # If `True` any created temporary files appear in the current directory
    PYUTIO_PLUGIN_AUTO_SELECT_ALL: str = 'pyutio_plugin_auto_select_all'  # if `True` auto-select shapes in plugins
    DEBUG_DIAGRAM_FRAME:           str = 'debug_diagram_frame'
    DEBUG_ERROR_VIEWS:             str = 'debug_error_views'              # If true allows testing of the error views through Pyut

    DEBUG_PREFERENCES:  PREFS_NAME_VALUES = {
        DEBUG_TEMP_FILE_LOCATION:       'False',
        PYUTIO_PLUGIN_AUTO_SELECT_ALL:  'False',
        DEBUG_DIAGRAM_FRAME:            'False',
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
    def useDebugTempFileLocation(self) -> bool:
        ans: bool = self._config.getboolean(DebugPreferences.DEBUG_SECTION, DebugPreferences.DEBUG_TEMP_FILE_LOCATION)
        return ans

    @useDebugTempFileLocation.setter
    def useDebugTempFileLocation(self, theNewValue: bool):
        self._config.set(DebugPreferences.DEBUG_SECTION, DebugPreferences.DEBUG_TEMP_FILE_LOCATION, str(theNewValue))
        self._preferencesCommon.saveConfig()

    @property
    def pyutIoPluginAutoSelectAll(self) -> bool:
        ans: bool = self._config.getboolean(DebugPreferences.DEBUG_SECTION, DebugPreferences.PYUTIO_PLUGIN_AUTO_SELECT_ALL)
        return ans

    @pyutIoPluginAutoSelectAll.setter
    def pyutIoPluginAutoSelectAll(self, theNewValue: bool):
        self._config.set(DebugPreferences.DEBUG_SECTION, DebugPreferences.PYUTIO_PLUGIN_AUTO_SELECT_ALL, str(theNewValue))
        self._preferencesCommon.saveConfig()

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

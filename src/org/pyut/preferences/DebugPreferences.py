
from logging import Logger
from logging import getLogger

from configparser import ConfigParser

from org.pyut.general.Singleton import Singleton

from org.pyut.preferences.PreferencesCommon import PREFS_NAME_VALUES
from org.pyut.preferences.PreferencesCommon import PreferencesCommon


class DebugPreferences(Singleton):

    DEBUG_SECTION:   str = 'Debug'

    DEBUG_TEMP_FILE_LOCATION:      str = 'debug_temp_file_location'       # If `True` any created temporary files appear in the current directory
    DEBUG_BASIC_SHAPE:             str = 'debug_basic_shape'              # If `True` turn on debug display code in basic Shape.py
    PYUTIO_PLUGIN_AUTO_SELECT_ALL: str = 'pyutio_plugin_auto_select_all'  # if `True` auto-select shapes in plugins
    DEBUG_DIAGRAM_FRAME:           str = 'debug_diagram_frame'

    DEBUG_PREFERENCES:  PREFS_NAME_VALUES = {
        DEBUG_TEMP_FILE_LOCATION:       'False',
        DEBUG_BASIC_SHAPE:              'False',
        PYUTIO_PLUGIN_AUTO_SELECT_ALL:  'False',
        DEBUG_DIAGRAM_FRAME:            'False'
    }

    def init(self, theMasterParser: ConfigParser):

        self.logger:             Logger            = getLogger(__name__)
        self._config:            ConfigParser      = theMasterParser
        self._preferencesCommon: PreferencesCommon = PreferencesCommon(theMasterParser)

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
    def debugBasicShape(self):
        ans: bool = self._config.getboolean(DebugPreferences.DEBUG_SECTION, DebugPreferences.DEBUG_BASIC_SHAPE)
        return ans

    @debugBasicShape.setter
    def debugBasicShape(self, theNewValue: bool):
        self._config.set(DebugPreferences.DEBUG_SECTION, DebugPreferences.DEBUG_BASIC_SHAPE, str(theNewValue))
        self._preferencesCommon.saveConfig()

    @property
    def debugDiagramFrame(self) -> bool:
        ans: bool = self._config.getboolean(DebugPreferences.DEBUG_SECTION, DebugPreferences.DEBUG_DIAGRAM_FRAME)
        return ans

    @debugDiagramFrame.setter
    def debugDiagramFrame(self, theNewValue: bool):
        self._config.set(DebugPreferences.DEBUG_SECTION, DebugPreferences.DEBUG_DIAGRAM_FRAME, str(theNewValue))
        self._preferencesCommon.saveConfig()

    @property
    def pyutIoPluginAutoSelectAll(self) -> bool:
        ans: bool = self._config.getboolean(DebugPreferences.DEBUG_SECTION, DebugPreferences.PYUTIO_PLUGIN_AUTO_SELECT_ALL)
        return ans

    @pyutIoPluginAutoSelectAll.setter
    def pyutIoPluginAutoSelectAll(self, theNewValue: bool):
        self._config.set(DebugPreferences.DEBUG_SECTION, DebugPreferences.PYUTIO_PLUGIN_AUTO_SELECT_ALL, str(theNewValue))
        self._preferencesCommon.saveConfig()

    def __addMissingDebugPreference(self, preferenceName, value):
        self._preferencesCommon.addMissingPreference(DebugPreferences.DEBUG_SECTION, preferenceName, value)

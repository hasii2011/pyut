
from logging import Logger
from logging import getLogger

from configparser import ConfigParser

from org.pyut.general.Singleton import Singleton

from org.pyut.preferences.PreferencesCommon import PREFS_NAME_VALUES
from org.pyut.preferences.PreferencesCommon import PreferencesCommon


class DiagramPreferences(Singleton):
    """
    """
    DIAGRAM_SECTION: str = 'Diagram'

    BACKGROUND_GRID_ENABLED:  str = 'background_grid_enabled'
    BACKGROUND_GRID_INTERVAL: str = 'background_grid_interval'

    DIAGRAM_PREFERENCES: PREFS_NAME_VALUES = {
        BACKGROUND_GRID_ENABLED: 'True',
        BACKGROUND_GRID_INTERVAL: '15'
    }

    def init(self, theMasterParser: ConfigParser):

        self.logger:             Logger            = getLogger(__name__)
        self._config:            ConfigParser      = theMasterParser
        self._preferencesCommon: PreferencesCommon = PreferencesCommon(theMasterParser)

    def addMissingDiagramPreferences(self):

        try:
            if self._config.has_section(DiagramPreferences.DIAGRAM_SECTION) is False:
                self._config.add_section(DiagramPreferences.DIAGRAM_SECTION)
            for prefName in DiagramPreferences.DIAGRAM_PREFERENCES:
                if self._config.has_option(DiagramPreferences.DIAGRAM_SECTION, prefName) is False:
                    self.__addMissingDiagramPreference(prefName, DiagramPreferences.DIAGRAM_PREFERENCES[prefName])

        except (ValueError, Exception) as e:
            self.logger.error(f"Error: {e}")

    @property
    def backgroundGridEnabled(self) -> bool:
        return self._config.getboolean(DiagramPreferences.DIAGRAM_SECTION, DiagramPreferences.BACKGROUND_GRID_ENABLED)

    @backgroundGridEnabled.setter
    def backgroundGridEnabled(self, theNewValue: bool):
        self._config.set(DiagramPreferences.DIAGRAM_SECTION, DiagramPreferences.BACKGROUND_GRID_ENABLED, str(theNewValue))
        self._preferencesCommon.saveConfig()

    @property
    def backgroundGridInterval(self) -> int:
        return self._config.getint(DiagramPreferences.DIAGRAM_SECTION, DiagramPreferences.BACKGROUND_GRID_INTERVAL)

    @backgroundGridInterval.setter
    def backgroundGridInterval(self, theNewValue: int):
        self._config.set(DiagramPreferences.DIAGRAM_SECTION, DiagramPreferences.BACKGROUND_GRID_INTERVAL, str(theNewValue))
        self._preferencesCommon.saveConfig()

    def __addMissingDiagramPreference(self, preferenceName, value):
        self._preferencesCommon.addMissingPreference(DiagramPreferences.DIAGRAM_SECTION, preferenceName, value)

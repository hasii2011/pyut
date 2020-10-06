
from logging import Logger
from logging import getLogger

from configparser import ConfigParser

from org.pyut.general.Singleton import Singleton

from org.pyut.miniogl.PyutColorEnum import PyutColorEnum
from org.pyut.miniogl.PyutPenStyle import PyutPenStyle

from org.pyut.preferences.PreferencesCommon import PREFS_NAME_VALUES
from org.pyut.preferences.PreferencesCommon import PreferencesCommon


class BackgroundPreferences(Singleton):
    """
    """
    DIAGRAM_SECTION:         str = 'Diagram'
    DEFAULT_GRID_LINE_COLOR: str = PyutColorEnum.LIGHT_GREY.value
    DEFAULT_GRID_LINE_STYLE: str = PyutPenStyle.DOT.value

    BACKGROUND_GRID_ENABLED:  str = 'background_grid_enabled'
    BACKGROUND_GRID_INTERVAL: str = 'background_grid_interval'
    GRID_LINE_COLOR:          str = 'grid_line_color'
    GRID_LINE_STYLE:          str = 'grid_line_style'

    DIAGRAM_PREFERENCES: PREFS_NAME_VALUES = {
        BACKGROUND_GRID_ENABLED: 'True',
        BACKGROUND_GRID_INTERVAL: '15',
        GRID_LINE_COLOR:          DEFAULT_GRID_LINE_COLOR,
        GRID_LINE_STYLE:          DEFAULT_GRID_LINE_STYLE
    }

    def init(self, theMasterParser: ConfigParser):

        self.logger:             Logger            = getLogger(__name__)
        self._config:            ConfigParser      = theMasterParser
        self._preferencesCommon: PreferencesCommon = PreferencesCommon(theMasterParser)

    def addMissingDiagramPreferences(self):

        try:
            if self._config.has_section(BackgroundPreferences.DIAGRAM_SECTION) is False:
                self._config.add_section(BackgroundPreferences.DIAGRAM_SECTION)
            for prefName in BackgroundPreferences.DIAGRAM_PREFERENCES:
                if self._config.has_option(BackgroundPreferences.DIAGRAM_SECTION, prefName) is False:
                    self.__addMissingDiagramPreference(prefName, BackgroundPreferences.DIAGRAM_PREFERENCES[prefName])

        except (ValueError, Exception) as e:
            self.logger.error(f"Error: {e}")

    @property
    def backgroundGridEnabled(self) -> bool:
        return self._config.getboolean(BackgroundPreferences.DIAGRAM_SECTION, BackgroundPreferences.BACKGROUND_GRID_ENABLED)

    @backgroundGridEnabled.setter
    def backgroundGridEnabled(self, theNewValue: bool):
        self._config.set(BackgroundPreferences.DIAGRAM_SECTION, BackgroundPreferences.BACKGROUND_GRID_ENABLED, str(theNewValue))
        self._preferencesCommon.saveConfig()

    @property
    def backgroundGridInterval(self) -> int:
        return self._config.getint(BackgroundPreferences.DIAGRAM_SECTION, BackgroundPreferences.BACKGROUND_GRID_INTERVAL)

    @backgroundGridInterval.setter
    def backgroundGridInterval(self, theNewValue: int):
        self._config.set(BackgroundPreferences.DIAGRAM_SECTION, BackgroundPreferences.BACKGROUND_GRID_INTERVAL, str(theNewValue))
        self._preferencesCommon.saveConfig()

    @property
    def gridLineColor(self) -> PyutColorEnum:

        colorName:     str           = self._config.get(BackgroundPreferences.DIAGRAM_SECTION, BackgroundPreferences.GRID_LINE_COLOR)
        pyutColorEnum: PyutColorEnum = PyutColorEnum(colorName)
        return pyutColorEnum

    @gridLineColor.setter
    def gridLineColor(self, theNewValue: PyutColorEnum):

        colorName: str = theNewValue.value
        self._config.set(BackgroundPreferences.DIAGRAM_SECTION, BackgroundPreferences.GRID_LINE_COLOR, colorName)
        self._preferencesCommon.saveConfig()

    @property
    def gridLineStyle(self) -> PyutPenStyle:
        penStyleName: str          = self._config.get(BackgroundPreferences.DIAGRAM_SECTION, BackgroundPreferences.GRID_LINE_STYLE)
        pyutPenStyle: PyutPenStyle = PyutPenStyle(penStyleName)
        return pyutPenStyle

    @gridLineStyle.setter
    def gridLineStyle(self, theNewValue: PyutPenStyle):

        penStyleName: str = theNewValue.value
        self._config.set(BackgroundPreferences.DIAGRAM_SECTION, BackgroundPreferences.GRID_LINE_STYLE, penStyleName)
        self._preferencesCommon.saveConfig()

    def __addMissingDiagramPreference(self, preferenceName, value):
        self._preferencesCommon.addMissingPreference(BackgroundPreferences.DIAGRAM_SECTION, preferenceName, value)

from logging import Logger
from logging import getLogger

from org.pyut.miniogl.MiniOglColorEnum import MiniOglColorEnum
from org.pyut.miniogl.MiniOglPenStyle import MiniOglPenStyle

from org.pyut.preferences.BaseSubPreference import BaseSubPreference

from org.pyut.preferences.PreferencesCommon import PREFS_NAME_VALUES
from org.pyut.preferences.PreferencesCommon import PreferencesCommon


class BackgroundPreferences(BaseSubPreference):
    """
    """
    DIAGRAM_SECTION:         str = 'Diagram'
    DEFAULT_GRID_LINE_COLOR: str = MiniOglColorEnum.LIGHT_GREY.value
    DEFAULT_GRID_LINE_STYLE: str = MiniOglPenStyle.DOT.value

    BACKGROUND_GRID_ENABLED:  str = 'background_grid_enabled'
    SNAP_TO_GRID:             str = 'snap_to_grid'
    BACKGROUND_GRID_INTERVAL: str = 'background_grid_interval'
    GRID_LINE_COLOR:          str = 'grid_line_color'
    GRID_LINE_STYLE:          str = 'grid_line_style'

    DIAGRAM_PREFERENCES: PREFS_NAME_VALUES = {
        BACKGROUND_GRID_ENABLED: 'True',
        SNAP_TO_GRID:            'True',
        BACKGROUND_GRID_INTERVAL: '25',
        GRID_LINE_COLOR:          DEFAULT_GRID_LINE_COLOR,
        GRID_LINE_STYLE:          DEFAULT_GRID_LINE_STYLE
    }

    def init(self, *args, **kwds):

        self.logger: Logger = getLogger(__name__)

        BaseSubPreference.init(self, *args, **kwds)

        self._preferencesCommon: PreferencesCommon = PreferencesCommon(self._config)

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
    def snapToGrid(self) -> bool:
        return self._config.getboolean(BackgroundPreferences.DIAGRAM_SECTION, BackgroundPreferences.SNAP_TO_GRID)

    @snapToGrid.setter
    def snapToGrid(self, theNewValue: bool):
        self._config.set(BackgroundPreferences.DIAGRAM_SECTION, BackgroundPreferences.SNAP_TO_GRID, str(theNewValue))
        self._preferencesCommon.saveConfig()

    @property
    def backgroundGridInterval(self) -> int:
        return self._config.getint(BackgroundPreferences.DIAGRAM_SECTION, BackgroundPreferences.BACKGROUND_GRID_INTERVAL)

    @backgroundGridInterval.setter
    def backgroundGridInterval(self, theNewValue: int):
        self._config.set(BackgroundPreferences.DIAGRAM_SECTION, BackgroundPreferences.BACKGROUND_GRID_INTERVAL, str(theNewValue))
        self._preferencesCommon.saveConfig()

    @property
    def gridLineColor(self) -> MiniOglColorEnum:

        colorName:     str           = self._config.get(BackgroundPreferences.DIAGRAM_SECTION, BackgroundPreferences.GRID_LINE_COLOR)
        pyutColorEnum: MiniOglColorEnum = MiniOglColorEnum(colorName)
        return pyutColorEnum

    @gridLineColor.setter
    def gridLineColor(self, theNewValue: MiniOglColorEnum):

        colorName: str = theNewValue.value
        self._config.set(BackgroundPreferences.DIAGRAM_SECTION, BackgroundPreferences.GRID_LINE_COLOR, colorName)
        self._preferencesCommon.saveConfig()

    @property
    def gridLineStyle(self) -> MiniOglPenStyle:
        penStyleName: str          = self._config.get(BackgroundPreferences.DIAGRAM_SECTION, BackgroundPreferences.GRID_LINE_STYLE)
        pyutPenStyle: MiniOglPenStyle = MiniOglPenStyle(penStyleName)
        return pyutPenStyle

    @gridLineStyle.setter
    def gridLineStyle(self, theNewValue: MiniOglPenStyle):

        penStyleName: str = theNewValue.value
        self._config.set(BackgroundPreferences.DIAGRAM_SECTION, BackgroundPreferences.GRID_LINE_STYLE, penStyleName)
        self._preferencesCommon.saveConfig()

    def __addMissingDiagramPreference(self, preferenceName, value):
        self._preferencesCommon.addMissingPreference(BackgroundPreferences.DIAGRAM_SECTION, preferenceName, value)

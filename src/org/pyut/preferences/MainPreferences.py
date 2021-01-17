
from logging import Logger
from logging import getLogger

from typing import Tuple

from org.pyut.preferences.ToolBarIconSize import ToolBarIconSize
from org.pyut.preferences.BaseSubPreference import BaseSubPreference

from org.pyut.preferences.PreferencesCommon import PREFS_NAME_VALUES
from org.pyut.preferences.PreferencesCommon import PreferencesCommon


class MainPreferences(BaseSubPreference):

    DEFAULT_PDF_EXPORT_FILE_NAME: str = 'PyutExport'

    MAIN_SECTION:    str = 'Main'

    USER_DIRECTORY:             str = 'userPath'
    ORG_DIRECTORY:              str = 'orgDirectory'
    LAST_DIRECTORY:             str = 'LastDirectory'
    SHOW_TIPS_ON_STARTUP:       str = 'Show_Tips_On_Startup'
    AUTO_RESIZE_SHAPE_ON_EDIT:  str = 'Auto_Resize_Shape_On_Edit'
    SHOW_PARAMETERS:            str = 'Show_Parameters'
    FULL_SCREEN:                str = 'Full_Screen'
    I18N:                       str = 'I18N'
    CURRENT_TIP:                str = 'Current_Tip'
    EDITOR:                     str = 'Editor'
    STARTUP_WIDTH:              str = 'startup_width'
    STARTUP_HEIGHT:             str = 'startup_height'
    CENTER_DIAGRAM:             str = 'center_diagram'
    CENTER_APP_ON_STARTUP:      str = 'center_app_on_startup'  # If 'False' honor startup_x, startup_y
    STARTUP_X:                  str = 'startup_x'
    STARTUP_Y:                  str = 'startup_y'
    PDF_EXPORT_FILE_NAME:       str = 'default_pdf_export_file_name'
    TOOL_BAR_ICON_SIZE:         str = 'tool_bar_icon_size'

    MAIN_PREFERENCES: PREFS_NAME_VALUES = {
        USER_DIRECTORY:            '.',
        ORG_DIRECTORY:             '.',
        LAST_DIRECTORY:            '.',
        SHOW_TIPS_ON_STARTUP:      'False',
        AUTO_RESIZE_SHAPE_ON_EDIT: 'True',
        SHOW_PARAMETERS:           'False',
        FULL_SCREEN:               'False',
        I18N:                      'en',       # TODO: I think this should be 'English' if I look at the preferences dialog `Close` code
        CURRENT_TIP:               '0',
        EDITOR:                    'brackets',
        STARTUP_WIDTH:             '1024',
        STARTUP_HEIGHT:            '768',
        CENTER_DIAGRAM:            'False',
        CENTER_APP_ON_STARTUP:     'True',
        STARTUP_X:                 '-1',
        STARTUP_Y:                 '-1',
        PDF_EXPORT_FILE_NAME:      DEFAULT_PDF_EXPORT_FILE_NAME,
        TOOL_BAR_ICON_SIZE:        ToolBarIconSize.SIZE_32.value
    }

    def init(self, *args, **kwds):

        self.logger:  Logger            = getLogger(__name__)

        BaseSubPreference.init(self, *args, **kwds)

        self._preferencesCommon: PreferencesCommon = PreferencesCommon(self._config)

    def addAnyMissingMainPreferences(self):

        try:
            if self._config.has_section(MainPreferences.MAIN_SECTION) is False:
                self._config.add_section(MainPreferences.MAIN_SECTION)

            for prefName in MainPreferences.MAIN_PREFERENCES.keys():
                if self._config.has_option(MainPreferences.MAIN_SECTION, prefName) is False:
                    self.__addMissingMainPreference(prefName, MainPreferences.MAIN_PREFERENCES[prefName])
        except (ValueError, Exception) as e:
            self.logger.error(f"Error: {e}")

    @property
    def userDirectory(self) -> str:
        return self._config.get(MainPreferences.MAIN_SECTION, MainPreferences.USER_DIRECTORY)

    @userDirectory.setter
    def userDirectory(self, theNewValue: str):
        self._config.set(MainPreferences.MAIN_SECTION, MainPreferences.USER_DIRECTORY, theNewValue)
        self._preferencesCommon.saveConfig()

    @property
    def orgDirectory(self) -> str:
        return self._config.get(MainPreferences.MAIN_SECTION, MainPreferences.ORG_DIRECTORY)

    @orgDirectory.setter
    def orgDirectory(self, theNewValue: str):
        self._config.set(MainPreferences.MAIN_SECTION, MainPreferences.ORG_DIRECTORY, theNewValue)
        self._preferencesCommon.saveConfig()

    @property
    def lastOpenedDirectory(self) -> str:
        return self._config.get(MainPreferences.MAIN_SECTION, MainPreferences.LAST_DIRECTORY)

    @lastOpenedDirectory.setter
    def lastOpenedDirectory(self, theNewValue: str):
        self._config.set(MainPreferences.MAIN_SECTION, MainPreferences.LAST_DIRECTORY, theNewValue)
        self._preferencesCommon.saveConfig()

    @property
    def showTipsOnStartup(self) -> bool:
        return self._config.getboolean(MainPreferences.MAIN_SECTION, MainPreferences.SHOW_TIPS_ON_STARTUP)

    @showTipsOnStartup.setter
    def showTipsOnStartup(self, newValue: bool):
        self._config.set(MainPreferences.MAIN_SECTION, MainPreferences.SHOW_TIPS_ON_STARTUP, str(newValue))
        self._preferencesCommon.saveConfig()

    @property
    def autoResizeShapesOnEdit(self) -> bool:
        return self._config.getboolean(MainPreferences.MAIN_SECTION, MainPreferences.AUTO_RESIZE_SHAPE_ON_EDIT)

    @autoResizeShapesOnEdit.setter
    def autoResizeShapesOnEdit(self, newValue: bool):
        self._config.set(MainPreferences.MAIN_SECTION, MainPreferences.AUTO_RESIZE_SHAPE_ON_EDIT, str(newValue))
        self._preferencesCommon.saveConfig()

    @property
    def showParameters(self) -> bool:
        return self._config.getboolean(MainPreferences.MAIN_SECTION, MainPreferences.SHOW_PARAMETERS)

    @showParameters.setter
    def showParameters(self, theNewValue: bool):
        self._config.set(MainPreferences.MAIN_SECTION, MainPreferences.SHOW_PARAMETERS, str(theNewValue))
        self._preferencesCommon.saveConfig()

    @property
    def fullScreen(self) -> bool:
        return self._config.getboolean(MainPreferences.MAIN_SECTION, MainPreferences.FULL_SCREEN)

    @fullScreen.setter
    def fullScreen(self, theNewValue: bool):
        self._config.set(MainPreferences.MAIN_SECTION, MainPreferences.FULL_SCREEN, str(theNewValue))
        self._preferencesCommon.saveConfig()

    @property
    def i18n(self) -> str:
        return self._config.get(MainPreferences.MAIN_SECTION, MainPreferences.I18N)

    @i18n.setter
    def i18n(self, theNewValue: str):
        self._config.set(MainPreferences.MAIN_SECTION, MainPreferences.I18N, theNewValue)
        self._preferencesCommon.saveConfig()

    @property
    def currentTip(self) -> int:
        return self._config.getint(MainPreferences.MAIN_SECTION, MainPreferences.CURRENT_TIP)

    @currentTip.setter
    def currentTip(self, theNewValue: int):
        self._config.set(MainPreferences.MAIN_SECTION, MainPreferences.CURRENT_TIP, str(theNewValue))
        self._preferencesCommon.saveConfig()

    @property
    def editor(self) -> str:
        return self._config.get(MainPreferences.MAIN_SECTION, MainPreferences.EDITOR)

    @editor.setter
    def editor(self, theNewValue: str):
        self._config.set(MainPreferences.MAIN_SECTION, MainPreferences.EDITOR, theNewValue)
        self._preferencesCommon.saveConfig()

    @property
    def startupWidth(self) -> int:
        return self._config.getint(MainPreferences.MAIN_SECTION, MainPreferences.STARTUP_WIDTH)

    @startupWidth.setter
    def startupWidth(self, newWidth: int):
        self._config.set(MainPreferences.MAIN_SECTION, MainPreferences.STARTUP_WIDTH, str(newWidth))
        self._preferencesCommon.saveConfig()

    @property
    def startupHeight(self) -> int:
        return self._config.getint(MainPreferences.MAIN_SECTION, MainPreferences.STARTUP_HEIGHT)

    @startupHeight.setter
    def startupHeight(self, newHeight: int):
        self._config.set(MainPreferences.MAIN_SECTION, MainPreferences.STARTUP_HEIGHT, str(newHeight))
        self._preferencesCommon.saveConfig()

    @property
    def centerDiagram(self):
        centerDiagram: bool = self._config.getboolean(MainPreferences.MAIN_SECTION, MainPreferences.CENTER_DIAGRAM)
        return centerDiagram

    @centerDiagram.setter
    def centerDiagram(self, theNewValue: bool):
        self._config.set(MainPreferences.MAIN_SECTION, MainPreferences.CENTER_DIAGRAM, str(theNewValue))
        self._preferencesCommon.saveConfig()

    @property
    def centerAppOnStartUp(self) -> bool:
        centerApp: bool = self._config.getboolean(MainPreferences.MAIN_SECTION, MainPreferences.CENTER_APP_ON_STARTUP)
        return centerApp

    @centerAppOnStartUp.setter
    def centerAppOnStartUp(self, theNewValue: bool):
        self._config.set(MainPreferences.MAIN_SECTION, MainPreferences.CENTER_APP_ON_STARTUP, str(theNewValue))
        self._preferencesCommon.saveConfig()

    @property
    def appStartupPosition(self) -> Tuple[int, int]:

        x: int = self._config.getint(MainPreferences.MAIN_SECTION, MainPreferences.STARTUP_X)
        y: int = self._config.getint(MainPreferences.MAIN_SECTION, MainPreferences.STARTUP_Y)

        return x, y

    @appStartupPosition.setter
    def appStartupPosition(self, theNewValue: Tuple[int, int]):

        x: int = theNewValue[0]
        y: int = theNewValue[1]

        self._config.set(MainPreferences.MAIN_SECTION, MainPreferences.STARTUP_X, str(x))
        self._config.set(MainPreferences.MAIN_SECTION, MainPreferences.STARTUP_Y, str(y))

        self._preferencesCommon.saveConfig()

    @property
    def pdfExportFileName(self) -> str:
        return self._config.get(MainPreferences.MAIN_SECTION, MainPreferences.PDF_EXPORT_FILE_NAME)

    @pdfExportFileName.setter
    def pdfExportFileName(self, newValue: str):
        self._config.set(MainPreferences.MAIN_SECTION, MainPreferences.PDF_EXPORT_FILE_NAME, newValue)
        self._preferencesCommon.saveConfig()

    @property
    def toolBarIconSize(self) -> ToolBarIconSize:
        enumStr: str = self._config.get(MainPreferences.MAIN_SECTION, MainPreferences.TOOL_BAR_ICON_SIZE)
        return ToolBarIconSize(enumStr)

    @toolBarIconSize.setter
    def toolBarIconSize(self, newSize: ToolBarIconSize):
        self._config.set(MainPreferences.MAIN_SECTION, MainPreferences.TOOL_BAR_ICON_SIZE, newSize.value)
        self._preferencesCommon.saveConfig()

    def __addMissingMainPreference(self, preferenceName, value: str):
        self._preferencesCommon.addMissingPreference(MainPreferences.MAIN_SECTION, preferenceName, value)

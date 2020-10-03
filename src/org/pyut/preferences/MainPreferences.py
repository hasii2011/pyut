
from logging import Logger
from logging import getLogger

from configparser import ConfigParser

from org.pyut.general.Singleton import Singleton
from org.pyut.preferences.PreferencesCommon import PREFS_NAME_VALUES

from org.pyut.preferences.PreferencesCommon import PreferencesCommon


class MainPreferences(Singleton):

    DEFAULT_PDF_EXPORT_FILE_NAME: str = 'PyutExport'

    MAIN_SECTION:    str = 'Main'

    ORG_DIRECTORY:              str = 'orgDirectory'
    LAST_DIRECTORY:             str = 'LastDirectory'
    USER_DIRECTORY:             str = 'userPath'
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

    MAIN_PREFERENCES: PREFS_NAME_VALUES = {
        USER_DIRECTORY:            '.',
        SHOW_TIPS_ON_STARTUP:      'False',
        AUTO_RESIZE_SHAPE_ON_EDIT: 'False',
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
        PDF_EXPORT_FILE_NAME:      DEFAULT_PDF_EXPORT_FILE_NAME
    }

    def init(self, theMasterParser: ConfigParser):

        self.logger:             Logger            = getLogger(__name__)
        self._config:            ConfigParser      = theMasterParser
        self._preferencesCommon: PreferencesCommon = PreferencesCommon(theMasterParser)

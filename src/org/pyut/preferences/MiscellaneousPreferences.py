from logging import Logger
from logging import getLogger

from org.pyut.preferences.BaseSubPreference import BaseSubPreference
from org.pyut.preferences.PreferencesCommon import PREFS_NAME_VALUES
from org.pyut.preferences.PreferencesCommon import PreferencesCommon


class MiscellaneousPreferences(BaseSubPreference):

    MISCELLANEOUS_SECTION: str = 'Miscellaneous'

    DEFAULT_PDF_EXPORT_FILE_NAME: str = 'PyutExport'

    I18N:                 str = 'I18N'
    PDF_EXPORT_FILE_NAME: str = 'default_pdf_export_file_name'

    MISCELLANEOUS_PREFERENCES: PREFS_NAME_VALUES = {

        I18N: 'en',  # TODO: I think this should be 'English' if I look at the preferences dialog `Close` code
        PDF_EXPORT_FILE_NAME: DEFAULT_PDF_EXPORT_FILE_NAME,
    }

    def init(self, *args, **kwds):

        self.logger:  Logger = getLogger(__name__)

        BaseSubPreference.init(self, *args, **kwds)

        self._preferencesCommon: PreferencesCommon = PreferencesCommon(self._config)

    def addAnyMissingPreferences(self):

        try:
            if self._config.has_section(MiscellaneousPreferences.MISCELLANEOUS_SECTION) is False:
                self._config.add_section(MiscellaneousPreferences.MISCELLANEOUS_SECTION)

            for prefName in MiscellaneousPreferences.MISCELLANEOUS_PREFERENCES.keys():
                if self._config.has_option(MiscellaneousPreferences.MISCELLANEOUS_SECTION, prefName) is False:
                    self.__addMissingPreference(prefName, MiscellaneousPreferences.MISCELLANEOUS_PREFERENCES[prefName])

        except (ValueError, Exception) as e:
            self.logger.error(f"Error: {e}")

    @property
    def i18n(self) -> str:
        return self._config.get(MiscellaneousPreferences.MISCELLANEOUS_SECTION, MiscellaneousPreferences.I18N)

    @i18n.setter
    def i18n(self, theNewValue: str):
        self._config.set(MiscellaneousPreferences.MISCELLANEOUS_SECTION, MiscellaneousPreferences.I18N, theNewValue)
        self._preferencesCommon.saveConfig()

    @property
    def pdfExportFileName(self) -> str:
        return self._config.get(MiscellaneousPreferences.MISCELLANEOUS_SECTION, MiscellaneousPreferences.PDF_EXPORT_FILE_NAME)

    @pdfExportFileName.setter
    def pdfExportFileName(self, newValue: str):
        self._config.set(MiscellaneousPreferences.MISCELLANEOUS_SECTION, MiscellaneousPreferences.PDF_EXPORT_FILE_NAME, newValue)
        self._preferencesCommon.saveConfig()

    def __addMissingPreference(self, preferenceName, value):
        self._preferencesCommon.addMissingPreference(MiscellaneousPreferences.MISCELLANEOUS_SECTION, preferenceName, value)

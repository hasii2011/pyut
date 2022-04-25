from typing import Dict

from logging import Logger
from logging import getLogger

from sys import platform as sysPlatform

from os import getenv as osGetEnv

from configparser import ConfigParser
from typing import Optional

from org.pyut.ogl.OglDimensions import OglDimensions
from org.pyut.ogl.OglTextFontFamily import OglTextFontFamily


OGL_PREFS_NAME_VALUES = Dict[str, str]


class OglPreferences:

    PREFERENCES_FILENAME:   str = 'ogl.ini'
    THE_GREAT_MAC_PLATFORM: str = 'darwin'

    OGL_PREFERENCES_SECTION:         str = 'OglPreferences'

    NOTE_TEXT:        str = 'note_text'
    NOTE_DIMENSIONS:  str = 'note_dimensions'
    TEXT_DIMENSIONS:  str = 'text_dimensions'
    TEXT_BOLD:        str = 'text_bold'
    TEXT_ITALICIZE:   str = 'text_italicize'
    TEXT_FONT_FAMILY:        str = 'text_font_family'
    TEXT_FONT_SIZE:   str = 'text_font_size'
    CLASS_NAME:       str = 'class_name'
    CLASS_DIMENSIONS: str = 'class_dimensions'

    DEFAULT_NAME_INTERFACE: str = 'default_name_interface'
    DEFAULT_NAME_USECASE:   str = 'default_name_usecase'
    DEFAULT_NAME_ACTOR:     str = 'default_name_actor'
    DEFAULT_NAME_METHOD:    str = 'default_name_method'

    OGL_PREFERENCES: OGL_PREFS_NAME_VALUES = {
        NOTE_TEXT:              'This is the note text',
        NOTE_DIMENSIONS:        OglDimensions(100, 50).__str__(),
        TEXT_DIMENSIONS:        OglDimensions(125, 50).__str__(),
        TEXT_BOLD:              'False',
        TEXT_ITALICIZE:         'False',
        TEXT_FONT_FAMILY:       'Swiss',
        TEXT_FONT_SIZE:         '14',
        CLASS_NAME:             'ClassName',
        CLASS_DIMENSIONS:        OglDimensions(100, 100).__str__(),
        DEFAULT_NAME_INTERFACE: 'IClassInterface',
        DEFAULT_NAME_USECASE:   'UseCaseName',
        DEFAULT_NAME_ACTOR:     'ActorName',
        DEFAULT_NAME_METHOD:    'MethodName',
    }

    def __init__(self):

        self.logger:  Logger       = getLogger(__name__)
        self._config: ConfigParser = ConfigParser()

        self._preferencesFileName: str = self._getPreferencesLocation()

        self._loadPreferences()

    def _getPreferencesLocation(self) -> str:

        if sysPlatform == "linux2" or sysPlatform == "linux" or sysPlatform == OglPreferences.THE_GREAT_MAC_PLATFORM:
            homeDir:  Optional[str] = osGetEnv('HOME')
            fullName: str           = f'{homeDir}/{OglPreferences.PREFERENCES_FILENAME}'
            preferencesFileName: str = fullName
        else:
            preferencesFileName = OglPreferences.PREFERENCES_FILENAME

        return preferencesFileName

    @property
    def noteText(self) -> str:
        return self._config.get(OglPreferences.OGL_PREFERENCES_SECTION, OglPreferences.NOTE_TEXT)

    @noteText.setter
    def noteText(self, theNewValue: str):
        self._config.set(OglPreferences.OGL_PREFERENCES_SECTION, OglPreferences.NOTE_TEXT, theNewValue)
        self.__saveConfig()

    @property
    def noteDimensions(self) -> OglDimensions:
        serializedDimensions: str = self._config.get(OglPreferences.OGL_PREFERENCES_SECTION, OglPreferences.NOTE_DIMENSIONS)
        return OglDimensions.deSerialize(serializedDimensions)

    @noteDimensions.setter
    def noteDimensions(self, newValue: OglDimensions):
        self._config.set(OglPreferences.OGL_PREFERENCES_SECTION, OglPreferences.NOTE_DIMENSIONS, newValue.__str__())
        self.__saveConfig()

    @property
    def textDimensions(self) -> OglDimensions:
        serializedDimensions: str = self._config.get(OglPreferences.OGL_PREFERENCES_SECTION, OglPreferences.TEXT_DIMENSIONS)
        return OglDimensions.deSerialize(serializedDimensions)

    @textDimensions.setter
    def textDimensions(self, newValue: OglDimensions):
        self._config.set(OglPreferences.OGL_PREFERENCES_SECTION, OglPreferences.TEXT_DIMENSIONS, newValue.__str__())
        self.__saveConfig()

    @property
    def textBold(self) -> bool:
        return self._config.getboolean(OglPreferences.OGL_PREFERENCES_SECTION, OglPreferences.TEXT_BOLD)

    @textBold.setter
    def textBold(self, newValue: bool):
        self._config.set(OglPreferences.OGL_PREFERENCES_SECTION, OglPreferences.TEXT_BOLD, str(newValue))
        self.__saveConfig()

    @property
    def textItalicize(self) -> bool:
        return self._config.getboolean(OglPreferences.OGL_PREFERENCES_SECTION, OglPreferences.TEXT_ITALICIZE)

    @textItalicize.setter
    def textItalicize(self, newValue: bool):
        self._config.set(OglPreferences.OGL_PREFERENCES_SECTION, OglPreferences.TEXT_ITALICIZE, str(newValue))
        self.__saveConfig()

    @property
    def textFontFamily(self) -> OglTextFontFamily:
        """

        Returns: The Text Font Family
        """

        fontStr: str = self._config.get(OglPreferences.OGL_PREFERENCES_SECTION, OglPreferences.TEXT_FONT_FAMILY)

        fontEnum: OglTextFontFamily = OglTextFontFamily(fontStr)

        return fontEnum

    @textFontFamily.setter
    def textFontFamily(self, newValue: OglTextFontFamily):
        self._config.set(OglPreferences.OGL_PREFERENCES_SECTION, OglPreferences.TEXT_FONT_FAMILY, newValue.value)
        self.__saveConfig()

    @property
    def textFontSize(self) -> int:
        return self._config.getint(OglPreferences.OGL_PREFERENCES_SECTION, OglPreferences.TEXT_FONT_SIZE)

    @textFontSize.setter
    def textFontSize(self, newValue: int):
        self._config.set(OglPreferences.OGL_PREFERENCES_SECTION, OglPreferences.TEXT_FONT_SIZE, str(newValue))
        self.__saveConfig()

    @property
    def className(self) -> str:
        return self._config.get(OglPreferences.OGL_PREFERENCES_SECTION, OglPreferences.CLASS_NAME)

    @className.setter
    def className(self, newValue: str):
        self._config.set(OglPreferences.OGL_PREFERENCES_SECTION, OglPreferences.CLASS_NAME, str(newValue))
        self.__saveConfig()

    @property
    def classDimensions(self) -> OglDimensions:
        serializedDimensions: str = self._config.get(OglPreferences.OGL_PREFERENCES_SECTION, OglPreferences.CLASS_DIMENSIONS)
        return OglDimensions.deSerialize(serializedDimensions)

    @classDimensions.setter
    def classDimensions(self, newValue: OglDimensions):
        self._config.set(OglPreferences.OGL_PREFERENCES_SECTION, OglPreferences.CLASS_DIMENSIONS, newValue.__str__())
        self.__saveConfig()

    @property
    def interfaceName(self) -> str:
        return self._config.get(OglPreferences.OGL_PREFERENCES_SECTION, OglPreferences.DEFAULT_NAME_INTERFACE)

    @interfaceName.setter
    def interfaceName(self, newValue: str):
        self._config.set(OglPreferences.OGL_PREFERENCES_SECTION, OglPreferences.DEFAULT_NAME_INTERFACE, newValue)
        self.__saveConfig()

    @property
    def useCaseName(self) -> str:
        return self._config.get(OglPreferences.OGL_PREFERENCES_SECTION, OglPreferences.DEFAULT_NAME_USECASE)

    @useCaseName.setter
    def useCaseName(self, newValue: str):
        self._config.set(OglPreferences.OGL_PREFERENCES_SECTION, OglPreferences.DEFAULT_NAME_USECASE, newValue)
        self.__saveConfig()

    @property
    def actorName(self) -> str:
        return self._config.get(OglPreferences.OGL_PREFERENCES_SECTION, OglPreferences.DEFAULT_NAME_ACTOR)

    @actorName.setter
    def actorName(self, newValue: str):
        self._config.set(OglPreferences.OGL_PREFERENCES_SECTION, OglPreferences.DEFAULT_NAME_ACTOR, newValue)
        self.__saveConfig()

    @property
    def methodName(self) -> str:
        return self._config.get(OglPreferences.OGL_PREFERENCES_SECTION, OglPreferences.DEFAULT_NAME_METHOD)

    @methodName.setter
    def methodName(self, newValue: str):
        self._config.set(OglPreferences.OGL_PREFERENCES_SECTION, OglPreferences.DEFAULT_NAME_METHOD, newValue)
        self.__saveConfig()

    def _loadPreferences(self):

        self._ensurePreferenceFileExists()

        # Read data
        self._config.read(self._preferencesFileName)
        self._addMissingPreferences()
        self.__saveConfig()

    def _ensurePreferenceFileExists(self):

        try:
            f = open(self._preferencesFileName, "r")
            f.close()
        except (ValueError, Exception):
            try:
                f = open(self._preferencesFileName, "w")
                f.write("")
                f.close()
                self.logger.warning(f'Preferences file re-created')
            except (ValueError, Exception) as e:
                self.logger.error(f"Error: {e}")
                return

    def _addMissingPreferences(self):

        try:
            if self._config.has_section(OglPreferences.OGL_PREFERENCES_SECTION) is False:
                self._config.add_section(OglPreferences.OGL_PREFERENCES_SECTION)
            for prefName in OglPreferences.OGL_PREFERENCES:
                if self._config.has_option(OglPreferences.OGL_PREFERENCES_SECTION, prefName) is False:
                    self.__addMissingOglPreference(prefName, OglPreferences.OGL_PREFERENCES[prefName])

        except (ValueError, Exception) as e:
            self.logger.error(f"Error: {e}")

    def __addMissingOglPreference(self, preferenceName, value):
        self.__addMissingPreference(OglPreferences.OGL_PREFERENCES_SECTION, preferenceName, value)

    def __addMissingPreference(self, sectionName: str, preferenceName: str, value: str):
        self._config.set(sectionName, preferenceName, value)
        self.__saveConfig()

    def __saveConfig(self):
        """
        Save data to the preferences file
        """
        f = open(self._preferencesFileName, "w")
        self._config.write(f)
        f.close()

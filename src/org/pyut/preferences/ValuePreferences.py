
from logging import Logger
from logging import getLogger

from org.pyut.preferences.BaseSubPreference import BaseSubPreference
from org.pyut.preferences.PreferencesCommon import PREFS_NAME_VALUES
from org.pyut.preferences.PreferencesCommon import PreferencesCommon

from org.pyut.model.PyutTextFontType import PyutTextFontType
from org.pyut.general.datatypes.Dimensions import Dimensions


class ValuePreferences(BaseSubPreference):

    VALUE_PREFERENCES_SECTION:         str = 'ValuePreferences'

    NOTE_TEXT:        str = 'note_text'
    NOTE_DIMENSIONS:  str = 'note_dimensions'
    TEXT_DIMENSIONS:  str = 'text_dimensions'
    TEXT_BOLD:        str = 'text_bold'
    TEXT_ITALICIZE:   str = 'text_italicize'
    TEXT_FONT:        str = 'text_font'
    TEXT_FONT_SIZE:   str = 'text_font_size'
    CLASS_NAME:       str = 'class_name'
    CLASS_DIMENSIONS: str = 'class_dimensions'

    DEFAULT_NAME_INTERFACE: str = 'default_name_interface'
    DEFAULT_NAME_USECASE:   str = 'default_name_usecase'
    DEFAULT_NAME_ACTOR:     str = 'default_name_actor'
    DEFAULT_NAME_METHOD:    str = 'default_name_method'

    VALUE_PREFERENCES: PREFS_NAME_VALUES = {
        NOTE_TEXT:       'This is the note text',
        NOTE_DIMENSIONS:  Dimensions(100, 50).__str__(),
        TEXT_DIMENSIONS:  Dimensions(125, 50).__str__(),
        TEXT_BOLD:        'False',
        TEXT_ITALICIZE:   'False',
        TEXT_FONT:        'Swiss',
        TEXT_FONT_SIZE:   '14',
        CLASS_NAME:       'ClassName',
        CLASS_DIMENSIONS: Dimensions(100, 100).__str__(),
        DEFAULT_NAME_INTERFACE: 'IClassInterface',
        DEFAULT_NAME_USECASE:   'UseCaseName',
        DEFAULT_NAME_ACTOR:     'ActorName',
        DEFAULT_NAME_METHOD:    'MethodName',
    }

    def init(self, *args, **kwds):

        self.logger: Logger = getLogger(__name__)

        BaseSubPreference.init(self, *args, **kwds)

        self._preferencesCommon: PreferencesCommon = PreferencesCommon(self._config)

    @property
    def noteText(self) -> str:
        return self._config.get(ValuePreferences.VALUE_PREFERENCES_SECTION, ValuePreferences.NOTE_TEXT)

    @noteText.setter
    def noteText(self, theNewValue: str):
        self._config.set(ValuePreferences.VALUE_PREFERENCES_SECTION, ValuePreferences.NOTE_TEXT, theNewValue)
        self._preferencesCommon.saveConfig()

    @property
    def noteDimensions(self) -> Dimensions:
        serializedDimensions: str = self._config.get(ValuePreferences.VALUE_PREFERENCES_SECTION, ValuePreferences.NOTE_DIMENSIONS)
        return Dimensions.deSerialize(serializedDimensions)

    @noteDimensions.setter
    def noteDimensions(self, newValue: Dimensions):
        self._config.set(ValuePreferences.VALUE_PREFERENCES_SECTION, ValuePreferences.NOTE_DIMENSIONS, newValue.__str__())
        self._preferencesCommon.saveConfig()

    @property
    def textDimensions(self) -> Dimensions:
        serializedDimensions: str = self._config.get(ValuePreferences.VALUE_PREFERENCES_SECTION, ValuePreferences.TEXT_DIMENSIONS)
        return Dimensions.deSerialize(serializedDimensions)

    @textDimensions.setter
    def textDimensions(self, newValue: Dimensions):
        self._config.set(ValuePreferences.VALUE_PREFERENCES_SECTION, ValuePreferences.TEXT_DIMENSIONS, newValue.__str__())
        self._preferencesCommon.saveConfig()

    @property
    def textBold(self) -> bool:
        return self._config.getboolean(ValuePreferences.VALUE_PREFERENCES_SECTION, ValuePreferences.TEXT_BOLD)

    @textBold.setter
    def textBold(self, newValue: bool):
        self._config.set(ValuePreferences.VALUE_PREFERENCES_SECTION, ValuePreferences.TEXT_BOLD, str(newValue))
        self._preferencesCommon.saveConfig()

    @property
    def textItalicize(self) -> bool:
        return self._config.getboolean(ValuePreferences.VALUE_PREFERENCES_SECTION, ValuePreferences.TEXT_ITALICIZE)

    @textItalicize.setter
    def textItalicize(self, newValue: bool):
        self._config.set(ValuePreferences.VALUE_PREFERENCES_SECTION, ValuePreferences.TEXT_ITALICIZE, str(newValue))
        self._preferencesCommon.saveConfig()

    @property
    def textFont(self) -> PyutTextFontType:

        fontStr: str = self._config.get(ValuePreferences.VALUE_PREFERENCES_SECTION, ValuePreferences.TEXT_FONT)

        fontEnum: PyutTextFontType = PyutTextFontType(fontStr)

        return fontEnum

    @textFont.setter
    def textFont(self, newValue: PyutTextFontType):
        self._config.set(ValuePreferences.VALUE_PREFERENCES_SECTION, ValuePreferences.TEXT_FONT, newValue.value)
        self._preferencesCommon.saveConfig()

    @property
    def textFontSize(self) -> int:
        return self._config.getint(ValuePreferences.VALUE_PREFERENCES_SECTION, ValuePreferences.TEXT_FONT_SIZE)

    @textFontSize.setter
    def textFontSize(self, newValue: int):
        self._config.set(ValuePreferences.VALUE_PREFERENCES_SECTION, ValuePreferences.TEXT_FONT_SIZE, str(newValue))
        self._preferencesCommon.saveConfig()

    @property
    def className(self) -> str:
        return self._config.get(ValuePreferences.VALUE_PREFERENCES_SECTION, ValuePreferences.CLASS_NAME)

    @className.setter
    def className(self, newValue: str):
        self._config.set(ValuePreferences.VALUE_PREFERENCES_SECTION, ValuePreferences.CLASS_NAME, str(newValue))
        self._preferencesCommon.saveConfig()

    @property
    def classDimensions(self) -> Dimensions:
        serializedDimensions: str = self._config.get(ValuePreferences.VALUE_PREFERENCES_SECTION, ValuePreferences.CLASS_DIMENSIONS)
        return Dimensions.deSerialize(serializedDimensions)

    @classDimensions.setter
    def classDimensions(self, newValue: Dimensions):
        self._config.set(ValuePreferences.VALUE_PREFERENCES_SECTION, ValuePreferences.CLASS_DIMENSIONS, newValue.__str__())
        self._preferencesCommon.saveConfig()

    @property
    def interfaceName(self) -> str:
        return self._config.get(ValuePreferences.VALUE_PREFERENCES_SECTION, ValuePreferences.DEFAULT_NAME_INTERFACE)

    @interfaceName.setter
    def interfaceName(self, newValue: str):
        self._config.set(ValuePreferences.VALUE_PREFERENCES_SECTION, ValuePreferences.DEFAULT_NAME_INTERFACE, newValue)
        self._preferencesCommon.saveConfig()

    @property
    def useCaseName(self) -> str:
        return self._config.get(ValuePreferences.VALUE_PREFERENCES_SECTION, ValuePreferences.DEFAULT_NAME_USECASE)

    @useCaseName.setter
    def useCaseName(self, newValue: str):
        self._config.set(ValuePreferences.VALUE_PREFERENCES_SECTION, ValuePreferences.DEFAULT_NAME_USECASE, newValue)
        self._preferencesCommon.saveConfig()

    @property
    def actorName(self) -> str:
        return self._config.get(ValuePreferences.VALUE_PREFERENCES_SECTION, ValuePreferences.DEFAULT_NAME_ACTOR)

    @actorName.setter
    def actorName(self, newValue: str):
        self._config.set(ValuePreferences.VALUE_PREFERENCES_SECTION, ValuePreferences.DEFAULT_NAME_ACTOR, newValue)
        self._preferencesCommon.saveConfig()

    @property
    def methodName(self) -> str:
        return self._config.get(ValuePreferences.VALUE_PREFERENCES_SECTION, ValuePreferences.DEFAULT_NAME_METHOD)

    @methodName.setter
    def methodName(self, newValue: str):
        self._config.set(ValuePreferences.VALUE_PREFERENCES_SECTION, ValuePreferences.DEFAULT_NAME_METHOD, newValue)
        self._preferencesCommon.saveConfig()

    def addMissingPreferences(self):

        try:
            if self._config.has_section(ValuePreferences.VALUE_PREFERENCES_SECTION) is False:
                self._config.add_section(ValuePreferences.VALUE_PREFERENCES_SECTION)
            for prefName in ValuePreferences.VALUE_PREFERENCES:
                if self._config.has_option(ValuePreferences.VALUE_PREFERENCES_SECTION, prefName) is False:
                    self.__addMissingValuePreference(prefName, ValuePreferences.VALUE_PREFERENCES[prefName])

        except (ValueError, Exception) as e:
            self.logger.error(f"Error: {e}")

    def __addMissingValuePreference(self, preferenceName, value):
        self._preferencesCommon.addMissingPreference(ValuePreferences.VALUE_PREFERENCES_SECTION, preferenceName, value)

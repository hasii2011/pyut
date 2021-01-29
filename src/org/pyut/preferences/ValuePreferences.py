
from logging import Logger
from logging import getLogger

from org.pyut.preferences.BaseSubPreference import BaseSubPreference
from org.pyut.preferences.Dimensions import Dimensions
from org.pyut.preferences.PreferencesCommon import PREFS_NAME_VALUES
from org.pyut.preferences.PreferencesCommon import PreferencesCommon


class ValuePreferences(BaseSubPreference):

    VALUE_PREFERENCES_SECTION:         str = 'ValuePreferences'

    NOTE_TEXT:       str = 'note_text'
    NOTE_DIMENSIONS: str = 'note_dimensions'
    TEXT_DIMENSIONS: str = 'text_dimensions'
    TEXT_BOLD:       str = 'text_bold'
    TEXT_ITALICIZE:  str = 'text_italicize'
    TEXT_FONT:       str = 'text_font'
    CLASS_NAME:      str = 'class_name'
    CLASS_WIDTH:     str = 'class_width'
    CLASS_HEIGHT:    str = 'class_height'

    DEFAULT_NAME_INTERFACE: str = 'default_name_interface'
    DEFAULT_NAME_USECASE:   str = 'default_name_usecase'
    DEFAULT_NAME_ACTOR:     str = 'default_name_actor'
    DEFAULT_NAME_METHOD:    str = 'default_name_method'

    VALUE_PREFERENCES: PREFS_NAME_VALUES = {
        NOTE_TEXT:       'This is the note text',
        NOTE_DIMENSIONS: Dimensions(100, 100).__str__(),
        TEXT_DIMENSIONS: Dimensions(100, 120).__str__(),
        TEXT_BOLD:       'False',
        TEXT_ITALICIZE:  'False',
        TEXT_FONT:      ' Swiss',
        CLASS_NAME:      'ClassName',
        CLASS_WIDTH:     '100',
        CLASS_HEIGHT:    '100',
        DEFAULT_NAME_INTERFACE: 'InterfaceName',
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

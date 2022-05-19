
from typing import Dict
from typing import Optional

from logging import Logger
from logging import getLogger

from sys import platform as sysPlatform

from os import getenv as osGetEnv

from configparser import ConfigParser

from org.pyut.general.Singleton import Singleton

from miniogl.MiniOglColorEnum import MiniOglColorEnum
from miniogl.MiniOglPenStyle import MiniOglPenStyle

from org.pyut.ogl.OglDimensions import OglDimensions
from org.pyut.ogl.OglTextFontFamily import OglTextFontFamily


OGL_PREFS_NAME_VALUES = Dict[str, str]


class OglPreferences(Singleton):

    PREFERENCES_FILENAME:   str = 'ogl.ini'
    THE_GREAT_MAC_PLATFORM: str = 'darwin'

    OGL_PREFERENCES_SECTION: str = 'Ogl'
    DIAGRAM_SECTION:         str = 'Diagram'
    DEBUG_SECTION:           str = 'Debug'

    NOTE_TEXT:        str = 'note_text'
    NOTE_DIMENSIONS:  str = 'note_dimensions'
    TEXT_DIMENSIONS:  str = 'text_dimensions'
    TEXT_BOLD:        str = 'text_bold'
    TEXT_ITALICIZE:   str = 'text_italicize'
    TEXT_FONT_FAMILY: str = 'text_font_family'
    TEXT_FONT_SIZE:   str = 'text_font_size'
    CLASS_NAME:       str = 'class_name'
    CLASS_DIMENSIONS: str = 'class_dimensions'

    DEFAULT_NAME_INTERFACE: str = 'default_name_interface'
    DEFAULT_NAME_USECASE:   str = 'default_name_usecase'
    DEFAULT_NAME_ACTOR:     str = 'default_name_actor'
    DEFAULT_NAME_METHOD:    str = 'default_name_method'

    SHOW_PARAMETERS:            str = 'Show_Parameters'

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
        SHOW_PARAMETERS: 'False',
    }

    DEFAULT_GRID_LINE_COLOR: str = MiniOglColorEnum.LIGHT_GREY.value
    DEFAULT_GRID_LINE_STYLE: str = MiniOglPenStyle.DOT.value

    BACKGROUND_GRID_ENABLED:  str = 'background_grid_enabled'
    SNAP_TO_GRID:             str = 'snap_to_grid'
    BACKGROUND_GRID_INTERVAL: str = 'background_grid_interval'
    GRID_LINE_COLOR:          str = 'grid_line_color'
    GRID_LINE_STYLE:          str = 'grid_line_style'
    CENTER_DIAGRAM:           str = 'center_diagram'

    DIAGRAM_PREFERENCES: OGL_PREFS_NAME_VALUES = {
        CENTER_DIAGRAM:          'False',
        BACKGROUND_GRID_ENABLED: 'True',
        SNAP_TO_GRID:            'True',
        BACKGROUND_GRID_INTERVAL: '25',
        GRID_LINE_COLOR:          DEFAULT_GRID_LINE_COLOR,
        GRID_LINE_STYLE:          DEFAULT_GRID_LINE_STYLE
    }

    DEBUG_DIAGRAM_FRAME:           str = 'debug_diagram_frame'
    DEBUG_BASIC_SHAPE:             str = 'debug_basic_shape'              # If `True` turn on debug display code in basic Shape.py

    DEBUG_PREFERENCES: OGL_PREFS_NAME_VALUES = {
        DEBUG_DIAGRAM_FRAME: 'False',
        DEBUG_BASIC_SHAPE:   'False',
    }

    def init(self, *args, **kwargs):

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

    @property
    def showParameters(self) -> bool:
        return self._config.getboolean(OglPreferences.OGL_PREFERENCES_SECTION, OglPreferences.SHOW_PARAMETERS)

    @showParameters.setter
    def showParameters(self, theNewValue: bool):
        self._config.set(OglPreferences.OGL_PREFERENCES_SECTION, OglPreferences.SHOW_PARAMETERS, str(theNewValue))
        self.__saveConfig()

    @property
    def centerDiagram(self):
        centerDiagram: bool = self._config.getboolean(OglPreferences.DIAGRAM_SECTION, OglPreferences.CENTER_DIAGRAM)
        return centerDiagram

    @centerDiagram.setter
    def centerDiagram(self, theNewValue: bool):
        self._config.set(OglPreferences.DIAGRAM_SECTION, OglPreferences.CENTER_DIAGRAM, str(theNewValue))
        self.__saveConfig()

    @property
    def backgroundGridEnabled(self) -> bool:
        return self._config.getboolean(OglPreferences.DIAGRAM_SECTION, OglPreferences.BACKGROUND_GRID_ENABLED)

    @backgroundGridEnabled.setter
    def backgroundGridEnabled(self, theNewValue: bool):
        self._config.set(OglPreferences.DIAGRAM_SECTION, OglPreferences.BACKGROUND_GRID_ENABLED, str(theNewValue))
        self.__saveConfig()

    @property
    def snapToGrid(self) -> bool:
        return self._config.getboolean(OglPreferences.DIAGRAM_SECTION, OglPreferences.SNAP_TO_GRID)

    @snapToGrid.setter
    def snapToGrid(self, theNewValue: bool):
        self._config.set(OglPreferences.DIAGRAM_SECTION, OglPreferences.SNAP_TO_GRID, str(theNewValue))
        self.__saveConfig()

    @property
    def backgroundGridInterval(self) -> int:
        return self._config.getint(OglPreferences.DIAGRAM_SECTION, OglPreferences.BACKGROUND_GRID_INTERVAL)

    @backgroundGridInterval.setter
    def backgroundGridInterval(self, theNewValue: int):
        self._config.set(OglPreferences.DIAGRAM_SECTION, OglPreferences.BACKGROUND_GRID_INTERVAL, str(theNewValue))
        self.__saveConfig()

    @property
    def gridLineColor(self) -> MiniOglColorEnum:

        colorName:     str           = self._config.get(OglPreferences.DIAGRAM_SECTION, OglPreferences.GRID_LINE_COLOR)
        pyutColorEnum: MiniOglColorEnum = MiniOglColorEnum(colorName)
        return pyutColorEnum

    @gridLineColor.setter
    def gridLineColor(self, theNewValue: MiniOglColorEnum):

        colorName: str = theNewValue.value
        self._config.set(OglPreferences.DIAGRAM_SECTION, OglPreferences.GRID_LINE_COLOR, colorName)
        self.__saveConfig()

    @property
    def gridLineStyle(self) -> MiniOglPenStyle:
        penStyleName: str          = self._config.get(OglPreferences.DIAGRAM_SECTION, OglPreferences.GRID_LINE_STYLE)
        pyutPenStyle: MiniOglPenStyle = MiniOglPenStyle(penStyleName)
        return pyutPenStyle

    @gridLineStyle.setter
    def gridLineStyle(self, theNewValue: MiniOglPenStyle):

        penStyleName: str = theNewValue.value
        self._config.set(OglPreferences.DIAGRAM_SECTION, OglPreferences.GRID_LINE_STYLE, penStyleName)
        self.__saveConfig()

    @property
    def debugDiagramFrame(self) -> bool:
        ans: bool = self._config.getboolean(OglPreferences.DEBUG_SECTION, OglPreferences.DEBUG_DIAGRAM_FRAME)
        return ans

    @debugDiagramFrame.setter
    def debugDiagramFrame(self, theNewValue: bool):
        self._config.set(OglPreferences.DEBUG_SECTION, OglPreferences.DEBUG_DIAGRAM_FRAME, str(theNewValue))
        self.__saveConfig()

    @property
    def debugBasicShape(self):
        ans: bool = self._config.getboolean(OglPreferences.DEBUG_SECTION, OglPreferences.DEBUG_BASIC_SHAPE)
        return ans

    @debugBasicShape.setter
    def debugBasicShape(self, theNewValue: bool):
        self._config.set(OglPreferences.DEBUG_SECTION, OglPreferences.DEBUG_BASIC_SHAPE, str(theNewValue))
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

            if self._config.has_section(OglPreferences.DIAGRAM_SECTION) is False:
                self._config.add_section(OglPreferences.DIAGRAM_SECTION)

            for prefName in OglPreferences.DIAGRAM_PREFERENCES:
                if self._config.has_option(OglPreferences.DIAGRAM_SECTION, prefName) is False:
                    self.__addMissingDiagramPreference(prefName, OglPreferences.DIAGRAM_PREFERENCES[prefName])

            if self._config.has_section(OglPreferences.DEBUG_SECTION) is False:
                self._config.add_section(OglPreferences.DEBUG_SECTION)

            for prefName in OglPreferences.DEBUG_PREFERENCES:
                if self._config.has_option(OglPreferences.DEBUG_SECTION, prefName) is False:
                    self.__addMissingDebugPreference(prefName, OglPreferences.DEBUG_PREFERENCES[prefName])

        except (ValueError, Exception) as e:
            self.logger.error(f"Error: {e}")

    def __addMissingOglPreference(self, preferenceName, value):
        self.__addMissingPreference(OglPreferences.OGL_PREFERENCES_SECTION, preferenceName, value)

    def __addMissingDiagramPreference(self, preferenceName, value):
        self.__addMissingPreference(OglPreferences.DIAGRAM_SECTION, preferenceName, value)

    def __addMissingDebugPreference(self, preferenceName, value):
        self.__addMissingPreference(OglPreferences.DEBUG_SECTION, preferenceName, value)

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

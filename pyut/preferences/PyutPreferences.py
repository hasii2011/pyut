
from typing import List

from logging import Logger
from logging import getLogger

from codeallybasic.DynamicConfiguration import DynamicConfiguration
from codeallybasic.DynamicConfiguration import KeyName
from codeallybasic.DynamicConfiguration import SectionName
from codeallybasic.DynamicConfiguration import Sections
from codeallybasic.DynamicConfiguration import ValueDescription
from codeallybasic.DynamicConfiguration import ValueDescriptions

from codeallybasic.Dimensions import Dimensions
from codeallybasic.Position import Position

from codeallybasic.SecureConversions import SecureConversions

from codeallybasic.SingletonV3 import SingletonV3

from pyut.general.datatypes.ToolBarIconSize import ToolBarIconSize
from pyut.preferences.FileHistoryPreference import FileHistoryPreference

DEFAULT_STARTUP_SIZE:     str = Dimensions(1024, 768).__str__()
DEFAULT_STARTUP_POSITION: str = Position(5, 5).__str__()
DEFAULT_TB_ICON_SIZE:     str = ToolBarIconSize.SIZE_32.value

DEFAULT_FILE_HISTORY_DISPLAY: str = FileHistoryPreference.SHOW_NEVER.value

DEFAULT_TRACKED_LOGGERS: List[str] = [
    'pyut',
    'pyutplugins',
    'ogl',
    'miniogl',
    'untanglepyut',
    'oglio',
    'pyutmodel',
    'codeallybasic',
    'codeallyadvanced',
]

SECTION_GENERAL: ValueDescriptions = ValueDescriptions(
    {
        KeyName('virtualWindowWidth'):      ValueDescription(defaultValue='16000',  deserializer=SecureConversions.secureInteger),
        KeyName('showTipsOnStartup'):       ValueDescription(defaultValue='False',  deserializer=SecureConversions.secureBoolean),
        KeyName('loadLastOpenedProject'):   ValueDescription(defaultValue='False',  deserializer=SecureConversions.secureBoolean),
        KeyName('displayProjectExtension'): ValueDescription(defaultValue='False',  deserializer=SecureConversions.secureBoolean),
        KeyName('autoResizeShapesOnEdit'):  ValueDescription(defaultValue='True',   deserializer=SecureConversions.secureBoolean),
        KeyName('fullScreen'):              ValueDescription(defaultValue='False',  deserializer=SecureConversions.secureBoolean),
        KeyName('centerAppOnStartup'):      ValueDescription(defaultValue='False',  deserializer=SecureConversions.secureBoolean),
        KeyName('currentTip'):              ValueDescription(defaultValue='0',      deserializer=SecureConversions.secureInteger),
        KeyName('diagramsDirectory'):       ValueDescription(defaultValue=''),     # will be rationally set by CurrentDirectoryHandler
        KeyName('startupSize'):             ValueDescription(defaultValue=DEFAULT_STARTUP_SIZE,     deserializer=Dimensions.deSerialize),
        KeyName('startupPosition'):         ValueDescription(defaultValue=DEFAULT_STARTUP_POSITION, deserializer=Position.deSerialize),
        KeyName('toolBarIconSize'):         ValueDescription(defaultValue=DEFAULT_TB_ICON_SIZE,         deserializer=ToolBarIconSize.deSerialize, enumUseValue=True),
        KeyName('fileHistoryDisplay'):      ValueDescription(defaultValue=DEFAULT_FILE_HISTORY_DISPLAY, deserializer=FileHistoryPreference,       enumUseValue=True),
    }
)

SECTION_FEATURES: ValueDescriptions = ValueDescriptions(
    {
        KeyName('displayLoggingControl'): ValueDescription(defaultValue='True', deserializer=SecureConversions.secureBoolean),
        KeyName('trackedLoggers'):        ValueDescription(defaultValue=DEFAULT_TRACKED_LOGGERS, isStringList=True),
    }
)

SECTION_DEBUG: ValueDescriptions = ValueDescriptions(
    {
        KeyName('debugErrorViews'):  ValueDescription(defaultValue='False', deserializer=SecureConversions.secureBoolean),
        KeyName('debugEventEngine'): ValueDescription(defaultValue='True',  deserializer=SecureConversions.secureBoolean),
    }
)

PYUT_SECTIONS: Sections = Sections(
    {
        SectionName('General'):  SECTION_GENERAL,
        SectionName('Features'): SECTION_FEATURES,
        SectionName('Debug'):    SECTION_DEBUG,
    }
)


class PyutPreferences(DynamicConfiguration, metaclass=SingletonV3):

    def __init__(self):

        super().__init__(baseFileName='pyut.ini', moduleName='pyut', sections=PYUT_SECTIONS)

        self._logger: Logger = getLogger(__name__)

        self._overrideProgramExitSize:     bool = False
        self._overrideProgramExitPosition: bool = False

        self._configParser.optionxform = str  # type: ignore

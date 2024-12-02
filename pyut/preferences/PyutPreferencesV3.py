
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

DEFAULT_STARTUP_SIZE:     str = Dimensions(1024, 768).__str__()
DEFAULT_STARTUP_POSITION: str = Position(5, 5).__str__()

SECTION_GENERAL: ValueDescriptions = ValueDescriptions(
    {
        KeyName('virtualWindowWidth'):      ValueDescription(defaultValue='16000',  deserializer=SecureConversions.secureInteger),
        KeyName('showTipsOnStartup'):       ValueDescription(defaultValue='False',  deserializer=SecureConversions.secureBoolean),
        KeyName('loadLastOpenedProject'):   ValueDescription(defaultValue='False',  deserializer=SecureConversions.secureBoolean),
        KeyName('displayProjectExtension'): ValueDescription(defaultValue='False',  deserializer=SecureConversions.secureBoolean),
        KeyName('autoResizeShapesOnEdit'):  ValueDescription(defaultValue='True',   deserializer=SecureConversions.secureBoolean),
        KeyName('fullScreen'):              ValueDescription(defaultValue='False',  deserializer=SecureConversions.secureBoolean),
        KeyName('centerAppOnStartup'):      ValueDescription(defaultValue='False',  deserializer=SecureConversions.secureBoolean),
        KeyName('toolBarIconSize'):         ValueDescription(defaultValue=ToolBarIconSize.SIZE_32.value, enumUseValue=True),
        KeyName('currentTip'):              ValueDescription(defaultValue='0',      deserializer=SecureConversions.secureInteger),
        KeyName('diagramsDirectory'):       ValueDescription(defaultValue=''),     # will be rationally set by CurrentDirectoryHandler
        KeyName('startupSize'):             ValueDescription(defaultValue=DEFAULT_STARTUP_SIZE,     deserializer=Dimensions.deSerialize),
        KeyName('startupPosition'):         ValueDescription(defaultValue=DEFAULT_STARTUP_POSITION, deserializer=Position.deSerialize),
    }
)

SECTION_FEATURES: ValueDescriptions = ValueDescriptions(
    {
    }
)

SECTION_DEBUG: ValueDescriptions = ValueDescriptions(
    {
        KeyName('debugErrorViews'): ValueDescription(defaultValue='False', deserializer=SecureConversions.secureBoolean),
    }
)

PYUT_SECTIONS: Sections = Sections(
    {
        SectionName('General'):  SECTION_GENERAL,
        SectionName('Features'): SECTION_FEATURES,
        SectionName('Debug'):    SECTION_DEBUG,
    }
)


class PyutPreferencesV3(DynamicConfiguration, metaclass=SingletonV3):

    def __init__(self):

        super().__init__(baseFileName='pyutv3.ini', moduleName='pyut', sections=PYUT_SECTIONS)

        self._logger: Logger = getLogger(__name__)

        self._overrideProgramExitSize: bool = False
        self._overrideProgramExitPosition: bool = False
        """
        Set to `True` by the preferences dialog when the end-user either manually specifies
        the size or position of the Pyut application.  If it is False, then normal end
        of application logic prevails;

        These are not persisted
        """

        self._configParser.optionxform = str  # type: ignore

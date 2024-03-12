
from logging import Logger
from logging import getLogger

from codeallybasic.ConfigurationProperties import ConfigurationNameValue
from codeallybasic.ConfigurationProperties import PropertyName
from codeallybasic.ConfigurationProperties import Section
from codeallybasic.ConfigurationProperties import configurationGetter
from codeallybasic.ConfigurationProperties import configurationSetter
from codeallybasic.Dimensions import Dimensions
from codeallybasic.Position import Position
from codeallybasic.SingletonV3 import SingletonV3
from codeallybasic.ConfigurationProperties import ConfigurationProperties
from codeallybasic.ConfigurationProperties import Sections
from codeallybasic.ConfigurationProperties import SectionName
from codeallybasic.SecureConversions import SecureConversions

from pyut.general.datatypes.ToolBarIconSize import ToolBarIconSize

SECTION_GENERAL: Section = Section(
    [
        ConfigurationNameValue(name=PropertyName('virtualWindowWidth'),      defaultValue='3000'),
        ConfigurationNameValue(name=PropertyName('showTipsOnStartup'),       defaultValue='False'),
        ConfigurationNameValue(name=PropertyName('loadLastOpenedProject'),   defaultValue='False'),
        ConfigurationNameValue(name=PropertyName('displayProjectExtension'), defaultValue='False'),
        ConfigurationNameValue(name=PropertyName('autoResizeShapeOnEdit'),   defaultValue='True'),
        ConfigurationNameValue(name=PropertyName('fullScreen'),              defaultValue='False'),
        ConfigurationNameValue(name=PropertyName('centerAppOnStartup'),      defaultValue='False'),
        ConfigurationNameValue(name=PropertyName('toolBarIconSize'),         defaultValue=ToolBarIconSize.SIZE_32.value),
        ConfigurationNameValue(name=PropertyName('currentTip'),              defaultValue='0'),
        ConfigurationNameValue(name=PropertyName('diagramsDirectory'),       defaultValue=''),      # will be rationally set by CurrentDirectoryHandler
        ConfigurationNameValue(name=PropertyName('startupSize'),             defaultValue=Dimensions(1024, 768).__str__()),
        ConfigurationNameValue(name=PropertyName('startupPosition'),         defaultValue=Position(5, 5).__str__()),
    ]
)

SECTION_DEBUG:    Section = Section(
    [
        ConfigurationNameValue(name=PropertyName('debugErrorViews'), defaultValue='False'),
    ]
)
SECTION_FEATURES: Section = Section([])

GENERAL_SECTION_NAME:  SectionName = SectionName('General')
DEBUG_SECTION_NAME:    SectionName = SectionName('Debug')
FEATURES_SECTION_NAME: SectionName = SectionName('Features')


PYUT_SECTIONS: Sections = Sections(
    {
        GENERAL_SECTION_NAME:  SECTION_GENERAL,
        DEBUG_SECTION_NAME:    SECTION_DEBUG,
        FEATURES_SECTION_NAME: SECTION_FEATURES,
    }
)


class PyutPreferencesV2(ConfigurationProperties, metaclass=SingletonV3):
    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        super().__init__(baseFileName='pyut.ini', moduleName='pyut', sections=PYUT_SECTIONS)

        self._configParser.optionxform = str        # type: ignore
        self._loadConfiguration()

    @property
    @configurationGetter(sectionName=GENERAL_SECTION_NAME, deserializeFunction=int)
    def virtualWindowWidth(self) -> int:
        return 0

    @virtualWindowWidth.setter
    @configurationSetter(sectionName=GENERAL_SECTION_NAME)
    def virtualWindowWidth(self, newValue: int):
        pass

    @property
    @configurationGetter(sectionName=GENERAL_SECTION_NAME, deserializeFunction=SecureConversions.secureBoolean)
    def showTipsOnStartup(self) -> bool:
        return False

    @showTipsOnStartup.setter
    @configurationSetter(sectionName=GENERAL_SECTION_NAME)
    def showTipsOnStartup(self, newValue: bool):
        pass

    @property
    @configurationGetter(sectionName=GENERAL_SECTION_NAME, deserializeFunction=SecureConversions.secureBoolean)
    def loadLastOpenedProject(self) -> bool:
        return False

    @loadLastOpenedProject.setter
    @configurationSetter(sectionName=GENERAL_SECTION_NAME)
    def loadLastOpenedProject(self, newValue: bool):
        pass

    @property
    @configurationGetter(sectionName=GENERAL_SECTION_NAME, deserializeFunction=SecureConversions.secureBoolean)
    def displayProjectExtension(self) -> bool:
        return False

    @displayProjectExtension.setter
    @configurationSetter(sectionName=GENERAL_SECTION_NAME)
    def displayProjectExtension(self, newValue: bool):
        pass

    @property
    @configurationGetter(sectionName=GENERAL_SECTION_NAME, deserializeFunction=SecureConversions.secureBoolean)
    def autoResizeShapeOnEdit(self) -> bool:
        return False

    @autoResizeShapeOnEdit.setter
    @configurationSetter(sectionName=GENERAL_SECTION_NAME)
    def autoResizeShapeOnEdit(self, newValue: bool):
        pass

    @property
    @configurationGetter(sectionName=GENERAL_SECTION_NAME, deserializeFunction=SecureConversions.secureBoolean)
    def fullScreen(self) -> bool:
        return False

    @fullScreen.setter
    @configurationSetter(sectionName=GENERAL_SECTION_NAME)
    def fullScreen(self, newValue: bool):
        pass

    @property
    @configurationGetter(sectionName=GENERAL_SECTION_NAME, deserializeFunction=SecureConversions.secureBoolean)
    def centerAppOnStartup(self) -> bool:
        return False

    @centerAppOnStartup.setter
    @configurationSetter(sectionName=GENERAL_SECTION_NAME)
    def centerAppOnStartup(self, newValue: bool):
        pass

    @property
    @configurationGetter(sectionName=GENERAL_SECTION_NAME, deserializeFunction=ToolBarIconSize.deSerialize)
    def toolBarIconSize(self) -> ToolBarIconSize:
        return ToolBarIconSize.SIZE_32

    @toolBarIconSize.setter
    @configurationSetter(sectionName=GENERAL_SECTION_NAME)
    def toolBarIconSize(self, newValue: ToolBarIconSize):
        pass

    @property
    @configurationGetter(sectionName=GENERAL_SECTION_NAME, deserializeFunction=int)
    def currentTip(self) -> int:
        return 0

    @currentTip.setter
    @configurationSetter(sectionName=GENERAL_SECTION_NAME)
    def currentTip(self, newValue: int):
        pass

    @property
    @configurationGetter(sectionName=GENERAL_SECTION_NAME, deserializeFunction=str)
    def diagramsDirectory(self) -> str:
        return ''

    @diagramsDirectory.setter
    @configurationSetter(sectionName=GENERAL_SECTION_NAME)
    def diagramsDirectory(self, newValue: str):
        pass

    @property
    @configurationGetter(sectionName=GENERAL_SECTION_NAME, deserializeFunction=Dimensions.deSerialize)
    def startupSize(self) -> Dimensions:
        return Dimensions(0, 0)

    @startupSize.setter
    @configurationSetter(sectionName=GENERAL_SECTION_NAME)
    def startupSize(self, newValue: Dimensions):
        pass

    @property
    @configurationGetter(sectionName=GENERAL_SECTION_NAME, deserializeFunction=Dimensions.deSerialize)
    def startupPosition(self) -> Position:
        return Position(0, 0)

    @startupPosition.setter
    @configurationSetter(sectionName=GENERAL_SECTION_NAME)
    def startupPosition(self, newValue: Position):
        pass

    @property
    @configurationGetter(sectionName=DEBUG_SECTION_NAME, deserializeFunction=SecureConversions.secureBoolean)
    def debugErrorViews(self) -> bool:
        return False

    @debugErrorViews.setter
    @configurationSetter(sectionName=DEBUG_SECTION_NAME)
    def debugErrorViews(self, newValue: bool):
        pass

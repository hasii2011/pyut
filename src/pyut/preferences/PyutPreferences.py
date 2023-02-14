
from typing import cast

from logging import Logger
from logging import getLogger

from configparser import ConfigParser

from hasiicommon.Dimensions import Dimensions
from hasiicommon.Position import Position

from pyut.general.Singleton import Singleton

from pyut.preferences.DebugPreferences import DebugPreferences
from pyut.preferences.FeaturePreferences import FeaturePreferences
from pyut.preferences.GeneralPreferences import GeneralPreferences
from pyut.preferences.PreferencesCommon import PreferencesCommon

from pyut.general.datatypes.ToolBarIconSize import ToolBarIconSize


class PyutPreferences(Singleton):


    """
    The goal of this class is to handle Pyut Preferences, to load them and save
    them from/to a file.
    
    To use it :
    
      - instantiate a PyutPreferences object :
        prefs: PyutPreferences = PyutPreferences()
        
      - to get a pyut' preference :
        prefs = myPP.preferenceName
        
      - to set a pyut' preference :
        prefs.preferenceName = xxx

    The preferences are loaded on the first instantiation of this
    class and are auto-saved when a value is added or changed.

    """
    # noinspection PyAttributeOutsideInit
    def init(self):
        """
        """
        self.logger:  Logger = getLogger(__name__)

        self._overrideProgramExitSize:     bool = False
        self._overrideProgramExitPosition: bool = False
        """
        Set to `True` by the preferences dialog when the end-user either manually specifies
        the size or position of the Pyut application.  If it is False, then normal end
        of application logic prevails;
        """
        self._config:                ConfigParser = cast(ConfigParser, None)    # initialized when empty preferences created

        self._preferencesCommon:  PreferencesCommon        = PreferencesCommon()
        self._generalPrefs:       GeneralPreferences       = GeneralPreferences()
        self._debugPrefs:         DebugPreferences         = DebugPreferences()
        self._featurePrefs:       FeaturePreferences       = FeaturePreferences()

        self._createEmptyPreferences()

        self.__loadConfig()

    @staticmethod
    def determinePreferencesLocation():
        """
        This method MUST (I repeat MUST) be called before attempting to instantiate the preferences Singleton
        """
        PreferencesCommon.determinePreferencesLocation()

    @staticmethod
    def getPreferencesLocation():
        return PreferencesCommon.getPreferencesLocation()

    @property
    def overrideProgramExitSize(self) -> bool:
        """
        Some values like the final application position and size are automatically computed and set
        when the application exits.  However, these can also be set by the end-user via
        the preferences' dialog.  It is up to Pyut to check the value of this flag to
        determine if the end-user has manually set these

        Returns: `True` if the application can use the computed values;  Else return `False` as the
        end-user has manually specified them.
        """
        return self._overrideProgramExitSize

    @overrideProgramExitSize.setter
    def overrideProgramExitSize(self, theNewValue: bool):
        # noinspection PyAttributeOutsideInit
        self._overrideProgramExitSize = theNewValue

    @property
    def overrideProgramExitPosition(self) -> bool:
        """
        """
        return self._overrideProgramExitPosition

    @overrideProgramExitPosition.setter
    def overrideProgramExitPosition(self, theNewValue: bool):
        # noinspection PyAttributeOutsideInit
        self._overrideProgramExitPosition = theNewValue

    @property
    def showTipsOnStartup(self) -> bool:
        return self._generalPrefs.showTipsOnStartup

    @showTipsOnStartup.setter
    def showTipsOnStartup(self, newValue: bool):
        self._generalPrefs.showTipsOnStartup = newValue

    @property
    def loadLastOpenedProject(self) -> bool:
        return self._generalPrefs.loadLastOpenedProject

    @loadLastOpenedProject.setter
    def loadLastOpenedProject(self, newValue: bool):
        self._generalPrefs.loadLastOpenedProject = newValue

    @property
    def displayProjectExtension(self) -> bool:
        return self._generalPrefs.displayProjectExtension

    @displayProjectExtension.setter
    def displayProjectExtension(self, newValue: bool):
        self._generalPrefs.displayProjectExtension = newValue

    @property
    def toolBarIconSize(self) -> ToolBarIconSize:
        return self._generalPrefs.toolBarIconSize

    @toolBarIconSize.setter
    def toolBarIconSize(self, newSize: ToolBarIconSize):
        self._generalPrefs.toolBarIconSize = newSize

    @property
    def autoResizeShapesOnEdit(self) -> bool:
        return self._generalPrefs.autoResizeShapesOnEdit

    @autoResizeShapesOnEdit.setter
    def autoResizeShapesOnEdit(self, newValue: bool):
        self._generalPrefs.autoResizeShapesOnEdit = newValue

    @property
    def userDirectory(self) -> str:
        return self._generalPrefs.userDirectory

    @userDirectory.setter
    def userDirectory(self, theNewValue: str):
        self._generalPrefs.userDirectory = theNewValue

    @property
    def lastOpenedDirectory(self) -> str:
        return self._generalPrefs.lastOpenedDirectory

    @lastOpenedDirectory.setter
    def lastOpenedDirectory(self, theNewValue: str):
        self._generalPrefs.lastOpenedDirectory = theNewValue

    @property
    def orgDirectory(self) -> str:
        return self._generalPrefs.orgDirectory

    @orgDirectory.setter
    def orgDirectory(self, theNewValue: str):
        self._generalPrefs.orgDirectory = theNewValue

    @property
    def centerAppOnStartUp(self) -> bool:
        return self._generalPrefs.centerAppOnStartUp

    @centerAppOnStartUp.setter
    def centerAppOnStartUp(self, theNewValue: bool):
        self._generalPrefs.centerAppOnStartUp = theNewValue

    @property
    def startupPosition(self) -> Position:
        return self._generalPrefs.startupPosition

    @startupPosition.setter
    def startupPosition(self, newValue: Position):
        self._generalPrefs.startupPosition = newValue
        self.overrideProgramExitPosition = True

    @property
    def startupSize(self) -> Dimensions:
        return self._generalPrefs.startupSize

    @startupSize.setter
    def startupSize(self, newValue: Dimensions):
        self._generalPrefs.startupSize = newValue
        self.overrideProgramExitSize = True

    @property
    def fullScreen(self) -> bool:
        return self._generalPrefs.fullScreen

    @fullScreen.setter
    def fullScreen(self, theNewValue: bool):
        self._generalPrefs.fullScreen = theNewValue

    @property
    def currentTip(self) -> int:
        return self._generalPrefs.currentTip

    @currentTip.setter
    def currentTip(self, theNewValue: int):
        self._generalPrefs.currentTip = theNewValue

    @property
    def debugErrorViews(self):
        return self._debugPrefs.debugErrorViews

    @debugErrorViews.setter
    def debugErrorViews(self, theNewValue: bool):
        self._debugPrefs.debugErrorViews = theNewValue

    def __loadConfig(self):
        """
        Load preferences from configuration file
        """
        # Make sure that the configuration file exists
        # noinspection PyUnusedLocal
        try:
            f = open(PyutPreferences.getPreferencesLocation(), "r")
            f.close()
        except (ValueError, Exception) as e:
            try:
                f = open(PyutPreferences.getPreferencesLocation(), "w")
                f.write("")
                f.close()
                self.logger.warning(f'Preferences file re-created')
            except (ValueError, Exception) as e:
                self.logger.error(f"Error: {e}")
                return

        # Read data
        self._config.read(PyutPreferences.getPreferencesLocation())

        self._generalPrefs.addAnyMissingMainPreferences()
        self._debugPrefs.addAnyMissingDebugPreferences()
        self._featurePrefs.addAnyMissingFeaturePreferences()

    def _createEmptyPreferences(self):

        self._config = ConfigParser()

        self._preferencesCommon.configParser  = self._config
        self._generalPrefs.configParser       = self._config
        self._debugPrefs.configParser         = self._config
        self._featurePrefs.configParser       = self._config
        #
        # OGL is its own preferences
        #

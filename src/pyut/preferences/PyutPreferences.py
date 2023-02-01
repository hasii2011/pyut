
from typing import cast

from logging import Logger
from logging import getLogger

from configparser import ConfigParser

from pyutplugins.toolplugins.orthogonal.LayoutAreaSize import LayoutAreaSize

from pyut.general.Singleton import Singleton

from miniogl.MiniOglColorEnum import MiniOglColorEnum
from miniogl.MiniOglPenStyle import MiniOglPenStyle
from ogl.OglDimensions import OglDimensions

from ogl.OglTextFontFamily import OglTextFontFamily

from pyut.preferences.DebugPreferences import DebugPreferences
from pyut.preferences.FeaturePreferences import FeaturePreferences
from pyut.preferences.GeneralPreferences import GeneralPreferences
from pyut.preferences.PreferencesCommon import PreferencesCommon

from ogl.preferences.OglPreferences import OglPreferences

from pyutplugins.preferences.PluginPreferences import PluginPreferences

from pyut.general.datatypes.Position import Position
from pyut.general.datatypes.ToolBarIconSize import ToolBarIconSize
from pyut.general.datatypes.Dimensions import Dimensions


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

        self._oglPrefs:    OglPreferences    = OglPreferences()
        self._pluginPrefs: PluginPreferences = PluginPreferences()

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
    def centerDiagram(self):
        return self._oglPrefs.centerDiagram

    @centerDiagram.setter
    def centerDiagram(self, theNewValue: bool):
        self._oglPrefs.centerDiagram = theNewValue

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
    def showParameters(self) -> bool:
        return self._oglPrefs.showParameters

    @showParameters.setter
    def showParameters(self, theNewValue: bool):
        self._oglPrefs.showParameters = theNewValue

    @property
    def debugBasicShape(self):
        return self._oglPrefs.debugBasicShape

    @debugBasicShape.setter
    def debugBasicShape(self, theNewValue: bool):
        self._oglPrefs.debugBasicShape = theNewValue

    @property
    def debugDiagramFrame(self) -> bool:
        return self._oglPrefs.debugDiagramFrame

    @debugDiagramFrame.setter
    def debugDiagramFrame(self, theNewValue: bool):
        self._oglPrefs.debugDiagramFrame = theNewValue

    @property
    def debugErrorViews(self):
        return self._debugPrefs.debugErrorViews

    @debugErrorViews.setter
    def debugErrorViews(self, theNewValue: bool):
        self._debugPrefs.debugErrorViews = theNewValue

    @property
    def backgroundGridEnabled(self) -> bool:
        return self._oglPrefs.backgroundGridEnabled

    @backgroundGridEnabled.setter
    def backgroundGridEnabled(self, theNewValue: bool):
        self._oglPrefs.backgroundGridEnabled = theNewValue

    @property
    def snapToGrid(self) -> bool:
        return self._oglPrefs.snapToGrid

    @snapToGrid.setter
    def snapToGrid(self, theNewValue: bool):
        self._oglPrefs.snapToGrid = theNewValue

    @property
    def backgroundGridInterval(self) -> int:
        return self._oglPrefs.backgroundGridInterval

    @backgroundGridInterval.setter
    def backgroundGridInterval(self, theNewValue: int):
        self._oglPrefs.backgroundGridInterval = theNewValue

    @property
    def gridLineColor(self) -> MiniOglColorEnum:
        return self._oglPrefs.gridLineColor

    @gridLineColor.setter
    def gridLineColor(self, theNewValue: MiniOglColorEnum):
        self._oglPrefs.gridLineColor = theNewValue

    @property
    def gridLineStyle(self) -> MiniOglPenStyle:
        return self._oglPrefs.gridLineStyle

    @gridLineStyle.setter
    def gridLineStyle(self, theNewValue: MiniOglPenStyle):
        self._oglPrefs.gridLineStyle = theNewValue

    @property
    def noteText(self) -> str:
        return self._oglPrefs.noteText

    @noteText.setter
    def noteText(self, theNewValue: str):
        self._oglPrefs.noteText = theNewValue

    @property
    def noteDimensions(self) -> OglDimensions:
        return self._oglPrefs.noteDimensions

    @noteDimensions.setter
    def noteDimensions(self, newValue: OglDimensions):
        self._oglPrefs.noteDimensions = newValue

    @property
    def textDimensions(self) -> OglDimensions:
        return self._oglPrefs.textDimensions

    @textDimensions.setter
    def textDimensions(self, newValue: OglDimensions):
        self._oglPrefs.textDimensions = newValue

    @property
    def textBold(self) -> bool:
        return self._oglPrefs.textBold

    @textBold.setter
    def textBold(self, newValue: bool):
        self._oglPrefs.textBold = newValue

    @property
    def textItalicize(self) -> bool:
        return self._oglPrefs.textItalicize

    @textItalicize.setter
    def textItalicize(self, newValue: bool):
        self._oglPrefs.textItalicize = newValue

    @property
    def textFontFamily(self) -> OglTextFontFamily:
        """
        Returns: The text font family
        """
        return self._oglPrefs.textFontFamily

    @textFontFamily.setter
    def textFontFamily(self, newValue: OglTextFontFamily):
        self._oglPrefs.textFontFamily = newValue

    @property
    def textFontSize(self) -> int:
        return self._oglPrefs.textFontSize

    @textFontSize.setter
    def textFontSize(self, newValue: int):
        self._oglPrefs.textFontSize = newValue

    @property
    def className(self) -> str:
        return self._oglPrefs.className

    @className.setter
    def className(self, newValue: str):
        self._oglPrefs.className = newValue

    @property
    def classDimensions(self) -> OglDimensions:
        return self._oglPrefs.classDimensions

    @classDimensions.setter
    def classDimensions(self, newValue: OglDimensions):
        self._oglPrefs.classDimensions = newValue

    @property
    def interfaceName(self) -> str:
        return self._oglPrefs.interfaceName

    @interfaceName.setter
    def interfaceName(self, newValue: str):
        self._oglPrefs.interfaceName = newValue

    @property
    def useCaseName(self) -> str:
        return self._oglPrefs.useCaseName

    @useCaseName.setter
    def useCaseName(self, newValue: str):
        self._oglPrefs.useCaseName = newValue

    @property
    def actorName(self) -> str:
        return self._oglPrefs.actorName

    @actorName.setter
    def actorName(self, newValue: str):
        self._oglPrefs.actorName = newValue

    @property
    def methodName(self) -> str:
        return self._oglPrefs.methodName

    @methodName.setter
    def methodName(self, newValue: str):
        self._oglPrefs.methodName = newValue

    @property
    def wxImageFileName(self) -> str:
        return self._pluginPrefs.wxImageFileName

    @wxImageFileName.setter
    def wxImageFileName(self, newValue: str):
        self._pluginPrefs.wxImageFileName = newValue

    @property
    def orthogonalLayoutSize(self) -> LayoutAreaSize:
        return self._pluginPrefs.orthogonalLayoutSize

    @orthogonalLayoutSize.setter
    def orthogonalLayoutSize(self, newValue: LayoutAreaSize):
        self._pluginPrefs.orthogonalLayoutSize = newValue

    @property
    def sugiyamaStepByStep(self) -> bool:
        ans: bool = self._pluginPrefs.sugiyamaStepByStep
        return ans

    @sugiyamaStepByStep.setter
    def sugiyamaStepByStep(self, newValue: bool):
        self._pluginPrefs.sugiyamaStepByStep = newValue

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

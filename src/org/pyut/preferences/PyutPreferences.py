
from typing import cast

from logging import Logger
from logging import getLogger

from configparser import ConfigParser

from org.pyut.general.Singleton import Singleton

from org.pyut.miniogl.MiniOglColorEnum import MiniOglColorEnum
from org.pyut.miniogl.MiniOglPenStyle import MiniOglPenStyle
from org.pyut.ogl.OglDimensions import OglDimensions

from org.pyut.ogl.OglTextFontFamily import OglTextFontFamily

from org.pyut.preferences.DebugPreferences import DebugPreferences
from org.pyut.preferences.GeneralPreferences import GeneralPreferences
from org.pyut.preferences.MiscellaneousPreferences import MiscellaneousPreferences
from org.pyut.preferences.PreferencesCommon import PreferencesCommon

from org.pyut.ogl.preferences.OglPreferences import OglPreferences

from org.pyut.general.datatypes.Position import Position
from org.pyut.general.datatypes.ToolBarIconSize import ToolBarIconSize
from org.pyut.general.datatypes.Dimensions import Dimensions


class PyutPreferences(Singleton):

    DEFAULT_NB_LOF: int = 5         # Number of last opened files, by default

    DEFAULT_PDF_EXPORT_FILE_NAME: str = 'PyutExport'

    FILE_KEY:       str = "File"

    OPENED_FILES_SECTION:       str = "RecentlyOpenedFiles"
    NUMBER_OF_ENTRIES:          str = "Number_of_Recently_Opened_Files"

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

      - To change the number of last opened files, use :
        prefs.setNbLOF(x)
      - To get the number of last opened files, use :
        prefs.getNbLOF()
      - To get the list of Last Opened files, use :
        prefs.getLastOpenedFilesList()
      - To add a file to the Last Opened Files list, use :
        prefs.addNewLastOpenedFilesEntry(filename)

    The preferences are loaded on the first instantiation of this
    class and are auto-saved when a value is added or changed.

    """
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
        self._miscellaneousPrefs: MiscellaneousPreferences = MiscellaneousPreferences()
        self._debugPrefs:         DebugPreferences         = DebugPreferences()

        self._oglPrefs: OglPreferences = OglPreferences()

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

    def getNbLOF(self) -> int:
        """

        Returns:  the number of last opened files to keep
        """
        ans: str = self._config.get(PyutPreferences.OPENED_FILES_SECTION, PyutPreferences.NUMBER_OF_ENTRIES)
        return int(ans)

    def setNbLOF(self, nbLOF: int):
        """
        Set the number of last opened files
        Args:
            nbLOF:  The new value for the number or last opened files to remember
        """
        self._config.set(PyutPreferences.OPENED_FILES_SECTION, PyutPreferences.NUMBER_OF_ENTRIES, str(max(nbLOF, 0)))
        self._preferencesCommon.saveConfig()

    def getLastOpenedFilesList(self):
        """

        Returns:          Return the list of files
        """
        lstFiles = []

        # Read data
        for index in range(self.getNbLOF()):
            fileNameKey: str = f'{PyutPreferences.FILE_KEY}{str(index+1)}'
            lstFiles.append(self._config.get(PyutPreferences.OPENED_FILES_SECTION, fileNameKey))
        return lstFiles

    def addNewLastOpenedFilesEntry(self, filename: str):
        """
        Add a file to the list of last opened files

        Args:
            filename:   The file name to add
        """
        # Get list
        lstFiles = self.getLastOpenedFilesList()

        # Already in list ? => remove
        if filename in lstFiles:
            lstFiles.remove(filename)

        # Insert on top of the list
        lstFiles = [filename]+lstFiles

        # Save
        for idx in range(PyutPreferences.DEFAULT_NB_LOF):
            fileNameKey: str = f'{PyutPreferences.FILE_KEY}{str(idx+1)}'
            self._config.set(PyutPreferences.OPENED_FILES_SECTION, fileNameKey, lstFiles[idx])
        self._preferencesCommon.saveConfig()

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
        self._overrideProgramExitSize = theNewValue

    @property
    def overrideProgramExitPosition(self) -> bool:
        """
        """
        return self._overrideProgramExitPosition

    @overrideProgramExitPosition.setter
    def overrideProgramExitPosition(self, theNewValue: bool):
        self._overrideProgramExitPosition = theNewValue

    @property
    def pdfExportFileName(self) -> str:
        return self._miscellaneousPrefs.pdfExportFileName

    @pdfExportFileName.setter
    def pdfExportFileName(self, newValue: str):
        self._miscellaneousPrefs.pdfExportFileName = newValue

    @property
    def wxImageFileName(self) -> str:
        return self._miscellaneousPrefs.wxImageFileName

    @wxImageFileName.setter
    def wxImageFileName(self, newValue: str):
        self._miscellaneousPrefs.wxImageFileName = newValue

    @property
    def orthogonalLayoutSize(self) -> Dimensions:
        return self._miscellaneousPrefs.orthogonalLayoutSize

    @orthogonalLayoutSize.setter
    def orthogonalLayoutSize(self, newValue: Dimensions):
        self._miscellaneousPrefs.orthogonalLayoutSize = newValue

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
    def i18n(self) -> str:
        return self._miscellaneousPrefs.i18n

    @i18n.setter
    def i18n(self, theNewValue: str):
        self._miscellaneousPrefs.i18n = theNewValue

    @property
    def currentTip(self) -> int:
        return self._generalPrefs.currentTip

    @currentTip.setter
    def currentTip(self, theNewValue: int):
        self._generalPrefs.currentTip = theNewValue

    @property
    def editor(self) -> str:
        return self._generalPrefs.editor

    @editor.setter
    def editor(self, theNewValue: str):
        self._generalPrefs.editor = theNewValue

    @property
    def showParameters(self) -> bool:
        return self._oglPrefs.showParameters

    @showParameters.setter
    def showParameters(self, theNewValue: bool):
        self._oglPrefs.showParameters = theNewValue

    @property
    def useDebugTempFileLocation(self) -> bool:
        return self._debugPrefs.useDebugTempFileLocation

    @useDebugTempFileLocation.setter
    def useDebugTempFileLocation(self, theNewValue: bool):
        self._debugPrefs.useDebugTempFileLocation = theNewValue

    @property
    def debugBasicShape(self):
        return self._oglPrefs.debugBasicShape

    @debugBasicShape.setter
    def debugBasicShape(self, theNewValue: bool):
        self._oglPrefs.debugBasicShape = theNewValue

    @property
    def pyutIoPluginAutoSelectAll(self) -> bool:
        return self._debugPrefs.pyutIoPluginAutoSelectAll

    @pyutIoPluginAutoSelectAll.setter
    def pyutIoPluginAutoSelectAll(self, theNewValue: bool):
        self._debugPrefs.pyutIoPluginAutoSelectAll = theNewValue

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

        # Create a "LastOpenedFiles" structure ?
        hasSection: bool = self._config.has_section(PyutPreferences.OPENED_FILES_SECTION)
        self.logger.debug(f'hasSection: {hasSection}')
        if hasSection is False:
            self.__addOpenedFilesSection()

        self._generalPrefs.addAnyMissingMainPreferences()
        self._miscellaneousPrefs.addAnyMissingPreferences()
        self._debugPrefs.addAnyMissingDebugPreferences()

    def __addOpenedFilesSection(self):

        self._config.add_section(PyutPreferences.OPENED_FILES_SECTION)
        # Set last opened files
        self._config.set(PyutPreferences.OPENED_FILES_SECTION, PyutPreferences.NUMBER_OF_ENTRIES, str(PyutPreferences.DEFAULT_NB_LOF))
        for idx in range(PyutPreferences.DEFAULT_NB_LOF):
            fileNameKey: str = f'{PyutPreferences.FILE_KEY}{str(idx+1)}'
            self._config.set(PyutPreferences.OPENED_FILES_SECTION, fileNameKey, "")
        self._preferencesCommon.saveConfig()

    def _createEmptyPreferences(self):

        self._config: ConfigParser = ConfigParser()

        self._preferencesCommon.configParser  = self._config
        self._generalPrefs.configParser          = self._config
        self._miscellaneousPrefs.configParser = self._config
        self._debugPrefs.configParser         = self._config

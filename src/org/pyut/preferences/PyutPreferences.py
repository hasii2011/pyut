
from typing import cast

from logging import Logger
from logging import getLogger

from configparser import ConfigParser

from org.pyut.general.Singleton import Singleton

from org.pyut.miniogl.PyutColorEnum import PyutColorEnum
from org.pyut.miniogl.PyutPenStyle import PyutPenStyle

from org.pyut.ogl.OglTextFontType import OglTextFontType

from org.pyut.preferences.DebugPreferences import DebugPreferences
from org.pyut.preferences.DiagramPreferences import BackgroundPreferences
from org.pyut.preferences.MainPreferences import MainPreferences
from org.pyut.preferences.MiscellaneousPreferences import MiscellaneousPreferences
from org.pyut.preferences.PreferencesCommon import PreferencesCommon
from org.pyut.preferences.ValuePreferences import ValuePreferences

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
        self._mainPrefs:          MainPreferences          = MainPreferences()
        self._diagramPrefs:       BackgroundPreferences    = BackgroundPreferences()
        self._valuePrefs:         ValuePreferences         = ValuePreferences()
        self._miscellaneousPrefs: MiscellaneousPreferences = MiscellaneousPreferences()
        self._debugPrefs:         DebugPreferences         = DebugPreferences()

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

    def addNewLastOpenedFilesEntry(self, filename):
        """
        Add a file to the list of last opened files

        @param String filename : filename to be added
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
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
        return self._mainPrefs.showTipsOnStartup

    @showTipsOnStartup.setter
    def showTipsOnStartup(self, newValue: bool):
        self._mainPrefs.showTipsOnStartup = newValue

    @property
    def toolBarIconSize(self) -> ToolBarIconSize:
        return self._mainPrefs.toolBarIconSize

    @toolBarIconSize.setter
    def toolBarIconSize(self, newSize: ToolBarIconSize):
        self._mainPrefs.toolBarIconSize = newSize

    @property
    def autoResizeShapesOnEdit(self) -> bool:
        return self._mainPrefs.autoResizeShapesOnEdit

    @autoResizeShapesOnEdit.setter
    def autoResizeShapesOnEdit(self, newValue: bool):
        self._mainPrefs.autoResizeShapesOnEdit = newValue

    @property
    def userDirectory(self) -> str:
        return self._mainPrefs.userDirectory

    @userDirectory.setter
    def userDirectory(self, theNewValue: str):
        self._mainPrefs.userDirectory = theNewValue

    @property
    def lastOpenedDirectory(self) -> str:
        return self._mainPrefs.lastOpenedDirectory

    @lastOpenedDirectory.setter
    def lastOpenedDirectory(self, theNewValue: str):
        self._mainPrefs.lastOpenedDirectory = theNewValue

    @property
    def orgDirectory(self) -> str:
        return self._mainPrefs.orgDirectory

    @orgDirectory.setter
    def orgDirectory(self, theNewValue: str):
        self._mainPrefs.orgDirectory = theNewValue

    @property
    def centerDiagram(self):
        return self._mainPrefs.centerDiagram

    @centerDiagram.setter
    def centerDiagram(self, theNewValue: bool):
        self._mainPrefs.centerDiagram = theNewValue

    @property
    def centerAppOnStartUp(self) -> bool:
        return self._mainPrefs.centerAppOnStartUp

    @centerAppOnStartUp.setter
    def centerAppOnStartUp(self, theNewValue: bool):
        self._mainPrefs.centerAppOnStartUp = theNewValue

    @property
    def startupPosition(self) -> Position:
        return self._mainPrefs.startupPosition

    @startupPosition.setter
    def startupPosition(self, newValue: Position):
        self._mainPrefs.startupPosition = newValue
        self.overrideProgramExitPosition = True

    @property
    def startupSize(self) -> Dimensions:
        return self._mainPrefs.startupSize

    @startupSize.setter
    def startupSize(self, newValue: Dimensions):
        self._mainPrefs.startupSize = newValue
        self.overrideProgramExitSize = True

    @property
    def fullScreen(self) -> bool:
        return self._mainPrefs.fullScreen

    @fullScreen.setter
    def fullScreen(self, theNewValue: bool):
        self._mainPrefs.fullScreen = theNewValue

    @property
    def i18n(self) -> str:
        return self._miscellaneousPrefs.i18n

    @i18n.setter
    def i18n(self, theNewValue: str):
        self._miscellaneousPrefs.i18n = theNewValue

    @property
    def currentTip(self) -> int:
        return self._mainPrefs.currentTip

    @currentTip.setter
    def currentTip(self, theNewValue: int):
        self._mainPrefs.currentTip = theNewValue

    @property
    def editor(self) -> str:
        return self._mainPrefs.editor

    @editor.setter
    def editor(self, theNewValue: str):
        self._mainPrefs.editor = theNewValue

    @property
    def showParameters(self) -> bool:
        return self._mainPrefs.showParameters

    @showParameters.setter
    def showParameters(self, theNewValue: bool):
        self._mainPrefs.showParameters = theNewValue

    @property
    def useDebugTempFileLocation(self) -> bool:
        return self._debugPrefs.useDebugTempFileLocation

    @useDebugTempFileLocation.setter
    def useDebugTempFileLocation(self, theNewValue: bool):
        self._debugPrefs.useDebugTempFileLocation = theNewValue

    @property
    def debugBasicShape(self):
        return self._debugPrefs.debugBasicShape

    @debugBasicShape.setter
    def debugBasicShape(self, theNewValue: bool):
        self._debugPrefs.debugBasicShape = theNewValue

    @property
    def pyutIoPluginAutoSelectAll(self) -> bool:
        return self._debugPrefs.pyutIoPluginAutoSelectAll

    @pyutIoPluginAutoSelectAll.setter
    def pyutIoPluginAutoSelectAll(self, theNewValue: bool):
        self._debugPrefs.pyutIoPluginAutoSelectAll = theNewValue

    @property
    def debugDiagramFrame(self) -> bool:
        return self._debugPrefs.debugDiagramFrame

    @debugDiagramFrame.setter
    def debugDiagramFrame(self, theNewValue: bool):
        self._debugPrefs.debugDiagramFrame = theNewValue

    @property
    def debugErrorViews(self):
        return self._debugPrefs.debugErrorViews

    @debugErrorViews.setter
    def debugErrorViews(self, theNewValue: bool):
        self._debugPrefs.debugErrorViews = theNewValue

    @property
    def backgroundGridEnabled(self) -> bool:
        return self._diagramPrefs.backgroundGridEnabled

    @backgroundGridEnabled.setter
    def backgroundGridEnabled(self, theNewValue: bool):
        self._diagramPrefs.backgroundGridEnabled = theNewValue

    @property
    def snapToGrid(self) -> bool:
        return self._diagramPrefs.snapToGrid

    @snapToGrid.setter
    def snapToGrid(self, theNewValue: bool):
        self._diagramPrefs.snapToGrid = theNewValue

    @property
    def backgroundGridInterval(self) -> int:
        return self._diagramPrefs.backgroundGridInterval

    @backgroundGridInterval.setter
    def backgroundGridInterval(self, theNewValue: int):
        self._diagramPrefs.backgroundGridInterval = theNewValue

    @property
    def gridLineColor(self) -> PyutColorEnum:
        return self._diagramPrefs.gridLineColor

    @gridLineColor.setter
    def gridLineColor(self, theNewValue: PyutColorEnum):
        self._diagramPrefs.gridLineColor = theNewValue

    @property
    def gridLineStyle(self) -> PyutPenStyle:
        return self._diagramPrefs.gridLineStyle

    @gridLineStyle.setter
    def gridLineStyle(self, theNewValue: PyutPenStyle):
        self._diagramPrefs.gridLineStyle = theNewValue

    @property
    def noteText(self) -> str:
        return self._valuePrefs.noteText

    @noteText.setter
    def noteText(self, theNewValue: str):
        self._valuePrefs.noteText = theNewValue

    @property
    def noteDimensions(self) -> Dimensions:
        return self._valuePrefs.noteDimensions

    @noteDimensions.setter
    def noteDimensions(self, newValue: Dimensions):
        self._valuePrefs.noteDimensions = newValue

    @property
    def textDimensions(self) -> Dimensions:
        return self._valuePrefs.textDimensions

    @textDimensions.setter
    def textDimensions(self, newValue: Dimensions):
        self._valuePrefs.textDimensions = newValue

    @property
    def textBold(self) -> bool:
        return self._valuePrefs.textBold

    @textBold.setter
    def textBold(self, newValue: bool):
        self._valuePrefs.textBold = newValue

    @property
    def textItalicize(self) -> bool:
        return self._valuePrefs.textItalicize

    @textItalicize.setter
    def textItalicize(self, newValue: bool):
        self._valuePrefs.textItalicize = newValue

    @property
    def textFont(self) -> OglTextFontType:
        return self._valuePrefs.textFont

    @textFont.setter
    def textFont(self, newValue: OglTextFontType):
        self._valuePrefs.textFont = newValue

    @property
    def textFontSize(self) -> int:
        return self._valuePrefs.textFontSize

    @textFontSize.setter
    def textFontSize(self, newValue: int):
        self._valuePrefs.textFontSize = newValue

    @property
    def className(self) -> str:
        return self._valuePrefs.className

    @className.setter
    def className(self, newValue: str):
        self._valuePrefs.className = newValue

    @property
    def classDimensions(self) -> Dimensions:
        return self._valuePrefs.classDimensions

    @classDimensions.setter
    def classDimensions(self, newValue: Dimensions):
        self._valuePrefs.classDimensions = newValue

    @property
    def interfaceName(self) -> str:
        return self._valuePrefs.interfaceName

    @interfaceName.setter
    def interfaceName(self, newValue: str):
        self._valuePrefs.interfaceName = newValue

    @property
    def useCaseName(self) -> str:
        return self._valuePrefs.useCaseName

    @useCaseName.setter
    def useCaseName(self, newValue: str):
        self._valuePrefs.useCaseName = newValue

    @property
    def actorName(self) -> str:
        return self._valuePrefs.actorName

    @actorName.setter
    def actorName(self, newValue: str):
        self._valuePrefs.actorName = newValue

    @property
    def methodName(self) -> str:
        return self._valuePrefs.methodName

    @methodName.setter
    def methodName(self, newValue: str):
        self._valuePrefs.methodName = newValue

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

        self._mainPrefs.addAnyMissingMainPreferences()
        self._miscellaneousPrefs.addAnyMissingPreferences()
        self._diagramPrefs.addMissingDiagramPreferences()
        self._valuePrefs.addMissingPreferences()
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
        self._mainPrefs.configParser          = self._config
        self._miscellaneousPrefs.configParser = self._config

        self._diagramPrefs.configParser       = self._config
        self._valuePrefs.configParser         = self._config
        self._debugPrefs.configParser         = self._config

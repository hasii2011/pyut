
from typing import List
from typing import Optional
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from sys import platform as sysPlatform

from os import getenv as osGetEnv

from wx import ACCEL_CTRL
from wx import BITMAP_TYPE_ICO
from wx import BOTH
from wx import DEFAULT_FRAME_STYLE
from wx import FRAME_FLOAT_ON_PARENT
from wx import FRAME_TOOL_WINDOW
from wx import EVT_WINDOW_DESTROY
from wx import EVT_CLOSE
from wx import EVT_ACTIVATE
from wx import ID_ANY
from wx import ID_FILE1

from wx import ActivateEvent
from wx import AcceleratorEntry
from wx import CommandEvent
from wx import FileHistory
from wx import Frame
from wx import CommandProcessor
from wx import NewIdRef
from wx import Point
from wx import Size
from wx import Icon
from wx import AcceleratorTable
from wx import Menu
from wx import ToolBar
from wx import WindowDestroyEvent

from wx import Yield as wxYield

from codeallybasic.Dimensions import Dimensions
from codeallybasic.Position import Position
from codeallybasic.SecureConversions import SecureConversions

from pyutplugins.PluginManager import PluginManager

from pyut import __version__ as pyutVersion

from pyut.ui.Action import Action

from pyut.ui.frame.FileMenuHandler import FileMenuHandler
from pyut.ui.frame.ToolsMenuHandler import ToolsMenuHandler
from pyut.ui.frame.EditMenuHandler import EditMenuHandler
from pyut.ui.frame.HelpMenuHandler import HelpMenuHandler
from pyut.ui.frame.PyutFileDropTarget import PyutFileDropTarget

from pyut.ui.tools.SharedIdentifiers import SharedIdentifiers
from pyut.ui.tools.MenuCreator import MenuCreator
from pyut.ui.tools.SharedTypes import ToolboxIdMap
from pyut.ui.tools.ToolsCreator import ToolsCreator

from pyut.ui.dialogs.tips.DlgTipsV2 import DlgTipsV2

from pyut.PyutUtils import PyutUtils

from pyut.PyutConstants import PyutConstants

from pyut.preferences.PyutPreferences import PyutPreferences


from pyut.ui.FileHistoryConfiguration import FileHistoryConfiguration
from pyut.ui.PluginAdapter import PluginAdapter
from pyut.ui.PyutUIV2 import PyutUIV2
from pyut.ui.ToolBoxHandler import ToolBoxHandler

from pyut.ui.eventengine.EventEngine import EventEngine
from pyut.ui.eventengine.Events import AssociateEditMenuEvent
from pyut.ui.eventengine.Events import EVENT_ASSOCIATE_EDIT_MENU
from pyut.ui.eventengine.Events import EVENT_OVERRIDE_PROGRAM_EXIT_POSITION
from pyut.ui.eventengine.Events import EVENT_OVERRIDE_PROGRAM_EXIT_SIZE
from pyut.ui.eventengine.Events import EVENT_SELECT_TOOL
from pyut.ui.eventengine.Events import EVENT_UPDATE_EDIT_MENU
from pyut.ui.eventengine.Events import EVENT_UPDATE_RECENT_PROJECTS
from pyut.ui.eventengine.Events import EventType
from pyut.ui.eventengine.Events import OverrideProgramExitPositionEvent
from pyut.ui.eventengine.Events import OverrideProgramExitSizeEvent
from pyut.ui.eventengine.Events import SelectToolEvent
from pyut.ui.eventengine.Events import UpdateEditMenuEvent
from pyut.ui.eventengine.Events import UpdateRecentProjectsEvent
from pyut.ui.eventengine.IEventEngine import IEventEngine

from pyut.ui.eventengine.Events import EVENT_UPDATE_APPLICATION_STATUS
from pyut.ui.eventengine.Events import EVENT_UPDATE_APPLICATION_TITLE
from pyut.ui.eventengine.Events import UpdateApplicationStatusEvent
from pyut.ui.eventengine.Events import UpdateApplicationTitleEvent

HACK_ADJUST_EXIT_HEIGHT: int = 16


class PyutApplicationFrameV2(Frame):
    """
    PyutApplicationFrame : main pyut frame; contain menus, status bar, and the UML frame

    Instantiated by PyutApp.py
    Use it:
        frame = PyutApplicationFrame(self, "Pyut")
        frame.Show()
        frame.Destroy()
    """

    def __init__(self, title: str):
        """

        Args:
            title:      Application title
        """
        self._prefs: PyutPreferences = PyutPreferences()
        appSize:     Size            = Size(self._prefs.startupSize.width, self._prefs.startupSize.height)

        appModeStr: Optional[str] = osGetEnv(PyutConstants.APP_MODE)
        if appModeStr is None:
            appMode: bool = False
        else:
            appMode = SecureConversions.secureBoolean(appModeStr)

        # wxPython 4.2.0 update:  using FRAME_TOOL_WINDOW causes the title to be above the toolbar
        # in production mode use FRAME_TOOL_WINDOW
        # Still the behavior in 4.2.2
        #
        frameStyle: int = DEFAULT_FRAME_STYLE | FRAME_FLOAT_ON_PARENT
        if appMode is True:
            frameStyle = frameStyle | FRAME_TOOL_WINDOW

        super().__init__(parent=None, id=ID_ANY, title=title, size=appSize, style=frameStyle)

        self.logger: Logger = getLogger(__name__)
        self._createApplicationIcon()

        self.CreateStatusBar()

        self._eventEngine: IEventEngine  = EventEngine(listeningWindow=self)
        self._pluginMgr:   PluginManager = PluginManager(pluginAdapter=PluginAdapter(eventEngine=self._eventEngine))
        self._fileHistory: FileHistory   = FileHistory(idBase=ID_FILE1)

        self._pyutUIV2:    PyutUIV2      = PyutUIV2(self, eventEngine=self._eventEngine)

        # set up the singleton
        self._toolBoxHandler: ToolBoxHandler = ToolBoxHandler(frame=self)

        self._eventEngine.sendEvent(EventType.UpdateApplicationStatus, applicationStatusMsg='')

        fileMenu, editMenu = self._initializeMenuHandlers()

        self._menuCreator.initializeMenus()

        fileHistoryConfiguration: FileHistoryConfiguration = FileHistoryConfiguration(appName='pyutV3',
                                                                                      vendorName='ElGatoMalo',
                                                                                      localFilename='pyutRecentFiles.ini')

        self._fileHistory.UseMenu(fileMenu)
        self._fileHistory.Load(fileHistoryConfiguration)

        self._setupKeyboardShortcuts()

        self._eventEngine.sendEvent(EventType.NewProject)
        wxYield()       # A hacky way to get the above to act like a method call
        if self._prefs.centerAppOnStartup is True:
            self.Center(BOTH)  # Center on the screen
        else:
            appPosition: Position = self._prefs.startupPosition
            self.SetPosition(pt=Point(x=appPosition.x, y=appPosition.y))

        # Initialize the tips frame
        self._tipAlreadyDisplayed: bool = False

        self.SetDropTarget(PyutFileDropTarget(eventEngine=self._eventEngine))

        if self.GetThemeEnabled() is True:
            self.SetThemeEnabled(True)

        self._initializeEventEngineHandlers()

        self._fileMenu: Menu = fileMenu     # So we can destroy you later !!!
        self._editMenu: Menu = editMenu

        self._overrideProgramExitSize:     bool = False
        self._overrideProgramExitPosition: bool = False
        """
        Set to `True` by the preferences dialog when the end-user either manually specifies
        the size or position of the Pyut application.  If it is False, then normal end
        of application logic prevails;  The preferences dialog sends this class an
        event; To change the value
        """

        self.Bind(EVT_WINDOW_DESTROY, self._cleanupFileHistory)
        self.Bind(EVT_ACTIVATE,       self._onActivate)
        self.Bind(EVT_CLOSE,          self.Close)

    def Close(self, force=False):
        """
        Closing handler overload. Save files and ask for confirmation.

        Args:
            force:
        """
        # Close all files
        self._pyutUIV2.handleUnsavedProjects()

        if self._overrideProgramExitPosition is False:
            # Only save position if we are not auto-saving
            if self._prefs.centerAppOnStartup is False:
                x, y = self.GetPosition()
                pos: Position = Position(x=x, y=y)
                self._prefs.startupPosition = pos
        if self._overrideProgramExitSize is False:
            ourSize: Tuple[int, int] = self.GetSize()

            # See issue https://github.com/hasii2011/PyUt/issues/452
            # I need to check this on a larger monitor;
            self._prefs.startupSize = Dimensions(ourSize[0], ourSize[1] - HACK_ADJUST_EXIT_HEIGHT)

        self._prefs     = cast(PyutPreferences, None)
        self._pluginMgr = cast(PluginManager, None)
        self._pyutUIV2  = cast(PyutUIV2, None)

        self.Destroy()

    def loadByFilename(self, filename):
        """
        Load the specified filename; called by PyutApp
        """
        # ignore until I find a good place for FileNames
        self._fileMenuHandler.loadFiles(fileNames=[filename])  # type: ignore

    def removeDefaultEmptyProject(self):

        self.logger.info(f'Remove the default project')
        self._pyutUIV2.closeDefaultEmptyProject()

    def loadLastOpenedProject(self):
        lastOpenFileName: str = self._fileHistory.GetHistoryFile(0)
        self.loadByFilename(filename=lastOpenFileName)

    # noinspection PyUnusedLocal
    def _cleanupFileHistory(self, event: WindowDestroyEvent):
        """
        A little extra cleanup is required for the FileHistory control;
        Take time to persist the file history
        Args:
            event:
        """
        #
        # On OS X this gets stored in ~/Library/Preferences
        # Nothing I did to the FileHistoryConfiguration object seemed to change that
        fileHistoryConfiguration: FileHistoryConfiguration = FileHistoryConfiguration(appName='pyutV3',
                                                                                      vendorName='ElGatoMalo',
                                                                                      localFilename='pyutRecentFiles.ini')

        self._fileHistory.Save(fileHistoryConfiguration)

    def _onUpdateTitle(self, event: UpdateApplicationTitleEvent):
        """
        This is a remake of the original mediator method
        Args:
            event:
        """
        filename:               str   = event.newFilename
        currentFrameZoomFactor: float = event.currentFrameZoomFactor
        projectModified:        bool  = event.projectModified
        projectName:            str   = PyutUtils.determineProjectName(filename=filename)

        txt:       str = f'Pyut v{pyutVersion} - {projectName}'
        indicator: str = ''
        if projectModified is True:
            indicator = '*'
        fullText: str  = f'{txt} ( {int(currentFrameZoomFactor * 100)}%) {indicator}'

        self.SetTitle(fullText)

    def _onUpdateStatus(self, event: UpdateApplicationStatusEvent):
        msg: str = event.applicationStatusMsg
        self.GetStatusBar().SetStatusText(msg)

    def _onSelectTool(self, event: SelectToolEvent):
        """
        First clean them all, then select the required one

        Args:
            event:  Contains the ID of the icon to toggle
        """

        toolId: int = event.toolId
        self._doToolSelect(toolId=toolId)
        # toolBar:    ToolBar   = self._toolsCreator.toolBar
        # toolBarIds: List[int] = self._toolsCreator.toolBarIds
        #
        # for deselectedToolId in toolBarIds:
        #     toolBar.ToggleTool(deselectedToolId, False)
        #
        # toolBar.ToggleTool(toolId, True)

    def _onUpdateRecentProjects(self, event: UpdateRecentProjectsEvent):
        projectFilename: str = event.projectFilename
        self._fileHistory.AddFileToHistory(filename=projectFilename)

    def _onNewAction(self, event: CommandEvent):
        """
        Call the mediator to specify the current action.

        Args:
            event:
        """
        currentAction: Action = SharedIdentifiers.ACTIONS[event.GetId()]

        self._eventEngine.sendEvent(EventType.SetToolAction, action=currentAction)
        self._doToolSelect(toolId=event.GetId())
        wxYield()

    def _doToolSelect(self, toolId: int):

        toolBar:    ToolBar   = self._toolsCreator.toolBar
        toolBarIds: List[int] = self._toolsCreator.toolBarIds

        for deselectedToolId in toolBarIds:
            toolBar.ToggleTool(deselectedToolId, False)

        toolBar.ToggleTool(toolId, True)

    def _onUpdateEditMenu(self, event: UpdateEditMenuEvent):
        cp: CommandProcessor = event.commandProcessor
        cp.SetMenuStrings()

    def _onAssociateEditMenu(self, event: AssociateEditMenuEvent):
        cp: CommandProcessor = event.commandProcessor
        cp.SetEditMenu(self._editMenu)

    def _onOverrideProgramExitSize(self, event: OverrideProgramExitSizeEvent):
        self._overrideProgramExitSize = event.override

    def _onOverrideProgramExitPosition(self, event: OverrideProgramExitPositionEvent):
        self._overrideProgramExitPosition = event.override

    def _onActivate(self, event: ActivateEvent):
        """
        EVT_ACTIVATE Callback; display tips frame.
        But only on the first activation

        Args:
            event:
        """
        self.logger.info(f'_onActivate event: {event.GetActive()}')
        if self._tipAlreadyDisplayed is True:
            pass
        else:
            # Display tips frame
            self._tipAlreadyDisplayed = True
            prefs: PyutPreferences = PyutPreferences()
            self.logger.info(f'Show tips on startup: {self._prefs.showTipsOnStartup=}')
            if prefs.showTipsOnStartup is True:
                # noinspection PyUnusedLocal
                tipsFrame: DlgTipsV2 = DlgTipsV2(self)
                tipsFrame.Show(show=True)

    def _initializePyutTools(self):
        """
        Initialize the toolboxes and the toolbar
        """

        fileMenuHandler: FileMenuHandler = self._fileMenuHandler
        editMenuHandler: EditMenuHandler = self._editMenuHandler

        self._toolsCreator: ToolsCreator = ToolsCreator(frame=self,
                                                        fileMenuHandler=fileMenuHandler,
                                                        editMenuHandler=editMenuHandler,
                                                        newActionCallback=self._onNewAction)
        self._toolsCreator.initTools()

    def _createAcceleratorTable(self):
        """
        Accelerator table initialization
        """
        # initialize the accelerator table
        # Since we are using the stock identifiers, we do not need to set up those accelerators
        lst = [
            (ACCEL_CTRL,     ord('n'),   SharedIdentifiers.ID_MENU_FILE_NEW_PROJECT),
            (ACCEL_CTRL,     ord('N'),   SharedIdentifiers.ID_MENU_FILE_NEW_PROJECT),
            (ACCEL_CTRL,     ord('l'),   SharedIdentifiers.ID_MENU_FILE_NEW_CLASS_DIAGRAM),
            (ACCEL_CTRL,     ord('E'),   SharedIdentifiers.ID_MENU_FILE_NEW_SEQUENCE_DIAGRAM),
            (ACCEL_CTRL,     ord('e'),   SharedIdentifiers.ID_MENU_FILE_NEW_SEQUENCE_DIAGRAM),
            (ACCEL_CTRL,     ord('U'),   SharedIdentifiers.ID_MENU_FILE_NEW_USECASE_DIAGRAM),
            (ACCEL_CTRL,     ord('u'),   SharedIdentifiers.ID_MENU_FILE_NEW_USECASE_DIAGRAM),
            (ACCEL_CTRL,     ord('p'),   SharedIdentifiers.ID_MENU_FILE_PRINT),
            (ACCEL_CTRL,     ord('P'),   SharedIdentifiers.ID_MENU_FILE_PRINT),
            (ACCEL_CTRL,     ord('d'),   SharedIdentifiers.ID_MENU_HELP_DEBUG),
            (ACCEL_CTRL,     ord('D'),   SharedIdentifiers.ID_MENU_HELP_DEBUG),
            ]
        acc = []
        for el in lst:
            (el1, el2, el3) = el
            acc.append(AcceleratorEntry(el1, el2, el3))
        return acc

    def _createToolboxIdMap(self) -> ToolboxIdMap:

        toolBoxIdMap: ToolboxIdMap = cast(ToolboxIdMap, {})

        toolBoxHandler: ToolBoxHandler = ToolBoxHandler()
        categories = toolBoxHandler.toolBoxCategoryNames

        for category in categories:
            categoryId = NewIdRef()
            toolBoxIdMap[categoryId] = category

        return toolBoxIdMap

    def _createApplicationIcon(self):

        if sysPlatform != PyutConstants.THE_GREAT_MAC_PLATFORM:
            fileName: str = PyutUtils.getResourcePath(packageName=PyutConstants.IMAGE_RESOURCES_PACKAGE, fileName='pyut.ico')
            icon: Icon = Icon(fileName, BITMAP_TYPE_ICO)
            self.SetIcon(icon)

    def _initializeEventEngineHandlers(self):
        self._eventEngine.registerListener(EVENT_UPDATE_APPLICATION_TITLE, self._onUpdateTitle)
        self._eventEngine.registerListener(EVENT_UPDATE_APPLICATION_STATUS, self._onUpdateStatus)
        self._eventEngine.registerListener(EVENT_SELECT_TOOL, self._onSelectTool)
        self._eventEngine.registerListener(EVENT_UPDATE_RECENT_PROJECTS, self._onUpdateRecentProjects)
        self._eventEngine.registerListener(EVENT_UPDATE_EDIT_MENU, self._onUpdateEditMenu)
        self._eventEngine.registerListener(EVENT_ASSOCIATE_EDIT_MENU, self._onAssociateEditMenu)
        self._eventEngine.registerListener(EVENT_OVERRIDE_PROGRAM_EXIT_SIZE, self._onOverrideProgramExitSize)
        self._eventEngine.registerListener(EVENT_OVERRIDE_PROGRAM_EXIT_POSITION, self._onOverrideProgramExitPosition)

    def _initializeMenuHandlers(self) -> Tuple[Menu, Menu]:
        """
        Returns: a tuple with the file menu and the edit menu
        """

        fileMenu:  Menu = Menu()
        editMenu:  Menu = Menu()
        toolsMenu: Menu = Menu()
        helpMenu:  Menu = Menu()
        self._fileMenuHandler: FileMenuHandler = FileMenuHandler(fileMenu=fileMenu, eventEngine=self._eventEngine,
                                                                 pluginManager=self._pluginMgr,
                                                                 fileHistory=self._fileHistory
                                                                 )

        self._editMenuHandler: EditMenuHandler = EditMenuHandler(editMenu=editMenu, eventEngine=self._eventEngine)
        self._initializePyutTools()

        self._toolboxIds:       ToolboxIdMap     = self._createToolboxIdMap()
        self._toolsMenuHandler: ToolsMenuHandler = ToolsMenuHandler(toolsMenu=toolsMenu, eventEngine=self._eventEngine, pluginManager=self._pluginMgr,
                                                                    toolboxIds=self._toolboxIds)
        self._helpMenuHandler: HelpMenuHandler = HelpMenuHandler(helpMenu=helpMenu)
        self._menuCreator:     MenuCreator     = MenuCreator(frame=self, pluginManager=self._pluginMgr)

        self._menuCreator.fileMenu  = fileMenu
        self._menuCreator.editMenu  = editMenu
        self._menuCreator.toolsMenu = toolsMenu
        self._menuCreator.helpMenu  = helpMenu

        self._menuCreator.fileMenuHandler  = self._fileMenuHandler
        self._menuCreator.editMenuHandler  = self._editMenuHandler
        self._menuCreator.toolsMenuHandler = self._toolsMenuHandler
        self._menuCreator.helpMenuHandler  = self._helpMenuHandler

        self._menuCreator.toolPlugins   = self._pluginMgr.toolPluginsMap.pluginIdMap
        self._menuCreator.exportPlugins = self._pluginMgr.outputPluginsMap.pluginIdMap
        self._menuCreator.importPlugins = self._pluginMgr.inputPluginsMap.pluginIdMap
        self._menuCreator.toolboxIds    = self._toolboxIds

        return fileMenu, editMenu

    def _setupKeyboardShortcuts(self):
        """
        Initialize the accelerators. These are the keyboard shortcuts
        """
        acc = self._createAcceleratorTable()
        accel_table = AcceleratorTable(acc)
        self.SetAcceleratorTable(accel_table)

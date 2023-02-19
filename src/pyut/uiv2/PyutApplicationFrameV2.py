
from typing import List
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from os import path as osPath

from sys import platform as sysPlatform

from wx import ACCEL_CTRL
from wx import BITMAP_TYPE_ICO
from wx import BOTH
from wx import DEFAULT_FRAME_STYLE
from wx import EVT_WINDOW_DESTROY
from wx import FRAME_TOOL_WINDOW
from wx import EVT_CLOSE
from wx import FRAME_EX_METAL
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

from hasiicommon.Dimensions import Dimensions
from hasiicommon.Position import Position

from pyutplugins.PluginManager import PluginManager

from pyut.general.PyutVersion import PyutVersion

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

from pyut.uiv2.dialogs.tips.DlgTips import DlgTips

from pyut.PyutUtils import PyutUtils

from pyut.PyutConstants import PyutConstants

from pyut.preferences.PyutPreferences import PyutPreferences

from pyut.general.Globals import IMAGE_RESOURCES_PACKAGE

from pyut.uiv2.FileHistoryConfiguration import FileHistoryConfiguration
from pyut.uiv2.PluginAdapter import PluginAdapter
from pyut.uiv2.PyutUIV2 import PyutUIV2
from pyut.uiv2.ToolBoxHandler import ToolBoxHandler

from pyut.uiv2.eventengine.EventEngine import EventEngine
from pyut.uiv2.eventengine.Events import AssociateEditMenuEvent
from pyut.uiv2.eventengine.Events import EVENT_ASSOCIATE_EDIT_MENU
from pyut.uiv2.eventengine.Events import EVENT_SELECT_TOOL
from pyut.uiv2.eventengine.Events import EVENT_UPDATE_EDIT_MENU
from pyut.uiv2.eventengine.Events import EVENT_UPDATE_RECENT_PROJECTS
from pyut.uiv2.eventengine.Events import EventType
from pyut.uiv2.eventengine.Events import SelectToolEvent
from pyut.uiv2.eventengine.Events import UpdateEditMenuEvent
from pyut.uiv2.eventengine.Events import UpdateRecentProjectsEvent
from pyut.uiv2.eventengine.IEventEngine import IEventEngine

from pyut.uiv2.eventengine.Events import EVENT_UPDATE_APPLICATION_STATUS
from pyut.uiv2.eventengine.Events import EVENT_UPDATE_APPLICATION_TITLE
from pyut.uiv2.eventengine.Events import UpdateApplicationStatusEvent
from pyut.uiv2.eventengine.Events import UpdateApplicationTitleEvent

HACK_ADJUST_EXIT_HEIGHT: int = 16

class PyutApplicationFrameV2(Frame):
    """
    PyutApplicationFrame : main pyut frame; contain menus, status bar, UML frame, ...

    Instantiated by PyutApp.py
    Use it as a normal Frame
        dlg=PyutApplicationFrame(self, wx.ID_ANY, "Pyut")
        dlg.Show()
        dlg.Destroy()
    """

    def __init__(self, title: str):
        """

        Args:
            title:      Title to display
        """
        self._prefs: PyutPreferences = PyutPreferences()

        appSize: Size = Size(self._prefs.startupSize.width, self._prefs.startupSize.height)

        # wxPython 4.2.0 update:  using FRAME_TOOL_WINDOW causes the title to be above the toolbar
        super().__init__(parent=None, id=ID_ANY, title=title, size=appSize, style=DEFAULT_FRAME_STYLE | FRAME_EX_METAL | FRAME_TOOL_WINDOW)

        self.logger: Logger = getLogger(__name__)
        self._createApplicationIcon()

        self.CreateStatusBar()

        self._eventEngine: IEventEngine  = EventEngine(listeningWindow=self)
        self._pluginMgr:   PluginManager = PluginManager(pluginAdapter=PluginAdapter(eventEngine=self._eventEngine))
        self._fileHistory: FileHistory   = FileHistory(idBase=ID_FILE1)

        self._pyutUIV2:    PyutUIV2      = PyutUIV2(self, eventEngine=self._eventEngine)

        # set up the singleton
        self._toolBoxHandler: ToolBoxHandler = ToolBoxHandler()
        self._toolBoxHandler.applicationFrame = self

        self._eventEngine.sendEvent(EventType.UpdateApplicationStatus, applicationStatusMsg='')

        # Initialization
        fileMenu:  Menu = Menu()
        editMenu:  Menu = Menu()
        toolsMenu: Menu = Menu()
        helpMenu:  Menu = Menu()

        self._fileMenuHandler:  FileMenuHandler  = FileMenuHandler(fileMenu=fileMenu, eventEngine=self._eventEngine,
                                                                   pluginManager=self._pluginMgr,
                                                                   fileHistory=self._fileHistory
                                                                   )
        self._editMenuHandler:  EditMenuHandler  = EditMenuHandler(editMenu=editMenu, eventEngine=self._eventEngine)

        self._initializePyutTools()

        self._toolboxIds: ToolboxIdMap = self._createToolboxIdMap()

        self._toolsMenuHandler: ToolsMenuHandler = ToolsMenuHandler(toolsMenu=toolsMenu, eventEngine=self._eventEngine, pluginManager=self._pluginMgr,
                                                                    toolboxIds=self._toolboxIds)
        self._helpMenuHandler:  HelpMenuHandler  = HelpMenuHandler(helpMenu=helpMenu)

        self._menuCreator: MenuCreator = MenuCreator(frame=self, pluginManager=self._pluginMgr)
        self._menuCreator.fileMenu  = fileMenu
        self._menuCreator.editMenu  = editMenu
        self._menuCreator.toolsMenu = toolsMenu
        self._menuCreator.helpMenu  = helpMenu
        self._menuCreator.fileMenuHandler  = self._fileMenuHandler
        self._menuCreator.editMenuHandler  = self._editMenuHandler
        self._menuCreator.toolsMenuHandler = self._toolsMenuHandler
        self._menuCreator.helpMenuHandler  = self._helpMenuHandler
        self._menuCreator.toolPlugins      = self._pluginMgr.toolPluginsMap.pluginIdMap
        self._menuCreator.exportPlugins    = self._pluginMgr.outputPluginsMap.pluginIdMap
        self._menuCreator.importPlugins    = self._pluginMgr.inputPluginsMap.pluginIdMap
        self._menuCreator.toolboxIds       = self._toolboxIds

        self._menuCreator.initializeMenus()

        fileHistoryConfiguration: FileHistoryConfiguration = FileHistoryConfiguration(appName='pyutV3',
                                                                                      vendorName='ElGatoMalo',
                                                                                      localFilename='pyutRecentFiles.ini')

        self._fileHistory.UseMenu(fileMenu)
        self._fileHistory.Load(fileHistoryConfiguration)

        self.__setupKeyboardShortcuts()

        self._eventEngine.sendEvent(EventType.NewProject)
        wxYield()       # A hacky way to get the above to act like a method call
        if self._prefs.centerAppOnStartUp is True:
            self.Center(BOTH)  # Center on the screen
        else:
            appPosition: Position = self._prefs.startupPosition
            self.SetPosition(pt=Point(x=appPosition.x, y=appPosition.y))

        # Initialize the tips frame
        self._alreadyDisplayedTipsFrame = False

        self.SetDropTarget(PyutFileDropTarget(eventEngine=self._eventEngine))

        if self.GetThemeEnabled() is True:
            self.SetThemeEnabled(True)

        self._eventEngine.registerListener(EVENT_UPDATE_APPLICATION_TITLE,  self._onUpdateTitle)
        self._eventEngine.registerListener(EVENT_UPDATE_APPLICATION_STATUS, self._onUpdateStatus)
        self._eventEngine.registerListener(EVENT_SELECT_TOOL,               self._onSelectTool)
        self._eventEngine.registerListener(EVENT_UPDATE_RECENT_PROJECTS,    self._onUpdateRecentProjects)
        self._eventEngine.registerListener(EVENT_UPDATE_EDIT_MENU,          self._onUpdateEditMenu)
        self._eventEngine.registerListener(EVENT_ASSOCIATE_EDIT_MENU,       self._onAssociateEditMenu)

        self._fileMenu: Menu = fileMenu     # So we can destroy you later !!!
        self._editMenu: Menu = editMenu

        self.Bind(EVT_WINDOW_DESTROY, self._cleanupFileHistory)
        self.Bind(EVT_ACTIVATE, self._onActivate)
        self.Bind(EVT_CLOSE, self.Close)

    def Close(self, force=False):
        """
        Closing handler overload. Save files and ask for confirmation.

        Args:
            force:
        """
        # Close all files
        self._pyutUIV2.handleUnsavedProjects()

        if self._prefs.overrideProgramExitPosition is False:
            # Only save position if we are not auto-saving
            if self._prefs.centerAppOnStartUp is False:
                x, y = self.GetPosition()
                pos: Position = Position(x=x, y=y)
                self._prefs.startupPosition = pos
        if self._prefs.overrideProgramExitSize is False:
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
        projectName:            str   = self._justTheFileName(filename=filename)
        pyutVersion:            str   = PyutVersion.getPyUtVersion()

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

    def _onActivate(self, event: ActivateEvent):
        """
        EVT_ACTIVATE Callback; display tips frame.
        But only, the first activate

        Args:
            event:
        """
        self.logger.debug(f'_onActivate event: {event}')
        try:
            if self._alreadyDisplayedTipsFrame is True or self._prefs is False:
                return
            # Display tips frame
            self._alreadyDisplayedTipsFrame = True
            prefs: PyutPreferences = PyutPreferences()
            self.logger.debug(f'Show tips on startup: {self._prefs.showTipsOnStartup=}')
            if prefs.showTipsOnStartup is True:
                # noinspection PyUnusedLocal
                tipsFrame = DlgTips(self)
                tipsFrame.Show(show=True)
        except (ValueError, Exception) as e:
            if self._prefs is not None:
                self.logger.error(f'_onActivate: {e}')

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
        #  initialize the accelerator table
        # Since we are using the stock IDs we do not need to set up those accelerators
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
            fileName: str = PyutUtils.getResourcePath(packageName=IMAGE_RESOURCES_PACKAGE, fileName='pyut.ico')
            icon: Icon = Icon(fileName, BITMAP_TYPE_ICO)
            self.SetIcon(icon)

    def __setupKeyboardShortcuts(self):
        """
        Accelerators init. (=Keyboards shortcuts)
        """
        acc = self._createAcceleratorTable()
        accel_table = AcceleratorTable(acc)
        self.SetAcceleratorTable(accel_table)

    def _justTheFileName(self, filename):
        """
        Return just the file name portion of the fully qualified path
        TODO: This is a dupe of what is in ProjectTree
        Args:
            filename:  file name to display

        Returns:
            A better file name
        """
        regularFileName: str = osPath.split(filename)[1]
        if PyutPreferences().displayProjectExtension is False:
            regularFileName = osPath.splitext(regularFileName)[0]

        return regularFileName

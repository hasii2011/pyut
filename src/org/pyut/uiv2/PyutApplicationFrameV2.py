
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
from wx import EVT_CLOSE
from wx import FRAME_EX_METAL
from wx import EVT_ACTIVATE

from wx import ActivateEvent
from wx import AcceleratorEntry
from wx import CommandEvent
from wx import FRAME_TOOL_WINDOW
from wx import Frame
from wx import ID_ANY

from wx import NewIdRef
from wx import Point
from wx import Size
from wx import Icon
from wx import AcceleratorTable
from wx import Menu
from wx import ToolBar

from wx import Yield as wxYield

from org.pyut.general.PyutVersion import PyutVersion

from org.pyut.ui.frame.EditMenuHandler import EditMenuHandler
from org.pyut.ui.frame.FileMenuHandler import FileMenuHandler
from org.pyut.ui.frame.HelpMenuHandler import HelpMenuHandler
from org.pyut.ui.frame.PyutFileDropTarget import PyutFileDropTarget
from org.pyut.ui.frame.ToolsMenuHandler import ToolsMenuHandler

from org.pyut.ui.tools.SharedIdentifiers import SharedIdentifiers

from org.pyut.ui.tools.MenuCreator import MenuCreator
from org.pyut.ui.tools.SharedTypes import PluginMap
from org.pyut.ui.tools.SharedTypes import ToolboxIdMap
from org.pyut.ui.tools.ToolsCreator import ToolsCreator

from org.pyut.dialogs.tips.DlgTips import DlgTips

from org.pyut.PyutUtils import PyutUtils

from org.pyut.PyutConstants import PyutConstants

from org.pyut.preferences.PyutPreferences import PyutPreferences

from org.pyut.general.datatypes.Dimensions import Dimensions
from org.pyut.general.datatypes.Position import Position

from org.pyut.general.Globals import IMAGE_RESOURCES_PACKAGE

from org.pyut.plugins.PluginManager import PluginManager  # Plugin Manager should not be in plugins directory

from org.pyut.uiv2.PyutUIV2 import PyutUIV2
from org.pyut.uiv2.ToolBoxHandler import ToolBoxHandler

from org.pyut.uiv2.eventengine.EventEngine import EventEngine
from org.pyut.uiv2.eventengine.Events import EVENT_SELECT_TOOL
from org.pyut.uiv2.eventengine.Events import EventType
from org.pyut.uiv2.eventengine.Events import SelectToolEvent
from org.pyut.uiv2.eventengine.IEventEngine import IEventEngine

from org.pyut.uiv2.eventengine.Events import EVENT_UPDATE_APPLICATION_STATUS
from org.pyut.uiv2.eventengine.Events import EVENT_UPDATE_APPLICATION_TITLE
from org.pyut.uiv2.eventengine.Events import UpdateApplicationStatusEvent
from org.pyut.uiv2.eventengine.Events import UpdateApplicationTitleEvent


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
        self._plugMgr: PluginManager = PluginManager()

        self.CreateStatusBar()

        self._eventEngine: IEventEngine = EventEngine(listeningWindow=self)
        self._pyutUIV2:    PyutUIV2     = PyutUIV2(self, eventEngine=self._eventEngine)

        # set up the singleton
        self._toolBoxHandler: ToolBoxHandler = ToolBoxHandler()
        self._toolBoxHandler.applicationFrame = self

        self._eventEngine.sendEvent(EventType.UpdateApplicationStatus, applicationStatusMsg='')
        # Last opened Files IDs
        self.lastOpenedFilesID = []
        for index in range(self._prefs.getNbLOF()):
            self.lastOpenedFilesID.append(PyutUtils.assignID(1)[0])

        self._toolPlugins:   PluginMap = self._plugMgr.mapWxIdsToToolPlugins()
        self._importPlugins: PluginMap = self._plugMgr.mapWxIdsToImportPlugins()
        self._exportPlugins: PluginMap = self._plugMgr.mapWxIdsToExportPlugins()

        # Initialization
        fileMenu:  Menu = Menu()
        editMenu:  Menu = Menu()
        toolsMenu: Menu = Menu()
        helpMenu:  Menu = Menu()
        self._fileMenuHandler:  FileMenuHandler  = FileMenuHandler(fileMenu=fileMenu, lastOpenFilesIDs=self.lastOpenedFilesID, eventEngine=self._eventEngine)
        self._editMenuHandler:  EditMenuHandler  = EditMenuHandler(editMenu=editMenu, eventEngine=self._eventEngine)

        self._initializePyutTools()

        self._toolboxIds: ToolboxIdMap = self._createToolboxIdMap()

        self._toolsMenuHandler: ToolsMenuHandler = ToolsMenuHandler(toolsMenu=toolsMenu, toolPluginsMap=self._toolPlugins, toolboxIds=self._toolboxIds)
        self._helpMenuHandler:  HelpMenuHandler  = HelpMenuHandler(helpMenu=helpMenu)

        self._menuCreator: MenuCreator = MenuCreator(frame=self, lastOpenFilesID=self.lastOpenedFilesID)
        self._menuCreator.fileMenu  = fileMenu
        self._menuCreator.editMenu  = editMenu
        self._menuCreator.toolsMenu = toolsMenu
        self._menuCreator.helpMenu  = helpMenu
        self._menuCreator.fileMenuHandler  = self._fileMenuHandler
        self._menuCreator.editMenuHandler  = self._editMenuHandler
        self._menuCreator.toolsMenuHandler = self._toolsMenuHandler
        self._menuCreator.helpMenuHandler  = self._helpMenuHandler
        self._menuCreator.toolPlugins      = self._toolPlugins
        self._menuCreator.exportPlugins    = self._exportPlugins
        self._menuCreator.importPlugins    = self._importPlugins
        self._menuCreator.toolboxIds       = self._toolboxIds

        self._menuCreator.initializeMenus()

        self.__setupKeyboardShortcuts()

        self._eventEngine.sendEvent(EventType.NewProject)

        if self._prefs.centerAppOnStartUp is True:
            self.Center(BOTH)  # Center on the screen
        else:
            appPosition: Position = self._prefs.startupPosition
            self.SetPosition(pt=Point(x=appPosition.x, y=appPosition.y))

        # Initialize the tips frame
        self._alreadyDisplayedTipsFrame = False

        # TODO:  Fix later for V2
        self.SetDropTarget(PyutFileDropTarget(eventEngine=self._eventEngine))

        if self.GetThemeEnabled() is True:
            self.SetThemeEnabled(True)

        self._eventEngine.registerListener(EVENT_UPDATE_APPLICATION_TITLE,  self._onUpdateTitle)
        self._eventEngine.registerListener(EVENT_UPDATE_APPLICATION_STATUS, self._onUpdateStatus)
        self._eventEngine.registerListener(EVENT_SELECT_TOOL,               self._onSelectTool)

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
            self._prefs.startupSize = Dimensions(ourSize[0], ourSize[1])

        self._clipboard = None
        self._mediator  = None
        self._prefs     = None
        self._plugMgr   = None
        self._pyutUIV2  = None

        self.Destroy()

    def loadByFilename(self, filename):
        """
        Load the specified filename; called by PyutApp
        """
        # ignore until I find a good place for FileNames
        self._fileMenuHandler.loadFile(fileNames=[filename])  # type: ignore

    def removeEmptyProject(self):

        self.logger.info(f'Remove the default project')

        # mainUI:   PyutUIV2            = self._treeNotebookHandler

        # defaultProject: PyutProject = mainUI.getProject(PyutConstants.DEFAULT_FILENAME)
        # if defaultProject is not None:
        #
        #     self.logger.info(f'Removing: {defaultProject}')
        #     mainUI.currentProject = defaultProject
        #     mainUI.closeCurrentProject()
        #
        #     projects: List[PyutProject] = mainUI.getProjects()
        #     self.logger.info(f'{projects=}')
        #
        #     firstProject: PyutProject = projects[0]
        #     self.selectProject(project=firstProject)

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

    def _onNewAction(self, event: CommandEvent):
        """
        Call the mediator to specify the current action.

        Args:
            event:
        """
        currentAction: int = SharedIdentifiers.ACTIONS[event.GetId()]

        # self._mediator.setCurrentAction(currentAction)
        # self._mediator.selectTool(event.GetId())
        self._eventEngine.sendEvent(EventType.SetToolAction, action=currentAction)
        self._doToolSelect(toolId=event.GetId())
        wxYield()

    def _doToolSelect(self, toolId: int):

        toolBar:    ToolBar   = self._toolsCreator.toolBar
        toolBarIds: List[int] = self._toolsCreator.toolBarIds

        for deselectedToolId in toolBarIds:
            toolBar.ToggleTool(deselectedToolId, False)

        toolBar.ToggleTool(toolId, True)

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
            (ACCEL_CTRL,     ord('n'),   SharedIdentifiers.ID_MNU_FILE_NEW_PROJECT),
            (ACCEL_CTRL,     ord('N'),   SharedIdentifiers.ID_MNU_FILE_NEW_PROJECT),
            (ACCEL_CTRL,     ord('l'),   SharedIdentifiers.ID_MNU_FILE_NEW_CLASS_DIAGRAM),
            (ACCEL_CTRL,     ord('E'),   SharedIdentifiers.ID_MNU_FILE_NEW_SEQUENCE_DIAGRAM),
            (ACCEL_CTRL,     ord('e'),   SharedIdentifiers.ID_MNU_FILE_NEW_SEQUENCE_DIAGRAM),
            (ACCEL_CTRL,     ord('U'),   SharedIdentifiers.ID_MNU_FILE_NEW_USECASE_DIAGRAM),
            (ACCEL_CTRL,     ord('u'),   SharedIdentifiers.ID_MNU_FILE_NEW_USECASE_DIAGRAM),
            (ACCEL_CTRL,     ord('p'),   SharedIdentifiers.ID_MNU_FILE_PRINT),
            (ACCEL_CTRL,     ord('P'),   SharedIdentifiers.ID_MNU_FILE_PRINT),
            (ACCEL_CTRL,     ord('d'),   SharedIdentifiers.ID_DEBUG),
            (ACCEL_CTRL,     ord('D'),   SharedIdentifiers.ID_DEBUG),
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

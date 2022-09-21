
from typing import Tuple
from typing import cast
from typing import List

from logging import Logger
from logging import getLogger

from os import getcwd

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

from wx import NewIdRef
from wx import Point
from wx import Size
from wx import Icon
from wx import AcceleratorTable
from wx import Menu
from wx import Window

from org.pyut.ui.PyutUI import PyutUI
from org.pyut.ui.PyutProject import PyutProject
from org.pyut.ui.Mediator import Mediator

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


class PyutApplicationFrame(Frame):
    """
    PyutApplicationFrame : main pyut frame; contain menus, status bar, UML frame, ...

    Instantiated by PyutApp.py
    Use it as a normal Frame
        dlg=PyutApplicationFrame(self, wx.ID_ANY, "Pyut")
        dlg.Show()
        dlg.Destroy()
    """

    def __init__(self, parent: Window, wxID: int, title: str):
        """

        Args:
            parent:     parent window
            wxID:       wx ID of this frame
            title:      Title to display
        """
        self._prefs: PyutPreferences = PyutPreferences()

        appSize: Size = Size(self._prefs.startupSize.width, self._prefs.startupSize.height)

        # wxPython 4.2.0 update:  using FRAME_TOOL_WINDOW causes the title to be above the toolbar
        super().__init__(parent=parent, id=wxID, title=title, size=appSize, style=DEFAULT_FRAME_STYLE | FRAME_EX_METAL | FRAME_TOOL_WINDOW)

        self.logger: Logger = getLogger(__name__)
        self._createApplicationIcon()
        self._plugMgr: PluginManager = PluginManager()

        self.CreateStatusBar()

        self._treeNotebookHandler: PyutUI = PyutUI(self)

        self._mediator: Mediator = Mediator()
        self._mediator.registerStatusBar(self.GetStatusBar())
        self._mediator.resetStatusText()
        self._mediator.registerAppFrame(self)
        self._mediator.registerFileHandling(self._treeNotebookHandler)
        self._mediator.registerAppPath(getcwd())

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
        self._fileMenuHandler:  FileMenuHandler  = FileMenuHandler(fileMenu=fileMenu, lastOpenFilesIDs=self.lastOpenedFilesID)
        self._editMenuHandler:  EditMenuHandler  = EditMenuHandler(editMenu=editMenu)

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

        # set application title
        self._treeNotebookHandler.newProject()
        self._mediator.updateTitle()

        if self._prefs.centerAppOnStartUp is True:
            self.Center(BOTH)  # Center on the screen
        else:
            appPosition: Position = self._prefs.startupPosition
            self.SetPosition(pt=Point(x=appPosition.x, y=appPosition.y))

        # Initialize the tips frame
        self._alreadyDisplayedTipsFrame = False

        self.SetDropTarget(PyutFileDropTarget(treeNotebookHandler=self._treeNotebookHandler))   # type: ignore

        if self.GetThemeEnabled() is True:
            self.SetThemeEnabled(True)

        self.Bind(EVT_ACTIVATE, self._onActivate)
        self.Bind(EVT_CLOSE, self.Close)

    def Close(self, force=False):
        """
        Closing handler overload. Save files and ask for confirmation.

        Args:
            force:
        """
        # Close all files
        if self._treeNotebookHandler.onClose() is False:
            return
        if self._prefs.overrideProgramExitPosition is False:
            # Only save position if we are not auto-saving
            if self._prefs.centerAppOnStartUp is False:
                x, y = self.GetPosition()
                pos: Position = Position(x=x, y=y)
                self._prefs.startupPosition = pos
        if self._prefs.overrideProgramExitSize is False:
            ourSize: Tuple[int, int] = self.GetSize()
            self._prefs.startupSize = Dimensions(ourSize[0], ourSize[1])

        self._clipboard    = None
        self._mediator     = None
        self._prefs        = None
        self._plugMgr      = None
        self._treeNotebookHandler = None

        self.Destroy()

    def loadByFilename(self, filename):
        """
        Load the specified filename; called by PyutApp
        """
        self._fileMenuHandler.loadFile(filename=filename)

    def removeEmptyProject(self):

        self.logger.info(f'Remove the default project')

        mainUI:   PyutUI            = self._treeNotebookHandler

        defaultProject: PyutProject = mainUI.getProject(PyutConstants.DEFAULT_FILENAME)
        if defaultProject is not None:

            self.logger.info(f'Removing: {defaultProject}')
            mainUI.currentProject = defaultProject
            mainUI.closeCurrentProject()

            projects: List[PyutProject] = mainUI.getProjects()
            self.logger.info(f'{projects=}')

            firstProject: PyutProject = projects[0]
            # mainUI.currentProject = firstProject
            # firstProject.selectSelf()
            # mainUI.currentFrame = firstProject.getFrames()[0]
            self.selectProject(project=firstProject)

    def selectProject(self, project: PyutProject):

        mainUI: PyutUI = self._treeNotebookHandler

        mainUI.currentProject = project
        project.selectSelf()
        mainUI.currentFrame = project.getFrames()[0]

    def _onNewAction(self, event: CommandEvent):
        """
        Call the mediator to specify the current action.

        Args:
            event:
        """
        currentAction: int = SharedIdentifiers.ACTIONS[event.GetId()]

        self._mediator.setCurrentAction(currentAction)
        self._mediator.selectTool(event.GetId())
        self._treeNotebookHandler.modified = True
        self._mediator.updateTitle()

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
            (ACCEL_CTRL,     ord('n'),   SharedIdentifiers.ID_MNUFILENEWPROJECT),
            (ACCEL_CTRL,     ord('N'),   SharedIdentifiers.ID_MNUFILENEWPROJECT),
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

        categories = self._mediator.getToolboxesCategories()

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

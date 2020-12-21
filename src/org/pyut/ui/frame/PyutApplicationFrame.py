
from typing import Tuple
from typing import cast
from typing import List

from logging import Logger
from logging import getLogger

from os import getcwd

from sys import platform as sysPlatform

from copy import copy

from urllib import request

from wx import ACCEL_CTRL
from wx import BITMAP_TYPE_ICO
from wx import BOTH
from wx import DEFAULT_FRAME_STYLE
from wx import FRAME_EX_METAL
from wx import ID_ANY
from wx import ID_OK
from wx import PAPER_A4
from wx import PORTRAIT
from wx import PRINT_QUALITY_HIGH
from wx import EVT_ACTIVATE
from wx import FD_OPEN
from wx import FD_MULTIPLE

from wx import PrintData

from wx import AcceleratorEntry
from wx import CommandEvent
from wx import Frame
from wx import Size
from wx import Icon
from wx import AcceleratorTable
from wx import Menu

from wx import FileDialog
from wx import PrintDialogData
from wx import PrintDialog
from wx import ClientDC
from wx import PreviewFrame
from wx import PrintPreview
from wx import Printer

from wx import BeginBusyCursor
from wx import EndBusyCursor
from wx import Window

from org.pyut.dialogs.DlgPyutDebug import DlgPyutDebug

from org.pyut.ogl.OglActor import OglActor
from org.pyut.ogl.OglClass import OglClass
from org.pyut.ogl.OglNote import OglNote
from org.pyut.ogl.OglUseCase import OglUseCase

from org.pyut.model.PyutActor import PyutActor
from org.pyut.model.PyutClass import PyutClass
from org.pyut.model.PyutNote import PyutNote
from org.pyut.model.PyutUseCase import PyutUseCase

from org.pyut.ui.TreeNotebookHandler import TreeNotebookHandler
from org.pyut.ui.PyutProject import PyutProject
from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame
from org.pyut.ui.PyutPrintout import PyutPrintout
from org.pyut.dialogs.tips.DlgTips import DlgTips

from org.pyut.ui.tools.MenuCreator import MenuCreator
from org.pyut.ui.tools.SharedTypes import SharedTypes
from org.pyut.ui.tools.ToolsCreator import ToolsCreator
from org.pyut.ui.tools.ActionCallbackType import ActionCallbackType
from org.pyut.ui.tools.SharedIdentifiers import SharedIdentifiers

from org.pyut.PyutUtils import PyutUtils

from org.pyut.PyutConstants import PyutConstants

from org.pyut.preferences.PyutPreferences import PyutPreferences

from org.pyut.general.Mediator import Mediator

from org.pyut.general.Globals import _
from org.pyut.general.Globals import IMAGE_RESOURCES_PACKAGE


class PyutApplicationFrame(Frame):
    """
    PyutApplicationFrame : main pyut frame; contain menus, status bar, UML frame, ...

    Instantiated by PyutApp.py
    Use it as a normal Frame
        dlg=PyutApplicationFrame(self, wx.ID_ANY, "Pyut")
        dlg.Show()
        dlg.Destroy()
    """
    PYUT_WIKI: str = 'https://github.com/hasii2011/PyUt/wiki/Pyut'

    def __init__(self, parent: Window, wxID: int, title: str):
        """

        Args:
            parent:     parent window
            wxID:       wx ID of this frame
            title:      Title to display
        """
        self._prefs: PyutPreferences = PyutPreferences()

        appSize: Size = Size(self._prefs.startupWidth, self._prefs.startupHeight)

        super().__init__(parent=parent, id=wxID, title=title, size=appSize, style=DEFAULT_FRAME_STYLE | FRAME_EX_METAL)

        self.logger: Logger = getLogger(__name__)
        self._createApplicationIcon()

        # Properties
        from org.pyut.plugins.PluginManager import PluginManager    # Plugin Manager should not be in plugins directory

        self.plugMgr:     PluginManager         = PluginManager()
        self.plugins:     SharedTypes.PluginMap = cast(SharedTypes.PluginMap, {})     # To store the plugins
        self.mnuFile:     Menu                  = cast(Menu, None)

        self._toolboxIds: SharedTypes.ToolboxIdMap = cast(SharedTypes.ToolboxIdMap, {})  # Association toolbox id -> category

        self._clipboard = []
        self._currentDirectory = getcwd()
        self._lastDir = self._prefs.lastOpenedDirectory

        if self._lastDir is None:  # Assert that the path is present
            self._lastDir = getcwd()

        self.CreateStatusBar()

        self._treeNotebookHandler: TreeNotebookHandler = TreeNotebookHandler(self)

        self._mediator: Mediator = Mediator()
        self._mediator.registerStatusBar(self.GetStatusBar())
        self._mediator.resetStatusText()
        self._mediator.registerAppFrame(self)
        self._mediator.registerFileHandling(self._treeNotebookHandler)
        self._mediator.registerAppPath(self._currentDirectory)

        # Last opened Files IDs
        self.lastOpenedFilesID = []
        for index in range(self._prefs.getNbLOF()):
            self.lastOpenedFilesID.append(PyutUtils.assignID(1)[0])

        # Initialization
        self._initPyutTools()   # Toolboxes, toolbar
        self._initMenu()        # Menu
        self._initPrinting()    # Printing data

        self.__setupKeyboardShortcuts()

        # set application title
        self._treeNotebookHandler.newProject()
        self._mediator.updateTitle()

        if self._prefs.centerAppOnStartUp is True:
            self.Center(BOTH)  # Center on the screen
        else:
            appPosition: Tuple[int, int] = self._prefs.appStartupPosition
            self.SetPosition(pt=appPosition)

        # Initialize the tips frame
        self._alreadyDisplayedTipsFrame = False
        self.SetThemeEnabled(True)

        self.Bind(EVT_ACTIVATE, self._onActivate)

    # noinspection PyUnusedLocal
    def updateCurrentDir(self, fullPath: str):
        """
        Deprecated use the singleton CurrentDirectoryHandler

        Set current working directory.

        Args:
            fullPath:   Full path, with filename
        """
        assert False, 'Deprecated'

    def getCurrentDir(self):
        """
        Return current working directory.

        @return String : Current directory

        @author P. Waelti <pwaelti@eivd.ch>
        @since 1.50
        """
        return self._lastDir

    def notifyTitleChanged(self):
        """
        Notify that the title changed.

        @since 1.50
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        self._mediator.updateTitle()

    def loadByFilename(self, filename):
        """
        load the specified filename
        called by PyutApp
        This is a simple indirection to _loadFile. Not direct call because
        it seems to be more logical to let _loadFile be private.
        PyutApp do not need to know the correct name of the _loadFile method.

        """
        self._loadFile(filename)

    def removeEmptyProject(self):

        self.logger.info(f'Remove the default project')

        mainUI:   TreeNotebookHandler            = self._treeNotebookHandler

        defaultProject: PyutProject = mainUI.getProject(PyutConstants.DefaultFilename)
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

        mainUI: TreeNotebookHandler = self._treeNotebookHandler

        mainUI.currentProject = project
        project.selectSelf()
        mainUI.currentFrame = project.getFrames()[0]

    def Close(self, force=False):
        """
        Closing handler overload. Save files and ask for confirmation.

        Args:
            force:

        Returns:

        """

        # Close all files
        if self._treeNotebookHandler.onClose() is False:
            return
        if self._prefs.overrideOnProgramExit is True:
            # Only save position if we are not auto-saving
            if self._prefs.centerAppOnStartUp is False:
                pos: Tuple[int, int] = self.GetPosition()
                self._prefs.appStartupPosition = pos

            ourSize: Tuple[int, int] = self.GetSize()
            self._prefs.startupWidth  = ourSize[0]
            self._prefs.startupHeight = ourSize[1]

        self._clipboard    = None
        self._treeNotebookHandler = None
        self._mediator         = None
        self._prefs        = None
        self.plugMgr       = None

        self._printData.Destroy()
        # TODO? wx.OGLCleanUp()
        self.Destroy()

    # noinspection PyUnusedLocal
    def OnImport(self, event):
        # self._treeNotebookHandler.newProject()
        # self._treeNotebookHandler.newDocument(DiagramType.CLASS_DIAGRAM)
        # self._mediator.updateTitle()
        # cl = self.plugins[event.GetId()]
        #
        # obj = cl(self._mediator.getUmlObjects(), self._mediator.getUmlFrame())
        #
        # # Do plugin functionality
        # BeginBusyCursor()
        # try:
        #     wxYield()  # time to process the refresh in newDiagram
        #     obj.doImport()
        # except (ValueError, Exception) as e:
        #     PyutUtils.displayError(_("An error occurred while executing the selected plugin"), _("Error..."), self)
        #     self.logger.error(f'{e}')
        #
        # EndBusyCursor()
        # self.Refresh()
        assert False, 'Use the file handler class'

    # noinspection PyUnusedLocal
    def OnExport(self, event: CommandEvent):
        """
        Callback.

        Args:
            event: wxEvent event
        """
        # Create a plugin instance
        # cl = self.plugins[event.GetId()]
        # umlObjects: List[OglClass]      = self._mediator.getUmlObjects()
        # umlFrame: UmlClassDiagramsFrame = self._mediator.getUmlFrame()
        # obj = cl(umlObjects, umlFrame)
        # # Do plugin functionality
        # # BeginBusyCursor()
        # obj.doExport()
        # # EndBusyCursor()
        assert False, 'Use the file handler class'

    def OnToolPlugin(self, event: CommandEvent):
        """

        Args:
            event:
        """
        # Create a plugin instance
        cl = self.plugins[event.GetId()]
        obj = cl(self._mediator.getUmlObjects(), self._mediator.getUmlFrame())

        # Do plugin functionality
        BeginBusyCursor()
        try:
            obj.callDoAction()
            self.logger.debug(f"After tool plugin do action")
        except (ValueError, Exception) as e:
            PyutUtils.displayError(_("An error occurred while executing the selected plugin"), _("Error..."), self)
            self.logger.error(f'{e}')
        EndBusyCursor()

        # Refresh screen
        umlFrame = self._mediator.getUmlFrame()
        if umlFrame is not None:
            umlFrame.Refresh()

    def OnToolboxMenuClick(self, event):
        self._mediator.displayToolbox(self._toolboxIds[event.GetId()])

    def cutSelectedShapes(self):
        """
        Cut all current shapes
        """
        selected = self._mediator.getSelectedShapes()
        if len(selected) > 0:
            self._clipboard = []
        else:
            return

        canvas = selected[0].GetDiagram().GetPanel()
        # the canvas which contain the shape
        # specify the canvas on which we will paint
        # dc = wxClientDC(canvas)
        # canvas.PrepareDC(dc)
        # diagram = self._mediator.getDiagram()

        # put the PyutObjects in the clipboard and remove them from the diagram
        for obj in selected:
            # remove the links
            # for each link
            # for link in obj.getLinks()[:]:
            # self._mediator.removeLink(link)
            obj.Detach()

        for obj in selected:
            self._clipboard.append(obj.getPyutObject())
            # self._mediator.removeClass(obj)

        self._treeNotebookHandler.setModified(True)
        self._mediator.updateTitle()
        canvas.Refresh()

    def _onActivate(self, event):
        """
        EVT_ACTIVATE Callback; display tips frame.  But only, the first activate
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

    def _initPyutTools(self):

        callbackMap: SharedTypes.CallbackMap = cast(SharedTypes.CallbackMap, {
            ActionCallbackType.NEW_ACTION:           self._OnNewAction,
            ActionCallbackType.NEW_CLASS_DIAGRAM:    self._OnMnuFileNewClassDiagram,
            ActionCallbackType.NEW_SEQUENCE_DIAGRAM: self._OnMnuFileNewSequenceDiagram,
            ActionCallbackType.NEW_USE_CASE_DIAGRAM: self._OnMnuFileNewUsecaseDiagram,
            ActionCallbackType.NEW_PROJECT:          self._OnMnuFileNewProject,
            ActionCallbackType.FILE_OPEN:            self._OnMnuFileOpen,
            ActionCallbackType.FILE_SAVE:            self._OnMnuFileSave,
            ActionCallbackType.UNDO:                 self._OnMnuUndo,
            ActionCallbackType.REDO:                 self._OnMnuRedo,
        })

        self._toolsCreator: ToolsCreator = ToolsCreator(frame=self, callbackMap=callbackMap)
        self._toolsCreator.initTools()

    def _initMenu(self):

        callbackMap: SharedTypes.CallbackMap = cast(SharedTypes.CallbackMap, {
            # ActionCallbackType.NEW_PROJECT:          self._OnMnuFileNewProject,
            ActionCallbackType.NEW_CLASS_DIAGRAM:    self._OnMnuFileNewClassDiagram,
            ActionCallbackType.NEW_SEQUENCE_DIAGRAM: self._OnMnuFileNewSequenceDiagram,
            ActionCallbackType.NEW_USE_CASE_DIAGRAM: self._OnMnuFileNewUsecaseDiagram,
            ActionCallbackType.INSERT_PROJECT:       self._OnMnuFileInsertProject,
            ActionCallbackType.PROJECT_CLOSE:        self._OnMnuFileClose,
            # ActionCallbackType.FILE_OPEN:            self._OnMnuFileOpen,
            # ActionCallbackType.FILE_SAVE:            self._OnMnuFileSave,
            ActionCallbackType.FILE_SAVE_AS:         self._OnMnuFileSaveAs,
            ActionCallbackType.REMOVE_DOCUMENT:      self._OnMnuFileRemoveDocument,
            ActionCallbackType.PRINT_SETUP:          self._OnMnuFilePrintSetup,
            ActionCallbackType.PRINT_PREVIEW:        self._OnMnuFilePrintPreview,
            ActionCallbackType.PRINT:                self._OnMnuFilePrint,
            ActionCallbackType.PYUT_PREFERENCES:     self._OnMnuFilePyutPreferences,
            ActionCallbackType.EXIT_PROGRAM:         self._OnMnuFileExit,
            ActionCallbackType.PROGRAM_ABOUT:        self._OnMnuHelpAbout,
            ActionCallbackType.HELP_INDEX:           self._OnMnuHelpIndex,
            ActionCallbackType.HELP_VERSION:         self._OnMnuHelpVersion,
            ActionCallbackType.HELP_WEB:             self._OnMnuHelpWeb,
            ActionCallbackType.ADD_PYUT_HIERARCHY:   self._OnMnuAddPyut,
            ActionCallbackType.ADD_OGL_HIERARCHY:    self._OnMnuAddOgl,

            ActionCallbackType.EDIT_COPY:            self._OnMnuEditCut,
            ActionCallbackType.EDIT_CUT:             self._OnMnuEditCopy,
            ActionCallbackType.EDIT_PASTE:           self._OnMnuEditPaste,
            ActionCallbackType.SELECT_ALL:           self._OnMnuSelectAll,
            ActionCallbackType.DEBUG:                self._OnMnuDebug,

            ActionCallbackType.UNDO: self._OnMnuUndo,
            ActionCallbackType.REDO: self._OnMnuRedo,

            ActionCallbackType.LAST_OPENED_FILES: self._OnMnuLOF,
            ActionCallbackType.CLOSE:             self.Close,
            ActionCallbackType.EXPORT:            self.OnExport,
            ActionCallbackType.IMPORT:            self.OnImport,
            ActionCallbackType.TOOL_PLUGIN:       self.OnToolPlugin,
            ActionCallbackType.TOOL_BOX_MENU:     self.OnToolboxMenuClick,
        })

        self._menuCreator: MenuCreator = MenuCreator(frame=self, callbackMap=callbackMap, lastOpenFilesID=self.lastOpenedFilesID)
        self._menuCreator.initMenus()
        self.mnuFile      = self._menuCreator.fileMenu
        self.plugins      = self._menuCreator.plugins
        self._toolboxIds  = self._menuCreator.toolboxIds
        self.logger.debug(f'self.mnuFile: {self.mnuFile}')

    def _createAcceleratorTable(self):
        """
        Accelerator table initialization

        @author C.Dutoit
        """
        #  init accelerator table
        lst = [
            (ACCEL_CTRL,     ord('n'),   SharedIdentifiers.ID_MNUFILENEWPROJECT),
            (ACCEL_CTRL,     ord('N'),   SharedIdentifiers.ID_MNUFILENEWPROJECT),
            (ACCEL_CTRL,     ord('l'),   SharedIdentifiers.ID_MNU_FILE_NEW_CLASS_DIAGRAM),
            (ACCEL_CTRL,     ord('E'),   SharedIdentifiers.ID_MNU_FILE_NEW_SEQUENCE_DIAGRAM),
            (ACCEL_CTRL,     ord('e'),   SharedIdentifiers.ID_MNU_FILE_NEW_SEQUENCE_DIAGRAM),
            (ACCEL_CTRL,     ord('U'),   SharedIdentifiers.ID_MNU_FILE_NEW_USECASE_DIAGRAM),
            (ACCEL_CTRL,     ord('u'),   SharedIdentifiers.ID_MNU_FILE_NEW_USECASE_DIAGRAM),
            (ACCEL_CTRL,     ord('o'),   SharedIdentifiers.ID_MNU_FILE_OPEN),
            (ACCEL_CTRL,     ord('O'),   SharedIdentifiers.ID_MNU_FILE_OPEN),
            (ACCEL_CTRL,     ord('s'),   SharedIdentifiers.ID_MNU_FILE_SAVE),
            (ACCEL_CTRL,     ord('S'),   SharedIdentifiers.ID_MNU_FILE_SAVE),
            (ACCEL_CTRL,     ord('a'),   SharedIdentifiers.ID_MNUFILESAVEAS),
            (ACCEL_CTRL,     ord('A'),   SharedIdentifiers.ID_MNUFILESAVEAS),
            (ACCEL_CTRL,     ord('p'),   SharedIdentifiers.ID_MNU_FILE_PRINT),
            (ACCEL_CTRL,     ord('P'),   SharedIdentifiers.ID_MNU_FILE_PRINT),
            (ACCEL_CTRL,     ord('x'),   SharedIdentifiers.ID_MNU_EDIT_CUT),
            (ACCEL_CTRL,     ord('X'),   SharedIdentifiers.ID_MNU_EDIT_CUT),
            (ACCEL_CTRL,     ord('c'),   SharedIdentifiers.ID_MNU_EDIT_COPY),
            (ACCEL_CTRL,     ord('C'),   SharedIdentifiers.ID_MNU_EDIT_COPY),
            (ACCEL_CTRL,     ord('v'),   SharedIdentifiers.ID_MNU_EDIT_PASTE),
            (ACCEL_CTRL,     ord('V'),   SharedIdentifiers.ID_MNU_EDIT_PASTE),
            (ACCEL_CTRL,     ord('d'),   SharedIdentifiers.ID_DEBUG),
            (ACCEL_CTRL,     ord('D'),   SharedIdentifiers.ID_DEBUG),
            ]
        acc = []
        for el in lst:
            (el1, el2, el3) = el
            acc.append(AcceleratorEntry(el1, el2, el3))
        return acc

    # noinspection PyUnusedLocal
    def _OnMnuFileNewProject(self, event: CommandEvent):
        assert False, 'Use the file menu handler'
    #     """
    #     Create a new project
    #
    #     Args:
    #         event:
    #     """
    #     self._treeNotebookHandler.newProject()
    #     self._mediator.updateTitle()

    # noinspection PyUnusedLocal
    def _OnMnuFileNewClassDiagram(self, event: CommandEvent):
        """
        Create a new class diagram

        Args:
            event:
        """
        # self._treeNotebookHandler.newDocument(DiagramType.CLASS_DIAGRAM)
        # self._mediator.updateTitle()
        assert False, 'Use the file menu handler'

    # noinspection PyUnusedLocal
    def _OnMnuFileNewSequenceDiagram(self, event: CommandEvent):
        """
        Create a new sequence diagram

        Args:
            event:
        """
        # self._treeNotebookHandler.newDocument(DiagramType.SEQUENCE_DIAGRAM)
        # self._mediator.updateTitle()
        assert False, 'Use the file menu handler'

    # noinspection PyUnusedLocal
    def _OnMnuFileNewUsecaseDiagram(self, event: CommandEvent):
        """
        Create a new use-case diagram

        Args:
            event:
        """
        # self._treeNotebookHandler.newDocument(DiagramType.USECASE_DIAGRAM)
        # self._mediator.updateTitle()
        assert False, 'Use the file menu handler'

    # noinspection PyUnusedLocal
    def _OnMnuFileInsertProject(self, event: CommandEvent):
        """
        Insert a project into this one

        Args:
            event:
        """
        # PyutUtils.displayWarning(_("The project insert is experimental, "
        #                            "use it at your own risk.\n"
        #                            "You risk a shapes ID duplicate with "
        #                            "unexpected results !"), parent=self)
        #
        # if (self._treeNotebookHandler.getCurrentProject()) is None:
        #     PyutUtils.displayError(_("No project to insert this file into !"), parent=self)
        #     return
        #
        # # Ask which project to insert
        # dlg = FileDialog(self, _("Choose a file"), self._lastDir, "", "*.put", FD_OPEN)
        # if dlg.ShowModal() != ID_OK:
        #     dlg.Destroy()
        #     return False
        # self.updateCurrentDir(dlg.GetPath())
        # filename = dlg.GetPath()
        # dlg.Destroy()
        #
        # print(("inserting file", str(filename)))
        #
        # # Insert the specified files
        # try:
        #     self._treeNotebookHandler.insertFile(filename)
        # except (ValueError, Exception) as e:
        #     PyutUtils.displayError(_(f"An error occurred while loading the project!  {e}"), parent=self)
        assert False, 'Use the file menu handler'

    # noinspection PyUnusedLocal
    def _OnMnuFileOpen(self, event: CommandEvent):
        assert False, 'Use the file menu handler'
    #     """
    #     Open a diagram
    #
    #     Args:
    #         event:
    #     """
    #     self._loadFile()

    # noinspection PyUnusedLocal
    def _OnMnuFileSave(self, event: CommandEvent):
        assert False, 'Use the file menu handler'
    #     """
    #     Save the current diagram to a file
    #
    #     Args:
    #         event:
    #     """
    #     self._saveFile()

    # noinspection PyUnusedLocal
    def _OnMnuFileSaveAs(self, event: CommandEvent):
        """
        Ask and save the current diagram to a file

        Args:
            event:
        """
        # self._saveFileAs()
        assert False, 'Use the file menu handler'

    # noinspection PyUnusedLocal
    def _OnMnuFileClose(self, event: CommandEvent):
        """
        Close the current file

        Args:
            event:
        """
        # self._treeNotebookHandler.closeCurrentProject()
        assert False, 'Use the file menu handler'

    # noinspection PyUnusedLocal
    def _OnMnuFileRemoveDocument(self, event: CommandEvent):
        """
        Remove the current document from the current project

        Args:
            event:
        """
        # project  = self._treeNotebookHandler.getCurrentProject()
        # document = self._treeNotebookHandler.getCurrentDocument()
        # if project is not None and document is not None:
        #     project.removeDocument(document)
        # else:
        #     PyutUtils.displayWarning(_("No document to remove"))
        assert False, 'Use the file menu handler'

    # noinspection PyUnusedLocal
    def _OnMnuFilePrintSetup(self, event: CommandEvent):
        """
        Display the print setup dialog box

        Args:
            event:
        """
        dlg: PrintDialog = PrintDialog(self)

        # dlg.GetPrintDialogData().SetSetupDialog(True)
        dlg.GetPrintDialogData().SetPrintData(self._printData)
        dlg.ShowModal()
        self._printData = dlg.GetPrintDialogData().GetPrintData()
        dlg.Destroy()

    # noinspection PyUnusedLocal
    def _OnMnuFilePrintPreview(self, event: CommandEvent):
        """
        Display the print preview frame; Preview before printing.

        Args:
            event:
        """
        self._mediator.deselectAllShapes()
        frame = self._mediator.getUmlFrame()
        if frame == -1:
            PyutUtils.displayError(_("Can't print nonexistent frame..."), _("Error..."), self)
            return

        printout  = PyutPrintout(frame)
        printout2 = PyutPrintout(frame)
        preview   = PrintPreview(printout, printout2, self._printData)

        if not preview.IsOk():
            PyutUtils.displayError(_("An unknown error occurred while previewing"), _("Error..."), self)
            return

        frame = PreviewFrame(preview, self, _("Diagram preview"))
        frame.Initialize()
        frame.Centre(BOTH)

        try:
            frame.Show(True)
        except (ValueError, Exception) as e:
            PyutUtils.displayError(_("An unknown error occurred while previewing"), _("Error..."), self)

    # noinspection PyUnusedLocal
    def _OnMnuFilePrint(self, event: CommandEvent):
        """
        Print the current diagram

        Args:
            event:
        """
        if self._mediator.getDiagram() is None:
            PyutUtils.displayError(_("No diagram to print !"), _("Error"), self)
            return
        self._mediator.deselectAllShapes()
        printDialogData: PrintDialogData = PrintDialogData()

        printDialogData.SetPrintData(self._printData)
        printDialogData.SetMinPage(1)
        printDialogData.SetMaxPage(1)
        printer  = Printer(printDialogData)
        printout = PyutPrintout(self._mediator.getUmlFrame())

        if not printer.Print(self, printout, True):
            PyutUtils.displayError(_("Cannot print"), _("Error"), self)

    # noinspection PyUnusedLocal
    def _OnMnuLOF(self, event: CommandEvent):
        """
        Open a file from the last opened files list

        Args:
            event:
        """
        # for index in range(self._prefs.getNbLOF()):
        #     if event.GetId() == self.lastOpenedFilesID[index]:
        #         try:
        #             lst = self._prefs.getLastOpenedFilesList()
        #             self._loadFile(lst[index])
        #             self._prefs.addNewLastOpenedFilesEntry(lst[index])
        #             self.__setLastOpenedFilesItems()
        #         except (ValueError, Exception) as e:
        #             self.logger.error(f'{e}')
        assert False, 'Use the file menu handler'

    # noinspection PyUnusedLocal
    def _OnMnuFileExit(self, event: CommandEvent):
        """
        Exit the program

        Args:
            event:
        """
        self.Close()

    # noinspection PyUnusedLocal
    def _OnMnuHelpAbout(self, event: CommandEvent):
        """
        Show the about box

        Args:
            event:
        """
        from org.pyut.dialogs.DlgAbout import DlgAbout
        from org.pyut.general.PyutVersion import PyutVersion
        dlg = DlgAbout(self, ID_ANY, _("About PyUt ") + PyutVersion.getPyUtVersion())
        dlg.ShowModal()
        dlg.Destroy()

    # noinspection PyUnusedLocal
    def _OnMnuHelpIndex(self, event: CommandEvent):
        """
        Display the help index
        """

        from org.pyut.dialogs import DlgHelp
        dlgHelp = DlgHelp.DlgHelp(self, -1, _("Pyut Help"))
        dlgHelp.Show(True)

    # noinspection PyUnusedLocal
    def _OnMnuHelpVersion(self, event: CommandEvent):
        """
        Check for newer version.
        Args:
            event:
        """
        # Init
        FILE_TO_CHECK = "http://pyut.sourceforge.net/backdoors/lastversion"     # TODO FIXME  :-)

        # Get file  -- Python 3 update
        f = request.urlopen(FILE_TO_CHECK)
        lstFile = f.readlines()
        f.close()

        # Verify data coherence
        if lstFile[0][:15] != "Last version = " or lstFile[1][:15] != "Old versions = ":
            msg = "Incorrect file on server"
        else:
            latestVersion = lstFile[0][15:]
            oldestVersions = lstFile[1][15:].split()
            print(oldestVersions)

            from org.pyut.general.PyutVersion import PyutVersion
            v = PyutVersion.getPyUtVersion()
            if v in oldestVersions:
                msg = _("PyUt version ") + str(latestVersion) + _(" is available on http://pyut.sf.net")
            else:
                msg = _("No newer version yet !")

        # Display dialog box
        PyutUtils.displayInformation(msg, _("Check for newer version"), self)

    # noinspection PyUnusedLocal
    def _OnMnuHelpWeb(self, event: CommandEvent):
        """

        Args:
            event:
        """
        PyutUtils.displayInformation(f"Please point your browser to {PyutApplicationFrame.PYUT_WIKI}", "Pyut's new wiki", self)

    # noinspection PyUnusedLocal
    def _OnMnuAddPyut(self, event: CommandEvent):
        """
        Add Pyut UML Diagram.

        Args:
            event:
        """
        frame: UmlClassDiagramsFrame = self._mediator.getUmlFrame()
        if self._isDiagramFromOpen(frame) is True:
            frame.addPyutHierarchy()
            self._refreshUI(frame)

    # noinspection PyUnusedLocal
    def _OnMnuAddOgl(self, event: CommandEvent):
        """
        Add Pyut-Ogl UML Diagram.

        Args:
            event:
        """
        frame: UmlClassDiagramsFrame = self._mediator.getUmlFrame()
        if self._isDiagramFromOpen(frame) is True:
            frame.addOglHierarchy()
            self._refreshUI(frame)

    def _isDiagramFromOpen(self, frame: UmlClassDiagramsFrame) -> bool:
        """
        Does 2 things, Checks and displays the dialog;  Oh well

        Args:
            frame:

        Returns: `True` if there is a frame open else, `False`

        """
        if frame is None:
            PyutUtils.displayWarning(msg=_("Please open a diagram to hold the UML"), title=_('Silly User'), parent=self)
            return False
        else:
            return True

    def _refreshUI(self, frame: UmlClassDiagramsFrame):

        project: PyutProject = self._treeNotebookHandler.getCurrentProject()
        project.setModified(True)
        self._mediator.updateTitle()
        frame.Refresh()

    def _loadFile(self, filename: str = ""):
        """
        Load the specified filename

        Args:
            filename: Its name
        """
        # Make a list to be compatible with multi-files loading
        fileNames = [filename]

        # Ask which filename to load
        # TODO This is bad practice to do something different based on input
        if filename == "":
            dlg = FileDialog(self, _("Choose a file"), self._lastDir, "", "*.put", FD_OPEN | FD_MULTIPLE)

            if dlg.ShowModal() != ID_OK:
                dlg.Destroy()
                return False

            fileNames = dlg.GetPaths()
            self.updateCurrentDir(fileNames[0])
            dlg.Destroy()

        self.logger.info(f"loading file(s) {filename}")

        # Open the specified files
        for filename in fileNames:
            try:
                if self._treeNotebookHandler.openFile(filename):
                    # Add to last opened files list
                    self._prefs.addNewLastOpenedFilesEntry(filename)
                    self.__setLastOpenedFilesItems()
                    self._mediator.updateTitle()
            except (ValueError, Exception) as e:
                PyutUtils.displayError(_("An error occurred while loading the project !"), parent=self)
                self.logger.error(f'{e}')

    def _saveFile(self):
        """
        Save to the current filename
        """
        self._treeNotebookHandler.saveFile()
        self._mediator.updateTitle()

        # Add to last opened files list
        project = self._treeNotebookHandler.getCurrentProject()
        if project is not None:
            self._prefs.addNewLastOpenedFilesEntry(project.getFilename())
            self.__setLastOpenedFilesItems()

    def _saveFileAs(self):
        """
        Save to the current filename; Ask for the name
        """
        self._treeNotebookHandler.saveFileAs()
        self._mediator.updateTitle()

        project = self._treeNotebookHandler.getCurrentProject()
        if project is not None:
            self._prefs.addNewLastOpenedFilesEntry(project.getFilename())
            self.__setLastOpenedFilesItems()

    def _OnNewAction(self, event: CommandEvent):
        """
        Call the mediator to specify the current action.

        Args:
            event:
        """
        currentAction: int = SharedIdentifiers.ACTIONS[event.GetId()]

        self._mediator.setCurrentAction(currentAction)
        self._mediator.selectTool(event.GetId())
        self._treeNotebookHandler.setModified(True)
        self._mediator.updateTitle()

    # noinspection PyUnusedLocal
    def _OnMnuEditCut(self, event: CommandEvent):
        """

        Args:
            event:
        """
        self.cutSelectedShapes()

    # noinspection PyUnusedLocal
    def _OnMnuEditCopy(self, event: CommandEvent):
        """
        TODO : adapt for OglLinks

        Args:
            event:
        """
        selected = self._mediator.getSelectedShapes()
        if len(selected) > 0:
            self._clipboard = []
        else:
            return

        # put a copy of the PyutObjects in the clipboard
        for obj in selected:
            obj = copy(obj.getPyutObject())
            obj.setLinks([])   # we don't want to copy the links
            self._clipboard.append(obj)

    # noinspection PyUnboundLocalVariable
    # noinspection PyUnusedLocal
    def _OnMnuEditPaste(self, event: CommandEvent):
        """

        Args:
            event:
        """
        if len(self._clipboard) == 0:
            return

        frame = self._mediator.getUmlFrame()
        if frame == -1:
            PyutUtils.displayError(_("No frame to paste into"))
            return

        # put the objects in the clipboard and remove them from the diagram
        x, y = 100, 100
        for obj in self._clipboard:
            obj = copy(obj)  # this is a PyutObject
            if isinstance(obj, PyutClass):
                po = OglClass(obj)
            elif isinstance(obj, PyutNote):
                po = OglNote(obj)
            elif isinstance(obj, PyutActor):
                po = OglActor(obj)
            elif isinstance(obj, PyutUseCase):
                po = OglUseCase(obj)
            else:
                self.logger.error("Error when try to paste object")
                return
            self._mediator.getUmlFrame().addShape(po, x, y)
            x += 20
            y += 20

        canvas = po.GetDiagram().GetPanel()
        # the canvas that contain the shape
        # specify the canvas on which we will paint
        dc = ClientDC(canvas)
        canvas.PrepareDC(dc)

        self._treeNotebookHandler.setModified(True)
        self._mediator.updateTitle()
        canvas.Refresh()
        # TODO : What are you doing with the dc ?

    # noinspection PyUnusedLocal
    def _OnMnuSelectAll(self, event: CommandEvent):
        """

        Args:
            event:
        """
        frame = self._mediator.getUmlFrame()
        if frame is None:
            PyutUtils.displayError(_("No frame found !"))
            return
        diagram = frame.GetDiagram()
        shapes = diagram.GetShapes()
        for shape in shapes:
            shape.SetSelected(True)
        frame.Refresh()

    # noinspection PyUnusedLocal
    def _OnMnuFilePyutPreferences(self, event: CommandEvent):

        # from org.pyut.dialogs.preferences.DlgPyutPreferences import DlgPyutPreferences
        #
        # self.logger.debug(f"Before dialog show")
        # with DlgPyutPreferences(self, ID_ANY) as dlg:
        #     if dlg.ShowModal() == ID_OK:
        #         self.logger.debug(f'Waiting for answer')
        #     else:
        #         self.logger.debug(f'Cancelled')
        #
        # umlFrame = self._mediator.getUmlFrame()
        # if umlFrame is not None:
        #     umlFrame.Refresh()
        pass

    # noinspection PyUnusedLocal
    def _OnMnuDebug(self, event: CommandEvent):
        """
        Open a dialog to access the Pyut loggers

        Args:
            event:
        """
        with DlgPyutDebug(self, ID_ANY) as dlg:
            dlg: DlgPyutDebug = cast(DlgPyutDebug, dlg)
            dlg.ShowModal()

    # noinspection PyUnusedLocal
    def _OnMnuUndo(self, event: CommandEvent):
        """

        Args:
            event:
        """
        if (self._treeNotebookHandler.getCurrentFrame()) is None:
            PyutUtils.displayWarning(msg=_('No selected frame'), title=_('Huh!'))
            return
        self._treeNotebookHandler.getCurrentFrame().getHistory().undo()

    # noinspection PyUnusedLocal
    def _OnMnuRedo(self, event: CommandEvent):
        """

        Args:
            event:
        """
        if (self._treeNotebookHandler.getCurrentFrame()) is None:
            PyutUtils.displayWarning(msg=_('No selected frame'), title=_('Huh!'))
            return
        self._treeNotebookHandler.getCurrentFrame().getHistory().redo()

    def _initPrinting(self):
        """
        printing data initialization
        """
        self._printData = PrintData()
        self._printData.SetPaperId(PAPER_A4)
        self._printData.SetQuality(PRINT_QUALITY_HIGH)
        self._printData.SetOrientation(PORTRAIT)
        self._printData.SetNoCopies(1)
        self._printData.SetCollate(True)

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

    def __setLastOpenedFilesItems(self):
        """
        Set the menu last opened files items
        """
        self.logger.debug(f'self.mnuFile: {self.mnuFile}')

        index = 0
        for el in self._prefs.getLastOpenedFilesList():
            openFilesId = self.lastOpenedFilesID[index]
            # self.mnuFile.SetLabel(id=openFilesId, label="&" + str(index+1) + " " + el)
            lbl: str = f"&{str(index+1)} {el}"
            self.logger.debug(f'lbL: {lbl}  openFilesId: {openFilesId}')
            self.mnuFile.SetLabel(id=openFilesId, label=lbl)

            index += 1

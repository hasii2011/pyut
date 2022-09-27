
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from wx import BOTH
from wx import FD_MULTIPLE
from wx import FD_OPEN
from wx import ID_ANY
from wx import ID_OK
from wx import PAPER_A4
from wx import PORTRAIT
from wx import PRINT_QUALITY_HIGH
from wx import EVT_CLOSE

from wx import CommandEvent
from wx import FileDialog
from wx import Menu
from wx import PreviewFrame
from wx import PrintData
from wx import PrintDialog
from wx import PrintDialogData
from wx import PrintPreview
from wx import Printer
from wx import Window
from wx import CloseEvent

from wx import PostEvent as wxPostEvent
from wx import Yield as wxYield

from org.pyut.PyutUtils import PyutUtils
from org.pyut.dialogs.preferences.DlgPyutPreferences import DlgPyutPreferences

from org.pyut.enums.DiagramType import DiagramType

# noinspection PyProtectedMember
from org.pyut.general.Globals import _
from org.pyut.general.exceptions.UnsupportedOperation import UnsupportedOperation

from ogl.OglClass import OglClass

from org.pyut.preferences.PyutPreferences import PyutPreferences

from org.pyut.ui.CurrentDirectoryHandler import CurrentDirectoryHandler
from org.pyut.ui.PyutPrintout import PyutPrintout

from org.pyut.ui.umlframes.UmlClassDiagramsFrame import UmlClassDiagramsFrame
from org.pyut.ui.frame.BaseMenuHandler import BaseMenuHandler

from org.pyut.ui.tools.SharedTypes import PluginMap

from org.pyut.uiv2.PyutUIV2 import PyutUIV2

from org.pyut.uiv2.eventengine.Events import EVENT_UPDATE_RECENT_PROJECTS
from org.pyut.uiv2.eventengine.Events import EventType
from org.pyut.uiv2.eventengine.Events import UpdateRecentProjectsEvent
from org.pyut.uiv2.eventengine.IEventEngine import IEventEngine


class FileMenuHandler(BaseMenuHandler):

    def __init__(self, fileMenu: Menu, lastOpenFilesIDs: List[int], eventEngine: IEventEngine = None):

        super().__init__(menu=fileMenu, eventEngine=eventEngine)

        self.logger: Logger = getLogger(__name__)

        self._lastOpenedFilesIDs: List[int]       = lastOpenFilesIDs
        self._preferences:        PyutPreferences = PyutPreferences()
        self._plugins:            PluginMap       = cast(PluginMap, {})     # To store the plugins

        self._currentDirectoryHandler: CurrentDirectoryHandler = CurrentDirectoryHandler()
        self._treeNotebookHandler:     PyutUIV2    = self._mediator.getFileHandling()

        self._printData: PrintData = cast(PrintData, None)

        self._initPrinting()    # Printing data
        self._eventEngine.registerListener(EVENT_UPDATE_RECENT_PROJECTS, self._onUpdateRecentProjects)

    @property
    def exportPlugins(self) -> PluginMap:
        raise UnsupportedOperation('Property is write only')

    @exportPlugins.setter
    def exportPlugins(self, exportPlugins: PluginMap):
        self._exportPlugins = exportPlugins

    @property
    def importPlugins(self) -> PluginMap:
        raise UnsupportedOperation('Property is write only')

    @importPlugins.setter
    def importPlugins(self, importPlugins: PluginMap):
        self._importPlugins = importPlugins

    def createTheLastOpenedFilesMenuItems(self):
        self._updateRecentlyOpenedMenuItems()

    # noinspection PyUnusedLocal
    def onNewProject(self, event: CommandEvent):
        """
        Create a new project

        Args:
            event:
        """
        self._treeNotebookHandler.newProject()
        self._mediator.updateTitle()

    # noinspection PyUnusedLocal
    def onNewClassDiagram(self, event: CommandEvent):
        """
        Create a new class diagram

        Args:
            event:
        """
        from org.pyut.ui.Mediator import Mediator

        if self._preferences.usev2ui is True:
            Mediator().newDocument(DiagramType.CLASS_DIAGRAM)
        else:
            self._treeNotebookHandler.newDocument(DiagramType.CLASS_DIAGRAM)
        self._mediator.updateTitle()

    # noinspection PyUnusedLocal
    def onNewSequenceDiagram(self, event: CommandEvent):
        """
        Create a new sequence diagram

        Args:
            event:
        """
        from org.pyut.ui.Mediator import Mediator

        if self._preferences.usev2ui is True:
            Mediator().newDocument(DiagramType.SEQUENCE_DIAGRAM)
        else:
            self._treeNotebookHandler.newDocument(DiagramType.SEQUENCE_DIAGRAM)
        self._mediator.updateTitle()

    # noinspection PyUnusedLocal
    def onNewUsecaseDiagram(self, event: CommandEvent):
        """
        Create a new use-case diagram

        Args:
            event:
        """
        from org.pyut.ui.Mediator import Mediator

        if self._preferences.usev2ui is True:
            Mediator().newDocument(DiagramType.USECASE_DIAGRAM)
        else:
            self._treeNotebookHandler.newDocument(DiagramType.USECASE_DIAGRAM)

        self._mediator.updateTitle()

    # noinspection PyUnusedLocal
    def onFileInsertProject(self, event: CommandEvent):
        """
        Insert a project into this one

        Args:
            event:
        """
        PyutUtils.displayWarning(_("The project insert is experimental, use it at your own risk.\n"
                                   "You risk a shapes ID duplicate with unexpected results !"))

        if self._treeNotebookHandler.currentProject is None:
            PyutUtils.displayError(_("No project to insert this file into !"))
            return

        # Ask which project to insert
        defaultDirectory: str    = self._currentDirectoryHandler.currentDirectory

        dlg = FileDialog(self._parent, _("Choose a project"), defaultDirectory, "", "*.put", FD_OPEN)
        if dlg.ShowModal() != ID_OK:
            dlg.Destroy()
            return False
        self._currentDirectoryHandler.currentDirectory = dlg.GetPath()
        filename = dlg.GetPath()
        dlg.Destroy()

        self.logger.warning(f'inserting file: {filename}')

        self._eventEngine.sendEvent(EventType.InsertProject, projectFilename=filename)

    # noinspection PyUnusedLocal
    def onFileOpen(self, event: CommandEvent):
        """
        Open a diagram

        Args:
            event:
        """
        self.loadFile()

    # noinspection PyUnusedLocal
    def onFileSave(self, event: CommandEvent):
        """
        Save the current project

        Args:
            event:
        """
        self._eventEngine.sendEvent(EventType.SaveProject)

    # noinspection PyUnusedLocal
    def onFileSaveAs(self, event: CommandEvent):
        """
        Rename the current project

        Args:
            event:
        """
        self._eventEngine.sendEvent(EventType.SaveProjectAs)

    # noinspection PyUnusedLocal
    def onFileClose(self, event: CommandEvent):
        """
        Close the current file

        Args:
            event:
        """
        # self._treeNotebookHandler.closeCurrentProject()
        self._eventEngine.sendEvent(EventType.CloseProject)

    # noinspection PyUnusedLocal
    def onRemoveDocument(self, event: CommandEvent):
        """
        Remove the current document from the current project
        Args:
            event:
        """
        self._eventEngine.sendEvent(EventType.RemoveDocument)

    def onImport(self, event: CommandEvent):

        self._treeNotebookHandler.newProject()
        self._treeNotebookHandler.newDocument(DiagramType.CLASS_DIAGRAM)
        self._mediator.updateTitle()
        cl = self._importPlugins[event.GetId()]

        obj = cl(self._mediator.getUmlObjects(), self._mediator.getUmlFrame())

        # Do plugin functionality
        try:
            wxYield()
            obj.doImport()
        except (ValueError, Exception) as e:
            PyutUtils.displayError(_("An error occurred while executing the selected plugin"), _("Error..."))
            self.logger.error(f'{e}')

        parent: Window = self._menu.GetWindow()

        parent.Refresh()

    def onExport(self, event: CommandEvent):
        """
        Callback.

        Args:
            event: A command event
        """
        # Create a plugin instance
        cl = self._exportPlugins[event.GetId()]
        umlObjects: List[OglClass]      = cast(List[OglClass], self._mediator.getUmlObjects())
        umlFrame: UmlClassDiagramsFrame = self._mediator.getUmlFrame()
        obj = cl(umlObjects, umlFrame)
        try:
            wxYield()
            obj.doExport()
        except (ValueError, Exception) as e:
            PyutUtils.displayError(_("An error occurred while executing the selected plugin"), _("Error..."))
            self.logger.error(f'{e}')

    # noinspection PyUnusedLocal
    def onPyutPreferences(self, event: CommandEvent):

        self.logger.debug(f"Before dialog show")

        with DlgPyutPreferences(self._parent, ID_ANY) as dlg:
            if dlg.ShowModal() == ID_OK:
                self.logger.debug(f'Waiting for answer')
            else:
                self.logger.debug(f'Cancelled')

        umlFrame = self._mediator.getUmlFrame()
        if umlFrame is not None:
            umlFrame.Refresh()

    # noinspection PyUnusedLocal
    def onPrintSetup(self, event: CommandEvent):
        """
        Display the print setup dialog box

        Args:
            event:
        """

        dlg: PrintDialog = PrintDialog(self._parent)

        dlg.GetPrintDialogData().SetPrintData(self._printData)
        dlg.ShowModal()
        self._printData = dlg.GetPrintDialogData().GetPrintData()
        dlg.Destroy()

    # noinspection PyUnusedLocal
    def onPrintPreview(self, event: CommandEvent):
        """
        Display the print preview frame; Preview before printing.

        Args:
            event:
        """
        parent: Window = self._parent

        self._mediator.deselectAllShapes()
        frame = self._mediator.getUmlFrame()
        if frame == -1:
            PyutUtils.displayError(_("Can't print nonexistent frame..."), _("Error..."))
            return

        printout  = PyutPrintout(frame)
        printout2 = PyutPrintout(frame)
        preview   = PrintPreview(printout, printout2, self._printData)

        if not preview.IsOk():
            PyutUtils.displayError(_("An unknown error occurred while previewing"), _("Error..."))
            return

        frame = PreviewFrame(preview, parent, _("Diagram preview"))
        frame.Initialize()
        frame.Centre(BOTH)

        try:
            frame.Show(True)
        except (ValueError, Exception) as e:
            PyutUtils.displayError(_("An unknown error occurred while previewing"), _("Error..."))

    # noinspection PyUnusedLocal
    def onPrint(self, event: CommandEvent):
        """
        Print the current diagram

        Args:
            event:
        """
        if self._mediator.getDiagram() is None:
            PyutUtils.displayError(_("No diagram to print !"), _("Error"))
            return
        self._mediator.deselectAllShapes()
        printDialogData: PrintDialogData = PrintDialogData()

        printDialogData.SetPrintData(self._printData)
        printDialogData.SetMinPage(1)
        printDialogData.SetMaxPage(1)
        printer  = Printer(printDialogData)
        printout = PyutPrintout(self._mediator.getUmlFrame())

        if not printer.Print(self._parent, printout, True):
            PyutUtils.displayError(_("Cannot print"), _("Error"))

    def onRecentlyOpenedFile(self, event: CommandEvent):
        """
        Open a file from the last opened files list

        Args:
            event:
        """
        for index in range(self._preferences.getNbLOF()):
            if event.GetId() == self._lastOpenedFilesIDs[index]:
                try:
                    lst = self._preferences.getLastOpenedFilesList()
                    self.loadFile(lst[index])
                    self._preferences.addNewLastOpenedFilesEntry(lst[index])
                    self._updateRecentlyOpenedMenuItems()
                except (ValueError, Exception) as e:
                    self.logger.error(f'{e}')

    # noinspection PyUnusedLocal
    def onExit(self, event: CommandEvent):
        """
        Exit the program

        Args:
            event:
        """
        closeEvent: CloseEvent = CloseEvent(EVT_CLOSE.typeId)

        parent: Window = event.GetEventObject().GetWindow()
        wxPostEvent(parent, closeEvent)

    def loadFile(self, filename: str = ""):
        """
        Load the specified filename;  This is externally available so that
        we can open a file from the command line

        Args:
            filename: Its name
        """
        # Make a list to be compatible with multi-files loading
        fileNames:  List[str] = [filename]
        currentDir: str       = self._mediator.getCurrentDir()

        # TODO This is bad practice to do something different based on input
        if filename == "":
            dlg = FileDialog(self._parent, _("Choose a file"), currentDir, "", "*.put", FD_OPEN | FD_MULTIPLE)

            if dlg.ShowModal() != ID_OK:
                dlg.Destroy()
                return False

            fileNames = dlg.GetPaths()
            self._currentDirectoryHandler.currentDirectory = fileNames[0]

            dlg.Destroy()

        self.logger.info(f"loading file(s) {filename}")

        # Open the specified files
        for filename in fileNames:
            try:
                if self._treeNotebookHandler.openFile(filename):
                    # Add to last opened files list
                    self._preferences.addNewLastOpenedFilesEntry(filename)
                    self._updateRecentlyOpenedMenuItems()
                    self._mediator.updateTitle()
                else:
                    PyutUtils.displayError(msg='File not loaded', title='Error')
            except (ValueError, Exception) as e:
                PyutUtils.displayError(_("An error occurred while loading the project !"))
                self.logger.error(f'{e}')

    # noinspection PyUnusedLocal
    def _onUpdateRecentProjects(self, event: UpdateRecentProjectsEvent):
        self._updateRecentlyOpenedMenuItems()

    def _updateRecentlyOpenedMenuItems(self):
        """
        Set the menu items for the last opened files
        """

        self.logger.debug(f'{self._menu=}')

        index: int = 0
        files: List[str] = self._preferences.getLastOpenedFilesList()
        for fileName in files:

            openFilesId: int = self._lastOpenedFilesIDs[index]
            menuLabel: str = f"&{str(index + 1)} {fileName}"
            self.logger.debug(f'lbL: {menuLabel}  openFilesId: {openFilesId}')
            self._menu.SetLabel(id=openFilesId, label=menuLabel)

            index += 1

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

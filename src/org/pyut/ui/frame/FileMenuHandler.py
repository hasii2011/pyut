
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

from org.pyut.ogl.OglClass import OglClass

from org.pyut.preferences.PyutPreferences import PyutPreferences

from org.pyut.ui.CurrentDirectoryHandler import CurrentDirectoryHandler
from org.pyut.ui.PyutPrintout import PyutPrintout
from org.pyut.ui.TreeNotebookHandler import TreeNotebookHandler
from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame
from org.pyut.ui.frame.BaseMenuHandler import BaseMenuHandler

from org.pyut.ui.tools.SharedTypes import PluginMap


class FileMenuHandler(BaseMenuHandler):

    def __init__(self, fileMenu: Menu, lastOpenFilesIDs: List[int]):

        super().__init__(menu=fileMenu)

        self.logger: Logger = getLogger(__name__)

        self._lastOpenedFilesIDs: List[int]       = lastOpenFilesIDs
        self._preferences:        PyutPreferences = PyutPreferences()
        self._plugins:            PluginMap       = cast(PluginMap, {})     # To store the plugins

        self._currentDirectoryHandler: CurrentDirectoryHandler = CurrentDirectoryHandler()
        self._treeNotebookHandler:     TreeNotebookHandler     = self._mediator.getFileHandling()

        self._printData: PrintData = cast(PrintData, None)

        self._initPrinting()    # Printing data

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
        self._treeNotebookHandler.newDocument(DiagramType.CLASS_DIAGRAM)
        self._mediator.updateTitle()

    # noinspection PyUnusedLocal
    def onNewSequenceDiagram(self, event: CommandEvent):
        """
        Create a new sequence diagram

        Args:
            event:
        """
        self._treeNotebookHandler.newDocument(DiagramType.SEQUENCE_DIAGRAM)
        self._mediator.updateTitle()

    # noinspection PyUnusedLocal
    def onNewUsecaseDiagram(self, event: CommandEvent):
        """
        Create a new use-case diagram

        Args:
            event:
        """
        self._treeNotebookHandler.newDocument(DiagramType.USECASE_DIAGRAM)
        self._mediator.updateTitle()

    # noinspection PyUnusedLocal
    def onFileInsertProject(self, event: CommandEvent):
        """
        Insert a project into this one

        Args:
            event:
        """
        PyutUtils.displayWarning(_("The project insert is experimental, "
                                   "use it at your own risk.\n"
                                   "You risk a shapes ID duplicate with "
                                   "unexpected results !"), parent=self)

        if (self._treeNotebookHandler.getCurrentProject()) is None:
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

        # Insert the specified files
        try:
            self._treeNotebookHandler.insertFile(filename)
        except (ValueError, Exception) as e:
            PyutUtils.displayError(_(f"An error occurred while loading the project!  {e}"))

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
        Save the current diagram to a file

        Args:
            event:
        """
        # self._saveFile()
        self._treeNotebookHandler.saveFile()
        self._mediator.updateTitle()

        # Add to last opened files list
        project = self._treeNotebookHandler.getCurrentProject()
        if project is not None:
            self._preferences.addNewLastOpenedFilesEntry(project.filename)
            self.setLastOpenedFilesItems()

    # noinspection PyUnusedLocal
    def onFileSaveAs(self, event: CommandEvent):
        """
        Ask and save the current diagram to a file

        Args:
            event:
        """
        self._treeNotebookHandler.saveFileAs()
        self._mediator.updateTitle()

        project = self._treeNotebookHandler.getCurrentProject()
        if project is not None:
            self._preferences.addNewLastOpenedFilesEntry(project.filename)
            self.setLastOpenedFilesItems()

    # noinspection PyUnusedLocal
    def onFileClose(self, event: CommandEvent):
        """
        Close the current file

        Args:
            event:
        """
        self._treeNotebookHandler.closeCurrentProject()

    # noinspection PyUnusedLocal
    def onRemoveDocument(self, event: CommandEvent):
        """
        Remove the current document from the current project

        Args:
            event:
        """
        project  = self._treeNotebookHandler.getCurrentProject()
        document = self._treeNotebookHandler.getCurrentDocument()
        if project is not None and document is not None:
            project.removeDocument(document)
        else:
            PyutUtils.displayWarning(_("No document to remove"))

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
                    self.setLastOpenedFilesItems()
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
                    self.setLastOpenedFilesItems()
                    self._mediator.updateTitle()
                else:
                    PyutUtils.displayError(msg='File not loaded', title='Error')
            except (ValueError, Exception) as e:
                PyutUtils.displayError(_("An error occurred while loading the project !"))
                self.logger.error(f'{e}')

    def setLastOpenedFilesItems(self):
        """
        Set the menu last opened files items
        """
        self.logger.debug(f'{self._menu=}')

        index = 0
        for el in self._preferences.getLastOpenedFilesList():
            openFilesId = self._lastOpenedFilesIDs[index]
            # self.mnuFile.SetLabel(id=openFilesId, label="&" + str(index+1) + " " + el)
            lbl: str = f"&{str(index+1)} {el}"
            self.logger.debug(f'lbL: {lbl}  openFilesId: {openFilesId}')
            self._menu.SetLabel(id=openFilesId, label=lbl)

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

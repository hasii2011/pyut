
from typing import List
from typing import NewType
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

from org.pyut.PyutUtils import PyutUtils
from org.pyut.dialogs.preferences.DlgPyutPreferences import DlgPyutPreferences

from org.pyut.enums.DiagramType import DiagramType

# noinspection PyProtectedMember
from org.pyut.general.Globals import _
from org.pyut.general.exceptions.UnsupportedOperation import UnsupportedOperation


from org.pyut.preferences.PyutPreferences import PyutPreferences

from org.pyut.ui.CurrentDirectoryHandler import CurrentDirectoryHandler
from org.pyut.ui.PyutPrintout import PyutPrintout

from org.pyut.ui.frame.BaseMenuHandler import BaseMenuHandler

from org.pyut.ui.tools.SharedTypes import PluginMap

from org.pyut.uiv2.eventengine.ActiveProjectInformation import ActiveProjectInformation

from org.pyut.uiv2.eventengine.Events import EVENT_UPDATE_RECENT_PROJECTS
from org.pyut.uiv2.eventengine.Events import EventType
from org.pyut.uiv2.eventengine.Events import UpdateRecentProjectsEvent
from org.pyut.uiv2.eventengine.IEventEngine import IEventEngine

FileNames = NewType('FileNames', List[str])


class FileMenuHandler(BaseMenuHandler):

    def __init__(self, fileMenu: Menu, lastOpenFilesIDs: List[int], eventEngine: IEventEngine = None):

        super().__init__(menu=fileMenu, eventEngine=eventEngine)

        self.logger: Logger = getLogger(__name__)

        self._lastOpenedFilesIDs: List[int]       = lastOpenFilesIDs
        self._preferences:        PyutPreferences = PyutPreferences()
        self._plugins:            PluginMap       = cast(PluginMap, {})     # To store the plugins

        self._currentDirectoryHandler: CurrentDirectoryHandler = CurrentDirectoryHandler()

        self._printData: PrintData = cast(PrintData, None)

        self._initPrinting()    # Printing data
        if self._preferences.usev2ui is True:
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
        self._eventEngine.sendEvent(EventType.NewProject)

    # noinspection PyUnusedLocal
    def onNewClassDiagram(self, event: CommandEvent):
        """
        Create a new class diagram

        Args:
            event:
        """
        self._eventEngine.sendEvent(EventType.NewDiagram, diagramType=DiagramType.CLASS_DIAGRAM)

    # noinspection PyUnusedLocal
    def onNewSequenceDiagram(self, event: CommandEvent):
        """
        Create a new sequence diagram

        Args:
            event:
        """
        self._eventEngine.sendEvent(EventType.NewDiagram, diagramType=DiagramType.SEQUENCE_DIAGRAM)

    # noinspection PyUnusedLocal
    def onNewUsecaseDiagram(self, event: CommandEvent):
        """
        Create a new use-case diagram

        Args:
            event:
        """
        self._eventEngine.sendEvent(EventType.NewDiagram, diagramType=DiagramType.USECASE_DIAGRAM)

    # noinspection PyUnusedLocal
    def onFileInsertProject(self, event: CommandEvent):
        """
        Insert a project into this one

        Args:
            event:
        """
        PyutUtils.displayWarning(msg="The project insert is experimental, use it at your own risk.\nYou risk a shapes ID duplicate with unexpected results !")

        self._eventEngine.sendEvent(EventType.ActiveProjectInformation, callback=self._doInsertProject)

    def _doInsertProject(self, activeProjectInformation: ActiveProjectInformation):
        """

        Args:
            activeProjectInformation:
        """
        if activeProjectInformation.pyutProject is not None:
            # Ask which project to insert
            defaultDirectory: str    = self._currentDirectoryHandler.currentDirectory

            dlg = FileDialog(self._parent, "Choose a project", defaultDirectory, "", "*.put", FD_OPEN)
            if dlg.ShowModal() != ID_OK:
                dlg.Destroy()
                return False
            self._currentDirectoryHandler.currentDirectory = dlg.GetPath()
            filename = dlg.GetPath()
            dlg.Destroy()

            self.logger.warning(f'inserting file: {filename}')

            self._eventEngine.sendEvent(EventType.InsertProject, projectFilename=filename)
        else:
            PyutUtils.displayError("No project to insert this file into !")

    # noinspection PyUnusedLocal
    def onFileOpen(self, event: CommandEvent):
        """
        Open a diagram

        Args:
            event:
        """
        fileNames: FileNames = self._askForFilesToLoad()
        if len(fileNames) > 0:
            self.loadFile(fileNames)

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
    def onDeleteDiagram(self, event: CommandEvent):
        """
        Remove the current document from the current project
        Args:
            event:
        """
        self._eventEngine.sendEvent(EventType.DeleteDiagram)

    def onImport(self, event: CommandEvent):
        """
        TODO: Re-enable plugins with PyutPluginCore
        """

    def onExport(self, event: CommandEvent):
        """
        TODO: Re-enable plugins with PyutPluginCore
        """

    # noinspection PyUnusedLocal
    def onPyutPreferences(self, event: CommandEvent):

        self.logger.debug(f"Before dialog show")

        with DlgPyutPreferences(self._parent, ID_ANY) as dlg:
            if dlg.ShowModal() == ID_OK:
                self.logger.debug(f'Waiting for answer')
            else:
                self.logger.debug(f'Cancelled')

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

        # self._mediator.deselectAllShapes()
        frame = self._mediator.activeUmlFrame
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
        # self._mediator.deselectAllShapes()
        printDialogData: PrintDialogData = PrintDialogData()

        printDialogData.SetPrintData(self._printData)
        printDialogData.SetMinPage(1)
        printDialogData.SetMaxPage(1)
        printer  = Printer(printDialogData)
        printout = PyutPrintout(self._mediator.activeUmlFrame)

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
                    lst:      List[str] = self._preferences.getLastOpenedFilesList()
                    fileName: str = lst[index]
                    self.loadFile(FileNames(FileNames([fileName])))
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

    def loadFile(self, fileNames: FileNames):
        """
        Load the specified filename;  This is externally available so that
        we can open a file from the command line

        Args:
            fileNames: A list of files to load
        """
        for fileName in fileNames:
            self._eventEngine.sendEvent(EventType.OpenProject, projectFilename=fileName)

    def _askForFilesToLoad(self) -> FileNames:
        """
        Ask for the files to load.

        Returns:    The list will be empty if the user cancelled the request
        """
        currentDir: str       = self._mediator.getCurrentDir()

        dlg = FileDialog(self._parent, _("Choose a file"), currentDir, "", "*.put", FD_OPEN | FD_MULTIPLE)
        fileNames: FileNames = FileNames([])
        if dlg.ShowModal() == ID_OK:
            fileNames = dlg.GetPaths()
            self._currentDirectoryHandler.currentDirectory = fileNames[0]

        dlg.Destroy()
        return fileNames

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

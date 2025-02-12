
from typing import List
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

from pyutplugins.PluginManager import PluginDetails
from wx import BOTH
from wx import FD_MULTIPLE
from wx import FD_OPEN
from wx import FileHistory
from wx import ID_FILE1
from wx import ID_OK
from wx import PAPER_A4
from wx import PORTRAIT
from wx import PRINTER_ERROR
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

from pyutplugins.PluginManager import PluginManager

from pyutplugins.plugintypes.PluginDataTypes import PluginIDMap

from pyut.PyutUtils import PyutUtils
from pyut.ui.dialogs.DlgEditProjectHistory import DlgEditProjectHistory
from pyut.ui.dialogs.preferences.DlgPyutPreferences import DlgPyutPreferences

from pyut.enums.DiagramType import DiagramType

from pyut.general.exceptions.UnsupportedOperation import UnsupportedOperation

from pyut.preferences.PyutPreferences import PyutPreferences

from pyut.ui.CurrentDirectoryHandler import CurrentDirectoryHandler
from pyut.ui.PyutPrintout import PyutPrintout

from pyut.ui.menuhandlers.BaseMenuHandler import BaseMenuHandler

from pyut.ui.umlframes.UmlClassDiagramsFrame import UmlClassDiagramsFrame

from pyut.ui.eventengine.eventinformation.ActiveProjectInformation import ActiveProjectInformation

from pyut.ui.eventengine.EventType import EventType

from pyut.ui.eventengine.IEventEngine import IEventEngine

FileNames = NewType('FileNames', List[str])


class FileMenuHandler(BaseMenuHandler):

    def __init__(self, fileMenu: Menu, eventEngine: IEventEngine, pluginManager: PluginManager):
        """

        Args:
            fileMenu:       The file menu
            eventEngine:    The event engine
            pluginManager:  Plugin manager to get IDs from
        """
        super().__init__(menu=fileMenu, eventEngine=eventEngine)

        self._pluginManager: PluginManager = pluginManager
        self._fileHistory:   FileHistory   = cast(FileHistory, None)    # Must be injected

        self.logger:       Logger          = getLogger(__name__)
        self._preferences: PyutPreferences = PyutPreferences()
        self._plugins:     PluginIDMap     = PluginIDMap({})

        self._exportPlugins: PluginIDMap   = cast(PluginIDMap, None)
        self._importPlugins: PluginIDMap   = cast(PluginIDMap, None)

        self._currentDirectoryHandler: CurrentDirectoryHandler = CurrentDirectoryHandler()
        self._printData:               PrintData               = cast(PrintData, None)

        self._initPrinting()    # Printing data

    @property
    def exportPlugins(self) -> PluginIDMap:
        raise UnsupportedOperation('Property is write only')

    @exportPlugins.setter
    def exportPlugins(self, exportPlugins: PluginIDMap):
        self._exportPlugins = exportPlugins

    @property
    def importPlugins(self) -> PluginIDMap:
        raise UnsupportedOperation('Property is write only')

    @importPlugins.setter
    def importPlugins(self, importPlugins: PluginIDMap):
        self._importPlugins = importPlugins

    def _setFileHistory(self, fileHistory: FileHistory):
        self._fileHistory = fileHistory

    # noinspection PyTypeChecker
    fileHistory = property(fget=None, fset=_setFileHistory)

    def loadFiles(self, fileNames: FileNames):
        """
        Load the specified filenames;  This is public so that
        we can open a files from the command line

        Args:
            fileNames: A list of files to load
        """
        for fileName in fileNames:
            self._eventEngine.sendEvent(EventType.OpenProject, projectFilename=fileName)

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
            self.loadFiles(fileNames)

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
        """
        wxId:          int           = event.GetId()
        pluginDetails: PluginDetails = self._pluginManager.doImport(wxId=wxId)

        self.logger.info(f'Import {pluginDetails=}')

    def onExport(self, event: CommandEvent):
        """
        """
        wxId:          int           = event.GetId()
        pluginDetails: PluginDetails = self._pluginManager.doExport(wxId=wxId)
        self.logger.info(f'Export    {pluginDetails=}')

    # noinspection PyUnusedLocal
    def onPyutPreferences(self, event: CommandEvent):

        with DlgPyutPreferences(self._parent, eventEngine=self._eventEngine) as dlg:
            if dlg.ShowModal() == ID_OK:
                self.logger.info(f'Got answer')
            else:
                self.logger.info(f'Cancelled')

    # noinspection PyUnusedLocal
    def onPrintSetup(self, event: CommandEvent):
        """
        Display the print setup dialog

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
        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._doPrintPreview)

    # noinspection PyUnusedLocal
    def onPrint(self, event: CommandEvent):
        """
        Print the current diagram

        Args:
            event:
        """
        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._doPrint)

    def onExit(self, event: CommandEvent):
        """
        Exit the program

        Args:
            event:
        """
        closeEvent: CloseEvent = CloseEvent(EVT_CLOSE.typeId)

        parent: Window = event.GetEventObject().GetWindow()
        wxPostEvent(parent, closeEvent)

    def onOpenRecent(self, event: CommandEvent):
        """
        Opens the selected 'recently' opened file
        Args:
            event:
        """
        fileNum: int = event.GetId() - ID_FILE1
        path:    str = self._fileHistory.GetHistoryFile(fileNum)

        self.logger.info(f'{event=} - filename: {path}')
        self.loadFiles(fileNames=FileNames([path]))

    # noinspection PyUnusedLocal
    def onManageFileHistory(self, event: CommandEvent):
        with DlgEditProjectHistory(parent=None, fileHistory=self._fileHistory) as dlg:
            dlg.ShowModal()

    def _doPrintPreview(self, diagramFrame: UmlClassDiagramsFrame):

        self._eventEngine.sendEvent(EventType.DeSelectAllShapes)
        wxYield()

        parent: Window = self._parent

        if diagramFrame is None:
            PyutUtils.displayError("No frame to print", "Keyboard to Computer Interface Error")
            return

        printout  = PyutPrintout(diagramFrame)
        printout2 = PyutPrintout(diagramFrame)
        preview   = PrintPreview(printout, printout2, self._printData)

        if not preview.IsOk():
            PyutUtils.displayError("Unknown Preview Error", "Error")
            return

        previewFrame: PreviewFrame = PreviewFrame(preview, parent, "Diagram preview")
        previewFrame.Initialize()
        previewFrame.Centre(BOTH)

        try:
            previewFrame.Show(True)
        except (ValueError, Exception) as e:
            PyutUtils.displayError(f"Preview error {e}", "Error")

    def _doPrint(self, diagramFrame: UmlClassDiagramsFrame):

        if diagramFrame is None:
            PyutUtils.displayError("No diagram to print !", "Error")
            return

        self._eventEngine.sendEvent(EventType.DeSelectAllShapes)
        wxYield()
        printDialogData: PrintDialogData = PrintDialogData()

        printDialogData.SetPrintData(self._printData)
        printDialogData.SetMinPage(1)
        printDialogData.SetMaxPage(1)
        printer  = Printer(printDialogData)
        printout = PyutPrintout(diagramFrame)

        if not printer.Print(self._parent, printout, True):
            # May have been canceled
            if Printer.GetLastError() == PRINTER_ERROR:
                PyutUtils.displayError("Cannot print", "Error")

    def _askForFilesToLoad(self) -> FileNames:
        """
        Ask for the files to load.

        Returns:    The list will be empty if the user canceled the request
        """
        currentDir: str = CurrentDirectoryHandler().currentDirectory

        dlg = FileDialog(self._parent, "Choose a file", currentDir, "", "*.put", FD_OPEN | FD_MULTIPLE)
        fileNames: FileNames = FileNames([])
        if dlg.ShowModal() == ID_OK:
            fileNames = dlg.GetPaths()
            self._currentDirectoryHandler.currentDirectory = fileNames[0]

        dlg.Destroy()
        return fileNames

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

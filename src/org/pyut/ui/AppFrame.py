
from typing import cast

from typing import List

from logging import Logger
from logging import getLogger

from os import sep as osSeparator
from os import getcwd

from copy import copy

from urllib import request

from pkg_resources import resource_filename

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
from wx import FD_SAVE
from wx import FD_MULTIPLE
from wx import FD_OVERWRITE_PROMPT

from wx import PrintData

from wx import AcceleratorEntry
from wx import CommandEvent
from wx import Frame
from wx import DefaultPosition
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

from wx import Yield as wxYield

from org.pyut.ogl.OglActor import OglActor
from org.pyut.ogl.OglClass import OglClass
from org.pyut.ogl.OglNote import OglNote
from org.pyut.ogl.OglUseCase import OglUseCase

from org.pyut.PyutProject import PyutProject
from org.pyut.PyutActor import PyutActor
from org.pyut.PyutClass import PyutClass
from org.pyut.PyutNote import PyutNote
from org.pyut.PyutUseCase import PyutUseCase
from org.pyut.PyutUtils import PyutUtils

from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame
from org.pyut.ui.PyutPrintout import PyutPrintout
from org.pyut.ui.TipsFrame import TipsFrame

from org.pyut.ui.tools.MenuCreator import MenuCreator
from org.pyut.ui.tools.SharedTypes import SharedTypes

from org.pyut.ui.tools.ToolsCreator import ToolsCreator
from org.pyut.ui.tools.ActionCallbackType import ActionCallbackType
from org.pyut.ui.tools.SharedIdentifiers import SharedIdentifiers

from org.pyut.PyutPreferences import PyutPreferences

from org.pyut.enums.DiagramType import DiagramType

from org.pyut.persistence.FileHandling import FileHandling

from org.pyut.plugins.PluginManager import PluginManager

from org.pyut.general.Mediator import ACTION_NEW_SD_MESSAGE
from org.pyut.general.Mediator import ACTION_NEW_SD_INSTANCE
from org.pyut.general.Mediator import getMediator
from org.pyut.general.Globals import _
from org.pyut.general.Globals import IMG_PKG


class AppFrame(Frame):
    """
    AppFrame : main pyut frame; contain menus, statusbar, UMLframe, ...

    Instantiated by PyutApp.py
    Use it as a normal Frame ::
        dlg=AppFrame(self, -1, "Pyut")
        dlg.Show()
        dlg.Destroy()

    :author: C.Dutoit
    :contact: dutoitc@hotmail.com
    :version: $Revision: 1.55 $
    """

    def __init__(self, parent, ID, title):
        """
        Constructor.

        @param wxWindow parent : parent window
        @param int ID : wx ID of this frame
        @param String title : Title to display
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        super().__init__(parent, ID, title, DefaultPosition, Size(960, 480), DEFAULT_FRAME_STYLE | FRAME_EX_METAL)

        self.logger: Logger = getLogger(__name__)
        # Create the application's icon
        fileName: str  = resource_filename(IMG_PKG, 'pyut.ico')
        icon:     Icon = Icon(fileName, BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        self.Center(BOTH)                     # Center on the screen
        self.CreateStatusBar()

        # Properties
        self.plugMgr:     PluginManager            = PluginManager()
        self.plugins:     SharedTypes.PluginMap    = cast(SharedTypes.PluginMap, {})     # To store the plugins
        self._toolboxIds: SharedTypes.ToolboxIdMap = cast(SharedTypes.ToolboxIdMap, {})  # Association toolbox id -> category
        self.mnuFile:     Menu            = cast(Menu, None)
        self._prefs:      PyutPreferences = PyutPreferences()
        self._clipboard = []
        self._currentDirectory = getcwd()

        self._lastDir = self._prefs["LastDirectory"]
        if self._lastDir is None:  # Assert that the path is present
            self._lastDir = getcwd()

        self._ctrl = getMediator()
        self._ctrl.registerStatusBar(self.GetStatusBar())
        self._ctrl.resetStatusText()
        self._ctrl.registerAppFrame(self)

        # Last opened Files IDs
        self.lastOpenedFilesID = []
        for index in range(self._prefs.getNbLOF()):
            self.lastOpenedFilesID.append(PyutUtils.assignID(1)[0])

        # loaded files handler
        self._fileHandling = FileHandling(self, self._ctrl)
        self._ctrl.registerFileHandling(self._fileHandling)

        # Initialization
        self._initPyutTools()   # Toolboxes, toolbar
        self._initMenu()        # Menu
        self._initPrinting()    # Printing data

        # Accelerators init. (=Keyboards shortcuts)
        acc = self._createAcceleratorTable()
        accel_table = AcceleratorTable(acc)
        self.SetAcceleratorTable(accel_table)

        self._ctrl.registerAppPath(self._currentDirectory)

        # set application title
        self._fileHandling.newProject()
        self._ctrl.updateTitle()

        # Init tips frame
        self._alreadyDisplayedTipsFrame = False
        self.Bind(EVT_ACTIVATE, self._onActivate)

    def updateCurrentDir(self, fullPath):
        """
        Set current working directory.

        @param String fullPath : Full path, with filename

        @author P. Waelti <pwaelti@eivd.ch>
        @since 1.50
        """
        self._lastDir = fullPath[:fullPath.rindex(osSeparator)]

        # Save last directory
        self._prefs["LastDirectory"] = self._lastDir

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
        self._ctrl.updateTitle()

    def Close(self, force=False):
        """
        Closing handler overload. Save files and ask for confirmation.

        @since 1.4
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        # Close all files
        if self._fileHandling.onClose() is False:
            return

        self._clipboard = None
        self._fileHandling = None
        self._ctrl = None
        self._prefs = None
        self.plugMgr = None
        self._printData.Destroy()
        # TODO? wx.OGLCleanUp()
        self.Destroy()

    def OnImport(self, event):
        self._fileHandling.newProject()
        self._fileHandling.newDocument(DiagramType.CLASS_DIAGRAM)
        self._ctrl.updateTitle()
        cl = self.plugins[event.GetId()]

        obj = cl(self._ctrl.getUmlObjects(), self._ctrl.getUmlFrame())

        # Do plugin functionality
        BeginBusyCursor()
        try:
            wxYield()  # time to process the refresh in newDiagram
            obj.doImport()
        except (ValueError, Exception) as e:
            PyutUtils.displayError(_("An error occured while executing the selected plugin"), _("Error..."), self)
            self.logger.error(f'{e}')

        EndBusyCursor()
        self.Refresh()

    def OnExport(self, event):
        """
        Callback.

        Args:
            event: wxEvent event

        @author L. Burgbacher <lb@alawa.ch>
        @since 1.26
        """
        # Create a plugin instance
        cl = self.plugins[event.GetId()]
        umlObjs: List[OglClass]         = self._ctrl.getUmlObjects()
        umlFrame: UmlClassDiagramsFrame = self._ctrl.getUmlFrame()
        obj = cl(umlObjs, umlFrame)
        # Do plugin functionality
        BeginBusyCursor()
        obj.doExport()
        EndBusyCursor()

    def OnToolPlugin(self, event):
        # Create a plugin instance
        cl = self.plugins[event.GetId()]
        obj = cl(self._ctrl.getUmlObjects(), self._ctrl.getUmlFrame())

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
        umlFrame = self._ctrl.getUmlFrame()
        if umlFrame is not None:
            umlFrame.Refresh()

    def OnToolboxMenuClick(self, event):
        self._ctrl.displayToolbox(self._toolboxIds[event.GetId()])

    def printDiagramToPostscript(self, filename):
        """
        print the current diagram to postscript

        @return True if succeeded
        @author C.Dutoit
        """
        # Verify that we do have a diagram to save
        if self._ctrl.getDiagram() is None:
            PyutUtils.displayError(_("No diagram to print !"), parent=self)
            self._ctrl.setStatusText(_("Error while printing to postscript"))
            return False

        # Init
        # printout = None
        # printer  = None
        try:
            self._ctrl.deselectAllShapes()
            datas = PrintDialogData()
            datas.SetPrintData(self._printData)
            datas.SetPrintToFile(True)
            datas.SetMinPage(1)
            datas.SetMaxPage(1)
            printDatas = datas.GetPrintData()
            printDatas.SetFilename(filename)
            printDatas.SetQuality(PRINT_QUALITY_HIGH)
            datas.SetPrintData(printDatas)
            printer  = Printer(datas)
            printout = PyutPrintout(self._ctrl.getUmlFrame())
        except (ValueError, Exception) as e:
            PyutUtils.displayError(_("Cannot export to Postscript"), parent=self)
            self._ctrl.setStatusText(_(f"Error while printing to postscript {e}"))
            return False

        # Print to postscript
        if not printer.Print(self, printout, False):
            PyutUtils.displayError(_("Cannot print"), parent=self)
            self._ctrl.setStatusText(_("Error while printing to postscript"))
            return False

        # Return
        self._ctrl.setStatusText(_("Printed to postscript"))
        return True

    def _onActivate(self, event):
        """
        EVT_ACTIVATE Callback; display tips frame.  But onlhy, the first activate
        """
        self.logger.debug(f'_onActivate event: {event}')
        try:
            if self._alreadyDisplayedTipsFrame is True or self._prefs is False:
                return
            # Display tips frame
            self._alreadyDisplayedTipsFrame = True
            prefs: PyutPreferences = PyutPreferences()
            self.logger.debug(f'Show tips on startup: {self._prefs.showTipsOnStartup()}')
            if prefs.showTipsOnStartup() is True:
                # noinspection PyUnusedLocal
                tipsFrame = TipsFrame(self)
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
            ActionCallbackType.NEW_PROJECT:          self._OnMnuFileNewProject,
            ActionCallbackType.NEW_CLASS_DIAGRAM:    self._OnMnuFileNewClassDiagram,
            ActionCallbackType.NEW_SEQUENCE_DIAGRAM: self._OnMnuFileNewSequenceDiagram,
            ActionCallbackType.NEW_USE_CASE_DIAGRAM: self._OnMnuFileNewUsecaseDiagram,
            ActionCallbackType.INSERT_PROJECT:       self._OnMnuFileInsertProject,
            ActionCallbackType.PROJECT_CLOSE:        self._OnMnuFileClose,
            ActionCallbackType.FILE_OPEN:            self._OnMnuFileOpen,
            ActionCallbackType.FILE_SAVE:            self._OnMnuFileSave,
            ActionCallbackType.FILE_SAVE_AS:         self._OnMnuFileSaveAs,
            ActionCallbackType.REMOVE_DOCUMENT:      self._OnMnuFileRemoveDocument,
            ActionCallbackType.PRINT_SETUP:          self._OnMnuFilePrintSetup,
            ActionCallbackType.PRINT_PREVIEW:        self._OnMnuFilePrintPreview,
            ActionCallbackType.PRINT:                self._OnMnuFilePrint,
            ActionCallbackType.PYUT_PROPERTIES:      self._OnMnuFilePyutProperties,
            ActionCallbackType.EXIT_PROGRAM:         self._OnMnuFileExit,
            ActionCallbackType.PROGRAM_ABOUT:        self._OnMnuHelpAbout,
            ActionCallbackType.HELP_INDEX:           self._OnMnuHelpIndex,
            ActionCallbackType.HELP_VERSION:         self._OnMnuHelpVersion,
            ActionCallbackType.HELP_WEB:             self._OnMnuHelpWeb,
            ActionCallbackType.ADD_PYUT_HIERARCHY:   self._OnMnuAddPyut,
            ActionCallbackType.ADD_OGL_HIERARCHY:    self._OnMnuAddOgl,
            ActionCallbackType.EXPORT_PNG:           self._OnMnuFileExportPng,
            ActionCallbackType.EXPORT_JPG:           self._OnMnuFileExportJpg,
            ActionCallbackType.EXPORT_BMP:           self._OnMnuFileExportBmp,
            ActionCallbackType.EXPORT_PS:            self._OnMnuFileExportPs,
            ActionCallbackType.EXPORT_PDF:           self._OnMnuFileExportPDF,

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
        self.plugins       = self._menuCreator.plugins
        self._toolboxIds = self._menuCreator.toolboxIds
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
            (ACCEL_CTRL,     ord('l'),   SharedIdentifiers.ID_MNUFILENEWCLASSDIAGRAM),
            (ACCEL_CTRL,     ord('E'),   SharedIdentifiers.ID_MNUFILENEWSEQUENCEDIAGRAM),
            (ACCEL_CTRL,     ord('e'),   SharedIdentifiers.ID_MNUFILENEWSEQUENCEDIAGRAM),
            (ACCEL_CTRL,     ord('U'),   SharedIdentifiers.ID_MNUFILENEWUSECASEDIAGRAM),
            (ACCEL_CTRL,     ord('u'),   SharedIdentifiers.ID_MNUFILENEWUSECASEDIAGRAM),
            (ACCEL_CTRL,     ord('o'),   SharedIdentifiers.ID_MNUFILEOPEN),
            (ACCEL_CTRL,     ord('O'),   SharedIdentifiers.ID_MNUFILEOPEN),
            (ACCEL_CTRL,     ord('s'),   SharedIdentifiers.ID_MNUFILESAVE),
            (ACCEL_CTRL,     ord('S'),   SharedIdentifiers.ID_MNUFILESAVE),
            (ACCEL_CTRL,     ord('a'),   SharedIdentifiers.ID_MNUFILESAVEAS),
            (ACCEL_CTRL,     ord('A'),   SharedIdentifiers.ID_MNUFILESAVEAS),
            (ACCEL_CTRL,     ord('p'),   SharedIdentifiers.ID_MNUFILEPRINT),
            (ACCEL_CTRL,     ord('P'),   SharedIdentifiers.ID_MNUFILEPRINT),
            (ACCEL_CTRL,     ord('x'),   SharedIdentifiers.ID_MNUEDITCUT),
            (ACCEL_CTRL,     ord('X'),   SharedIdentifiers.ID_MNUEDITCUT),
            (ACCEL_CTRL,     ord('c'),   SharedIdentifiers.ID_MNUEDITCOPY),
            (ACCEL_CTRL,     ord('C'),   SharedIdentifiers.ID_MNUEDITCOPY),
            (ACCEL_CTRL,     ord('v'),   SharedIdentifiers.ID_MNUEDITPASTE),
            (ACCEL_CTRL,     ord('V'),   SharedIdentifiers.ID_MNUEDITPASTE),
            (ACCEL_CTRL,     ord('d'),   SharedIdentifiers.ID_DEBUG),
            (ACCEL_CTRL,     ord('D'),   SharedIdentifiers.ID_DEBUG),
            ]
        acc = []
        for el in lst:
            (el1, el2, el3) = el
            acc.append(AcceleratorEntry(el1, el2, el3))
        return acc

    def _initPrinting(self):
        """
        printing data initialization

        @author C.Dutoit
        """
        self._printData = PrintData()
        self._printData.SetPaperId(PAPER_A4)
        self._printData.SetQuality(PRINT_QUALITY_HIGH)
        self._printData.SetOrientation(PORTRAIT)
        self._printData.SetNoCopies(1)
        self._printData.SetCollate(True)

    # noinspection PyUnusedLocal
    def _OnMnuFileNewProject(self, event):
        """
        begin a new project

        @author C.Dutoit
        """
        self._fileHandling.newProject()
        self._ctrl.updateTitle()

    # noinspection PyUnusedLocal
    def _OnMnuFileNewClassDiagram(self, event):
        """
        begin a new class diagram

        @author C.Dutoit
        """
        self._fileHandling.newDocument(DiagramType.CLASS_DIAGRAM)
        self._ctrl.updateTitle()

    # noinspection PyUnusedLocal
    def _OnMnuFileNewSequenceDiagram(self, event):
        """
        begin a new sequence diagram

        @author C.Dutoit
        """
        self._fileHandling.newDocument(DiagramType.SEQUENCE_DIAGRAM)
        self._ctrl.updateTitle()

    # noinspection PyUnusedLocal
    def _OnMnuFileNewUsecaseDiagram(self, event):
        """
        begin a new use-case diagram

        @author C.Dutoit
        """
        self._fileHandling.newDocument(DiagramType.USECASE_DIAGRAM)
        self._ctrl.updateTitle()

    # noinspection PyUnusedLocal
    def _OnMnuFileInsertProject(self, event):
        """
        Insert a project into this one

        @author C.Dutoit
        """
        PyutUtils.displayWarning(_("The project insert is experimental, "
                                   "use it at your own risk.\n"
                                   "You risk a shapes ID duplicate with "
                                   "unexpected results !"), parent=self)

        if (self._fileHandling.getCurrentProject()) is None:
            PyutUtils.displayError(_("No project to insert this file into !"), parent=self)
            return

        # Ask which project to insert
        dlg = FileDialog(self, _("Choose a file"), self._lastDir, "", "*.put", FD_OPEN)
        if dlg.ShowModal() != ID_OK:
            dlg.Destroy()
            return False
        self.updateCurrentDir(dlg.GetPath())
        filename = dlg.GetPath()
        dlg.Destroy()

        print(("inserting file", str(filename)))

        # Insert the specified files
        try:
            self._fileHandling.insertFile(filename)
        except (ValueError, Exception) as e:
            PyutUtils.displayError(_(f"An error occurred while loading the project!  {e}"), parent=self)

    # noinspection PyUnusedLocal
    def _OnMnuFileOpen(self, event):
        """
        Open a diagram

        @author C.Dutoit
        """
        self._loadFile()

    # noinspection PyUnusedLocal
    def _OnMnuFileSave(self, event):
        """
        Save the current diagram to a file

        @since 1.4
        @author C.Dutoit < dutoitc@hotmail.com>
        """
        self._saveFile()

    # noinspection PyUnusedLocal
    def _OnMnuFileSaveAs(self, event):
        """
        Ask and save the current diagram to a file

        @since 1.4
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._saveFileAs()

    # noinspection PyUnusedLocal
    def _OnMnuFileClose(self, event):
        """
        Close the current file

        @since 1.4
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._fileHandling.closeCurrentProject()

    # noinspection PyUnusedLocal
    def _OnMnuFileRemoveDocument(self, event):
        """
        Remove the current document from the current project

        @author C.Dutoit
        """
        project  = self._fileHandling.getCurrentProject()
        document = self._fileHandling.getCurrentDocument()
        if project is not None and document is not None:
            project.removeDocument(document)
        else:
            PyutUtils.displayWarning(_("No document to remove"))

    # noinspection PyUnusedLocal
    def _OnMnuFileExportBmp(self, event):
        """
        Display the Export to bitmap dialog box

        @since 1.23
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._fileHandling.exportToBmp(-1)

    # noinspection PyUnusedLocal
    def _OnMnuFileExportJpg(self, event):
        """
        Display the Export to jpeg dialog box

        @since 1.23
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._fileHandling.exportToJpg(-1)

    # noinspection PyUnusedLocal
    def _OnMnuFileExportPng(self):
        """
        Display the Export to png dialog box

        @since 1.23
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._fileHandling.exportToPng(-1)

    # noinspection PyUnusedLocal
    def _OnMnuFileExportPs(self, event):
        """
        Display the Export to postscript dialog box

        @since 1.23
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        # Choose filename
        # filename = ""
        try:
            dlg = FileDialog(self, _("Save as Postscript"), self._lastDir, "", "*.ps", FD_SAVE)
            if dlg.ShowModal() != ID_OK:
                dlg.Destroy()
                return False
            filename = dlg.GetPath()
            if len(filename) < 3 or filename[-3:] != ".ps":
                filename += ".ps"
            dlg.Destroy()
        except (ValueError, Exception) as e:
            PyutUtils.displayError(_("Error while displaying Postscript saving dialog"), parent=self)
            return

        # export to PDF
        self.printDiagramToPostscript(filename)

    # noinspection PyUnusedLocal
    def _OnMnuFileExportPDF(self, event):
        """
        Display the Export to pdf dialog box

        @author C.Dutoit
        """
        # Choose filename
        filename = ""
        try:
            dlg = FileDialog(self, _("Save as PDF"), self._lastDir, "", "*.pdf", FD_SAVE | FD_OVERWRITE_PROMPT)
            if dlg.ShowModal() != ID_OK:
                dlg.Destroy()
                return False
            filename = dlg.GetPath()
            if len(filename) < 4 or filename[-4:] != ".pdf":
                filename += ".pdf"
            dlg.Destroy()
        except (ValueError, Exception) as e:
            PyutUtils.displayError(_("Error while displaying pdf saving dialog"), parent=self)
            self._ctrl.setStatusText(_("Can't export to pdf"))
            return

        # export to PDF
        # TODO -- externalize this command
        if self.printDiagramToPostscript("/tmp/pdfexport.ps"):
            # Convert file to pdf
            import os
            # noinspection PyUnusedLocal
            try:
                if os.system("ps2epsi /tmp/pdfexport.ps /tmp/pdfexport.eps") != 0:
                    PyutUtils.displayError(_("Can't execute ps2epsi !"), parent=self)
                    return
                if os.system("epstopdf /tmp/pdfexport.eps --outfile=" + filename) != 0:
                    PyutUtils.displayError(_("Can't execute ps2epsi !"), parent=self)
                    return
                self._ctrl.setStatusText(_("Exported to pdf"))
            except (ValueError, Exception) as e:
                PyutUtils.displayError("Can't export to pdf !", parent=self)

    # noinspection PyUnusedLocal
    def _OnMnuFilePrintSetup(self, event):
        """
        Display the print setup dialog box

        @since 1.10
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        dlg = PrintDialog(self)
        dlg.GetPrintDialogData().SetSetupDialog(True)
        dlg.GetPrintDialogData().SetPrintData(self._printData)
        dlg.ShowModal()
        self._printData = dlg.GetPrintDialogData().GetPrintData()
        dlg.Destroy()

    # noinspection PyUnusedLocal
    def _OnMnuFilePrintPreview(self, event):
        """
        Display the print preview frame; Preview before printing.
        """
        self._ctrl.deselectAllShapes()
        frame = self._ctrl.getUmlFrame()
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
    def _OnMnuFilePrint(self, event):
        """
        Print the current diagram

        @since 1.10
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        if self._ctrl.getDiagram() is None:
            PyutUtils.displayError(_("No diagram to print !"), _("Error"), self)
            return
        self._ctrl.deselectAllShapes()
        datas = PrintDialogData()
        datas.SetPrintData(self._printData)
        datas.SetMinPage(1)
        datas.SetMaxPage(1)
        printer  = Printer(datas)
        printout = PyutPrintout(self._ctrl.getUmlFrame())

        if not printer.Print(self, printout, True):
            PyutUtils.displayError(_("Cannot print"), _("Error"), self)

    def _OnMnuLOF(self, event):
        """
        Open a file from the last opened files list

        @since 1.43
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        for index in range(self._prefs.getNbLOF()):
            if event.GetId() == self.lastOpenedFilesID[index]:
                try:
                    lst = self._prefs.getLastOpenedFilesList()
                    self._loadFile(lst[index])
                    self._prefs.addNewLastOpenedFilesEntry(lst[index])
                    self._setLastOpenedFilesItems()
                except (ValueError, Exception) as e:
                    self.logger.error(f'{e}')

    # noinspection PyUnusedLocal
    def _OnMnuFileExit(self, event):
        """
        Exit the program

        @since 1.4
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self.Close()

    # noinspection PyUnusedLocal
    def _OnMnuHelpAbout(self, event):
        """
        Show the about box

        @since 1.4
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        from org.pyut.dialogs.DlgAbout import DlgAbout
        from org.pyut.general.PyutVersion import PyutVersion
        dlg = DlgAbout(self, ID_ANY, _("About PyUt ") + PyutVersion.getPyUtVersion())
        dlg.ShowModal()
        dlg.Destroy()

    # noinspection PyUnusedLocal
    def _OnMnuHelpIndex(self, event):
        """
        Display the help index

        @since 1.9
        @author C.Dutoit <dutoitc@hotmail.com>
        """

        from org.pyut.dialogs import DlgHelp
        dlgHelp = DlgHelp.DlgHelp(self, -1, _("Pyut Help"))
        dlgHelp.Show(True)

    # noinspection PyUnusedLocal
    def _OnMnuHelpVersion(self, event):
        """
        Check for newer version.

        @since 1.49.2.28
        @author C.Dutoit <dutoitc@hotmail.com>
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
    def _OnMnuHelpWeb(self, event):
        """
        Launch PyUt web site

        @since 1.9
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        PyutUtils.displayInformation(_("Please point your browser at http://pyut.sf.net"), _("Pyut''s web site"), self)

    # noinspection PyUnusedLocal
    def _OnMnuAddPyut(self, event: CommandEvent):
        """
        Add Pyut UML Diagram.
        """
        frame: UmlClassDiagramsFrame = self._ctrl.getUmlFrame()
        if self._isDiagramFromOpen(frame) is True:
            frame.addPyutHierarchy()
            self._refreshUI(frame)

    # noinspection PyUnusedLocal
    def _OnMnuAddOgl(self, event: CommandEvent):
        """
        Add Pyut-Ogl UML Diagram.
        """
        frame: UmlClassDiagramsFrame = self._ctrl.getUmlFrame()
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

        project: PyutProject = self._fileHandling.getCurrentProject()
        project.setModified(True)
        self._ctrl.updateTitle()
        frame.Refresh()

    def loadByFilename(self, filename):
        """
        load the specified filename
        called by pyutApp.py
        This is a simple indirection to __loadFile. No direct call because
        it seems to be more logical to let loadFile private.
        pyutApp do not need to know the correct name of the __loadFile method.
        @since 1.31
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._loadFile(filename)

    def _loadFile(self, filename=""):
        """
        load the specified filename
        called by PyutFileDropTarget.py

        @since 1.4
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        # Make a list to be compatible with multi-files loading
        filenames = [filename]

        # Ask which filename to load ?
        if filename == "":
            dlg = FileDialog(self, _("Choose a file"), self._lastDir, "", "*.put", FD_OPEN | FD_MULTIPLE)

            if dlg.ShowModal() != ID_OK:
                dlg.Destroy()
                return False
            self.updateCurrentDir(dlg.GetPath())
            filenames = dlg.GetPaths()
            dlg.Destroy()

        print(f"loading file(s) {str(filename)}")

        # Open the specified files
        for filename in filenames:
            try:
                if self._fileHandling.openFile(filename):
                    # Add to last opened files list
                    self._prefs.addNewLastOpenedFilesEntry(filename)
                    self._setLastOpenedFilesItems()
                    self._ctrl.updateTitle()
            except (ValueError, Exception) as e:
                PyutUtils.displayError(_("An error occurred while loading the project !"), parent=self)
                self.logger.error(f'{e}')

    def _saveFile(self):
        """
        save to the current filename

        @since 1.9
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._fileHandling.saveFile()
        self._ctrl.updateTitle()

        # Add to last opened files list
        # diag=self._ctrl.getUmlFrame()
        project = self._fileHandling.getCurrentProject()
        if project is not None:
            self._prefs.addNewLastOpenedFilesEntry(project.getFilename())
            self._setLastOpenedFilesItems()

    def _saveFileAs(self):
        """
        save to the current filename; Ask for the name

        @since 1.9
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._fileHandling.saveFileAs()
        self._ctrl.updateTitle()

        project = self._fileHandling.getCurrentProject()
        if project is not None:
            self._prefs.addNewLastOpenedFilesEntry(project.getFilename())
            self._setLastOpenedFilesItems()

    def _setLastOpenedFilesItems(self):
        """
        Set the menu last opened files items

        @since 1.43
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self.logger.info(f'self.mnuFile: {self.mnuFile}')

        index = 0
        for el in self._prefs.getLastOpenedFilesList():
            openFilesId = self.lastOpenedFilesID[index]
            # self.mnuFile.SetLabel(id=openFilesId, label="&" + str(index+1) + " " + el)
            lbl: str = f"&{str(index+1)} {el}"
            self.logger.info(f'lbL: {lbl}  openFilesId: {openFilesId}')
            self.mnuFile.SetLabel(id=openFilesId, label=lbl)

            index += 1

    def _OnNewAction(self, event):
        """
        Call the mediator to specifiy the current action.

        Args:
            event:
        """
        self.logger.info(f'SD Instance: `{ACTION_NEW_SD_INSTANCE}`, SD Message: `{ACTION_NEW_SD_MESSAGE}`')
        currentAction: int = SharedIdentifiers.ACTIONS[event.GetId()]
        self._ctrl.setCurrentAction(currentAction)
        self._ctrl.selectTool(event.GetId())
        self._fileHandling.setModified(True)
        self._ctrl.updateTitle()

    # noinspection PyUnusedLocal
    def _OnMnuEditCut(self, event):
        self.cutSelectedShapes()

    def cutSelectedShapes(self):
        """
        Cut all current shapes

        @author C.Dutoit from lb code (splitted)
        """
        selected = self._ctrl.getSelectedShapes()
        if len(selected) > 0:
            self._clipboard = []
        else:
            return

        canvas = selected[0].GetDiagram().GetPanel()
        # the canvas which contain the shape
        # specify the canvas on which we will paint
        # dc = wxClientDC(canvas)
        # canvas.PrepareDC(dc)
        # diagram = self._ctrl.getDiagram()

        # put the PyutObjects in the clipboard and remove them from the diagram
        for obj in selected:
            # remove the links
            # for each link
            # for link in obj.getLinks()[:]:
            # self._ctrl.removeLink(link)
            obj.Detach()

        for obj in selected:
            self._clipboard.append(obj.getPyutObject())
            # self._ctrl.removeClass(obj)

        self._fileHandling.setModified(True)
        self._ctrl.updateTitle()
        canvas.Refresh()

    # noinspection PyUnusedLocal
    def _OnMnuEditCopy(self, event):
        """
        TODO : adapt for OglLinks

        """
        selected = self._ctrl.getSelectedShapes()
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
    def _OnMnuEditPaste(self, event):
        if len(self._clipboard) == 0:
            return

        frame = self._ctrl.getUmlFrame()
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
            self._ctrl.getUmlFrame().addShape(po, x, y)
            x += 20
            y += 20

        canvas = po.GetDiagram().GetPanel()
        # the canvas wich contain the shape
        # specify the canvas on which we will paint
        dc = ClientDC(canvas)
        canvas.PrepareDC(dc)

        self._fileHandling.setModified(True)
        self._ctrl.updateTitle()
        canvas.Refresh()
        # TODO : What are you doing with the dc ?

    # noinspection PyUnusedLocal
    def _OnMnuSelectAll(self, event):
        frame = self._ctrl.getUmlFrame()
        if frame is None:
            PyutUtils.displayError(_("No frame found !"))
            return
        diagram = frame.GetDiagram()
        shapes = diagram.GetShapes()
        for shape in shapes:
            shape.SetSelected(True)
        frame.Refresh()

    # noinspection PyUnusedLocal
    def _OnMnuFilePyutProperties(self, event):
        """
        Callback.

        @param event
        @author L. Burgbacher <lb@alawa.ch>
        @since 1.34
        """
        from org.pyut.dialogs.DlgPyutProperties import DlgPyutProperties

        self.logger.debug(f"Before dialog show")
        with DlgPyutProperties(self, -1, self._ctrl, self._prefs) as dlg:
            if dlg.ShowModal() == ID_OK:
                self.logger.debug(f'Waiting for answer')
            else:
                self.logger.debug(f'Cancelled')

        umlFrame = self._ctrl.getUmlFrame()
        if umlFrame is not None:
            umlFrame.Refresh()

    # noinspection PyUnusedLocal
    def _OnMnuDebug(self, event):
        """
        Open a IPython shell
        """
        self.logger.warning(f'not yet implemented on Python 3')

        # try:
        #     from IPython.Shell import IPShellEmbed
        # except ImportError:
        #     displayError(_("You don't have IPython installed !"))
        #     return
        # ipshell = IPShellEmbed()
        # ipshell(local_ns=vars(), global_ns=globals())

    # noinspection PyUnusedLocal
    def _OnMnuUndo(self, event):
        if (self._fileHandling.getCurrentFrame()) is None:
            return   # TODO : dialog box
        self._fileHandling.getCurrentFrame().getHistory().undo()

    # noinspection PyUnusedLocal
    def _OnMnuRedo(self, event):
        if (self._fileHandling.getCurrentFrame()) is None:
            return   # TODO : dialog box
        self._fileHandling.getCurrentFrame().getHistory().redo()


from typing import cast
from typing import Callable

from logging import Logger
from logging import getLogger

from os import sep as osSeparator
from os import getcwd

from copy import copy

from urllib import request

from pkg_resources import resource_filename

from wx import ACCEL_CTRL
from wx import BITMAP_TYPE_ICO
from wx import BITMAP_TYPE_BMP
from wx import BOTH
from wx import DEFAULT_FRAME_STYLE
from wx import FRAME_EX_METAL
from wx import ID_OK
from wx import ITEM_CHECK
from wx import ITEM_NORMAL
from wx import NO_BORDER
from wx import PAPER_A4
from wx import PORTRAIT
from wx import PRINT_QUALITY_HIGH
from wx import TB_FLAT
from wx import TB_HORIZONTAL


from wx import EVT_ACTIVATE
from wx import EVT_CLOSE
from wx import EVT_MENU
from wx import EVT_TOOL
from wx import FD_OPEN
from wx import FD_SAVE
from wx import FD_MULTIPLE
from wx import FD_OVERWRITE_PROMPT

from wx import NewId
from wx import PrintData

from wx import AcceleratorEntry
from wx import Frame
from wx import DefaultPosition
from wx import Size
from wx import Icon
from wx import AcceleratorTable
from wx import Bitmap
from wx import Menu
from wx import MenuBar
from wx import FileDialog
from wx import PrintDialogData
from wx import PrintDialog
from wx import MessageDialog
from wx import ToolBar
from wx import ClientDC
from wx import PreviewFrame
from wx import PrintPreview
from wx import Printer

from wx import BeginBusyCursor
from wx import EndBusyCursor

from wx import Yield as wxYield

from FileHandling import FileHandling

from OglActor import OglActor
from OglClass import OglClass
from OglNote import OglNote
from OglUseCase import OglUseCase

from PluginManager import PluginManager
from PyutActor import PyutActor
from PyutClass import PyutClass
from PyutConsts import CLASS_DIAGRAM
from PyutConsts import SEQUENCE_DIAGRAM
from PyutConsts import USECASE_DIAGRAM
from PyutNote import PyutNote

from PyutPreferences import PyutPreferences
from PyutPrintout import PyutPrintout
from PyutUseCase import PyutUseCase

from Tool import Tool

from Mediator import ACTION_NEW_ACTOR
from Mediator import ACTION_NEW_INHERIT_LINK
from Mediator import ACTION_NEW_NOTE_LINK
from Mediator import ACTION_NEW_AGGREGATION_LINK
from Mediator import ACTION_SELECTOR
from Mediator import ACTION_NEW_CLASS
from Mediator import ACTION_NEW_NOTE
from Mediator import ACTION_NEW_IMPLEMENT_LINK
from Mediator import ACTION_NEW_COMPOSITION_LINK
from Mediator import ACTION_NEW_ASSOCIATION_LINK
from Mediator import ACTION_ZOOM_OUT
from Mediator import ACTION_ZOOM_IN
from Mediator import ACTION_NEW_SD_MESSAGE
from Mediator import ACTION_NEW_SD_INSTANCE
from Mediator import ACTION_NEW_USECASE
from Mediator import getMediator

from pyutUtils import assignID
from pyutUtils import displayError
from pyutUtils import displayInformation
from pyutUtils import displayWarning

from TipsFrame import TipsFrame

from globals import _
from globals import IMG_PKG

[
    ID_MNUFILENEWPROJECT,        ID_MNUFILEOPEN,          ID_MNUFILESAVE,
    ID_MNUFILESAVEAS,            ID_MNUFILEEXIT,          ID_MNUEDITCUT,
    ID_MNUEDITCOPY,              ID_MNUEDITPASTE,         ID_MNUHELPABOUT,
    ID_MNUFILEIMP,               ID_MNUFILE,              ID_MNUFILEDIAGRAMPROPER,
    ID_MNUFILEPRINTSETUP,        ID_MNUFILEPRINTPREV,     ID_MNUFILEPRINT,
    ID_MNUADDPYUTHIERARCHY,      ID_MNUADDOGLHIERARCHY,   ID_MNUHELPINDEX,
    ID_MNUHELPWEB,               ID_MNUFILEEXP,           ID_MNUFILEEXPBMP,
    ID_MNUEDITSHOWTOOLBAR,       ID_ARROW,                ID_CLASS,
    ID_REL_INHERITANCE,          ID_REL_REALISATION,      ID_REL_COMPOSITION,
    ID_REL_AGREGATION,           ID_REL_ASSOCIATION,      ID_MNUFILEEXPJPG,
    ID_MNUPROJECTCLOSE,          ID_NOTE,                 ID_ACTOR,
    ID_USECASE,                  ID_REL_NOTE,             ID_MNUHELPVERSION,
    ID_MNUFILEEXPPS,             ID_MNUFILEEXPPNG,        ID_MNUFILEPYUTPROPER,
    ID_MNUFILEEXPPDF,            ID_MNUFILENEWCLASSDIAGRAM, ID_MNUFILENEWSEQUENCEDIAGRAM,
    ID_MNUFILENEWUSECASEDIAGRAM, ID_SD_INSTANCE,
    ID_MNUFILEINSERTPROJECT,     ID_SD_MESSAGE,           ID_MNUEDITSELECTALL,
    ID_MNUFILEREMOVEDOCUMENT,    ID_DEBUG,
    ID_ZOOMIN,                   ID_ZOOMOUT,              ID_ZOOM_VALUE,
    ID_MNUREDO,                  ID_MNUUNDO
] = assignID(54)

# Assign constants

ACTIONS = {
    ID_ARROW: ACTION_SELECTOR,
    ID_CLASS: ACTION_NEW_CLASS,
    ID_NOTE: ACTION_NEW_NOTE,
    ID_REL_INHERITANCE: ACTION_NEW_INHERIT_LINK,
    ID_REL_REALISATION: ACTION_NEW_IMPLEMENT_LINK,
    ID_REL_COMPOSITION: ACTION_NEW_COMPOSITION_LINK,
    ID_REL_AGREGATION: ACTION_NEW_AGGREGATION_LINK,
    ID_REL_ASSOCIATION: ACTION_NEW_ASSOCIATION_LINK,
    ID_REL_NOTE:    ACTION_NEW_NOTE_LINK,
    ID_ACTOR:       ACTION_NEW_ACTOR,
    ID_USECASE:     ACTION_NEW_USECASE,
    ID_SD_INSTANCE: ACTION_NEW_SD_INSTANCE,
    ID_SD_MESSAGE:  ACTION_NEW_SD_MESSAGE,
    ID_ZOOMIN:      ACTION_ZOOM_IN,
    ID_ZOOMOUT:     ACTION_ZOOM_OUT
}


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
        # Application initialisation
        # Frame.__init__(self, parent, ID, title, DefaultPosition, Size(640, 480))
        super().__init__(parent, ID, title, DefaultPosition, Size(960, 480), DEFAULT_FRAME_STYLE | FRAME_EX_METAL)

        self.logger: Logger = getLogger(__name__)

        # Create the application's icon
        # icon = Icon('img' + osSeparator + 'icon.ico', BITMAP_TYPE_ICO)
        fileName = resource_filename(IMG_PKG, 'pyut.ico')
        icon = Icon(fileName, BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        self.Center(BOTH)                     # Center on the screen
        self.CreateStatusBar()

        # Properties
        self.plugMgr = PluginManager()
        self.plugs = {}                         # To store the plugins
        # self.toolbox = Toolbox(self)                # tools plugins, ..
        self._toolboxesID = {}                  # Association toolbox category/id

        # Preferences
        self._prefs = PyutPreferences()  # getPrefs()
        self._lastDir = self._prefs["LastDirectory"]
        if self._lastDir is None:  # Assert that the path is present
            self._lastDir = getcwd()

        # get the mediator
        self._ctrl = getMediator()
        self._ctrl.registerStatusBar(self.GetStatusBar())
        self._ctrl.resetStatusText()
        self._ctrl.registerAppFrame(self)

        # Last opened Files IDs
        self.lastOpenedFilesID = []
        for index in range(self._prefs.getNbLOF()):
            self.lastOpenedFilesID.append(assignID(1)[0])

        # loaded files handler
        self._fileHandling = FileHandling(self, self._ctrl)
        self._ctrl.registerFileHandling(self._fileHandling)

        # Initialization
        self._initPyutTools()   # Toolboxes, toolbar
        self._initMenu()        # Menu
        #  self._initToolBar()  # Toolbar
        self._initPrinting()    # Printing data

        # Accelerators init. (=Keyboards shortcuts)
        acc = self._createAcceleratorTable()
        accel_table = AcceleratorTable(acc)
        self.SetAcceleratorTable(accel_table)

        # Members vars
        self._currentDirectory = getcwd()
        self._ctrl.registerAppPath(self._currentDirectory)
        self._clipboard = []

        # set application title
        self._fileHandling.newProject()
        self._ctrl.updateTitle()

        # Init tips frame
        self._alreadyDisplayedTipsFrame = False
        self.Bind(EVT_ACTIVATE, self._onActivate)

    def _onActivate(self, event):
        """
        EVT_ACTIVATE Callback; display tips frame.
        """
        self.logger.debug(f'_onActivate event: {event}')
        try:
            if self._alreadyDisplayedTipsFrame is True or self._prefs["SHOW_TIPS_ON_STARTUP"] == "0" or self._prefs["SHOW_TIPS_ON_STARTUP"] == "False":
                return
            # Display tips frame
            self._alreadyDisplayedTipsFrame = True
            prefs: PyutPreferences = PyutPreferences()
            if prefs.getOpenHints() is True:
                # noinspection PyUnusedLocal
                tipsFrame = TipsFrame(self)
                #  tipsFrame.Show()     # weird the tips frame constructor does a .show itself  TODO look at this in future
        except (ValueError, Exception) as e:
            if self._prefs is not None:
                self.logger.error(f'_onActivate: {e}')

    def _initPyutTools(self):
        """
        Init all PyUt tools for toolbar and toolbox
        @author C.Dutoit
        """
        import os
        # import img.ImgToolboxUnknown
        import img.ImgToolboxActor
        import img.ImgToolboxClass
        import img.ImgToolboxNote
        import img.ImgToolboxArrow
        import img.ImgToolboxSystem

        # Element tools
        toolArrow = Tool("pyut-arrow", img.ImgToolboxArrow.getBitmap(),
                         _("Arrow"),      _("Select tool"),
                         _(_("PyUt tools")),
                         (lambda x: self._OnNewAction(x)),
                         cast(Callable, None), wxID=ID_ARROW, isToggle=True)
        toolClass = Tool("pyut-class", img.ImgToolboxClass.getBitmap(),
                         _("Class"),      _("Create a new class"),
                         _(_("PyUt tools")),
                         (lambda x: self._OnNewAction(x)),
                         cast(Callable, None), wxID=ID_CLASS, isToggle=True)
        toolActor = Tool("pyut-actor", img.ImgToolboxActor.getBitmap(),
                         _("Actor"),      _("Create a new actor"),
                         _(_("PyUt tools")),
                         (lambda x: self._OnNewAction(x)),
                         cast(Callable, None), wxID=ID_ACTOR, isToggle=True)
        toolUseCase = Tool("pyut-system", img.ImgToolboxSystem.getBitmap(),
                           _("System"),     _("Create a new use case"),
                           _(_("PyUt tools")),
                           (lambda x: self._OnNewAction(x)),
                           cast(Callable, None), wxID=ID_USECASE, isToggle=True)
        toolNote = Tool("pyut-note", img.ImgToolboxNote.getBitmap(),
                        _("Note"),     _("Create a new note"),
                        _(_("PyUt tools")),
                        (lambda x: self._OnNewAction(x)),
                        cast(Callable, None), wxID=ID_NOTE, isToggle=True)
        # toolSDInstance = Tool("pyut-instance", img.ImgToolboxUnknown.getBitmap(),
        #             _("Instance"),     _("Create a new class diagram instance object"),
        #             _(_("PyUt tools")),
        #             (lambda x: self._OnNewAction(x)),
        #             cast(Callable, None), wxID=ID_SD_INSTANCE, isToggle=True)
        # toolSDMessage = Tool("pyut-message", img.ImgToolboxUnknown.getBitmap(),
        #             _("Message"),     _("Create a new class diagram message object"),
        #             _(_("PyUt tools")),
        #             (lambda x: self._OnNewAction(x)),
        #             cast(Callable, None), wxID=ID_SD_MESSAGE, isToggle=True)

        # Added by P. Dabrowski 20.11.2005

        toolZoomIn = Tool("pyut-zoomIn",
                          Bitmap(f'img{os.sep}zoomin.bmp', BITMAP_TYPE_BMP),
                          _("Zoom In"),
                          _("Zoom in on the selected area"),
                          _(_("PyUt tools")),
                          (lambda x: self._OnNewAction(x)),
                          cast(Callable, None), wxID=ID_ZOOMIN, isToggle=True)
        toolZoomOut = Tool("pyut-zoomOut",
                           Bitmap('img' + os.sep + 'zoomout.bmp', BITMAP_TYPE_BMP),
                           _("Zoom Out"),
                           _("Zoom out from the clicked point"),
                           _(_("PyUt tools")),
                           (lambda x: self._OnNewAction(x)),
                           cast(Callable, None), wxID=ID_ZOOMOUT, isToggle=True)

        # Menu tools
        toolNewProject = Tool("pyut-new-project",
                              Bitmap('img' + os.sep + 'newproject.bmp', BITMAP_TYPE_BMP),
                              _("new project"),
                              _("Create a new project"),
                              _("PyUt menu"),
                              (lambda x: self._OnMnuFileNewProject(x)),
                              cast(Callable, None), wxID=ID_MNUFILENEWPROJECT)
        toolNewClassDiagram = Tool("pyut-new-class-diagram",
                                   Bitmap('img' + os.sep + 'newcd.bmp', BITMAP_TYPE_BMP),
                                   _("New Class Diagram"),
                                   _("Create a new class diagram"),
                                   _("PyUt menu"),
                                   (lambda x: self._OnMnuFileNewClassDiagram(x)),
                                   cast(Callable, None), wxID=ID_MNUFILENEWCLASSDIAGRAM)
        toolNewSequenceDiagram = Tool("pyut-new-sequence-diagram",
                                      Bitmap('img' + os.sep + 'newsd.bmp', BITMAP_TYPE_BMP),
                                      _("New Sequence Diagram"),
                                      _("Create a new sequence diagram"),
                                      _(_("PyUt menu")),
                                      (lambda x: self._OnMnuFileNewSequenceDiagram(x)),
                                      cast(Callable, None), wxID=ID_MNUFILENEWSEQUENCEDIAGRAM)
        toolNewUseCaseDiagram = Tool("pyut-new-use-case-diagram",
                                     Bitmap('img' + os.sep + 'newud.bmp', BITMAP_TYPE_BMP),
                                     _("New Use-Case diagram"),
                                     _("Create a new use-case diagram"),
                                     _("PyUt menu"),
                                     (lambda x: self._OnMnuFileNewUsecaseDiagram(x)),
                                     cast(Callable, None), wxID=ID_MNUFILENEWUSECASEDIAGRAM)
        toolOpen = Tool("pyut-open",
                        Bitmap('img' + os.sep + 'open.bmp', BITMAP_TYPE_BMP),
                        _("Open"),
                        _("Open a file"),
                        _("PyUt menu"),
                        (lambda x: self._OnMnuFileOpen(x)),
                        cast(Callable, None), wxID=ID_MNUFILEOPEN)
        toolSave = Tool("pyut-save",
                        Bitmap('img' + os.sep + 'save.bmp', BITMAP_TYPE_BMP),
                        _("Save"),
                        _("Save current UML Diagram"),
                        _("PyUt menu"),
                        (lambda x: self._OnMnuFileSave(x)),
                        cast(Callable, None), wxID=ID_MNUFILESAVE)
        # Patch from D.Dabrowsky, 20060129
        toolUndo = Tool("pyut-undo",
                        Bitmap('img' + os.sep + 'undo.bmp', BITMAP_TYPE_BMP),
                        _("undo"),
                        _("undo the last performed action"),
                        _("PyUt menu"),
                        (lambda x: self._OnMnuUndo(x)),
                        cast(Callable, None), wxID=ID_MNUUNDO)
        toolRedo = Tool("pyut-redo",
                        Bitmap('img' + os.sep + 'redo.bmp', BITMAP_TYPE_BMP),
                        _("redo"),
                        _("redo the last undone action"),
                        _("PyUt menu"),
                        (lambda x: self._OnMnuRedo(x)),
                        cast(Callable, None), wxID=ID_MNUREDO)

        # Relations tools
        toolRelInheritance = Tool("pyut-rel-inheritance",
                                  Bitmap('img' + os.sep + 'relinheritance.bmp', BITMAP_TYPE_BMP),
                                  _("New inheritance relation"), _("New inheritance relation"),
                                  _("PyUt tools"),
                                  (lambda x: self._OnNewAction(x)),
                                  cast(Callable, None), wxID=ID_REL_INHERITANCE, isToggle=True)
        toolRelRealisation = Tool("pyut-rel-realisation",
                                  Bitmap('img' + os.sep + 'relrealisation.bmp', BITMAP_TYPE_BMP),
                                  _("New realisation relation"), _("New realisation relation"),
                                  _("PyUt tools"),
                                  (lambda x: self._OnNewAction(x)),
                                  cast(Callable, None), wxID=ID_REL_REALISATION, isToggle=True)
        toolRelComposition = Tool("pyut-rel-composition",
                                  Bitmap('img' + os.sep + 'relcomposition.bmp', BITMAP_TYPE_BMP),
                                  _("New composition relation"), _("New composition relation"),
                                  _("PyUt tools"),
                                  (lambda x: self._OnNewAction(x)),
                                  cast(Callable, None), wxID=ID_REL_COMPOSITION, isToggle=True)
        toolRelAgregation = Tool("pyut-rel-agregation",
                                 Bitmap('img' + os.sep + 'relagregation.bmp', BITMAP_TYPE_BMP),
                                 _("New aggregation relation"), _("New aggregation relation"),
                                 _("PyUt tools"),
                                 (lambda x: self._OnNewAction(x)),
                                 cast(Callable, None), wxID=ID_REL_AGREGATION, isToggle=True)

        toolRelAssociation = Tool("pyut-rel-association",
                                  Bitmap('img' + os.sep + 'relassociation.bmp', BITMAP_TYPE_BMP),
                                  _("New association relation"), _("New association relation"),
                                  _("PyUt tools"),
                                  (lambda x: self._OnNewAction(x)),
                                  cast(Callable, None), wxID=ID_REL_ASSOCIATION, isToggle=True)
        toolRelNote = Tool("pyut-rel-note",
                           Bitmap('img' + os.sep + 'relnote.bmp', BITMAP_TYPE_BMP),
                           _("New note relation"), _("New note relation"),
                           _("PyUt tools"),
                           (lambda x: self._OnNewAction(x)),
                           cast(Callable, None), wxID=ID_REL_NOTE, isToggle=True)
        toolSDInstance = Tool("pyut-sd-instance",
                              Bitmap('img' + os.sep + 'sdinstance.bmp', BITMAP_TYPE_BMP),
                              _("New sequence diagram instance object"),
                              _("New sequence diagram instance object"),
                              _("PyUt tools"),
                              (lambda x: self._OnNewAction(x)),
                              cast(Callable, None), wxID=ID_SD_INSTANCE, isToggle=True)
        toolSDMessage = Tool("pyut-sd-message",
                             Bitmap('img' + os.sep + 'sdmessage.bmp', BITMAP_TYPE_BMP),
                             _("New sequence diagram message object"),
                             _("New sequence diagram message object"),
                             _("PyUt tools"),
                             (lambda x: self._OnNewAction(x)),
                             cast(Callable, None), wxID=ID_SD_MESSAGE, isToggle=True)

        # Create toolboxes
        for tool in [toolNewProject, toolNewClassDiagram, toolNewSequenceDiagram,
                     toolNewUseCaseDiagram, toolOpen, toolSave,

                     # added by P. Dabrowski 20.11.2005
                     toolArrow, toolZoomIn, toolZoomOut, toolUndo, toolRedo,
                     toolClass, toolActor, toolUseCase, toolNote,
                     toolRelInheritance, toolRelRealisation, toolRelComposition,
                     toolRelAgregation, toolRelAssociation, toolRelNote,
                     toolSDInstance, toolSDMessage
                     ]:
            self._ctrl.registerTool(tool)

        # Create toolbar

        self._tb: ToolBar = self.CreateToolBar(TB_HORIZONTAL | NO_BORDER | TB_FLAT)
        self.SetToolBar(self._tb)
        #  self._tb.SetTitle("Standard")    # This toolbar does not have a .SetTitle method

        for tool in [toolNewProject, toolNewClassDiagram, toolNewSequenceDiagram,
                     toolNewUseCaseDiagram, toolOpen, toolSave, None,
                     # Patch from D.Dabrowsky, 20060129
                     toolArrow, toolZoomIn, toolZoomOut, toolUndo, toolRedo, None,
                     toolClass, toolActor, toolUseCase, toolNote, None,
                     toolRelInheritance, toolRelRealisation, toolRelComposition,
                     toolRelAgregation, toolRelAssociation, toolRelNote, None,
                     toolSDInstance, toolSDMessage
                     ]:

            # Add tool
            if tool is not None:
                # self._tb.AddTool(tool.getWXID(), tool.getImg(), shortHelpString=tool.getCaption(), longHelpString=tool.getToolTip(),
                #                  isToggle=tool.getIsToggle())
                toolId = tool.getWXID()
                bitMap = tool.getImg()
                shortHelpString: str  = tool.getCaption()
                isToggle:        bool = tool.getIsToggle()
                if isToggle is True:
                    itemKind = ITEM_CHECK
                else:
                    itemKind = ITEM_NORMAL
                """
                AddTool(toolId, label, bitmap, shortHelp=EmptyString, kind=ITEM_NORMAL) -> ToolBarToolBase
                """
                self._tb.AddTool(toolId, '', bitMap, shortHelpString, itemKind)     # TODO hasii -- do we need a lablel

                self.Bind(EVT_TOOL, tool.getActionCallback(), id=tool.getWXID())
            else:
                self._tb.AddSeparator()

        # Add contextual help
        # self._tb.AddSeparator()
        # btn = wxContextHelpButton(self._tb)
        # btn.SetHelpText("Contextual help button")
        # self._tb.AddControl(btn)
        # EVT_HELP(self, ...)

        # Do toolbar
        self._tb.Realize()

        # Register toolbar on mediator
        self._ctrl.registerToolBar(self._tb)
        self._ctrl.registerToolBarTools([
            ID_ARROW, ID_CLASS, ID_NOTE, ID_REL_INHERITANCE,
            ID_REL_REALISATION, ID_REL_COMPOSITION, ID_REL_AGREGATION,
            ID_REL_ASSOCIATION, ID_REL_NOTE, ID_ACTOR, ID_USECASE,
            ID_SD_INSTANCE, ID_SD_MESSAGE, ID_ZOOMIN, ID_ZOOMOUT
        ])

    def _initMenu(self):
        """
        Menu initialization.

        @since 1.0
        @author N.Dubois
        """
        self.mnuFile = Menu()
        self.mnuFileNew = Menu()
        self.mnuFileNew.Append(ID_MNUFILENEWPROJECT,         _("&New project\tCtrl-N"), _("New project"))
        self.mnuFileNew.Append(ID_MNUFILENEWCLASSDIAGRAM,    _("New c&lass diagram\tCtrl-L"), _("New class diagram"))
        self.mnuFileNew.Append(ID_MNUFILENEWSEQUENCEDIAGRAM, _("New s&equence diagram\tCtrl-E"), _("New sequence diagram"))
        self.mnuFileNew.Append(ID_MNUFILENEWUSECASEDIAGRAM,  _("New &use-case diagram\tCtrl-U"), _("New use-case diagram"))

        self.mnuFile.Append(NewId(), _("&New"), self.mnuFileNew)
        self.mnuFile.Append(ID_MNUFILEINSERTPROJECT,  _("&Insert a project...\t"), _("Insert a project in the current project..."))
        self.mnuFile.Append(ID_MNUFILEOPEN,           _("&Open...\tCtrl-O"), _("Open a file..."))
        self.mnuFile.Append(ID_MNUFILESAVE,           _("&Save\tCtrl-S"), _("Save current data"))
        self.mnuFile.Append(ID_MNUFILESAVEAS,         _("Save &As...\tCtrl-A"), _("Save current data"))
        self.mnuFile.Append(ID_MNUPROJECTCLOSE,       _("&Close project\tCtrl-W"), _("Close current project"))
        self.mnuFile.Append(ID_MNUFILEREMOVEDOCUMENT, _("&Remove document"), _("Remove the document from the project"))
        self.mnuFile.AppendSeparator()

        # added by L. Burgbacher, dynamic plugin support
        sub = self.makeExportMenu()

        # Fixed Export
        if sub is None:
            sub = Menu()
        sub.Append(ID_MNUFILEEXPBMP, "&bmp",        _("Export data to a bitmap file"))
        sub.Append(ID_MNUFILEEXPJPG, "&jpeg",       _("Export data to a jpeg file"))
        sub.Append(ID_MNUFILEEXPPNG, "&png",        _("Export data to a png file"))
        sub.Append(ID_MNUFILEEXPPS,  "&Postscript", _("Export data to a postscript file"))
        sub.Append(ID_MNUFILEEXPPDF, "P&DF",        _("Export data to a PDF file"))

        if sub is not None:
            self.mnuFile.Append(NewId(), _("Export"), sub)

        sub = self.makeImportMenu()
        if sub is not None:
            # self.mnuFile.AppendMenu(NewId(), _("Import"), sub)
            self.mnuFile.Append(NewId(), _("Import"), sub)

        self.mnuFile.AppendSeparator()
        self.mnuFile.Append(ID_MNUFILEPYUTPROPER, _("PyUt P&roperties"), _("PyUt properties"))
        # self.mnuFile.Append(ID_MNUFILEDIAGRAMPROPER,_("&Diagram Properties"), _("Diagram properties"))
        self.mnuFile.AppendSeparator()
        self.mnuFile.Append(ID_MNUFILEPRINTSETUP, _("Print se&tup..."), _("Display the print setup dialog box"))
        self.mnuFile.Append(ID_MNUFILEPRINTPREV,  _("Print pre&view"),  _("Diagram preview before printing"))
        self.mnuFile.Append(ID_MNUFILEPRINT,      _("&Print\tCtrl-P"),  _("Print the current diagram"))
        self.mnuFile.AppendSeparator()

        #  Add Last opened files
        index = 0
        #  TODO : does not work ? verify function return...
        for el in self._prefs.getLastOpenedFilesList():
            index += 1
            self.mnuFile.Append(self.lastOpenedFilesID[index-1], "&" + str(index) + " " + el)
        for index in range(index, self._prefs.getNbLOF()):
            self.mnuFile.Append(self.lastOpenedFilesID[index], "&" + str(index+1) + " -")

        # exit
        self.mnuFile.AppendSeparator()
        self.mnuFile.Append(ID_MNUFILEEXIT, _("E&xit"), _("Exit PyUt"))

        # -----------------
        #     Edit menu
        # -----------------
        mnuEdit = Menu()
        # Path from D.Dabrowsky, 20060129
        mnuEdit.Append(ID_MNUUNDO, _("&Undo\tCtrl-Z"), _("Undo the last performed action"))
        mnuEdit.Append(ID_MNUREDO, _("&Redo\tCtrl-Y"), _("Redo the last undone action"))
        mnuEdit.AppendSeparator()
        mnuEdit.Append(ID_MNUEDITCUT,    _("Cu&t\tCtrl-X"),   _("Cut selected data"))
        mnuEdit.Append(ID_MNUEDITCOPY,   _("&Copy\tCtrl-C"),  _("Copy selected data"))
        mnuEdit.Append(ID_MNUEDITPASTE,  _("&Paste\tCtrl-V"), _("Paste selected data"))
        mnuEdit.AppendSeparator()
        mnuEdit.Append(ID_MNUEDITSELECTALL, _("&Select all"), _("Select all elements"))
        mnuEdit.AppendSeparator()
        mnuEdit.Append(ID_MNUADDPYUTHIERARCHY, _("&Add Pyut hierarchy"), _("Add the UML Diagram of Pyut"))
        mnuEdit.Append(ID_MNUADDOGLHIERARCHY, _("Add &Ogl hierarchy"),   _("Add the UML Diagram of Pyut - Ogl"))

        # -----------------
        #    Tools menu
        # -----------------
        mnuTools = Menu()
        sub = self.makeToolsMenu()
        if sub is not None:
            # mnuTools.AppendMenu(NewId(), _("Plugins tools"), sub)
            mnuTools.Append(NewId(), _("Plugins tools"), sub)

        sub = self.makeToolboxesMenu()
        if sub is not None:
            mnuTools.Append(NewId(), _("toolboxes"), sub)

        # -----------------
        #    Help menu
        # -----------------
        mnuHelp = Menu()
        mnuHelp.Append(ID_MNUHELPINDEX, _("&Index"), _("Display help index"))
        mnuHelp.AppendSeparator()
        mnuHelp.Append(ID_MNUHELPVERSION, _("Check for newer versions"), _("Check if a newer version of Pyut exists"))
        mnuHelp.Append(ID_MNUHELPWEB, _("&Web site"), _("Open PyUt web site"))
        mnuHelp.Append(ID_DEBUG,      _("&Debug"), _("Open IPython shell"))
        mnuHelp.AppendSeparator()
        mnuHelp.Append(ID_MNUHELPABOUT, _("&About PyUt..."), _("Display the About PyUt dialog box"))

        # -----------------
        #   make menu bar
        # -----------------
        mnuBar = MenuBar()
        mnuBar.Append(self.mnuFile, _("&File"))
        mnuBar.Append(mnuEdit, _("&Edit"))
        mnuBar.Append(mnuTools, _("&Tools"))
        mnuBar.Append(mnuHelp, "&?")
        self.SetMenuBar(mnuBar)

        # -----------------
        # Events menu click
        # -----------------
        self.Bind(EVT_MENU, self._OnMnuFileNewProject,      id=ID_MNUFILENEWPROJECT)
        self.Bind(EVT_MENU, self._OnMnuFileNewClassDiagram, id=ID_MNUFILENEWCLASSDIAGRAM)
        self.Bind(EVT_MENU, self._OnMnuFileNewSequenceDiagram, id=ID_MNUFILENEWSEQUENCEDIAGRAM)
        self.Bind(EVT_MENU, self._OnMnuFileNewUsecaseDiagram,  id=ID_MNUFILENEWUSECASEDIAGRAM)
        self.Bind(EVT_MENU, self._OnMnuFileInsertProject,      id=ID_MNUFILEINSERTPROJECT)
        self.Bind(EVT_MENU, self._OnMnuFileOpen, id=ID_MNUFILEOPEN)
        self.Bind(EVT_MENU, self._OnMnuFileSave, id=ID_MNUFILESAVE)
        self.Bind(EVT_MENU, self._OnMnuFileSaveAs, id=ID_MNUFILESAVEAS)
        self.Bind(EVT_MENU, self._OnMnuFileClose,  id=ID_MNUPROJECTCLOSE)
        self.Bind(EVT_MENU, self._OnMnuFileRemoveDocument,  id=ID_MNUFILEREMOVEDOCUMENT)
        self.Bind(EVT_MENU, self._OnMnuFilePrintSetup,      id=ID_MNUFILEPRINTSETUP)
        self.Bind(EVT_MENU, self._OnMnuFilePrintPreview,    id=ID_MNUFILEPRINTPREV)
        self.Bind(EVT_MENU, self._OnMnuFilePrint,           id=ID_MNUFILEPRINT)
        self.Bind(EVT_MENU, self._OnMnuFilePyutProperties,  id=ID_MNUFILEPYUTPROPER)
        #  EVT_MENU(self, ID_MNUFILEDIAGRAMPROPER,self._OnMnuFileDiagramProperties)
        self.Bind(EVT_MENU, self._OnMnuFileExit,     id=ID_MNUFILEEXIT)
        self.Bind(EVT_MENU, self._OnMnuHelpAbout,    id=ID_MNUHELPABOUT)
        self.Bind(EVT_MENU, self._OnMnuHelpIndex,    id=ID_MNUHELPINDEX)
        self.Bind(EVT_MENU, self._OnMnuHelpVersion,  id=ID_MNUHELPVERSION)
        self.Bind(EVT_MENU, self._OnMnuHelpWeb,      id=ID_MNUHELPWEB)
        self.Bind(EVT_MENU, self._OnMnuAddPyut,      id=ID_MNUADDPYUTHIERARCHY)
        self.Bind(EVT_MENU, self._OnMnuAddOgl,       id=ID_MNUADDOGLHIERARCHY)
        self.Bind(EVT_MENU, self._OnMnuFileExportBmp, id=ID_MNUFILEEXPBMP)
        self.Bind(EVT_MENU, self._OnMnuFileExportJpg, id=ID_MNUFILEEXPJPG)
        self.Bind(EVT_MENU, self._OnMnuFileExportPng, id=ID_MNUFILEEXPPNG)
        self.Bind(EVT_MENU, self._OnMnuFileExportPs,  id=ID_MNUFILEEXPPS)
        self.Bind(EVT_MENU, self._OnMnuFileExportPDF, id=ID_MNUFILEEXPPDF)
        self.Bind(EVT_MENU, self._OnMnuEditCut,       id=ID_MNUEDITCUT)
        self.Bind(EVT_MENU, self._OnMnuEditCopy,      id=ID_MNUEDITCOPY)
        self.Bind(EVT_MENU, self._OnMnuEditPaste,     id=ID_MNUEDITPASTE)
        self.Bind(EVT_MENU, self._OnMnuSelectAll,     id=ID_MNUEDITSELECTALL)
        self.Bind(EVT_MENU, self._OnMnuDebug,         id=ID_DEBUG)

        #  Added by P. Dabrowski 20.11.2005
        self.Bind(EVT_MENU, self._OnMnuUndo, id=ID_MNUUNDO)
        self.Bind(EVT_MENU, self._OnMnuRedo, id=ID_MNUREDO)

        for index in range(self._prefs.getNbLOF()):
            self.Bind(EVT_MENU, self._OnMnuLOF, id=self.lastOpenedFilesID[index])

        # ----------------------
        # Others events handlers
        # ----------------------
        self.Bind(EVT_CLOSE, self.Close)

    def makeExportMenu(self):
        """
        Make the export submenu.

        @author L. Burgbacher <lb@alawa.ch>
        @since 1.26
        """
        plugs = self.plugMgr.getOutputPlugins()
        nb = len(plugs)
        if nb == 0:
            return None
        sub = Menu()

        for i in range(nb):
            pluginId = NewId()
            obj = plugs[i](None, None)
            sub.Append(pluginId, obj.getOutputFormat()[0])
            self.Bind(EVT_MENU, self.OnExport, id=pluginId)
            self.plugs[pluginId] = plugs[i]
        return sub

    def makeImportMenu(self):
        """
        Make the import submenu.

        @author L. Burgbacher <lb@alawa.ch>
        @since 1.26
        """
        plugs = self.plugMgr.getInputPlugins()
        nb = len(plugs)
        if nb == 0:
            return None
        sub = Menu()

        for i in range(nb):
            importId = NewId()
            obj = plugs[i](None, None)
            sub.Append(importId, obj.getInputFormat()[0])
            self.Bind(EVT_MENU, self.OnImport, id=importId)
            self.plugs[importId] = plugs[i]
        return sub

    def makeToolsMenu(self):
        """
        Make the tools submenu.

        @author L. Burgbacher <lb@alawa.ch>
        @since 1.26
        """
        plugs = self.plugMgr.getToolPlugins()
        nb = len(plugs)
        if nb == 0:
            return None
        sub = Menu()

        for i in range(nb):
            anId = NewId()
            obj = plugs[i](None, None)
            sub.Append(anId, obj.getMenuTitle())
            self.Bind(EVT_MENU, self.OnToolPlugin, id=anId)
            self.plugs[anId] = plugs[i]
        return sub

    def makeToolboxesMenu(self):
        """
        Make the toolboxes submenu.

        @author C.Dutoit <dutoitc@hotmail.com>
        @since 1.4
        """
        # Get categories
        categories = self._ctrl.getToolboxesCategories()
        nb = len(categories)
        if nb == 0:
            return None
        sub = Menu()

        for category in categories:
            categoryId = NewId()
            self._toolboxesID[categoryId] = category
            sub.Append(categoryId, category)
            self.Bind(EVT_MENU, self.OnToolboxMenuClick, id=categoryId)
        return sub

    def getCurrentDir(self):
        """
        Return current working directory.

        @return String : Current directory

        @author P. Waelti <pwaelti@eivd.ch>
        @since 1.50
        """
        return self._lastDir

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

    def _createAcceleratorTable(self):
        """
        Accelerator table initialization

        @author C.Dutoit
        """
        #  init accelerator table
        lst = [
            (ACCEL_CTRL,     ord('n'),   ID_MNUFILENEWPROJECT),
            (ACCEL_CTRL,     ord('N'),   ID_MNUFILENEWPROJECT),
            (ACCEL_CTRL,     ord('L'),   ID_MNUFILENEWCLASSDIAGRAM),
            (ACCEL_CTRL,     ord('l'),   ID_MNUFILENEWCLASSDIAGRAM),
            (ACCEL_CTRL,     ord('E'),   ID_MNUFILENEWSEQUENCEDIAGRAM),
            (ACCEL_CTRL,     ord('e'),   ID_MNUFILENEWSEQUENCEDIAGRAM),
            (ACCEL_CTRL,     ord('U'),   ID_MNUFILENEWUSECASEDIAGRAM),
            (ACCEL_CTRL,     ord('u'),   ID_MNUFILENEWUSECASEDIAGRAM),
            (ACCEL_CTRL,     ord('o'),   ID_MNUFILEOPEN),
            (ACCEL_CTRL,     ord('O'),   ID_MNUFILEOPEN),
            (ACCEL_CTRL,     ord('s'),   ID_MNUFILESAVE),
            (ACCEL_CTRL,     ord('S'),   ID_MNUFILESAVE),
            (ACCEL_CTRL,     ord('a'),   ID_MNUFILESAVEAS),
            (ACCEL_CTRL,     ord('A'),   ID_MNUFILESAVEAS),
            (ACCEL_CTRL,     ord('p'),   ID_MNUFILEPRINT),
            (ACCEL_CTRL,     ord('P'),   ID_MNUFILEPRINT),
            (ACCEL_CTRL,     ord('x'),   ID_MNUEDITCUT),
            (ACCEL_CTRL,     ord('X'),   ID_MNUEDITCUT),
            (ACCEL_CTRL,     ord('c'),   ID_MNUEDITCOPY),
            (ACCEL_CTRL,     ord('C'),   ID_MNUEDITCOPY),
            (ACCEL_CTRL,     ord('v'),   ID_MNUEDITPASTE),
            (ACCEL_CTRL,     ord('V'),   ID_MNUEDITPASTE),
            (ACCEL_CTRL,     ord('d'),   ID_DEBUG),
            (ACCEL_CTRL,     ord('D'),   ID_DEBUG),
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
        self._fileHandling.newDocument(CLASS_DIAGRAM)
        self._ctrl.updateTitle()

    # noinspection PyUnusedLocal
    def _OnMnuFileNewSequenceDiagram(self, event):
        """
        begin a new sequence diagram

        @author C.Dutoit
        """
        self._fileHandling.newDocument(SEQUENCE_DIAGRAM)
        self._ctrl.updateTitle()

    # noinspection PyUnusedLocal
    def _OnMnuFileNewUsecaseDiagram(self, event):
        """
        begin a new use-case diagram

        @author C.Dutoit
        """
        self._fileHandling.newDocument(USECASE_DIAGRAM)
        self._ctrl.updateTitle()

    # noinspection PyUnusedLocal
    def _OnMnuFileInsertProject(self, event):
        """
        Insert a project into this one

        @author C.Dutoit
        """
        displayWarning(_("The project insert is experimental, "
                         "use it at your own risk.\n"
                         "You risk a shapes ID duplicate with "
                         "unexpected results !"), parent=self)

        if (self._fileHandling.getCurrentProject()) is None:
            displayError(_("No project to insert this file into !"), parent=self)
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
            displayError(_(f"An error occurred while loading the project!  {e}"), parent=self)

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
            displayWarning(_("No document to remove"))

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
            displayError(_("Error while displaying Postscript saving dialog"), parent=self)
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
            displayError(_("Error while displaying pdf saving dialog"), parent=self)
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
                    displayError(_("Can't execute ps2epsi !"), parent=self)
                    return
                if os.system("epstopdf /tmp/pdfexport.eps --outfile=" + filename) != 0:
                    displayError(_("Can't execute ps2epsi !"), parent=self)
                    return
                self._ctrl.setStatusText(_("Exported to pdf"))
            except (ValueError, Exception) as e:
                displayError("Can't export to pdf !", parent=self)

    def printDiagramToPostscript(self, filename):
        """
        print the current diagram to postscript

        @return True if succeeded
        @author C.Dutoit
        """
        # Verify that we do have a diagram to save
        if self._ctrl.getDiagram() is None:
            displayError(_("No diagram to print !"), parent=self)
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
            displayError(_("Cannot export to Postscript"), parent=self)
            self._ctrl.setStatusText(_(f"Error while printing to postscript {e}"))
            return False

        # Print to postscript
        if not printer.Print(self, printout, False):
            displayError(_("Cannot print"), parent=self)
            self._ctrl.setStatusText(_("Error while printing to postscript"))
            return False

        # Return
        self._ctrl.setStatusText(_("Printed to postscript"))
        return True

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

        @since 1.10
        @author C.Dutoit <dutoitc@hotmail.com>
        """

        msg: str = "If you have a link using wxDASHED_LINE " + \
                   "(OglNoteLink, OglAssociation)," + \
                   " this print preview crash pyut." + \
                   "This is an unresolved bug.\n" + \
                   "This bug come from gtk or gdk ? " + \
                   "It crash in wxPython demo!!! \n" + \
                   "Do you still want to continue ? "

        # print "AppFrame-OnMnuFilePrintPreview-2"
        # dlg = wx.MessageDialog(self, msg, _("Warning"),
        #        wx.YES_NO | wx.ICON_EXCLAMATION | wx.CENTRE | wx.NO_DEFAULT)
        # dlg = wx.MessageDialog(self, msg, _("Warning"))
        dlg = MessageDialog(self, msg, "1")

        if dlg.ShowModal() == 5104:

            print("Abandoning")
            dlg.Destroy()
            dlg = None
            return

        dlg.Destroy()

        self._ctrl.deselectAllShapes()
        frame = self._ctrl.getUmlFrame()
        if frame == -1:
            displayError(_("Can't print nonexistent frame..."), _("Error..."), self)
            return

        printout  = PyutPrintout(frame)
        printout2 = PyutPrintout(frame)
        preview   = PrintPreview(printout, printout2, self._printData)

        if not preview.Ok():
            displayError(_("An unknown error occurred while previewing"), _("Error..."), self)
            return

        frame = PreviewFrame(preview, self, _("Diagram preview"))
        frame.Initialize()
        frame.Centre(BOTH)

        try:
            frame.Show(True)
        except (ValueError, Exception) as e:
            displayError(_("An unknown error occurred while previewing"), _("Error..."), self)

    # noinspection PyUnusedLocal
    def _OnMnuFilePrint(self, event):
        """
        Print the current diagram

        @since 1.10
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        if self._ctrl.getDiagram() is None:
            displayError(_("No diagram to print !"), _("Error"), self)
            return
        self._ctrl.deselectAllShapes()
        datas = PrintDialogData()
        datas.SetPrintData(self._printData)
        datas.SetMinPage(1)
        datas.SetMaxPage(1)
        printer  = Printer(datas)
        printout = PyutPrintout(self._ctrl.getUmlFrame())

        if not printer.Print(self, printout, True):
            displayError(_("Cannot print"), _("Error"), self)

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
        import PyutVersion
        dlg = DlgAbout(self, -1, _("About PyUt ") + PyutVersion.getPyUtVersion())
        dlg.ShowModal()
        dlg.Destroy()

    # noinspection PyUnusedLocal
    def _OnMnuHelpIndex(self, event):
        """
        Display the help index

        @since 1.9
        @author C.Dutoit <dutoitc@hotmail.com>
        """

        import DlgHelp  # fixed for python 2.2 compatibility
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

            import PyutVersion
            v = PyutVersion.getPyUtVersion()
            if v in oldestVersions:
                msg = _("PyUt version ") + str(latestVersion) + _(" is available on http://pyut.sf.net")
            else:
                msg = _("No newer version yet !")

        # Display dialog box
        displayInformation(msg, _("Check for newer version"), self)

    # noinspection PyUnusedLocal
    def _OnMnuHelpWeb(self, event):
        """
        Launch PyUt web site

        @since 1.9
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        displayInformation(_("Please point your browser at http://pyut.sf.net"), _("Pyut''s web site"), self)  # TODO FIXME :-)

    # noinspection PyUnusedLocal
    def _OnMnuAddPyut(self, event):
        """
        Add Pyut UML Diagram.

        @since 1.19
        @author L. Burgbacher <lb@alawa.ch>
        """
        frame = self._ctrl.getUmlFrame()
        if frame is None:
            displayError(_("Please open a diagram to execute this action"), parent=self)
            return
        frame.addPyutHierarchy()
        project = self._fileHandling.getCurrentProject()
        project.setModified(True)
        self._ctrl.updateTitle()
        frame.Refresh()

    # noinspection PyUnusedLocal
    def _OnMnuAddOgl(self, event):
        """
        Add Pyut-Ogl UML Diagram.

        @since 1.19
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        frame = self._ctrl.getUmlFrame()
        if frame is None:
            displayError(_("Please open a diagram to execute this action"), parent=self)
            return
        frame.addOglHierarchy()
        frame.setModified(True)
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
                displayError(_("An error occurred while loading the project !"), parent=self)
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
        index = 0
        for el in self._prefs.getLastOpenedFilesList():
            self.mnuFile.SetLabel(self.lastOpenedFilesID[index], "&" + str(index+1) + " " + el)
            index += 1

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

    # def _setTitle(self):
    #     """
    #     Set the application title, fonction of version and current filename
    #
    #     @since 1.4
    #     @author C.Dutoit <dutoitc@hotmail.com>
    #     """
    #     self._mediator.updateTitle()

    def notifyTitleChanged(self):
        """
        Notify that the title changed.

        @since 1.50
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        self._ctrl.updateTitle()

    def OnImport(self, event):
        self._fileHandling.newProject()
        self._fileHandling.newDocument(CLASS_DIAGRAM)
        self._ctrl.updateTitle()
        cl = self.plugs[event.GetId()]
        obj = cl(self._ctrl.getUmlObjects(), self._ctrl.getUmlFrame())

        # Do plugin functionality
        BeginBusyCursor()
        try:
            wxYield()  # time to process the refresh in newDiagram
            obj.doImport()
        except (ValueError, Exception) as e:
            displayError(_("An error occured while executing the selected plugin"), _("Error..."), self)
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
        cl = self.plugs[event.GetId()]
        obj = cl(self._ctrl.getUmlObjects(), self._ctrl.getUmlFrame())

        # Do plugin functionality
        BeginBusyCursor()
        obj.doExport()
        EndBusyCursor()

    def OnToolPlugin(self, event):
        # Create a plugin instance
        cl = self.plugs[event.GetId()]
        obj = cl(self._ctrl.getUmlObjects(), self._ctrl.getUmlFrame())

        # Do plugin functionality
        BeginBusyCursor()
        try:
            obj.callDoAction()
            self.logger.info(f"After tool plugin do action")
        except (ValueError, Exception) as e:
            displayError(_("An error occurred while executing the selected plugin"), _("Error..."), self)
            self.logger.error(f'{e}')
        EndBusyCursor()

        # Refresh screen
        umlFrame = self._ctrl.getUmlFrame()
        if umlFrame is not None:
            umlFrame.Refresh()

    def OnToolboxMenuClick(self, event):
        self._ctrl.displayToolbox(self._toolboxesID[event.GetId()])

    # noinspection PyUnusedLocal
    # def _OnMnuEditShowToolbar(self, event):
    #     self._mainToolbar.Show(True)

    def _OnNewAction(self, event):
        """
        Call the mediator to specifiy the current action.

        Args:
            event:
        """
        self._ctrl.setCurrentAction(ACTIONS[event.GetId()])
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
            displayError(_("No frame to paste into"))
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
            displayError(_("No frame found !"))
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
        dlg = DlgPyutProperties(self, -1, self._ctrl, self._prefs)
        dlg.ShowModal()
        dlg.Destroy()
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

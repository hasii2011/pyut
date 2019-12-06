
from logging import Logger
from logging import getLogger

from wx import EVT_CLOSE
from wx import EVT_MENU

from wx import Frame
from wx import Menu
from wx import MenuBar
from wx import NewId

from org.pyut.PyutPreferences import PyutPreferences

from org.pyut.general.Mediator import Mediator

from org.pyut.plugins.PluginManager import PluginManager

from org.pyut.ui.tools.ActionCallbackType import ActionCallbackType
from org.pyut.ui.tools.SharedIdentifiers import SharedIdentifiers

from org.pyut.general.Globals import _


class MenuCreator:

    DEBUG_ERROR_VIEWS: bool = True      # TODO Make this a runtime flag

    def __init__(self, frame: Frame,  callbackMap: SharedIdentifiers.CallbackMap, lastOpenFilesID):

        self._containingFrame: Frame = frame
        self._callbackMap:     SharedIdentifiers.CallbackMap = callbackMap
        self.lastOpenedFilesID = lastOpenFilesID

        self.logger:  Logger          = getLogger(__name__)
        self._prefs:  PyutPreferences = PyutPreferences()
        self.plugMgr: PluginManager   = PluginManager()
        self._mnuFile: Menu           = Menu()

        self._plugs = {}                        # To store the plugins
        self._toolboxesID = {}                  # Association toolbox category/id

    def getFileMenu(self) -> Menu:
        return self._mnuFile

    def setFileMenu(self, theNewValue: Menu):
        self._mnuFile = theNewValue

    def getPlugs(self):
        return self._plugs

    def setPlugs(self, theNewValue):
        self._plugs = theNewValue

    def getToolboxIds(self):
        return self._toolboxesID

    def setToolboxIds(self, theNewValues):
        self._toolboxesID = theNewValues

    fileMenu    = property(getFileMenu, setFileMenu)
    plugs       = property(getPlugs, setPlugs)
    toolboxIds  = property(getToolboxIds, setToolboxIds)

    def initMenus(self):

        self.mnuFileNew = Menu()
        self.mnuFileNew.Append(SharedIdentifiers.ID_MNUFILENEWPROJECT,         _("&New project\tCtrl-N"), _("New project"))
        self.mnuFileNew.Append(SharedIdentifiers.ID_MNUFILENEWCLASSDIAGRAM,    _("New c&lass diagram\tCtrl-L"), _("New class diagram"))
        self.mnuFileNew.Append(SharedIdentifiers.ID_MNUFILENEWSEQUENCEDIAGRAM, _("New s&equence diagram\tCtrl-E"), _("New sequence diagram"))
        self.mnuFileNew.Append(SharedIdentifiers.ID_MNUFILENEWUSECASEDIAGRAM,  _("New &use-case diagram\tCtrl-U"), _("New use-case diagram"))

        self.fileMenu.Append(NewId(), _("&New"), self.mnuFileNew)
        self.fileMenu.Append(SharedIdentifiers.ID_MNUFILEINSERTPROJECT, _("&Insert a project...\t"), _("Insert a project in the current project..."))
        self.fileMenu.Append(SharedIdentifiers.ID_MNUFILEOPEN, _("&Open...\tCtrl-O"), _("Open a file..."))
        self.fileMenu.Append(SharedIdentifiers.ID_MNUFILESAVE, _("&Save\tCtrl-S"), _("Save current data"))
        self.fileMenu.Append(SharedIdentifiers.ID_MNUFILESAVEAS, _("Save &As...\tCtrl-A"), _("Save current data"))
        self.fileMenu.Append(SharedIdentifiers.ID_MNUPROJECTCLOSE, _("&Close project\tCtrl-W"), _("Close current project"))
        self.fileMenu.Append(SharedIdentifiers.ID_MNUFILEREMOVEDOCUMENT, _("&Remove document"), _("Remove the document from the project"))
        self.fileMenu.AppendSeparator()

        sub = self.makeExportMenu()

        if sub is None:
            sub = Menu()
        sub.Append(SharedIdentifiers.ID_MNUFILEEXPBMP, "&bmp",        _("Export data to a bitmap file"))
        sub.Append(SharedIdentifiers.ID_MNUFILEEXPJPG, "&jpeg",       _("Export data to a jpeg file"))
        sub.Append(SharedIdentifiers.ID_MNUFILEEXPPNG, "&png",        _("Export data to a png file"))
        sub.Append(SharedIdentifiers.ID_MNUFILEEXPPS,  "&Postscript", _("Export data to a postscript file"))
        sub.Append(SharedIdentifiers.ID_MNUFILEEXPPDF, "P&DF",        _("Export data to a PDF file"))

        if sub is not None:
            self.fileMenu.Append(NewId(), _("Export"), sub)

        sub = self.makeImportMenu()
        if sub is not None:
            self.fileMenu.Append(NewId(), _("Import"), sub)

        self.fileMenu.AppendSeparator()
        self.fileMenu.Append(SharedIdentifiers.ID_MNUFILEPYUTPROPER, _("PyUt P&roperties"), _("PyUt properties"))
        # self.fileMenu.Append(ID_MNUFILEDIAGRAMPROPER,_("&Diagram Properties"), _("Diagram properties"))
        self.fileMenu.AppendSeparator()
        self.fileMenu.Append(SharedIdentifiers.ID_MNUFILEPRINTSETUP, _("Print se&tup..."), _("Display the print setup dialog box"))
        self.fileMenu.Append(SharedIdentifiers.ID_MNUFILEPRINTPREV, _("Print pre&view"), _("Diagram preview before printing"))
        self.fileMenu.Append(SharedIdentifiers.ID_MNUFILEPRINT, _("&Print\tCtrl-P"), _("Print the current diagram"))
        self.fileMenu.AppendSeparator()

        #  Add Last opened files
        index = 0
        #  TODO : does not work ? verify function return...
        for el in self._prefs.getLastOpenedFilesList():
            index += 1
            # self.fileMenu.Append(self.lastOpenedFilesID[index - 1], "&" + str(index) + " " + el)
            lof: str = f"&{str(index)} {el}"
            self.logger.info(f'self.lastOpenedFilesID[index - 1]: {self.lastOpenedFilesID[index - 1]}  lof: {lof}  ')
            self.fileMenu.Append(self.lastOpenedFilesID[index - 1], lof)

        for index in range(index, self._prefs.getNbLOF()):
            # self.fileMenu.Append(self.lastOpenedFilesID[index], "&" + str(index + 1) + " -")
            lofAgain: str = f"&{str(index + 1)} -"
            self.fileMenu.Append(self.lastOpenedFilesID[index], lofAgain)

        self.fileMenu.AppendSeparator()
        self.fileMenu.Append(SharedIdentifiers.ID_MNUFILEEXIT, _("E&xit"), _("Exit PyUt"))

        mnuEdit = Menu()

        mnuEdit.Append(SharedIdentifiers.ID_MNUUNDO, _("&Undo\tCtrl-Z"), _("Undo the last performed action"))
        mnuEdit.Append(SharedIdentifiers.ID_MNUREDO, _("&Redo\tCtrl-Y"), _("Redo the last undone action"))
        mnuEdit.AppendSeparator()
        mnuEdit.Append(SharedIdentifiers.ID_MNUEDITCUT,    _("Cu&t\tCtrl-X"),   _("Cut selected data"))
        mnuEdit.Append(SharedIdentifiers.ID_MNUEDITCOPY,   _("&Copy\tCtrl-C"),  _("Copy selected data"))
        mnuEdit.Append(SharedIdentifiers.ID_MNUEDITPASTE,  _("&Paste\tCtrl-V"), _("Paste selected data"))
        mnuEdit.AppendSeparator()
        mnuEdit.Append(SharedIdentifiers.ID_MNUEDITSELECTALL, _("&Select all"), _("Select all elements"))
        mnuEdit.AppendSeparator()
        mnuEdit.Append(SharedIdentifiers.ID_MNUADDPYUTHIERARCHY, _("&Add Pyut hierarchy"), _("Add the UML Diagram of Pyut"))
        mnuEdit.Append(SharedIdentifiers.ID_MNUADDOGLHIERARCHY, _("Add &Ogl hierarchy"),   _("Add the UML Diagram of Pyut - Ogl"))
        if MenuCreator.DEBUG_ERROR_VIEWS is True:
            mnuEdit.AppendSeparator()
            mnuEdit.Append(SharedIdentifiers.ID_MENU_GRAPHIC_ERROR_VIEW, 'Show &Graphic Error View',  'Test graphical error view')
            mnuEdit.Append(SharedIdentifiers.ID_MENU_TEXT_ERROR_VIEW,    'Show &Text Error View',     'Test text error view')
            mnuEdit.Append(SharedIdentifiers.ID_MENU_RAISE_ERROR_VIEW,   'Show &Exception Error View', 'Test raising exception')
        # -----------------
        #    Tools menu
        # -----------------
        mnuTools = Menu()
        sub = self.makeToolsMenu()
        if sub is not None:
            mnuTools.Append(NewId(), _("Plugins tools"), sub)

        sub = self.makeToolboxesMenu()
        if sub is not None:
            mnuTools.Append(NewId(), _("toolboxes"), sub)

        mnuHelp = Menu()
        mnuHelp.Append(SharedIdentifiers.ID_MNUHELPINDEX, _("&Index"), _("Display help index"))
        mnuHelp.AppendSeparator()
        mnuHelp.Append(SharedIdentifiers.ID_MNUHELPVERSION, _("Check for newer versions"), _("Check if a newer version of Pyut exists"))
        mnuHelp.Append(SharedIdentifiers.ID_MNUHELPWEB, _("&Web site"), _("Open PyUt web site"))
        mnuHelp.Append(SharedIdentifiers.ID_DEBUG,      _("&Debug"), _("Open IPython shell"))
        mnuHelp.AppendSeparator()
        mnuHelp.Append(SharedIdentifiers.ID_MNUHELPABOUT, _("&About PyUt..."), _("Display the About PyUt dialog box"))

        mnuBar = MenuBar()
        mnuBar.Append(self.fileMenu, _("&File"))
        mnuBar.Append(mnuEdit, _("&Edit"))
        mnuBar.Append(mnuTools, _("&Tools"))
        mnuBar.Append(mnuHelp, "&?")

        containingFrame: Frame = self._containingFrame
        containingFrame.SetMenuBar(mnuBar)

        cb: SharedIdentifiers.CallbackMap = self._callbackMap

        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.NEW_PROJECT],       id=SharedIdentifiers.ID_MNUFILENEWPROJECT)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.NEW_CLASS_DIAGRAM], id=SharedIdentifiers.ID_MNUFILENEWCLASSDIAGRAM)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.NEW_SEQUENCE_DIAGRAM], id=SharedIdentifiers.ID_MNUFILENEWSEQUENCEDIAGRAM)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.NEW_USE_CASE_DIAGRAM], id=SharedIdentifiers.ID_MNUFILENEWUSECASEDIAGRAM)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.INSERT_PROJECT],   id=SharedIdentifiers.ID_MNUFILEINSERTPROJECT)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.FILE_OPEN],        id=SharedIdentifiers.ID_MNUFILEOPEN)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.FILE_SAVE],        id=SharedIdentifiers.ID_MNUFILESAVE)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.FILE_SAVE_AS],     id=SharedIdentifiers.ID_MNUFILESAVEAS)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.PROJECT_CLOSE],  id=SharedIdentifiers.ID_MNUPROJECTCLOSE)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.REMOVE_DOCUMENT],  id=SharedIdentifiers.ID_MNUFILEREMOVEDOCUMENT)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.PRINT_SETUP],      id=SharedIdentifiers.ID_MNUFILEPRINTSETUP)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.PRINT_PREVIEW],    id=SharedIdentifiers.ID_MNUFILEPRINTPREV)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.PRINT],           id=SharedIdentifiers.ID_MNUFILEPRINT)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.PYUT_PROPERTIES],  id=SharedIdentifiers.ID_MNUFILEPYUTPROPER)
        #  EVT_MENU(self, ID_MNUFILEDIAGRAMPROPER,self._OnMnuFileDiagramProperties)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.EXIT_PROGRAM],     id=SharedIdentifiers.ID_MNUFILEEXIT)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.PROGRAM_ABOUT],    id=SharedIdentifiers.ID_MNUHELPABOUT)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.HELP_INDEX],    id=SharedIdentifiers.ID_MNUHELPINDEX)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.HELP_VERSION],  id=SharedIdentifiers.ID_MNUHELPVERSION)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.HELP_WEB],      id=SharedIdentifiers.ID_MNUHELPWEB)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.ADD_PYUT_HIERARCHY],      id=SharedIdentifiers.ID_MNUADDPYUTHIERARCHY)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.ADD_OGL_HIERARCHY],       id=SharedIdentifiers.ID_MNUADDOGLHIERARCHY)

        if MenuCreator.DEBUG_ERROR_VIEWS is True:
            from org.pyut.experimental.DebugErrorViews import DebugErrorViews
            containingFrame.Bind(EVT_MENU, DebugErrorViews.debugGraphicErrorView, id=SharedIdentifiers.ID_MENU_GRAPHIC_ERROR_VIEW)
            containingFrame.Bind(EVT_MENU, DebugErrorViews.debugTextErrorView,    id=SharedIdentifiers.ID_MENU_TEXT_ERROR_VIEW)
            containingFrame.Bind(EVT_MENU, DebugErrorViews.debugRaiseErrorView,   id=SharedIdentifiers.ID_MENU_RAISE_ERROR_VIEW)

        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.EXPORT_BMP], id=SharedIdentifiers.ID_MNUFILEEXPBMP)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.EXPORT_JPG], id=SharedIdentifiers.ID_MNUFILEEXPJPG)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.EXPORT_PNG], id=SharedIdentifiers.ID_MNUFILEEXPPNG)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.EXPORT_PS],  id=SharedIdentifiers.ID_MNUFILEEXPPS)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.EXPORT_PDF], id=SharedIdentifiers.ID_MNUFILEEXPPDF)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.EDIT_CUT],       id=SharedIdentifiers.ID_MNUEDITCUT)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.EDIT_COPY],      id=SharedIdentifiers.ID_MNUEDITCOPY)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.EDIT_PASTE],     id=SharedIdentifiers.ID_MNUEDITPASTE)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.SELECT_ALL],     id=SharedIdentifiers.ID_MNUEDITSELECTALL)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.DEBUG],         id=SharedIdentifiers.ID_DEBUG)

        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.UNDO], id=SharedIdentifiers.ID_MNUUNDO)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.REDO], id=SharedIdentifiers.ID_MNUREDO)

        for index in range(self._prefs.getNbLOF()):
            containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.LAST_OPENED_FILES], id=self.lastOpenedFilesID[index])

        containingFrame.Bind(EVT_CLOSE, cb[ActionCallbackType.CLOSE])

    def makeExportMenu(self):
        """
        Make the export submenu.
        """
        plugs = self.plugMgr.getOutputPlugins()
        nb = len(plugs)
        if nb == 0:
            return None
        sub: Menu = Menu()
        cb:  SharedIdentifiers.CallbackMap = self._callbackMap

        for i in range(nb):
            pluginId = NewId()
            obj = plugs[i](None, None)
            sub.Append(pluginId, obj.getOutputFormat()[0])
            self._containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.EXPORT], id=pluginId)
            self.plugs[pluginId] = plugs[i]
        return sub

    def makeImportMenu(self):
        """
        Make the import submenu.
        """
        plugs = self.plugMgr.getInputPlugins()
        nb = len(plugs)
        if nb == 0:
            return None
        sub: Menu = Menu()
        cb: SharedIdentifiers.CallbackMap = self._callbackMap

        for i in range(nb):
            importId = NewId()
            obj = plugs[i](None, None)
            sub.Append(importId, obj.getInputFormat()[0])
            self._containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.IMPORT], id=importId)
            self.plugs[importId] = plugs[i]
        return sub

    def makeToolsMenu(self):
        """
        Make the tools submenu.
        """
        plugs = self.plugMgr.getToolPlugins()
        nb = len(plugs)
        if nb == 0:
            return None
        sub: Menu = Menu()
        cb: SharedIdentifiers.CallbackMap = self._callbackMap

        for i in range(nb):
            wxId = NewId()
            obj = plugs[i](None, None)
            sub.Append(wxId, obj.getMenuTitle())
            self._containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.TOOL_PLUGIN], id=wxId)
            self.plugs[wxId] = plugs[i]
        return sub

    def makeToolboxesMenu(self):
        """
        Make the toolboxes submenu.
        """
        mediator: Mediator = Mediator()
        # Get categories
        categories = mediator.getToolboxesCategories()
        nb = len(categories)
        if nb == 0:
            return None
        sub: Menu = Menu()
        cb: SharedIdentifiers.CallbackMap = self._callbackMap

        for category in categories:
            categoryId = NewId()
            self._toolboxesID[categoryId] = category
            sub.Append(categoryId, category)
            self._containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.TOOL_BOX_MENU], id=categoryId)
        return sub

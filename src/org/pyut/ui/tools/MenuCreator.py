
from typing import cast

from logging import Logger
from logging import getLogger

from wx import EVT_MENU
from wx import ID_ABOUT

from wx import Frame
from wx import ID_EXIT
from wx import Menu
from wx import MenuBar
from wx import NewId

from org.pyut.preferences.PyutPreferences import PyutPreferences

from org.pyut.general.Mediator import Mediator
from org.pyut.ui.frame.EditMenuHandler import EditMenuHandler
from org.pyut.ui.frame.FileMenuHandler import FileMenuHandler

from org.pyut.ui.tools.ActionCallbackType import ActionCallbackType
from org.pyut.ui.tools.SharedIdentifiers import SharedIdentifiers
from org.pyut.ui.tools.SharedTypes import SharedTypes

from org.pyut.general.Globals import _


class MenuCreator:

    DEBUG_ERROR_VIEWS: bool = True      # TODO Make this a runtime flag

    def __init__(self, frame: Frame,  callbackMap: SharedTypes.CallbackMap, lastOpenFilesID):

        from org.pyut.plugins.PluginManager import PluginManager    # Plugin Manager should not be in plugins directory

        self._containingFrame: Frame = frame
        self._callbackMap:     SharedTypes.CallbackMap = callbackMap
        self.lastOpenedFilesID = lastOpenFilesID

        self.logger:    Logger          = getLogger(__name__)
        self._prefs:    PyutPreferences = PyutPreferences()
        self.plugMgr:   PluginManager   = PluginManager()
        self._fileMenu: Menu            = Menu()
        self._editMenu: Menu            = Menu()

        self._plugins:     SharedTypes.PluginMap    = cast(SharedTypes.PluginMap, {})     # To store the plugins
        self._toolboxesID: SharedTypes.ToolboxIdMap = cast(SharedTypes.ToolboxIdMap, {})  # Association toolbox id

        self._fileMenuHandler: FileMenuHandler = FileMenuHandler(fileMenu=self.fileMenu, lastOpenFilesIDs=self.lastOpenedFilesID)
        self._editMenuHandler: EditMenuHandler = EditMenuHandler(editMenu=self.editMenu)

    @property
    def fileMenu(self) -> Menu:
        return self._fileMenu

    @fileMenu.setter
    def fileMenu(self, theNewValue: Menu):
        self._fileMenu = theNewValue

    @property
    def editMenu(self) -> Menu:
        return self._editMenu

    @property
    def plugins(self) -> SharedTypes.PluginMap:
        return self._plugins

    @plugins.setter
    def plugins(self, theNewValues: SharedTypes.PluginMap):
        self._plugins = theNewValues

    @property
    def toolboxIds(self) -> SharedTypes.ToolboxIdMap:
        return self._toolboxesID

    @toolboxIds.setter
    def toolboxIds(self, theNewValues: SharedTypes.ToolboxIdMap):
        self._toolboxesID = theNewValues

    @property
    def fileMenuHandler(self) -> FileMenuHandler:
        return self._fileMenuHandler

    @property
    def editMenuHandler(self) -> EditMenuHandler:
        return self._editMenuHandler

    def initMenus(self):

        self._initializeFileMenu()
        self._initializeEditMenu()

        # -----------------
        #    Tools menu
        # -----------------
        mnuTools = Menu()
        sub = self._makeToolsMenu()
        if sub is not None:
            mnuTools.Append(NewId(), _("Plugins tools"), sub)

        sub = self._makeToolboxesMenu()
        if sub is not None:
            mnuTools.Append(NewId(), _("toolboxes"), sub)

        # Plugins identified
        self.fileMenuHandler.plugins = self.plugins

        mnuHelp = Menu()
        mnuHelp.Append(ID_ABOUT, _("&About PyUt..."), _("Display the About PyUt dialog box"))
        mnuHelp.AppendSeparator()
        mnuHelp.Append(SharedIdentifiers.ID_MNU_HELP_INDEX, _("&Index"), _("Display help index"))
        mnuHelp.Append(SharedIdentifiers.ID_MNU_HELP_VERSION, _("Check for newer versions"), _("Check if a newer version of Pyut exists"))
        mnuHelp.Append(SharedIdentifiers.ID_MNU_HELP_WEB, _("&Web site"), _("Open PyUt web site"))
        mnuHelp.AppendSeparator()
        mnuHelp.Append(SharedIdentifiers.ID_DEBUG,      _("&Debug"), _("Open IPython shell"))

        mnuBar = MenuBar()
        mnuBar.Append(self.fileMenu, _("&File"))
        mnuBar.Append(self.editMenu, _("&Edit"))
        mnuBar.Append(mnuTools, _("&Tools"))
        mnuBar.Append(mnuHelp, "&Help")

        containingFrame: Frame = self._containingFrame
        containingFrame.SetMenuBar(mnuBar)

        cb: SharedTypes.CallbackMap = self._callbackMap

        self._bindFileMenuHandlers(containingFrame, self.fileMenuHandler)

        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.PROGRAM_ABOUT], id=ID_ABOUT)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.HELP_INDEX], id=SharedIdentifiers.ID_MNU_HELP_INDEX)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.HELP_VERSION], id=SharedIdentifiers.ID_MNU_HELP_VERSION)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.HELP_WEB], id=SharedIdentifiers.ID_MNU_HELP_WEB)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.DEBUG], id=SharedIdentifiers.ID_DEBUG)

        self._bindEditMenuHandlers(containingFrame, self.editMenuHandler)

    def _initializeFileMenu(self):

        fileMenu: Menu = self.fileMenu

        self.mnuFileNew = Menu()
        self.mnuFileNew.Append(SharedIdentifiers.ID_MNUFILENEWPROJECT, _("&New project\tCtrl-N"), _("New project"))
        self.mnuFileNew.Append(SharedIdentifiers.ID_MNU_FILE_NEW_CLASS_DIAGRAM, _("New c&lass diagram\tCtrl-L"), _("New class diagram"))
        self.mnuFileNew.Append(SharedIdentifiers.ID_MNU_FILE_NEW_SEQUENCE_DIAGRAM, _("New s&equence diagram\tCtrl-E"),
                               _("New sequence diagram"))
        self.mnuFileNew.Append(SharedIdentifiers.ID_MNU_FILE_NEW_USECASE_DIAGRAM, _("New &use-case diagram\tCtrl-U"),
                               _("New use-case diagram"))
        fileMenu.Append(NewId(), _("&New"), self.mnuFileNew)
        fileMenu.Append(SharedIdentifiers.ID_MNU_FILE_INSERT_PROJECT, _("&Insert a project...\t"),
                        _("Insert a project in the current project..."))
        fileMenu.Append(SharedIdentifiers.ID_MNU_FILE_OPEN, _("&Open...\tCtrl-O"), _("Open a file..."))
        fileMenu.Append(SharedIdentifiers.ID_MNU_FILE_SAVE, _("&Save\tCtrl-S"), _("Save current data"))
        fileMenu.Append(SharedIdentifiers.ID_MNUFILESAVEAS, _("Save &As...\tCtrl-A"), _("Save current data"))
        fileMenu.Append(SharedIdentifiers.ID_MNU_PROJECT_CLOSE, _("&Close project\tCtrl-W"), _("Close current project"))
        fileMenu.Append(SharedIdentifiers.ID_MNU_FILE_REMOVE_DOCUMENT, _("&Remove document"), _("Remove the document from the project"))
        fileMenu.AppendSeparator()

        fileMenuHandler: FileMenuHandler = self._fileMenuHandler

        sub = self._makeExportMenu(fileMenuHandler=fileMenuHandler)
        if sub is None:
            sub = Menu()
        if sub is not None:
            self.fileMenu.Append(NewId(), _("Export"), sub)
        sub = self._makeImportMenu(fileMenuHandler=fileMenuHandler)
        if sub is not None:
            self.fileMenu.Append(NewId(), _("Import"), sub)
        fileMenu.AppendSeparator()
        fileMenu.Append(SharedIdentifiers.ID_MENU_FILE_PYUT_PREFERENCES, _("PyUt P&references"), _("PyUt preferences"))
        # fileMenu.Append(ID_MNU_FILE_DIAGRAM_PROPERTIES,_("&Diagram Properties"), _("Diagram properties"))
        fileMenu.AppendSeparator()
        fileMenu.Append(SharedIdentifiers.ID_MNU_FILE_PRINT_SETUP, _("Print se&tup..."), _("Display the print setup dialog box"))
        fileMenu.Append(SharedIdentifiers.ID_MNU_FILE_PRINT_PREVIEW, _("Print pre&view"), _("Diagram preview before printing"))
        fileMenu.Append(SharedIdentifiers.ID_MNU_FILE_PRINT, _("&Print\tCtrl-P"), _("Print the current diagram"))
        fileMenu.AppendSeparator()
        sub = self._makeRecentlyOpenedMenu()
        fileMenu.Append(NewId(), _('Recently Opened'), sub)
        fileMenu.AppendSeparator()

        fileMenu.Append(ID_EXIT, _("E&xit"), _("Exit PyUt"))

    def _initializeEditMenu(self):

        mnuEdit: Menu = self._editMenu

        mnuEdit.Append(SharedIdentifiers.ID_MNU_UNDO, _("&Undo\tCtrl-Z"), _("Undo the last performed action"))
        mnuEdit.Append(SharedIdentifiers.ID_MNU_REDO, _("&Redo\tCtrl-Y"), _("Redo the last undone action"))
        mnuEdit.AppendSeparator()
        mnuEdit.Append(SharedIdentifiers.ID_MNU_EDIT_CUT, _("Cu&t\tCtrl-X"), _("Cut selected data"))
        mnuEdit.Append(SharedIdentifiers.ID_MNU_EDIT_COPY, _("&Copy\tCtrl-C"), _("Copy selected data"))
        mnuEdit.Append(SharedIdentifiers.ID_MNU_EDIT_PASTE, _("&Paste\tCtrl-V"), _("Paste selected data"))
        mnuEdit.AppendSeparator()
        mnuEdit.Append(SharedIdentifiers.ID_MNU_EDIT_SELECT_ALL, _("&Select all"), _("Select all elements"))
        mnuEdit.AppendSeparator()

        mnuEdit = self._initializeAddHierarchySubMenu(mnuEdit)

        if MenuCreator.DEBUG_ERROR_VIEWS is True:
            mnuEdit.AppendSeparator()
            mnuEdit = self._initializeErrorViewSubMenu(mnuEdit)

    def _initializeErrorViewSubMenu(self, mnuEdit: Menu) -> Menu:

        sub: Menu = Menu()
        sub.Append(SharedIdentifiers.ID_MENU_GRAPHIC_ERROR_VIEW, '&Graphic Error View',   'Test graphical error view')
        sub.Append(SharedIdentifiers.ID_MENU_TEXT_ERROR_VIEW,    '&Text Error View',      'Test text error view')
        sub.Append(SharedIdentifiers.ID_MENU_RAISE_ERROR_VIEW,   '&Exception Error View', 'Test raising exception')

        mnuEdit.Append(NewId(), _('Show Error View'), sub)

        return mnuEdit

    def _initializeAddHierarchySubMenu(self, mnuEdit: Menu) -> Menu:

        sub: Menu = Menu()
        sub.Append(SharedIdentifiers.ID_MNU_ADD_PYUT_HIERARCHY, _("&Pyut"), _("Add the UML Diagram of Pyut"))
        sub.Append(SharedIdentifiers.ID_MNU_ADD_OGL_HIERARCHY, _("&Ogl"), _("Add the UML Diagram of Pyut - Ogl"))

        mnuEdit.Append(NewId(), _('Add Hierarchy'), sub)

        return mnuEdit

    def _makeRecentlyOpenedMenu(self):

        sub: Menu = Menu()

        index = 0
        for index in range(index, self._prefs.getNbLOF()):
            # self.fileMenu.Append(self.lastOpenedFilesID[index], "&" + str(index + 1) + " -")
            lofAgain: str = f"&{str(index + 1)} -"
            sub.Append(self.lastOpenedFilesID[index], lofAgain)

        return sub

    def _makeExportMenu(self, fileMenuHandler: FileMenuHandler):
        """
        Make the export submenu.
        """
        plugs = self.plugMgr.getOutputPlugins()
        nb = len(plugs)
        if nb == 0:
            return None
        sub: Menu = Menu()

        for i in range(nb):
            pluginId = NewId()
            obj = plugs[i](None, None)
            sub.Append(pluginId, obj.getOutputFormat()[0])
            self._containingFrame.Bind(EVT_MENU, fileMenuHandler.onExport, id=pluginId)
            self.plugins[pluginId] = plugs[i]
        return sub

    def _makeImportMenu(self, fileMenuHandler: FileMenuHandler):
        """
        Make the import submenu.
        """
        plugs = self.plugMgr.getInputPlugins()
        nb = len(plugs)
        if nb == 0:
            return None
        sub: Menu = Menu()

        for i in range(nb):
            importId = NewId()
            obj = plugs[i](None, None)
            sub.Append(importId, obj.getInputFormat()[0])
            self._containingFrame.Bind(EVT_MENU, fileMenuHandler.onImport, id=importId)
            self.plugins[importId] = plugs[i]
        return sub

    def _makeToolsMenu(self):
        """
        Make the tools submenu.
        """
        plugs = self.plugMgr.getToolPlugins()
        nb = len(plugs)
        if nb == 0:
            return None
        sub: Menu = Menu()
        cb: SharedTypes.CallbackMap = self._callbackMap

        for i in range(nb):
            wxId = NewId()
            obj = plugs[i](None, None)
            sub.Append(wxId, obj.getMenuTitle())
            self._containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.TOOL_PLUGIN], id=wxId)
            self.plugins[wxId] = plugs[i]
        return sub

    def _makeToolboxesMenu(self):
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
        cb: SharedTypes.CallbackMap = self._callbackMap

        for category in categories:
            categoryId = NewId()
            self._toolboxesID[categoryId] = category
            sub.Append(categoryId, category)
            self._containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.TOOL_BOX_MENU], id=categoryId)
        return sub

    def _bindFileMenuHandlers(self, containingFrame: Frame, fileMenuHandler: FileMenuHandler):

        containingFrame.Bind(EVT_MENU, fileMenuHandler.onNewProject,        id=SharedIdentifiers.ID_MNUFILENEWPROJECT)
        containingFrame.Bind(EVT_MENU, fileMenuHandler.onNewClassDiagram,   id=SharedIdentifiers.ID_MNU_FILE_NEW_CLASS_DIAGRAM)
        containingFrame.Bind(EVT_MENU, fileMenuHandler.onNewSequenceDiagram, id=SharedIdentifiers.ID_MNU_FILE_NEW_SEQUENCE_DIAGRAM)
        containingFrame.Bind(EVT_MENU, fileMenuHandler.onNewUsecaseDiagram, id=SharedIdentifiers.ID_MNU_FILE_NEW_USECASE_DIAGRAM)
        containingFrame.Bind(EVT_MENU, fileMenuHandler.onFileInsertProject, id=SharedIdentifiers.ID_MNU_FILE_INSERT_PROJECT)
        containingFrame.Bind(EVT_MENU, fileMenuHandler.onFileOpen,          id=SharedIdentifiers.ID_MNU_FILE_OPEN)
        containingFrame.Bind(EVT_MENU, fileMenuHandler.onFileSave,          id=SharedIdentifiers.ID_MNU_FILE_SAVE)
        containingFrame.Bind(EVT_MENU, fileMenuHandler.onFileSaveAs,        id=SharedIdentifiers.ID_MNUFILESAVEAS)
        containingFrame.Bind(EVT_MENU, fileMenuHandler.onFileClose,         id=SharedIdentifiers.ID_MNU_PROJECT_CLOSE)
        containingFrame.Bind(EVT_MENU, fileMenuHandler.onRemoveDocument,    id=SharedIdentifiers.ID_MNU_FILE_REMOVE_DOCUMENT)
        containingFrame.Bind(EVT_MENU, fileMenuHandler.onPyutPreferences,   id=SharedIdentifiers.ID_MENU_FILE_PYUT_PREFERENCES)
        containingFrame.Bind(EVT_MENU, fileMenuHandler.onPrintSetup,        id=SharedIdentifiers.ID_MNU_FILE_PRINT_SETUP)
        containingFrame.Bind(EVT_MENU, fileMenuHandler.onPrintPreview,      id=SharedIdentifiers.ID_MNU_FILE_PRINT_PREVIEW)
        containingFrame.Bind(EVT_MENU, fileMenuHandler.onPrint,             id=SharedIdentifiers.ID_MNU_FILE_PRINT)

        #  EVT_MENU(self, ID_MNU_FILE_DIAGRAM_PROPERTIES,self._OnMnuFileDiagramProperties)

        for index in range(self._prefs.getNbLOF()):
            containingFrame.Bind(EVT_MENU, fileMenuHandler.onRecentlyOpenedFile, id=self.lastOpenedFilesID[index])

        containingFrame.Bind(EVT_MENU, fileMenuHandler.onExit, id=ID_EXIT)

    def _bindEditMenuHandlers(self, containingFrame: Frame, editMenuHandler: EditMenuHandler):

        cb: SharedTypes.CallbackMap = self._callbackMap

        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.UNDO], id=SharedIdentifiers.ID_MNU_UNDO)
        containingFrame.Bind(EVT_MENU, cb[ActionCallbackType.REDO], id=SharedIdentifiers.ID_MNU_REDO)

        containingFrame.Bind(EVT_MENU, editMenuHandler.onCut,   id=SharedIdentifiers.ID_MNU_EDIT_CUT)
        containingFrame.Bind(EVT_MENU, editMenuHandler.onCopy,  id=SharedIdentifiers.ID_MNU_EDIT_COPY)
        containingFrame.Bind(EVT_MENU, editMenuHandler.onPaste, id=SharedIdentifiers.ID_MNU_EDIT_PASTE)

        containingFrame.Bind(EVT_MENU, editMenuHandler.onAddPyut, id=SharedIdentifiers.ID_MNU_ADD_PYUT_HIERARCHY)
        containingFrame.Bind(EVT_MENU, editMenuHandler.onAddOgl,  id=SharedIdentifiers.ID_MNU_ADD_OGL_HIERARCHY)

        containingFrame.Bind(EVT_MENU, editMenuHandler.onSelectAll, id=SharedIdentifiers.ID_MNU_EDIT_SELECT_ALL)

        if MenuCreator.DEBUG_ERROR_VIEWS is True:
            from org.pyut.experimental.DebugErrorViews import DebugErrorViews
            containingFrame.Bind(EVT_MENU, DebugErrorViews.debugGraphicErrorView, id=SharedIdentifiers.ID_MENU_GRAPHIC_ERROR_VIEW)
            containingFrame.Bind(EVT_MENU, DebugErrorViews.debugTextErrorView, id=SharedIdentifiers.ID_MENU_TEXT_ERROR_VIEW)
            containingFrame.Bind(EVT_MENU, DebugErrorViews.debugRaiseErrorView, id=SharedIdentifiers.ID_MENU_RAISE_ERROR_VIEW)

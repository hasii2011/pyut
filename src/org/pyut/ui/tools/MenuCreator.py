
from typing import Callable

from logging import Logger
from logging import getLogger

from wx import EVT_MENU
from wx import ID_ABOUT
from wx import ID_EXIT

from wx import Frame
from wx import ID_PREFERENCES
from wx import Menu
from wx import MenuBar

from org.pyut.general.exceptions.InvalidCategoryException import InvalidCategoryException
from org.pyut.plugins.base.PyutIoPlugin import PyutIoPlugin
from org.pyut.plugins.base.PyutToPlugin import PyutToPlugin

from org.pyut.preferences.PyutPreferences import PyutPreferences

from org.pyut.ui.Mediator import Mediator
from org.pyut.general.exceptions.UnsupportedOperation import UnsupportedOperation

from org.pyut.ui.frame.EditMenuHandler import EditMenuHandler
from org.pyut.ui.frame.FileMenuHandler import FileMenuHandler
from org.pyut.ui.frame.HelpMenuHandler import HelpMenuHandler
from org.pyut.ui.frame.ToolsMenuHandler import ToolsMenuHandler

from org.pyut.ui.tools.SharedIdentifiers import SharedIdentifiers

# noinspection PyProtectedMember
from org.pyut.general.Globals import _
from org.pyut.ui.tools.SharedTypes import PluginMap
from org.pyut.ui.tools.SharedTypes import ToolboxIdMap


class MenuCreator:

    def __init__(self, frame: Frame, lastOpenFilesID):

        from org.pyut.plugins.PluginManager import PluginManager    # Plugin Manager should not be in plugins directory

        self._containingFrame: Frame = frame
        self.lastOpenedFilesID = lastOpenFilesID

        self.logger:    Logger          = getLogger(__name__)
        self._prefs:    PyutPreferences = PyutPreferences()
        self.plugMgr:   PluginManager   = PluginManager()

        self._plugins:    PluginMap    = PluginMap({})     # To store the plugins
        self._toolboxIds: ToolboxIdMap = ToolboxIdMap({})  # Dictionary id --> toolbox

    @property
    def fileMenu(self) -> Menu:
        raise UnsupportedOperation('Property is write only')

    @fileMenu.setter
    def fileMenu(self, fileMenu: Menu):
        self._fileMenu = fileMenu

    @property
    def editMenu(self) -> Menu:
        raise UnsupportedOperation('Property is write only')

    @editMenu.setter
    def editMenu(self, editMenu: Menu):
        self._editMenu = editMenu

    @property
    def toolsMenu(self) -> Menu:
        raise UnsupportedOperation('Property is write only')

    @toolsMenu.setter
    def toolsMenu(self, toolsMenu: Menu):
        self._toolsMenu: Menu = toolsMenu

    @property
    def helpMenu(self):
        raise UnsupportedOperation('Property is write only')

    @helpMenu.setter
    def helpMenu(self, helpMenu: Menu):
        self._helpMenu = helpMenu

    @property
    def toolPlugins(self) -> PluginMap:
        raise UnsupportedOperation('Property is write only')

    @toolPlugins.setter
    def toolPlugins(self, toolPlugins: PluginMap):
        self._toolPlugins = toolPlugins

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

    @property
    def toolboxIds(self) -> ToolboxIdMap:
        raise UnsupportedOperation('Property is write only')

    @toolboxIds.setter
    def toolboxIds(self, theNewValues: ToolboxIdMap):
        self._toolboxIds = theNewValues

    @property
    def fileMenuHandler(self) -> FileMenuHandler:
        raise UnsupportedOperation('Property is write only')

    @fileMenuHandler.setter
    def fileMenuHandler(self, fileMenuHandler: FileMenuHandler):
        self._fileMenuHandler = fileMenuHandler

    @property
    def editMenuHandler(self) -> EditMenuHandler:
        raise UnsupportedOperation('Property is write only')

    @editMenuHandler.setter
    def editMenuHandler(self, editMenuHandler: EditMenuHandler):
        self._editMenuHandler = editMenuHandler

    @property
    def toolsMenuHandler(self) -> ToolsMenuHandler:
        raise UnsupportedOperation('Property is write only')

    @toolsMenuHandler.setter
    def toolsMenuHandler(self, toolsMenuHandler: ToolsMenuHandler):
        self._toolsMenuHandler = toolsMenuHandler

    @property
    def helpMenuHandler(self) -> HelpMenuHandler:
        raise UnsupportedOperation('Property is write only')

    @helpMenuHandler.setter
    def helpMenuHandler(self, helpMenuHandler: HelpMenuHandler):
        self._helpMenuHandler = helpMenuHandler

    def initializeMenus(self):

        self._initializeFileMenu()
        self._initializeEditMenu()

        # -----------------
        #    Tools menu
        # -----------------
        # mnuTools = Menu()
        sub = self._makeToolsMenu()
        if sub is not None:
            self._toolsMenu.AppendSubMenu(sub, _("Tools"), _('Tools are here'))

        sub = self._makeToolboxesMenu()
        if sub is not None:
            self._toolsMenu.AppendSubMenu(sub, _("Toolboxes"), _('Toolboxes are here'))

        # Plugins identified
        self._fileMenuHandler.importPlugins = self._importPlugins
        self._fileMenuHandler.exportPlugins = self._exportPlugins

        self._initializeHelpMenu()

        mnuBar = MenuBar()
        mnuBar.Append(self._fileMenu,  _("&File"))
        mnuBar.Append(self._editMenu,  _("&Edit"))
        mnuBar.Append(self._toolsMenu, _("&Tools"))
        mnuBar.Append(self._helpMenu,  _("&Help"))

        containingFrame: Frame = self._containingFrame
        containingFrame.SetMenuBar(mnuBar)

        self._fileMenuHandler.setLastOpenedFilesItems()

        self._bindFileMenuHandlers(containingFrame, self._fileMenuHandler)
        self._bindEditMenuHandlers(containingFrame, self._editMenuHandler)
        self._bindHelpMenuHandlers(containingFrame, self._helpMenuHandler)

    def _initializeFileMenu(self):

        fileMenu: Menu = self._fileMenu

        self.mnuFileNew = Menu()
        self.mnuFileNew.Append(SharedIdentifiers.ID_MNUFILENEWPROJECT, _("&New project\tCtrl-N"), _("New project"))
        self.mnuFileNew.Append(SharedIdentifiers.ID_MNU_FILE_NEW_CLASS_DIAGRAM, _("New c&lass diagram\tCtrl-L"), _("New class diagram"))
        self.mnuFileNew.Append(SharedIdentifiers.ID_MNU_FILE_NEW_SEQUENCE_DIAGRAM, _("New s&equence diagram\tCtrl-E"),
                               _("New sequence diagram"))
        self.mnuFileNew.Append(SharedIdentifiers.ID_MNU_FILE_NEW_USECASE_DIAGRAM, _("New &use-case diagram\tCtrl-U"),
                               _("New use-case diagram"))
        fileMenu.AppendSubMenu(self.mnuFileNew, _("&New"))
        fileMenu.Append(SharedIdentifiers.ID_MNU_FILE_INSERT_PROJECT, _("&Insert a project...\t"),
                        _("Insert a project in the current project..."))
        fileMenu.Append(SharedIdentifiers.ID_MNU_FILE_OPEN, _("&Open...\tCtrl-O"), _("Open a file..."))
        fileMenu.Append(SharedIdentifiers.ID_MNU_FILE_SAVE, _("&Save\tCtrl-S"), _("Save current data"))
        fileMenu.Append(SharedIdentifiers.ID_MNUFILESAVEAS, _("Save &As..."), _("Save current data"))
        fileMenu.Append(SharedIdentifiers.ID_MNU_PROJECT_CLOSE, _("&Close project\tCtrl-W"), _("Close current project"))
        fileMenu.Append(SharedIdentifiers.ID_MNU_FILE_REMOVE_DOCUMENT, _("&Remove document"), _("Remove the document from the project"))
        fileMenu.AppendSeparator()

        fileMenuHandler: FileMenuHandler = self._fileMenuHandler

        sub = self._makeExportMenu(fileMenuHandler=fileMenuHandler)
        if sub is None:
            sub = Menu()
        if sub is not None:
            self._fileMenu.AppendSubMenu(sub, _("Export"))
        sub = self._makeImportMenu(fileMenuHandler=fileMenuHandler)
        if sub is not None:
            # self._fileMenu.AppendSubMenu(NewIdRef(), _("Import"), sub)
            self._fileMenu.AppendSubMenu(sub, _("Import"))
        fileMenu.AppendSeparator()
        fileMenu.Append(ID_PREFERENCES, _("P&references"), _("PyUt preferences"))
        # fileMenu.Append(ID_MNU_FILE_DIAGRAM_PROPERTIES,_("&Diagram Properties"), _("Diagram properties"))
        fileMenu.AppendSeparator()
        fileMenu.Append(SharedIdentifiers.ID_MNU_FILE_PRINT_SETUP, _("Print se&tup..."), _("Display the print setup dialog box"))
        fileMenu.Append(SharedIdentifiers.ID_MNU_FILE_PRINT_PREVIEW, _("Print pre&view"), _("Diagram preview before printing"))
        fileMenu.Append(SharedIdentifiers.ID_MNU_FILE_PRINT, _("&Print\tCtrl-P"), _("Print the current diagram"))
        fileMenu.AppendSeparator()
        sub = self._makeRecentlyOpenedMenu()
        fileMenu.AppendSubMenu(sub, _('Recently Opened'))
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
        mnuEdit.Append(SharedIdentifiers.ID_MNU_EDIT_SELECT_ALL, _("&Select all\tCtrl-A"), _("Select all elements"))
        mnuEdit.AppendSeparator()

        mnuEdit = self._initializeAddHierarchySubMenu(mnuEdit)

        if self._prefs.debugErrorViews is True:
            mnuEdit.AppendSeparator()
            # noinspection PyUnusedLocal
            mnuEdit = self._initializeErrorViewSubMenu(mnuEdit)

    def _initializeHelpMenu(self):

        mnuHelp = self._helpMenu

        mnuHelp.Append(ID_ABOUT, _("&About PyUt..."), _("Display the About PyUt dialog box"))
        mnuHelp.AppendSeparator()
        mnuHelp.Append(SharedIdentifiers.ID_MNU_HELP_VERSION, _("Check for newer versions"), _("Check if a newer version of Pyut exists"))
        mnuHelp.Append(SharedIdentifiers.ID_MNU_HELP_WEB,     _("&Web site"), _("Open PyUt web site"))
        mnuHelp.AppendSeparator()
        mnuHelp.Append(SharedIdentifiers.ID_DEBUG, _("&Debug"), _("Open IPython shell"))

    def _initializeErrorViewSubMenu(self, mnuEdit: Menu) -> Menu:

        sub: Menu = Menu()
        sub.Append(SharedIdentifiers.ID_MENU_GRAPHIC_ERROR_VIEW, '&Graphic Error View',   'Test graphical error view')
        sub.Append(SharedIdentifiers.ID_MENU_TEXT_ERROR_VIEW,    '&Text Error View',      'Test text error view')
        sub.Append(SharedIdentifiers.ID_MENU_RAISE_ERROR_VIEW,   '&Exception Error View', 'Test raising exception')

        mnuEdit.AppendSubMenu(sub, _('Show Error View'))

        return mnuEdit

    def _initializeAddHierarchySubMenu(self, mnuEdit: Menu) -> Menu:

        sub: Menu = Menu()
        sub.Append(SharedIdentifiers.ID_MNU_ADD_PYUT_HIERARCHY, _("&Pyut"), _("Add the UML Diagram of Pyut"))
        sub.Append(SharedIdentifiers.ID_MNU_ADD_OGL_HIERARCHY, _("&Ogl"), _("Add the UML Diagram of Pyut - Ogl"))

        mnuEdit.AppendSubMenu(sub,  _('Add Hierarchy'))

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
        pluginMap: PluginMap = self._exportPlugins
        sub:       Menu = Menu()

        for wxId in pluginMap:

            clazz: type = pluginMap[wxId]
            pluginInstance: PyutIoPlugin = clazz(None, None)

            pluginName: str = pluginInstance.getOutputFormat()[0]
            sub = self.__makeSubMenuEntry(subMenu=sub, wxId=wxId, pluginName=pluginName, callback=fileMenuHandler.onExport)
            # sub.Append(wxId, pluginName)
            # self._containingFrame.Bind(EVT_MENU, fileMenuHandler.onExport, id=wxId)

        return sub

    def _makeImportMenu(self, fileMenuHandler: FileMenuHandler):
        """
        Make the import submenu.
        """
        pluginMap: PluginMap = self._importPlugins

        sub: Menu = Menu()

        for wxId in pluginMap:

            clazz: type = pluginMap[wxId]
            pluginInstance: PyutIoPlugin = clazz(None, None)

            pluginName: str = pluginInstance.getInputFormat()[0]

            # sub.Append(wxId, pluginName)
            # self._containingFrame.Bind(EVT_MENU, fileMenuHandler.onImport, id=wxId)
            sub = self.__makeSubMenuEntry(subMenu=sub, wxId=wxId, pluginName=pluginName, callback=fileMenuHandler.onImport)
        return sub

    def _makeToolsMenu(self):
        """
        Make the Tools submenu.
        """
        pluginMap: PluginMap = self._toolPlugins
        sub:       Menu = Menu()

        for wxId in pluginMap:

            clazz: type = pluginMap[wxId]

            pluginInstance: PyutToPlugin = clazz(None, None)
            sub.Append(wxId, pluginInstance.getMenuTitle())

            self._containingFrame.Bind(EVT_MENU, self._toolsMenuHandler.onToolPlugin, id=wxId)

        return sub

    def _makeToolboxesMenu(self):
        """
        Make the Toolboxes submenu.
        """
        mediator: Mediator = Mediator()
        # Get categories
        categories = mediator.getToolboxesCategories()
        nb = len(categories)
        if nb == 0:
            return None
        sub: Menu = Menu()

        for category in categories:

            categoryId = self.__getWxId(category)
            sub.Append(categoryId, category)
            self._containingFrame.Bind(EVT_MENU, self._toolsMenuHandler.onToolboxMenuClick, id=categoryId)
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
        containingFrame.Bind(EVT_MENU, fileMenuHandler.onPrintSetup,        id=SharedIdentifiers.ID_MNU_FILE_PRINT_SETUP)
        containingFrame.Bind(EVT_MENU, fileMenuHandler.onPrintPreview,      id=SharedIdentifiers.ID_MNU_FILE_PRINT_PREVIEW)
        containingFrame.Bind(EVT_MENU, fileMenuHandler.onPrint,             id=SharedIdentifiers.ID_MNU_FILE_PRINT)

        #  EVT_MENU(self, ID_MNU_FILE_DIAGRAM_PROPERTIES,self._OnMnuFileDiagramProperties)

        for index in range(self._prefs.getNbLOF()):
            containingFrame.Bind(EVT_MENU, fileMenuHandler.onRecentlyOpenedFile, id=self.lastOpenedFilesID[index])

        containingFrame.Bind(EVT_MENU, fileMenuHandler.onPyutPreferences, id=ID_PREFERENCES)
        containingFrame.Bind(EVT_MENU, fileMenuHandler.onExit,            id=ID_EXIT)

    def _bindEditMenuHandlers(self, containingFrame: Frame, editMenuHandler: EditMenuHandler):

        containingFrame.Bind(EVT_MENU, editMenuHandler.onUndo, id=SharedIdentifiers.ID_MNU_UNDO)
        containingFrame.Bind(EVT_MENU, editMenuHandler.onRedo, id=SharedIdentifiers.ID_MNU_REDO)

        containingFrame.Bind(EVT_MENU, editMenuHandler.onCut,   id=SharedIdentifiers.ID_MNU_EDIT_CUT)
        containingFrame.Bind(EVT_MENU, editMenuHandler.onCopy,  id=SharedIdentifiers.ID_MNU_EDIT_COPY)
        containingFrame.Bind(EVT_MENU, editMenuHandler.onPaste, id=SharedIdentifiers.ID_MNU_EDIT_PASTE)

        containingFrame.Bind(EVT_MENU, editMenuHandler.onAddPyut, id=SharedIdentifiers.ID_MNU_ADD_PYUT_HIERARCHY)
        containingFrame.Bind(EVT_MENU, editMenuHandler.onAddOgl,  id=SharedIdentifiers.ID_MNU_ADD_OGL_HIERARCHY)

        containingFrame.Bind(EVT_MENU, editMenuHandler.onSelectAll, id=SharedIdentifiers.ID_MNU_EDIT_SELECT_ALL)

        if self._prefs.debugErrorViews is True:
            from org.pyut.experimental.DebugErrorViews import DebugErrorViews
            containingFrame.Bind(EVT_MENU, DebugErrorViews.debugGraphicErrorView, id=SharedIdentifiers.ID_MENU_GRAPHIC_ERROR_VIEW)
            containingFrame.Bind(EVT_MENU, DebugErrorViews.debugTextErrorView,    id=SharedIdentifiers.ID_MENU_TEXT_ERROR_VIEW)
            containingFrame.Bind(EVT_MENU, DebugErrorViews.debugRaiseErrorView,   id=SharedIdentifiers.ID_MENU_RAISE_ERROR_VIEW)

    def _bindHelpMenuHandlers(self, containingFrame: Frame, helpMenuHandler: HelpMenuHandler):

        containingFrame.Bind(EVT_MENU, helpMenuHandler.onAbout,       id=ID_ABOUT)
        containingFrame.Bind(EVT_MENU, helpMenuHandler.onHelpVersion, id=SharedIdentifiers.ID_MNU_HELP_VERSION)
        containingFrame.Bind(EVT_MENU, helpMenuHandler.onHelpWeb,     id=SharedIdentifiers.ID_MNU_HELP_WEB)
        containingFrame.Bind(EVT_MENU, helpMenuHandler.onDebug,       id=SharedIdentifiers.ID_DEBUG)

    def __makeSubMenuEntry(self, subMenu: Menu, wxId: int, pluginName: str, callback: Callable) -> Menu:

        subMenu.Append(wxId, pluginName)
        self._containingFrame.Bind(EVT_MENU, callback, id=wxId)

        return subMenu

    def __getWxId(self, categoryName: str):

        for key, value in self._toolboxIds.items():
            if categoryName == value:
                return key

        raise InvalidCategoryException(f'{categoryName} does not exist')

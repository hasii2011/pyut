
from typing import Callable

from logging import Logger
from logging import getLogger
from typing import cast

from wx import EVT_MENU
from wx import EVT_MENU_RANGE
from wx import ID_ABOUT
from wx import ID_CUT
from wx import ID_COPY
from wx import ID_FILE1
from wx import ID_FILE9
from wx import ID_OPEN
from wx import ID_PASTE
from wx import ID_EXIT
from wx import ID_REDO
from wx import ID_SAVE
from wx import ID_SAVEAS
from wx import ID_SELECTALL
from wx import ID_PREFERENCES

from wx import Frame
from wx import ID_UNDO
from wx import Menu
from wx import MenuBar

from pyutplugins.PluginManager import PluginManager

from pyutplugins.plugintypes.PluginDataTypes import PluginIDMap
from pyutplugins.plugintypes.PluginDataTypes import FormatName

from pyutplugins.plugininterfaces.IOPluginInterface import IOPluginInterface
from pyutplugins.plugininterfaces.ToolPluginInterface import ToolPluginInterface

from pyut.general.exceptions.InvalidCategoryException import InvalidCategoryException

from pyut.preferences.PyutPreferences import PyutPreferences

from pyut.general.exceptions.UnsupportedOperation import UnsupportedOperation

from pyut.ui.menuhandlers.EditMenuHandler import EditMenuHandler
from pyut.ui.menuhandlers.FileMenuHandler import FileMenuHandler
from pyut.ui.menuhandlers.HelpMenuHandler import HelpMenuHandler
from pyut.ui.menuhandlers.ToolsMenuHandler import ToolsMenuHandler

from pyut.ui.tools.SharedIdentifiers import SharedIdentifiers

from pyut.ui.tools.SharedTypes import ToolboxIdMap
from pyut.ui.tools.ToolboxTypes import CategoryNames
from pyut.ui.ToolBoxHandler import ToolBoxHandler


class MenuCreator:

    def __init__(self, frame: Frame, pluginManager: PluginManager):

        self._containingFrame: Frame = frame

        self.logger:       Logger          = getLogger(__name__)
        self._preferences: PyutPreferences = PyutPreferences()
        self.plugMgr:      PluginManager   = pluginManager

        self._plugins:    PluginIDMap   = PluginIDMap({})     # To store the plugins and their activation IDs
        self._toolboxIds: ToolboxIdMap = ToolboxIdMap({})  # Dictionary id --> toolbox

        self._fileMenu: Menu = cast(Menu, None)
        self._editMenu: Menu = cast(Menu, None)
        self._toolMenu: Menu = cast(Menu, None)
        self._helpMenu: Menu = cast(Menu, None)

        self._toolPlugins:   PluginIDMap = cast(PluginIDMap, None)
        self._exportPlugins: PluginIDMap = cast(PluginIDMap, None)
        self._importPlugins: PluginIDMap = cast(PluginIDMap, None)

        self._fileMenuHandler:  FileMenuHandler  = cast(FileMenuHandler, None)
        self._editMenuHandler:  EditMenuHandler  = cast(EditMenuHandler, None)
        self._toolsMenuHandler: ToolsMenuHandler = cast(ToolsMenuHandler, None)
        self._helpMenuHandler:  HelpMenuHandler  = cast(HelpMenuHandler, None)

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
        self._toolMenu = toolsMenu

    @property
    def helpMenu(self):
        raise UnsupportedOperation('Property is write only')

    @helpMenu.setter
    def helpMenu(self, helpMenu: Menu):
        self._helpMenu = helpMenu

    @property
    def toolPlugins(self) -> PluginIDMap:
        raise UnsupportedOperation('Property is write only')

    @toolPlugins.setter
    def toolPlugins(self, toolPlugins: PluginIDMap):
        self._toolPlugins = toolPlugins

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
        sub = self._makeToolMenu()
        if sub is not None:
            self._toolMenu.AppendSubMenu(sub, "Tools", 'Tools are here')

        sub = self._makeToolboxMenu()
        if sub is not None:
            self._toolMenu.AppendSubMenu(sub, "Toolboxes", 'Toolboxes are here')

        # Plugins identified
        self._fileMenuHandler.importPlugins = self._importPlugins
        self._fileMenuHandler.exportPlugins = self._exportPlugins

        self._initializeHelpMenu()

        mnuBar = MenuBar()
        mnuBar.Append(self._fileMenu,  "&File")
        mnuBar.Append(self._editMenu,  "&Edit")
        mnuBar.Append(self._toolMenu, "&Tools")
        mnuBar.Append(self._helpMenu,  "&Help")

        containingFrame: Frame = self._containingFrame
        containingFrame.SetMenuBar(mnuBar)

        self._bindFileMenuHandlers(containingFrame, self._fileMenuHandler)
        self._bindEditMenuHandlers(containingFrame, self._editMenuHandler)
        self._bindHelpMenuHandlers(containingFrame, self._helpMenuHandler)

    def _initializeFileMenu(self):

        fileMenu: Menu = self._fileMenu

        self.mnuFileNew = Menu()
        self.mnuFileNew.Append(SharedIdentifiers.ID_MENU_FILE_NEW_PROJECT, "&New project\tCtrl-N", "New project")
        self.mnuFileNew.Append(SharedIdentifiers.ID_MENU_FILE_NEW_CLASS_DIAGRAM, "New c&lass diagram\tCtrl-L", "New class diagram")
        self.mnuFileNew.Append(SharedIdentifiers.ID_MENU_FILE_NEW_SEQUENCE_DIAGRAM, "New s&equence diagram\tCtrl-E",
                               "New sequence diagram")
        self.mnuFileNew.Append(SharedIdentifiers.ID_MENU_FILE_NEW_USECASE_DIAGRAM, "New &use-case diagram\tCtrl-U",
                               "New use-case diagram")
        fileMenu.AppendSubMenu(self.mnuFileNew, "&New")
        fileMenu.Append(SharedIdentifiers.ID_MENU_FILE_INSERT_PROJECT, "&Insert a project...",
                        "Insert a project in the current project...")
        # Use stock identifier and properties
        fileMenu.Append(ID_OPEN)
        fileMenu.Append(ID_SAVE)
        fileMenu.Append(ID_SAVEAS)
        fileMenu.Append(SharedIdentifiers.ID_MENU_FILE_PROJECT_CLOSE, "&Close project\tCtrl-W", "Close current project")
        fileMenu.Append(SharedIdentifiers.ID_MENU_FILE_REMOVE_DIAGRAM, "&Delete diagram", "Delete the diagram from the project")
        fileMenu.AppendSeparator()

        fileMenuHandler: FileMenuHandler = self._fileMenuHandler

        sub = self._makeExportMenu(fileMenuHandler=fileMenuHandler)
        if sub is None:
            sub = Menu()
        if sub is not None:
            self._fileMenu.AppendSubMenu(sub, "Export")
        sub = self._makeImportMenu(fileMenuHandler=fileMenuHandler)
        if sub is not None:
            self._fileMenu.AppendSubMenu(sub, "Import")
        fileMenu.AppendSeparator()
        fileMenu.Append(ID_PREFERENCES, "P&references", "Pyut preferences")
        # fileMenu.Append(ID_MNU_FILE_DIAGRAM_PROPERTIES,_("&Diagram Properties"), _("Diagram properties"))
        fileMenu.AppendSeparator()
        fileMenu.Append(SharedIdentifiers.ID_MENU_FILE_PRINT_SETUP, "Print se&tup...", "Display the print setup dialog box")
        fileMenu.Append(SharedIdentifiers.ID_MENU_FILE_PRINT_PREVIEW, "Print pre&view", "Diagram preview before printing")
        fileMenu.Append(SharedIdentifiers.ID_MENU_FILE_PRINT, "&Print\tCtrl-P", "Print the current diagram")
        fileMenu.AppendSeparator()
        fileMenu.Append(SharedIdentifiers.ID_MENU_FILE_MANAGE_FILE_HISTORY, 'Manage Projects')
        fileMenu.AppendSeparator()
        # TODO:  Use File History manager to create the recently opened list here
        fileMenu.Append(ID_EXIT, "E&xit", "Exit PyUt")

    def _initializeEditMenu(self):

        mnuEdit: Menu = self._editMenu

        mnuEdit.Append(ID_UNDO)
        mnuEdit.Append(ID_REDO)
        mnuEdit.AppendSeparator()
        #
        # Use all the stock properties
        #
        mnuEdit.Append(ID_CUT)
        mnuEdit.Append(ID_COPY)
        mnuEdit.Append(ID_PASTE)
        mnuEdit.AppendSeparator()
        mnuEdit.Append(ID_SELECTALL)
        mnuEdit.AppendSeparator()

        mnuEdit = self._initializeAddDiagramSubMenu(mnuEdit)

        if self._preferences.debugErrorViews is True:
            mnuEdit.AppendSeparator()
            # noinspection PyUnusedLocal
            mnuEdit = self._initializeErrorViewSubMenu(mnuEdit)

    def _initializeHelpMenu(self):

        mnuHelp = self._helpMenu

        # Use the stock properties
        mnuHelp.Append(ID_ABOUT)
        mnuHelp.AppendSeparator()
        mnuHelp.Append(SharedIdentifiers.ID_MENU_HELP_VERSION, "Check for newer versions", "Check if a newer version of Pyut exists")
        mnuHelp.Append(SharedIdentifiers.ID_MENU_HELP_WEB, "&Web site", "Open Pyut web site")
        mnuHelp.AppendSeparator()
        if self._preferences.displayLoggingControl is True:
            mnuHelp.Append(SharedIdentifiers.ID_MENU_HELP_LOGGING_CONTROL, "&Logging Control", "Open Logging Control Dialog")
        if self._preferences.debugEventEngine is True:
            mnuHelp.Append(SharedIdentifiers.ID_MENU_HELP_DEBUG_EVENT_ENGINE, "Debug &Event Engine", "Open Debug Loggers")

    def _initializeErrorViewSubMenu(self, mnuEdit: Menu) -> Menu:

        sub: Menu = Menu()
        sub.Append(SharedIdentifiers.ID_MENU_GRAPHIC_ERROR_VIEW, '&Graphic Error View',   'Test graphical error view')
        sub.Append(SharedIdentifiers.ID_MENU_TEXT_ERROR_VIEW,    '&Text Error View',      'Test text error view')
        sub.Append(SharedIdentifiers.ID_MENU_RAISE_ERROR_VIEW,   '&Exception Error View', 'Test raising exception')

        mnuEdit.AppendSubMenu(sub, 'Show Error View')

        return mnuEdit

    def _initializeAddDiagramSubMenu(self, mnuEdit: Menu) -> Menu:

        sub: Menu = Menu()
        sub.Append(SharedIdentifiers.ID_MENU_EDIT_ADD_PYUT_DIAGRAM, "&Pyut Data Model", "Add the Pyut UML Diagram")
        sub.Append(SharedIdentifiers.ID_MENU_EDIT_ADD_OGL_DIAGRAM, "&Ogl Graphical Model", "Add the Ogl UML Diagram")

        mnuEdit.AppendSubMenu(sub,  'Add Diagram')

        return mnuEdit

    def _makeExportMenu(self, fileMenuHandler: FileMenuHandler):
        """
        Make the export submenu.
        """
        pluginMap: PluginIDMap = self._exportPlugins
        sub:       Menu = Menu()

        for wxId in pluginMap:
            # TODO figure out how to quiet mypy
            clazz: type = pluginMap[wxId]
            pluginInstance: IOPluginInterface = clazz(None)

            formatName: FormatName = pluginInstance.outputFormat.formatName
            sub = self.__makeSubMenuEntry(subMenu=sub, wxId=wxId, formatName=formatName, callback=fileMenuHandler.onExport)

        return sub

    def _makeImportMenu(self, fileMenuHandler: FileMenuHandler) -> Menu:
        """
        Make the import submenu.
        """
        pluginMap: PluginIDMap = self._importPlugins

        sub: Menu = Menu()

        for wxId in pluginMap:
            # TODO figure out how to quiet mypy
            clazz: type = pluginMap[wxId]
            pluginInstance: IOPluginInterface = clazz(None)

            formatName: FormatName = pluginInstance.inputFormat.formatName
            sub = self.__makeSubMenuEntry(subMenu=sub, wxId=wxId, formatName=formatName, callback=fileMenuHandler.onImport)

        return sub

    def _makeToolMenu(self):
        """
        Make the Tools submenu.
        """
        pluginMap: PluginIDMap = self._toolPlugins
        sub:       Menu = Menu()

        for wxId in pluginMap:

            clazz: type = pluginMap[wxId]

            pluginInstance: ToolPluginInterface = clazz(None)
            sub.Append(wxId, pluginInstance.menuTitle)

            self._containingFrame.Bind(EVT_MENU, self._toolsMenuHandler.onToolPlugin, id=wxId)

        return sub

    def _makeToolboxMenu(self):
        """
        Make the Toolboxes submenu.
        """
        # mediator: Mediator = Mediator()
        toolBoxHandler: ToolBoxHandler = ToolBoxHandler()
        # Get categories
        # categories = mediator.getToolboxesCategories()
        categories: CategoryNames = toolBoxHandler.toolBoxCategoryNames
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

        containingFrame.Bind(EVT_MENU, fileMenuHandler.onNewProject, id=SharedIdentifiers.ID_MENU_FILE_NEW_PROJECT)
        containingFrame.Bind(EVT_MENU, fileMenuHandler.onNewClassDiagram, id=SharedIdentifiers.ID_MENU_FILE_NEW_CLASS_DIAGRAM)
        containingFrame.Bind(EVT_MENU, fileMenuHandler.onNewSequenceDiagram, id=SharedIdentifiers.ID_MENU_FILE_NEW_SEQUENCE_DIAGRAM)
        containingFrame.Bind(EVT_MENU, fileMenuHandler.onNewUsecaseDiagram, id=SharedIdentifiers.ID_MENU_FILE_NEW_USECASE_DIAGRAM)
        containingFrame.Bind(EVT_MENU, fileMenuHandler.onFileInsertProject, id=SharedIdentifiers.ID_MENU_FILE_INSERT_PROJECT)
        containingFrame.Bind(EVT_MENU, fileMenuHandler.onFileOpen,          id=ID_OPEN)
        containingFrame.Bind(EVT_MENU, fileMenuHandler.onFileSave,          id=ID_SAVE)
        containingFrame.Bind(EVT_MENU, fileMenuHandler.onFileSaveAs,        id=ID_SAVEAS)
        containingFrame.Bind(EVT_MENU, fileMenuHandler.onFileClose, id=SharedIdentifiers.ID_MENU_FILE_PROJECT_CLOSE)
        containingFrame.Bind(EVT_MENU, fileMenuHandler.onDeleteDiagram, id=SharedIdentifiers.ID_MENU_FILE_REMOVE_DIAGRAM)
        containingFrame.Bind(EVT_MENU, fileMenuHandler.onPrintSetup, id=SharedIdentifiers.ID_MENU_FILE_PRINT_SETUP)
        containingFrame.Bind(EVT_MENU, fileMenuHandler.onPrintPreview, id=SharedIdentifiers.ID_MENU_FILE_PRINT_PREVIEW)
        containingFrame.Bind(EVT_MENU, fileMenuHandler.onPrint, id=SharedIdentifiers.ID_MENU_FILE_PRINT)

        #  EVT_MENU(self, ID_MNU_FILE_DIAGRAM_PROPERTIES,self._OnMnuFileDiagramProperties)

        containingFrame.Bind(EVT_MENU, fileMenuHandler.onPyutPreferences, id=ID_PREFERENCES)
        containingFrame.Bind(EVT_MENU, fileMenuHandler.onExit,            id=ID_EXIT)

        containingFrame.Bind(EVT_MENU,       fileMenuHandler.onManageFileHistory, id=SharedIdentifiers.ID_MENU_FILE_MANAGE_FILE_HISTORY)

        containingFrame.Bind(EVT_MENU_RANGE, fileMenuHandler.onOpenRecent, id=ID_FILE1, id2=ID_FILE9)

    def _bindEditMenuHandlers(self, containingFrame: Frame, editMenuHandler: EditMenuHandler):

        containingFrame.Bind(EVT_MENU, editMenuHandler.onUndo, id=ID_UNDO)
        containingFrame.Bind(EVT_MENU, editMenuHandler.onRedo, id=ID_REDO)

        containingFrame.Bind(EVT_MENU, editMenuHandler.onCut,   id=ID_CUT)
        containingFrame.Bind(EVT_MENU, editMenuHandler.onCopy,  id=ID_COPY)
        containingFrame.Bind(EVT_MENU, editMenuHandler.onPaste, id=ID_PASTE)

        containingFrame.Bind(EVT_MENU, editMenuHandler.onAddPyut, id=SharedIdentifiers.ID_MENU_EDIT_ADD_PYUT_DIAGRAM)
        containingFrame.Bind(EVT_MENU, editMenuHandler.onAddOgl, id=SharedIdentifiers.ID_MENU_EDIT_ADD_OGL_DIAGRAM)

        containingFrame.Bind(EVT_MENU, editMenuHandler.onSelectAll, id=ID_SELECTALL)

        if self._preferences.debugErrorViews is True:
            from pyut.experimental.DebugErrorViews import DebugErrorViews
            containingFrame.Bind(EVT_MENU, DebugErrorViews.debugGraphicErrorView, id=SharedIdentifiers.ID_MENU_GRAPHIC_ERROR_VIEW)
            containingFrame.Bind(EVT_MENU, DebugErrorViews.debugTextErrorView,    id=SharedIdentifiers.ID_MENU_TEXT_ERROR_VIEW)
            containingFrame.Bind(EVT_MENU, DebugErrorViews.debugRaiseErrorView,   id=SharedIdentifiers.ID_MENU_RAISE_ERROR_VIEW)

    def _bindHelpMenuHandlers(self, containingFrame: Frame, helpMenuHandler: HelpMenuHandler):

        containingFrame.Bind(EVT_MENU, helpMenuHandler.onAbout,            id=ID_ABOUT)
        containingFrame.Bind(EVT_MENU, helpMenuHandler.onHelpVersion,      id=SharedIdentifiers.ID_MENU_HELP_VERSION)
        containingFrame.Bind(EVT_MENU, helpMenuHandler.onHelpWeb,          id=SharedIdentifiers.ID_MENU_HELP_WEB)
        containingFrame.Bind(EVT_MENU, helpMenuHandler.onDebug, id=SharedIdentifiers.ID_MENU_HELP_LOGGING_CONTROL)
        containingFrame.Bind(EVT_MENU, helpMenuHandler.onDebugEventEngine, id=SharedIdentifiers.ID_MENU_HELP_DEBUG_EVENT_ENGINE)

    def __makeSubMenuEntry(self, subMenu: Menu, wxId: int, formatName: str, callback: Callable) -> Menu:

        subMenu.Append(wxId, formatName)
        self._containingFrame.Bind(EVT_MENU, callback, id=wxId)

        return subMenu

    def __getWxId(self, categoryName: str):

        for key, value in self._toolboxIds.items():
            if categoryName == value:
                return key

        raise InvalidCategoryException(f'{categoryName} does not exist')


from typing import List
from typing import Union
from typing import cast

from logging import Logger
from logging import getLogger
from logging import DEBUG

from wx import CANCEL
from wx import CENTRE
from wx import EVT_MENU
from wx import EVT_MENU_CLOSE
from wx import EVT_NOTEBOOK_PAGE_CHANGED
from wx import EVT_TREE_ITEM_RIGHT_CLICK
from wx import EVT_TREE_SEL_CHANGED
from wx import ICON_ERROR
from wx import ICON_QUESTION
from wx import ID_OK
from wx import ID_YES
from wx import OK
from wx import YES_NO
from wx import ITEM_NORMAL

from wx import ClientDC
from wx import SplitterWindow
from wx import CommandProcessor
from wx import Frame
from wx import TreeEvent
from wx import TreeItemId
from wx import CommandEvent
from wx import MenuEvent
from wx import Menu
from wx import MessageBox
from wx import MessageDialog
from wx import TextEntryDialog

from wx import Yield as wxYield

from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.PyutNote import PyutNote
from pyutmodelv2.PyutText import PyutText
from pyutmodelv2.PyutActor import PyutActor
from pyutmodelv2.PyutUseCase import PyutUseCase

from ogl.OglObject import OglObject
from ogl.OglClass import OglClass
from ogl.OglInterface2 import OglInterface2

from oglio.Types import OglDocument
from oglio.Types import OglProject

from pyutplugins.ExternalTypes import CurrentProjectCallback
from pyutplugins.ExternalTypes import FrameInformation
from pyutplugins.ExternalTypes import FrameInformationCallback
from pyutplugins.ExternalTypes import FrameSize
from pyutplugins.ExternalTypes import FrameSizeCallback
from pyutplugins.ExternalTypes import OglObjects
from pyutplugins.ExternalTypes import PluginProject
from pyutplugins.ExternalTypes import SelectedOglObjectsCallback

from pyut.PyutConstants import PyutConstants
from pyut.PyutUtils import PyutUtils

from pyut.ui.dialogs.DlgEditClass import DlgEditClass
from pyut.ui.dialogs.DlgEditInterface import DlgEditInterface

from pyut.ui.dialogs.Wrappers import DlgEditActor
from pyut.ui.dialogs.Wrappers import DlgEditUseCase

from pyut.ui.dialogs.textdialogs.DlgEditNote import DlgEditNote
from pyut.ui.dialogs.textdialogs.DlgEditText import DlgEditText

from pyut.enums.DiagramType import DiagramType

from pyut.ui.Action import Action

from pyut.ui.tools.SharedIdentifiers import SharedIdentifiers

from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame
from pyut.ui.umlframes.UmlFrame import UmlObjects

from pyut.ui.IPyutDocument import IPyutDocument
from pyut.ui.IPyutProject import IPyutProject

from pyut.ui.DiagramNotebook import DiagramNotebook
from pyut.ui.LayoutEngine import LayoutEngine
from pyut.ui.PluginProjectCreator import PluginProjectCreator
from pyut.ui.ProjectException import ProjectException
from pyut.ui.ProjectException import ProjectExceptionType
from pyut.ui.ProjectManager import ProjectManager
from pyut.ui.ProjectManager import PyutProjects
from pyut.ui.ProjectTree import ProjectTree
from pyut.ui.PyutDocument import PyutDocument
from pyut.ui.PyutProject import PyutProject
from pyut.ui.PyutProject import UmlFrameType

from pyut.ui.Types import createDiagramFrame

from pyut.ui.eventengine.EventType import EventType

from pyut.ui.eventengine.EventEngine import NewNamedProjectCallback

from pyut.ui.eventengine.Events import EVENT_ACTIVE_PROJECT_INFORMATION
from pyut.ui.eventengine.Events import EVENT_ADD_SHAPE
from pyut.ui.eventengine.Events import EVENT_CLOSE_PROJECT
from pyut.ui.eventengine.Events import EVENT_EDIT_ACTOR
from pyut.ui.eventengine.Events import EVENT_EDIT_CLASS
from pyut.ui.eventengine.Events import EVENT_ACTIVE_UML_FRAME
from pyut.ui.eventengine.Events import EVENT_EDIT_INTERFACE
from pyut.ui.eventengine.Events import EVENT_EDIT_NOTE
from pyut.ui.eventengine.Events import EVENT_EDIT_TEXT
from pyut.ui.eventengine.Events import EVENT_EDIT_USE_CASE
from pyut.ui.eventengine.Events import EVENT_FRAME_INFORMATION
from pyut.ui.eventengine.Events import EVENT_FRAME_SIZE
from pyut.ui.eventengine.Events import EVENT_MINI_PROJECT_INFORMATION
from pyut.ui.eventengine.Events import EVENT_INSERT_PROJECT
from pyut.ui.eventengine.Events import EVENT_NEW_DIAGRAM
from pyut.ui.eventengine.Events import EVENT_NEW_NAMED_PROJECT
from pyut.ui.eventengine.Events import EVENT_NEW_PROJECT
from pyut.ui.eventengine.Events import EVENT_NEW_PROJECT_DIAGRAM
from pyut.ui.eventengine.Events import EVENT_OPEN_PROJECT
from pyut.ui.eventengine.Events import EVENT_DELETE_DIAGRAM
from pyut.ui.eventengine.Events import EVENT_REFRESH_FRAME
from pyut.ui.eventengine.Events import EVENT_REQUEST_CURRENT_PROJECT
from pyut.ui.eventengine.Events import EVENT_SAVE_PROJECT
from pyut.ui.eventengine.Events import EVENT_SAVE_PROJECT_AS
from pyut.ui.eventengine.Events import EVENT_SELECTED_OGL_OBJECTS
from pyut.ui.eventengine.Events import EVENT_UML_DIAGRAM_MODIFIED
from pyut.ui.eventengine.Events import EditActorEvent
from pyut.ui.eventengine.Events import EditInterfaceEvent
from pyut.ui.eventengine.Events import EditNoteEvent
from pyut.ui.eventengine.Events import EditTextEvent
from pyut.ui.eventengine.Events import EditUseCaseEvent
from pyut.ui.eventengine.Events import AddShapeEvent
from pyut.ui.eventengine.Events import ActiveUmlFrameEvent
from pyut.ui.eventengine.Events import FrameInformationEvent
from pyut.ui.eventengine.Events import FrameSizeEvent
from pyut.ui.eventengine.Events import MiniProjectInformationEvent
from pyut.ui.eventengine.Events import InsertProjectEvent
from pyut.ui.eventengine.Events import NewDiagramEvent
from pyut.ui.eventengine.Events import NewNamedProjectEvent
from pyut.ui.eventengine.Events import NewProjectDiagramEvent
from pyut.ui.eventengine.Events import NewProjectEvent
from pyut.ui.eventengine.Events import OpenProjectEvent
from pyut.ui.eventengine.Events import RefreshFrameEvent
from pyut.ui.eventengine.Events import RequestCurrentProjectEvent
from pyut.ui.eventengine.Events import SaveProjectAsEvent
from pyut.ui.eventengine.Events import SaveProjectEvent
from pyut.ui.eventengine.Events import SelectedOglObjectsEvent
from pyut.ui.eventengine.Events import UMLDiagramModifiedEvent
from pyut.ui.eventengine.Events import EditClassEvent
from pyut.ui.eventengine.Events import ActiveProjectInformationEvent

from pyut.ui.eventengine.eventinformation.MiniProjectInformation import MiniProjectInformation
from pyut.ui.eventengine.eventinformation.ActiveProjectInformation import ActiveProjectInformation
from pyut.ui.eventengine.eventinformation.NewProjectDiagramInformation import NewProjectDiagramCallback
from pyut.ui.eventengine.eventinformation.NewProjectDiagramInformation import NewProjectDiagramInformation

from pyut.ui.eventengine.EventEngine import ActiveProjectInformationCallback

from pyut.ui.eventengine.IEventEngine import IEventEngine

TreeDataType        = Union[PyutProject, PyutDocument]

SASH_POSITION:                 int = 160        # TODO make this a preference and remember it
MAX_NOTEBOOK_PAGE_NAME_LENGTH: int = 12         # TODO make this a preference

NO_DIAGRAM_FRAME: UmlDiagramsFrame = cast(UmlDiagramsFrame, None)
NO_PYUT_PROJECT:  IPyutProject     = cast(IPyutProject, None)
NO_PYUT_DIAGRAM:  IPyutDocument    = cast(IPyutDocument, None)
NO_MENU:          Menu             = cast(Menu, None)


class PyutUI(SplitterWindow):

    def __init__(self, topLevelWindow: Frame, eventEngine: IEventEngine):

        super().__init__(parent=topLevelWindow)

        self.logger: Logger = getLogger(__name__)

        self._parentWindow:     Frame            = topLevelWindow
        self._eventEngine:      IEventEngine     = eventEngine
        self._projectTree:      ProjectTree      = ProjectTree(parentWindow=self)
        self._diagramNotebook:  DiagramNotebook  = DiagramNotebook(parentWindow=self, eventEngine=eventEngine)
        self._frame:            UmlDiagramsFrame = cast(UmlDiagramsFrame, None)
        # Set splitter
        self.SetMinimumPaneSize(20)
        self.SplitVertically(self._projectTree, self._diagramNotebook, SASH_POSITION)

        self._notebookCurrentPageNumber: int  = -1
        self._projectPopupMenu:          Menu = NO_MENU
        self._documentPopupMenu:         Menu = NO_MENU

        self._projectManager: ProjectManager = ProjectManager(projectTree=self._projectTree, diagramNoteBook=self._diagramNotebook)

        self._parentWindow.Bind(EVT_NOTEBOOK_PAGE_CHANGED, self._onDiagramNotebookPageChanged)
        self._parentWindow.Bind(EVT_TREE_SEL_CHANGED,      self._onProjectTreeSelectionChanged)
        self._projectTree.Bind(EVT_TREE_ITEM_RIGHT_CLICK,  self._onProjectTreeRightClick)
        #
        # Register listeners for things I do that the rest of the application wants
        #
        # Reuse the event handlers on the popup menu;  It does not use the passed in event
        self._eventEngine.registerListener(pyEventBinder=EVENT_DELETE_DIAGRAM,       callback=self._onDeleteDiagram)
        self._eventEngine.registerListener(pyEventBinder=EVENT_NEW_PROJECT,          callback=self._onNewProject)
        self._eventEngine.registerListener(pyEventBinder=EVENT_NEW_NAMED_PROJECT,    callback=self._onNewNamedProject)
        self._eventEngine.registerListener(pyEventBinder=EVENT_NEW_DIAGRAM,          callback=self._onNewDiagram)
        self._eventEngine.registerListener(pyEventBinder=EVENT_NEW_PROJECT_DIAGRAM,  callback=self._onNewProjectDiagram)
        self._eventEngine.registerListener(pyEventBinder=EVENT_OPEN_PROJECT,         callback=self._onOpenProject)
        self._eventEngine.registerListener(pyEventBinder=EVENT_CLOSE_PROJECT,        callback=self._onCloseProject)
        self._eventEngine.registerListener(pyEventBinder=EVENT_SAVE_PROJECT,         callback=self._onSaveProject)
        self._eventEngine.registerListener(pyEventBinder=EVENT_SAVE_PROJECT_AS,      callback=self._onSaveProjectAs)
        self._eventEngine.registerListener(pyEventBinder=EVENT_INSERT_PROJECT,       callback=self._onInsertProject)
        self._eventEngine.registerListener(pyEventBinder=EVENT_UML_DIAGRAM_MODIFIED, callback=self._onDiagramModified)

        self._eventEngine.registerListener(pyEventBinder=EVENT_MINI_PROJECT_INFORMATION,   callback=self._onMiniProjectInformation)
        self._eventEngine.registerListener(pyEventBinder=EVENT_ACTIVE_UML_FRAME, callback=self._onGetActiveUmlFrame)
        self._eventEngine.registerListener(pyEventBinder=EVENT_ACTIVE_PROJECT_INFORMATION, callback=self._onActiveProjectInformation)
        # TODO:  Should these handler go somewhere else
        self._eventEngine.registerListener(pyEventBinder=EVENT_EDIT_CLASS,     callback=self._onEditClass)
        self._eventEngine.registerListener(pyEventBinder=EVENT_EDIT_NOTE,      callback=self._onEditNote)
        self._eventEngine.registerListener(pyEventBinder=EVENT_EDIT_TEXT,      callback=self._onEditText)
        self._eventEngine.registerListener(pyEventBinder=EVENT_EDIT_ACTOR,     callback=self._onEditActor)
        self._eventEngine.registerListener(pyEventBinder=EVENT_EDIT_USE_CASE,  callback=self._onEditUseCase)
        self._eventEngine.registerListener(pyEventBinder=EVENT_EDIT_INTERFACE, callback=self._onEditInterface)
        #
        # Following provided for the Plugin Adapter
        self._eventEngine.registerListener(pyEventBinder=EVENT_ADD_SHAPE,            callback=self._onAddShape)
        self._eventEngine.registerListener(pyEventBinder=EVENT_FRAME_INFORMATION,    callback=self._onFrameInformation)
        self._eventEngine.registerListener(pyEventBinder=EVENT_FRAME_SIZE,           callback=self._onFrameSize)
        self._eventEngine.registerListener(pyEventBinder=EVENT_SELECTED_OGL_OBJECTS, callback=self._selectedOglObjects)
        self._eventEngine.registerListener(pyEventBinder=EVENT_REFRESH_FRAME,        callback=self._refreshFrame)

        self._eventEngine.registerListener(pyEventBinder=EVENT_REQUEST_CURRENT_PROJECT, callback=self._pluginRequestCurrentProject)

    def handleUnsavedProjects(self):
        """
        Close all files

        Returns:
            True if everything is ok
        """
        # Close projects and ask how to handle unsaved, modified projects
        projects: PyutProjects = self._projectManager.projects
        for project in projects:
            pyutProject: IPyutProject = cast(IPyutProject, project)
            if pyutProject.modified is True:
                dlg: MessageDialog = MessageDialog(self._parentWindow,
                                                   f"Project `{pyutProject.projectName}` has not been saved! Would you like to save it?",
                                                   "Save changes?",
                                                   YES_NO | ICON_QUESTION)
                if dlg.ShowModal() == ID_YES:
                    self._projectManager.saveProject(projectToSave=pyutProject)
                dlg.Destroy()

        self._diagramNotebook.DeleteAllPages()

    def closeDefaultEmptyProject(self):

        defaultProject: IPyutProject = self._projectManager.getProject(PyutConstants.DEFAULT_PROJECT_NAME)
        if defaultProject is not None:
            self.logger.info(f'Removing the default project')
            self._closeProject(projectToClose=defaultProject)

    def showFrame(self, frame: UmlDiagramsFrame):
        self._frame = frame
        frame.Show()

    def _onNewDiagram(self, event: NewDiagramEvent):
        """
        Create a new document;
        Adds the tree entry
        Selects the tree entry
        Selects the appropriate notebook frame
        Args:
           event    The event which contains the diagram type to create

        """
        diagramType:      DiagramType      = event.diagramType
        pyutProject: IPyutProject = self._projectManager.currentProject
        if pyutProject is None:
            pyutProject = self._projectManager.newProject()
            self._projectManager.currentProject  = pyutProject
            self._projectManager.currentFrame    = NO_DIAGRAM_FRAME
            self._projectManager.currentDocument = NO_DIAGRAM_FRAME

        self._newDiagram(pyutProject=pyutProject, diagramType=diagramType)

    def _onNewProjectDiagram(self, event: NewProjectDiagramEvent):

        info: NewProjectDiagramInformation = event.newProjectDiagramInformation

        pyutDocument: IPyutDocument = self._newDiagram(pyutProject=info.pyutProject,
                                                       diagramType=info.diagramType,
                                                       diagramName=info.diagramName)
        cb: NewProjectDiagramCallback = info.callback

        cb(pyutDocument)

    def _newDiagram(self, pyutProject: IPyutProject,
                    diagramType: DiagramType, diagramName: str = '') -> IPyutDocument:
        """
        Create a new frame on the input project
        Update the project
        Update the UI elements

        Args:
            pyutProject:    The project to place the new diagram in
            diagramType:    Diagram Type
            diagramName:    Diagram Name

        Returns: The new created PyutDocument, aka diagram
        """
        umlFrame, defaultDiagramName = createDiagramFrame(parentFrame=self._diagramNotebook,
                                                          diagramType=diagramType,
                                                          eventEngine=self._eventEngine)
        document: PyutDocument     = PyutDocument(diagramFrame=umlFrame, docType=diagramType, eventEngine=self._eventEngine)

        document.title = defaultDiagramName

        if diagramName != '':
            document.title = diagramName

        pyutProject.documents.append(document)

        self._updateProjectManagerWithNewDocument(pyutProject=pyutProject, document=document)
        self._addNewDocumentToDiagramNotebook(newDocument=document)

        self._updateApplicationTitle()

        cp: CommandProcessor = umlFrame.commandProcessor
        self._eventEngine.sendEvent(EventType.AssociateEditMenu, commandProcessor=cp)
        return document

    def _getProjectFromFrame(self, frame: UmlDiagramsFrame) -> IPyutProject:
        """
        Return the project that owns a given frame

        Args:
            frame:  the frame to get This project

        Returns:
            PyutProject or None if not found
        """
        for project in self._projectManager.projects:
            if frame in project.frames:
                return project
        return NO_PYUT_PROJECT

    # noinspection PyUnusedLocal
    def _onDiagramNotebookPageChanged(self, event):
        """
        Callback for notebook page changed

        Args:
            event:
        """
        self._notebookCurrentPageNumber = self._diagramNotebook.GetSelection()

        self._projectManager.currentFrame = self._diagramNotebook.currentNotebookFrame
        frameTreeItem: TreeItemId = self._projectTree.getTreeItemFromFrame(self._projectManager.currentFrame)
        self._projectTree.SelectItem(frameTreeItem)

        self._projectManager.currentProject = self._getProjectFromFrame(self._projectManager.currentFrame)

        self._projectManager.syncPageFrameAndNotebook(frame=self._projectManager.currentFrame)
        self._updateApplicationTitle()

        cp: CommandProcessor = self._projectManager.currentFrame.commandProcessor
        self._eventEngine.sendEvent(EventType.UpdateEditMenu, commandProcessor=cp)

    def _onProjectTreeSelectionChanged(self, event: TreeEvent):
        """
        Called when the selection in the project changes

        Args:
            event:
        """
        itm:      TreeItemId   = event.GetItem()
        pyutData: TreeDataType = self._projectTree.GetItemData(itm)
        self.logger.debug(f'Clicked on: {itm=} `{pyutData=}`')

        # Use our own base type
        if isinstance(pyutData, IPyutDocument):
            pyutDocument: IPyutDocument    = cast(IPyutDocument, pyutData)
            frame:        UmlDiagramsFrame = pyutDocument.diagramFrame

            self._projectManager.currentFrame    = frame
            # self._projectManager.projectToClose  = self.getProjectFromFrame(frame)
            self._projectManager.currentProject  = self._projectManager.currentProject
            self._projectManager.currentDocument = pyutDocument

            self._projectManager.syncPageFrameAndNotebook(frame=frame)

        elif isinstance(pyutData, IPyutProject):
            project: IPyutProject = pyutData
            self._projectManager.currentProject = project
            projectFrames: List[UmlFrameType] = project.frames
            if len(projectFrames) > 0:
                self._projectManager.currentFrame = projectFrames[0]
            else:
                self._projectManager.currentFrame = NO_DIAGRAM_FRAME

            self._projectManager.syncPageFrameAndNotebook(frame=self._projectManager.currentFrame)
            self._updateApplicationTitle()
            self._projectManager.currentProject = project

        self._eventEngine.sendEvent(EventType.SetToolAction, action=Action.SELECTOR)
        self._eventEngine.sendEvent(EventType.SelectTool, toolId=SharedIdentifiers.ID_ARROW)

    def _onProjectTreeRightClick(self, treeEvent: TreeEvent):

        itemId: TreeItemId = treeEvent.GetItem()
        data = self._projectTree.GetItemData(item=itemId)
        self.logger.debug(f'Item Data: `{data}`')
        if isinstance(data, IPyutProject):
            self._popupProjectMenu()
        elif isinstance(data, IPyutDocument):
            self._popupProjectDiagramMenu()

    def _popupProjectMenu(self):

        self._updateApplicationStatus(statusMessage='Select Project Action')
        if self._projectPopupMenu is None:

            self.logger.debug(f'Create the project popup menu')
            [closeProjectMenuID] = PyutUtils.assignID(1)
            popupMenu: Menu = Menu('Actions')
            popupMenu.AppendSeparator()
            popupMenu.Append(closeProjectMenuID, 'Close Project', 'Remove project from tree', ITEM_NORMAL)
            popupMenu.Bind(EVT_MENU, self._onCloseProject, id=closeProjectMenuID)

            popupMenu.Bind(EVT_MENU_CLOSE, self._onPopupMenuClose)
            self._projectPopupMenu = popupMenu

        self.logger.info(f'projectToClose: `{self._projectManager.currentProject}`')

        self._parentWindow.PopupMenu(self._projectPopupMenu)

    def _popupProjectDiagramMenu(self):

        self._updateApplicationStatus(statusMessage='Select Document Action')
        if self._documentPopupMenu is None:

            self.logger.debug(f'Create the diagram popup menu')

            [editDiagramNameMenuID, deleteDiagramMenuID] = PyutUtils.assignID(2)

            popupMenu: Menu = Menu('Actions')
            popupMenu.AppendSeparator()
            popupMenu.Append(editDiagramNameMenuID, 'Edit Diagram Name', 'Change diagram name', ITEM_NORMAL)
            popupMenu.Append(deleteDiagramMenuID,   'Delete Diagram',    'Delete it',           ITEM_NORMAL)

            popupMenu.Bind(EVT_MENU, self._onEditDiagramName, id=editDiagramNameMenuID)
            popupMenu.Bind(EVT_MENU, self._onDeleteDiagram, id=deleteDiagramMenuID)

            popupMenu.Bind(EVT_MENU_CLOSE, self._onPopupMenuClose)

            self.__documentPopupMenu = popupMenu

        self.logger.debug(f'Current diagram: `{self._projectManager.currentDocument}`')
        self._parentWindow.PopupMenu(self.__documentPopupMenu)

    # noinspection PyUnusedLocal
    def _onCloseProject(self, event: CommandEvent):
        """

        Args:
            event:  May also be a  CloseProjectEvent
        """
        self._closeCurrentProject()

    # noinspection PyUnusedLocal
    def _onEditDiagramName(self, event: CommandEvent):

        currentDocument: IPyutDocument    = self._projectManager.currentDocument
        currentFrame:    UmlDiagramsFrame = self._projectManager.currentFrame
        # dlgEditDocument: DlgEditDocument = DlgEditDocument(parent=currentFrame, dialogIdentifier=ID_ANY, document=currentDocument)
        # dlgEditDocument.Destroy()
        with TextEntryDialog(currentFrame, "Edit Diagram Title", "Diagram Title", currentDocument.title, OK | CANCEL | CENTRE) as dlg:
            if dlg.ShowModal() == ID_OK:
                currentDocument.title = dlg.GetValue()
                self._eventEngine.sendEvent(EventType.UMLDiagramModified)

        notebookCurrentPageNumber: int = self._diagramNotebook.GetSelection()
        self._diagramNotebook.SetPageText(page=notebookCurrentPageNumber, text=currentDocument.title)
        self._projectManager.updateDocumentName(pyutDocument=currentDocument)

    # noinspection PyUnusedLocal
    def _onDeleteDiagram(self, event: CommandEvent):
        """
        Invoked from the popup menu in the tree;  Right-clicking on the document makes it
        the current document

        Args:
            event:  May be invoked via the event engine with a RemoveDocumentEvent
        """
        project:         IPyutProject  = self._projectManager.currentProject
        currentDocument: IPyutDocument = self._projectManager.currentDocument

        self._projectManager.deleteDocument(project=project, document=currentDocument)

    # noinspection PyUnusedLocal
    def _onPopupMenuClose(self, event: MenuEvent):
        """
        I want to clean up my messages
        Args:
            event:
        """
        self._updateApplicationStatus(statusMessage='')

    def _closeCurrentProject(self):
        """
        Close the current project
        """
        currentProject: IPyutProject = self._projectManager.currentProject

        if currentProject is None:
            self._displayError(message='No frame to close!')
            return

        self._closeProject(projectToClose=currentProject)

    # noinspection PyUnusedLocal
    def _onNewProject(self, event: NewProjectEvent):
        """
        Returns:  A default empty project
        """
        pyutProject: IPyutProject = self._projectManager.newProject()

        self._projectManager.currentProject  = pyutProject
        self._projectManager.currentFrame    = NO_DIAGRAM_FRAME
        self._projectManager.currentDocument = NO_PYUT_DIAGRAM

    def _onNewNamedProject(self, event: NewNamedProjectEvent):
        fqFileName: str = event.projectFilename

        pyutProject: IPyutProject = self._projectManager.newNamedProject(filename=fqFileName)

        cb: NewNamedProjectCallback = event.callback

        cb(pyutProject)

    def _onOpenProject(self, event: OpenProjectEvent):

        projectFilename: str = event.projectFilename
        if self._projectManager.isProjectLoaded(projectFilename) is True:
            self._displayError("The selected project is already loaded !")
        else:
            try:
                oglProject, pyutProject = self._projectManager.openProject(filename=projectFilename)
                self._placeShapesOnFrames(oglProject=oglProject, pyutProject=pyutProject)

                self._updateApplicationTitle()
                self._eventEngine.sendEvent(EventType.UpdateRecentProjects, projectFilename=projectFilename)
                self.closeDefaultEmptyProject()
            except ProjectException as pe:
                self._handleOpenProjectException(pe)

    # noinspection PyUnusedLocal
    def _onSaveProject(self, event: SaveProjectEvent):

        projectToSave: IPyutProject = self._projectManager.currentProject
        self._projectManager.saveProject(projectToSave=projectToSave)
        self._updateApplicationTitle()

        commandProcessor: CommandProcessor = self._projectManager.currentFrame.commandProcessor
        commandProcessor.MarkAsSaved()
        commandProcessor.ClearCommands()

        self._eventEngine.sendEvent(EventType.UpdateRecentProjects, projectFilename=projectToSave.filename)

    # noinspection PyUnusedLocal
    def _onSaveProjectAs(self, event: SaveProjectAsEvent):

        projectToSaveAs: IPyutProject = self._projectManager.currentProject

        self._projectManager.saveProjectAs(projectToSave=projectToSaveAs)
        self._updateApplicationTitle()

        commandProcessor: CommandProcessor = self._projectManager.currentFrame.commandProcessor
        commandProcessor.MarkAsSaved()
        commandProcessor.ClearCommands()
        self._eventEngine.sendEvent(EventType.UpdateRecentProjects, projectFilename=projectToSaveAs.filename)

    # noinspection PyUnusedLocal
    def _onInsertProject(self, event: InsertProjectEvent):
        """
        Insert a file into the current project

        Args:
            event: The project filename to insert

        """
        self._displayError("Currently unsupported")
        # filename: str = event.projectFilename
        # # Get current project
        # xxProject: IPyutProject = self._projectManager.projectToClose
        #
        # # Save number of initial documents
        # nbInitialDocuments = len(project.documents)
        #
        # if not project.insertProject(filename):
        #     self._displayError("The specified file can't be loaded !")
        # else:
        #     self.__notebookCurrentPage = self._diagramNotebook.GetPageCount()-1
        #     self._diagramNotebook.SetSelection(self.__notebookCurrentPage)
        #     # Select first frame as current frame
        #     if len(project.documents) > nbInitialDocuments:
        #         self._frame = project.documents[nbInitialDocuments].diagramFrame

    # noinspection PyUnusedLocal
    def _onDiagramModified(self, event: UMLDiagramModifiedEvent):
        self._setProjectModified()

    def _onMiniProjectInformation(self, event: MiniProjectInformationEvent):
        projectInformation: MiniProjectInformation  = MiniProjectInformation()

        projectInformation.projectName     = self._projectManager.currentProject.projectName
        projectInformation.projectModified = self._projectManager.currentProject.modified
        projectInformation.frameZoom       = self._projectManager.currentFrame.currentZoom

        cb = event.eventHandler
        cb(projectInformation)

    def _onGetActiveUmlFrame(self, event: ActiveUmlFrameEvent):
        cb = event.callback
        cb(self._projectManager.currentFrame)

    def _onActiveProjectInformation(self, event: ActiveProjectInformationEvent):
        cb: ActiveProjectInformationCallback = event.eventHandler

        activeProjectInformation: ActiveProjectInformation = ActiveProjectInformation()
        activeProjectInformation.umlFrame    = self._projectManager.currentFrame
        activeProjectInformation.pyutProject = self._projectManager.currentProject

        cb(activeProjectInformation)

    def _onEditClass(self, event: EditClassEvent):
        pyutClass: PyutClass = event.pyutClass
        umlFrame: UmlDiagramsFrame = self._projectManager.currentFrame

        self.logger.debug(f"Edit: {pyutClass}")

        with DlgEditClass(umlFrame, self._eventEngine, pyutClass) as dlg:
            if dlg.ShowModal() == ID_OK:
                umlFrame.Refresh()
                # Sends its own modify event

    def _onEditNote(self, event: EditNoteEvent):
        pyutNote: PyutNote         = event.pyutNote
        umlFrame: UmlDiagramsFrame = self._projectManager.currentFrame

        self.logger.debug(f"Edit: {pyutNote}")
        with DlgEditNote(umlFrame, pyutNote=pyutNote) as dlg:
            if dlg.ShowModal() == ID_OK:
                self._setProjectModified()

                umlFrame.Refresh()

    def _onEditText(self, event: EditTextEvent):
        pyutText: PyutText         = event.pyutText
        umlFrame: UmlDiagramsFrame = self._projectManager.currentFrame

        self.logger.debug(f"Edit: {pyutText}")
        with DlgEditText(umlFrame, pyutText=pyutText) as dlg:
            if dlg.ShowModal() == ID_OK:
                self._setProjectModified()
                umlFrame.Refresh()

    def _onEditActor(self, event: EditActorEvent):
        pyutActor: PyutActor        = event.pyutActor
        umlFrame:  UmlDiagramsFrame = self._projectManager.currentFrame

        with DlgEditActor(umlFrame, actorName=pyutActor.name) as dlg:
            if dlg.ShowModal() == ID_OK:
                pyutActor.name = dlg.GetValue()
                self._setProjectModified()
                umlFrame.Refresh()

    def _onEditUseCase(self, event: EditUseCaseEvent):

        pyutUseCase: PyutUseCase      = event.pyutUseCase
        umlFrame:    UmlDiagramsFrame = self._projectManager.currentFrame

        with DlgEditUseCase(umlFrame, useCaseName=pyutUseCase.name) as dlg:
            if dlg.ShowModal() == ID_OK:
                pyutUseCase.name = dlg.GetValue()
                self._setProjectModified()
                umlFrame.Refresh()

    def _onEditInterface(self, event: EditInterfaceEvent):

        umlFrame:      UmlDiagramsFrame = self._projectManager.currentFrame
        oglInterface2: OglInterface2    = event.oglInterface2
        implementor:   OglClass         = event.implementor

        with DlgEditInterface(umlFrame, eventEngine=self._eventEngine, oglInterface2=oglInterface2) as dlg:
            if dlg.ShowModal() == OK:
                pyutInterface = dlg.pyutInterface
                self.logger.info(f'model: {pyutInterface}')

                pyutClass: PyutClass = cast(PyutClass, implementor.pyutObject)
                pyutClass.addInterface(pyutInterface)

    def _onAddShape(self, event: AddShapeEvent):

        oglObject: OglObject        = event.shapeToAdd
        umlFrame:  UmlDiagramsFrame = self._projectManager.currentFrame

        layoutEngine: LayoutEngine = LayoutEngine()
        layoutEngine.addShape(umlFrame=umlFrame, oglObject=oglObject)     # too cute for words

    def _onFrameInformation(self, event: FrameInformationEvent):

        projectManager: ProjectManager = self._projectManager
        info: FrameInformation = FrameInformation()
        if projectManager.currentFrame is None:
            info.frameActive = False
        else:
            info.frameActive        = True
            info.clientDC           = ClientDC(projectManager.currentFrame)
            info.diagramType        = projectManager.currentDocument.diagramType.__str__()
            info.diagramTitle       = projectManager.currentDocument.title
            info.selectedOglObjects = cast(OglObjects, self._diagramNotebook.selectedUmlObjects)      # TODO:  Fix this;  This does not seem right

            (width, height) = projectManager.currentFrame.GetSize()
            frameSize: FrameSize = FrameSize(width=width, height=height)
            info.frameSize = frameSize

        cb: FrameInformationCallback = event.callback
        cb(info)

    def _onFrameSize(self, event: FrameSizeEvent):

        projectManager: ProjectManager = self._projectManager

        frameSize: FrameSize = FrameSize()
        if projectManager.currentFrame is None:
            pass
        else:
            (width, height) = projectManager.currentFrame.GetSize()
            frameSize.width  = width
            frameSize.height = height

        cb: FrameSizeCallback = event.eventHandler

        cb(frameSize)

    def _pluginRequestCurrentProject(self, event: RequestCurrentProjectEvent):

        cb:                   CurrentProjectCallback = event.callback
        pyutProject:          IPyutProject           = self._projectManager.currentProject
        pluginProjectCreator: PluginProjectCreator   = PluginProjectCreator()
        pluginProject:        PluginProject          = pluginProjectCreator.toPluginProject(pyutProject=pyutProject)

        cb(pluginProject)

    def _selectedOglObjects(self, event: SelectedOglObjectsEvent):
        umlObjects: UmlObjects = self._projectManager.currentFrame.umlObjects

        selectedObjects: OglObjects = OglObjects([])
        if umlObjects is not None:
            for obj in umlObjects:
                if obj.selected is True:
                    from pyutplugins.ExternalTypes import OglObjectType
                    selectedObjects.append(cast(OglObjectType, obj))

        cb: SelectedOglObjectsCallback = event.callback

        cb(selectedObjects)

    # noinspection PyUnusedLocal
    def _refreshFrame(self, event: RefreshFrameEvent):
        self._projectManager.currentFrame.Refresh()

    def _placeShapesOnFrames(self, oglProject: OglProject, pyutProject: IPyutProject):
        """
        Creates the necessary frames to load the various OglDocuments onto
        respective Pyut frames in the DiagramNotebook

        Assumes `._openProject()` was called to set up the current project
        Args:
            oglProject:   The ogl project to display
            pyutProject:   My version
        """
        layoutEngine: LayoutEngine = LayoutEngine()
        for document in oglProject.oglDocuments.values():
            oglDocument: OglDocument = cast(OglDocument, document)
            diagramType: DiagramType = DiagramType.toEnum(oglDocument.documentType)
            self._newDiagram(pyutProject=pyutProject, diagramType=diagramType, diagramName=oglDocument.documentTitle)

            newFrame = self._projectManager.currentFrame
            layoutEngine.layout(umlFrame=newFrame, oglDocument=oglDocument)

    def _updateApplicationTitle(self):

        # Account for "Untitled" project with no frame
        if self._projectManager.currentFrame is None:
            currentZoom: float = 1.0
        else:
            currentZoom = self._projectManager.currentFrame.currentZoom
        if self._projectManager.currentProject is None:
            newFilename:     str = ''
            projectModified: bool = False
        else:
            newFilename     = self._projectManager.currentProject.filename
            projectModified = self._projectManager.currentProject.modified

        self._eventEngine.sendEvent(eventType=EventType.UpdateApplicationTitle,
                                    newFilename=newFilename,
                                    currentFrameZoomFactor=currentZoom,
                                    projectModified=projectModified)

    def _updateApplicationStatus(self, statusMessage: str):

        self._eventEngine.sendEvent(eventType=EventType.UpdateApplicationStatus, applicationStatusMsg=statusMessage)

    def _displayError(self, message: str):

        booBoo: MessageDialog = MessageDialog(parent=None, message=message, caption='Error', style=OK | ICON_ERROR)
        booBoo.ShowModal()

    def _updateProjectManagerWithNewDocument(self, pyutProject: IPyutProject, document: PyutDocument):
        """

        Args:
            pyutProject:
            document:
        """
        self._projectManager.addDocumentNodeToTree(pyutProject=pyutProject, documentNode=document)
        self._projectManager.currentDocument = document
        self._projectManager.currentFrame    = document.diagramFrame
        self._projectManager.currentProject  = pyutProject
        self._projectManager.currentFrame.Refresh()
        wxYield()

    def _addNewDocumentToDiagramNotebook(self, newDocument: PyutDocument):
        """

        Args:
            newDocument:   The new document to add
        """
        self._diagramNotebook.AddPage(page=newDocument.diagramFrame, text=newDocument.title)

        notebookCurrentPageNumber  = self._diagramNotebook.GetPageCount() - 1
        if notebookCurrentPageNumber >= 0:
            if self.logger.isEnabledFor(DEBUG):
                self.logger.debug(f'Current notebook page: {notebookCurrentPageNumber}')
            self._diagramNotebook.SetSelection(notebookCurrentPageNumber)

    def _setProjectModified(self):
        self._projectManager.currentProject.modified = True
        self._updateApplicationTitle()

    def _handleOpenProjectException(self, pe: ProjectException):
        from wx import EndBusyCursor

        EndBusyCursor()
        MessageBox(message=f'{pe}', caption='Project Open Error', style=ICON_ERROR)
        if (pe.exceptionType == ProjectExceptionType.INVALID_PROJECT or
                pe.exceptionType == ProjectExceptionType.PROJECT_NOT_FOUND or
                pe.exceptionType == ProjectExceptionType.ATTRIBUTE_ERROR):

            self._closeProject(projectToClose=pe.project)

    def _closeProject(self, projectToClose: IPyutProject):
        """
        Close the named project

        Updates the project manager and all the UI elements
        TODO:  This is a hefty method

        Args:
            projectToClose:
        """
        if projectToClose.modified is True:
            frame = self._projectManager.currentProject.frames[0]
            frame.SetFocus()
            self.showFrame(frame)

            dlg = MessageDialog(None, "Your project has not been saved. Would you like to save it ?", "Save changes ?", YES_NO | ICON_QUESTION)
            if dlg.ShowModal() == ID_YES:
                self._projectManager.saveProject(projectToSave=projectToClose)

        # Remove the frame in the notebook
        pages = list(range(self._diagramNotebook.GetPageCount()))
        pages.reverse()

        for i in pages:
            pageFrame = self._diagramNotebook.GetPage(i)
            if pageFrame in projectToClose.frames:
                self._diagramNotebook.DeletePage(i)

        projectTreeRoot: TreeItemId = projectToClose.projectTreeRoot
        self._projectTree.Delete(projectTreeRoot)
        self._projectManager.removeProject(projectToClose)
        self.logger.debug(f'{projectToClose.filename=}')
        self._projectManager.currentFrame = NO_DIAGRAM_FRAME
        currentProjects: PyutProjects = self._projectManager.projects
        nbrProjects: int = len(currentProjects)

        if self.logger.isEnabledFor(DEBUG) is True:
            self.logger.debug(f'{nbrProjects=}')

        if nbrProjects > 0:
            newCurrentProject: IPyutProject = currentProjects[0]
            self._projectManager.currentProject = newCurrentProject
            self._projectManager.updateDiagramNotebookIfPossible(project=newCurrentProject)
        else:
            self._projectManager.currentProject = cast(IPyutProject, None)

        self._updateApplicationTitle()


from typing import List
from typing import Union
from typing import cast

from logging import Logger
from logging import getLogger
from logging import DEBUG

from wx import ClientDC
from wx import EVT_MENU
from wx import EVT_MENU_CLOSE
from wx import EVT_NOTEBOOK_PAGE_CHANGED
from wx import EVT_TREE_ITEM_RIGHT_CLICK
from wx import EVT_TREE_SEL_CHANGED
from wx import ICON_ERROR
from wx import ICON_QUESTION
from wx import ID_ANY
from wx import ID_YES
from wx import OK
from wx import YES_NO
from wx import ITEM_NORMAL

from wx import Frame
from wx import TreeEvent
from wx import TreeItemId
from wx import CommandEvent
from wx import MenuEvent
from wx import Menu
from wx import MessageDialog

from wx import Yield as wxYield

from miniogl.Diagram import Diagram
from miniogl.SelectAnchorPoint import SelectAnchorPoint

from pyutmodel.PyutClass import PyutClass

from ogl.OglObject import OglObject
from ogl.OglInterface2 import OglInterface2

from ogl.sd.OglSDInstance import OglSDInstance
from ogl.sd.OglSDMessage import OglSDMessage

from oglio.Types import OglClasses
from ogl.OglLink import OglLink
from oglio.Types import OglNotes
from oglio.Types import OglSDInstances
from oglio.Types import OglSDMessages
from oglio.Types import OglTexts
from oglio.Types import OglActors
from oglio.Types import OglUseCases
from oglio.Types import OglDocument
from oglio.Types import OglLinks
from oglio.Types import OglProject

from core.types.Types import OglObjects
from core.types.Types import FrameInformation
from core.types.Types import FrameSize
from core.types.Types import FrameInformationCallback
from core.types.Types import FrameSizeCallback
from core.types.Types import SelectedOglObjectsCallback

from pyut.PyutUtils import PyutUtils

from pyut.dialogs.DlgEditClass import DlgEditClass
from pyut.dialogs.DlgEditDocument import DlgEditDocument

from pyut.enums.DiagramType import DiagramType

from pyut.ui.Actions import ACTION_SELECTOR
from pyut.ui.tools.SharedIdentifiers import SharedIdentifiers

from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame
from pyut.ui.umlframes.UmlFrame import UmlObjects

from pyut.uiv2.IPyutDocument import IPyutDocument
from pyut.uiv2.IPyutProject import IPyutProject

from pyut.uiv2.IPyutUI import IPyutUI
from pyut.uiv2.DiagramNotebook import DiagramNotebook
from pyut.uiv2.ProjectManager import ProjectManager
from pyut.uiv2.ProjectManager import PyutProjects
from pyut.uiv2.ProjectTree import ProjectTree
from pyut.uiv2.PyutDocumentV2 import PyutDocumentV2
from pyut.uiv2.PyutProjectV2 import PyutProjectV2
from pyut.uiv2.PyutProjectV2 import UmlFrameType

from pyut.uiv2.Types import createDiagramFrame

from pyut.uiv2.eventengine.EventEngine import NewNamedProjectCallback

from pyut.uiv2.eventengine.Events import EVENT_ACTIVE_PROJECT_INFORMATION
from pyut.uiv2.eventengine.Events import EVENT_ADD_SHAPE
from pyut.uiv2.eventengine.Events import EVENT_CLOSE_PROJECT
from pyut.uiv2.eventengine.Events import EVENT_EDIT_CLASS
from pyut.uiv2.eventengine.Events import EVENT_ACTIVE_UML_FRAME
from pyut.uiv2.eventengine.Events import EVENT_FRAME_INFORMATION
from pyut.uiv2.eventengine.Events import EVENT_FRAME_SIZE
from pyut.uiv2.eventengine.Events import EVENT_MINI_PROJECT_INFORMATION
from pyut.uiv2.eventengine.Events import EVENT_INSERT_PROJECT
from pyut.uiv2.eventengine.Events import EVENT_NEW_DIAGRAM
from pyut.uiv2.eventengine.Events import EVENT_NEW_NAMED_PROJECT
from pyut.uiv2.eventengine.Events import EVENT_NEW_PROJECT
from pyut.uiv2.eventengine.Events import EVENT_NEW_PROJECT_DIAGRAM
from pyut.uiv2.eventengine.Events import EVENT_OPEN_PROJECT
from pyut.uiv2.eventengine.Events import EVENT_DELETE_DIAGRAM
from pyut.uiv2.eventengine.Events import EVENT_REFRESH_FRAME
from pyut.uiv2.eventengine.Events import EVENT_SAVE_PROJECT
from pyut.uiv2.eventengine.Events import EVENT_SAVE_PROJECT_AS
from pyut.uiv2.eventengine.Events import EVENT_SELECTED_OGL_OBJECTS
from pyut.uiv2.eventengine.Events import EVENT_UML_DIAGRAM_MODIFIED

from pyut.uiv2.eventengine.Events import EventType
from pyut.uiv2.eventengine.Events import AddShapeEvent
from pyut.uiv2.eventengine.Events import ActiveUmlFrameEvent
from pyut.uiv2.eventengine.Events import FrameInformationEvent
from pyut.uiv2.eventengine.Events import FrameSizeEvent
from pyut.uiv2.eventengine.Events import MiniProjectInformationEvent
from pyut.uiv2.eventengine.Events import InsertProjectEvent
from pyut.uiv2.eventengine.Events import NewDiagramEvent
from pyut.uiv2.eventengine.Events import NewNamedProjectEvent
from pyut.uiv2.eventengine.Events import NewProjectDiagramEvent
from pyut.uiv2.eventengine.Events import NewProjectEvent
from pyut.uiv2.eventengine.Events import OpenProjectEvent
from pyut.uiv2.eventengine.Events import RefreshFrameEvent
from pyut.uiv2.eventengine.Events import SaveProjectAsEvent
from pyut.uiv2.eventengine.Events import SaveProjectEvent
from pyut.uiv2.eventengine.Events import SelectedOglObjectsEvent
from pyut.uiv2.eventengine.Events import UMLDiagramModifiedEvent
from pyut.uiv2.eventengine.Events import EditClassEvent
from pyut.uiv2.eventengine.Events import ActiveProjectInformationEvent

from pyut.uiv2.eventengine.eventinformation.MiniProjectInformation import MiniProjectInformation
from pyut.uiv2.eventengine.eventinformation.ActiveProjectInformation import ActiveProjectInformation

from pyut.uiv2.eventengine.EventEngine import ActiveProjectInformationCallback

from pyut.uiv2.eventengine.IEventEngine import IEventEngine
from pyut.uiv2.eventengine.eventinformation.NewProjectDiagramInformation import NewProjectDiagramCallback
from pyut.uiv2.eventengine.eventinformation.NewProjectDiagramInformation import NewProjectDiagramInformation

TreeDataType        = Union[PyutProjectV2, PyutDocumentV2]

SASH_POSITION:                 int = 160        # TODO make this a preference and remember it
MAX_NOTEBOOK_PAGE_NAME_LENGTH: int = 12         # TODO make this a preference

NO_DIAGRAM_FRAME: UmlDiagramsFrame = cast(UmlDiagramsFrame, None)
NO_PYUT_PROJECT:  IPyutProject     = cast(IPyutProject, None)
NO_PYUT_DIAGRAM:  IPyutDocument    = cast(IPyutDocument, None)
NO_MENU:          Menu             = cast(Menu, None)


class PyutUIV2(IPyutUI):

    def __init__(self, topLevelWindow: Frame, eventEngine: IEventEngine):

        super().__init__(topLevelWindow=topLevelWindow)

        self.logger: Logger = getLogger(__name__)

        self._parentWindow:    Frame           = topLevelWindow
        self._eventEngine:     IEventEngine    = eventEngine
        self._projectTree:     ProjectTree     = ProjectTree(parentWindow=self)
        self._diagramNotebook: DiagramNotebook = DiagramNotebook(parentWindow=self, eventEngine=eventEngine)

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
        self._eventEngine.registerListener(pyEventBinder=EVENT_ACTIVE_UML_FRAME,           callback=self._onGetActivateUmlFrame)
        self._eventEngine.registerListener(pyEventBinder=EVENT_ACTIVE_PROJECT_INFORMATION, callback=self._onActiveProjectInformation)
        self._eventEngine.registerListener(pyEventBinder=EVENT_EDIT_CLASS, callback=self._onEditClass)
        #
        # Following provided for the Plugin Adapter
        self._eventEngine.registerListener(pyEventBinder=EVENT_ADD_SHAPE,            callback=self._onAddShape)
        self._eventEngine.registerListener(pyEventBinder=EVENT_FRAME_INFORMATION,    callback=self._onFrameInformation)
        self._eventEngine.registerListener(pyEventBinder=EVENT_FRAME_SIZE,           callback=self._onFrameSize)
        self._eventEngine.registerListener(pyEventBinder=EVENT_SELECTED_OGL_OBJECTS, callback=self._selectedOglObjects)
        self._eventEngine.registerListener(pyEventBinder=EVENT_REFRESH_FRAME,        callback=self._refreshFrame)

    @property
    def currentProject(self) -> IPyutProject:
        return self._projectManager.currentProject

    @currentProject.setter
    def currentProject(self, newProject: IPyutProject):

        self._projectManager.currentProject = newProject

        self._notebookCurrentPageNumber = self._diagramNotebook.GetPageCount() - 1
        self._diagramNotebook.SetSelection(self._notebookCurrentPageNumber)

        self.logger.debug(f'{self._notebookCurrentPageNumber=}')

    @property
    def currentDocument(self) -> IPyutDocument:
        """
        Get the current document.

        Returns:
            the current document or None if not found
        """
        return self._projectManager.currentDocument

    @property
    def currentFrame(self) -> UmlDiagramsFrame:
        return self._projectManager.currentFrame

    @currentFrame.setter
    def currentFrame(self, newFrame: UmlDiagramsFrame):
        self._projectManager.currentFrame = newFrame

    @property
    def diagramNotebook(self) -> DiagramNotebook:
        """
        This will be removed when we use eventing from the mediator to send messages

        Returns:  The UI component
        """
        return self._diagramNotebook

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

        self.diagramNotebook.DeleteAllPages()

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
        diagramType: DiagramType = event.diagramType
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

    def _newDiagram(self, pyutProject: IPyutProject, diagramType: DiagramType, diagramName: str = '') -> IPyutDocument:
        """
        Create a new frame on the input project
        Update the project
        Update the UI elements

        Args:
            pyutProject:    The project to place the new diagram in
            diagramType:    Diagram Type
            diagramName:    Diagram Name

        Returns:

        """
        umlFrame, defaultDiagramName = createDiagramFrame(parentFrame=self._diagramNotebook, diagramType=diagramType, eventEngine=self._eventEngine)
        document: PyutDocumentV2     = PyutDocumentV2(diagramFrame=umlFrame, docType=diagramType, eventEngine=self._eventEngine)

        document.title = defaultDiagramName

        if diagramName != '':
            document.title = diagramName

        pyutProject.documents.append(document)

        self._updateProjectManagerWithNewDocument(pyutProject=pyutProject, document=document)
        self._addNewDocumentToDiagramNotebook(newDocument=document)

        self._updateApplicationTitle()

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
            # self._projectManager.currentProject  = self.getProjectFromFrame(frame)
            self._projectManager.currentProject  = self._projectManager.currentProject
            self._projectManager.currentDocument = pyutDocument

            self._projectManager.syncPageFrameAndNotebook(frame=frame)

        elif isinstance(pyutData, PyutProjectV2):
            project: PyutProjectV2 = pyutData
            self._projectManager.currentProject = project
            projectFrames: List[UmlFrameType] = project.frames
            if len(projectFrames) > 0:
                self._projectManager.currentFrame = projectFrames[0]
            else:
                self._projectManager.currentFrame = NO_DIAGRAM_FRAME

            self._projectManager.syncPageFrameAndNotebook(frame=self.currentFrame)
            self._updateApplicationTitle()
            self._projectManager.currentProject = project

        self._eventEngine.sendEvent(EventType.SetToolAction, action=ACTION_SELECTOR)
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

        self.logger.info(f'currentProject: `{self._projectManager.currentProject}`')

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

        self.logger.debug(f'Current diagram: `{self.currentDocument}`')
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

        currentDocument: IPyutDocument   = self._projectManager.currentDocument
        dlgEditDocument: DlgEditDocument = DlgEditDocument(parent=self.currentFrame, dialogIdentifier=ID_ANY, document=currentDocument)

        dlgEditDocument.Destroy()

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
        currentDocument: IPyutDocument = self.currentDocument

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
        if currentProject is None and self.currentFrame is not None:
            # currentProject = self.getProjectFromFrame(self.currentFrame)
            currentProject = self._projectManager.currentProject
        if currentProject is None:
            self._displayError(message='No frame to close!')
            return

        # Close the project
        if currentProject.modified is True:
            frame = self._projectManager.currentProject.frames[0]
            frame.SetFocus()
            self.showFrame(frame)

            dlg = MessageDialog(None, "Your project has not been saved. Would you like to save it ?", "Save changes ?", YES_NO | ICON_QUESTION)
            if dlg.ShowModal() == ID_YES:
                self._projectManager.saveProject(projectToSave=currentProject)

        # Remove the frame in the notebook
        pages = list(range(self._diagramNotebook.GetPageCount()))
        pages.reverse()
        for i in pages:
            pageFrame = self._diagramNotebook.GetPage(i)
            if pageFrame in currentProject.frames:
                self._diagramNotebook.DeletePage(i)

        projectTreeRoot: TreeItemId = currentProject.projectTreeRoot
        self._projectTree.Delete(projectTreeRoot)

        self._projectManager.removeProject(currentProject)

        self.logger.debug(f'{currentProject.filename=}')

        self._projectManager.currentFrame = NO_DIAGRAM_FRAME

        currentProjects: PyutProjects = self._projectManager.projects
        nbrProjects:     int          = len(currentProjects)
        if self.logger.isEnabledFor(DEBUG) is True:
            self.logger.debug(f'{nbrProjects=}')

        if nbrProjects > 0:
            newCurrentProject: IPyutProject = currentProjects[0]
            self._projectManager.currentProject = newCurrentProject
            self._projectManager.updateDiagramNotebookIfPossible(project=newCurrentProject)
        else:
            self._projectManager.currentProject = None

        self._updateApplicationTitle()

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
            oglProject, pyutProject = self._projectManager.openProject(filename=projectFilename)

            self._placeShapesOnFrames(oglProject=oglProject, pyutProject=pyutProject)

            self._updateApplicationTitle()
            self._eventEngine.sendEvent(EventType.UpdateRecentProjects)

    # noinspection PyUnusedLocal
    def _onSaveProject(self, event: SaveProjectEvent):

        self._projectManager.saveProject(projectToSave=self._projectManager.currentProject)
        self._updateApplicationTitle()
        self._eventEngine.sendEvent(EventType.UpdateRecentProjects)

    # noinspection PyUnusedLocal
    def _onSaveProjectAs(self, event: SaveProjectAsEvent):
        currentProject: IPyutProject = self._projectManager.currentProject

        self._projectManager.saveProjectAs(projectToSave=currentProject)
        self._updateApplicationTitle()
        self._eventEngine.sendEvent(EventType.UpdateRecentProjects)

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
        # xxProject: IPyutProject = self._projectManager.currentProject
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
        self._projectManager.currentProject.modified = True
        self._updateApplicationTitle()

    def _onMiniProjectInformation(self, event: MiniProjectInformationEvent):
        projectInformation: MiniProjectInformation  = MiniProjectInformation()

        projectInformation.projectName     = self._projectManager.currentProject.projectName
        projectInformation.projectModified = self._projectManager.currentProject.modified
        projectInformation.frameZoom       = self._projectManager.currentFrame.GetCurrentZoom()

        cb = event.callback
        cb(projectInformation)

    def _onGetActivateUmlFrame(self, event: ActiveUmlFrameEvent):
        cb = event.callback
        cb(self._projectManager.currentFrame)

    def _onActiveProjectInformation(self, event: ActiveProjectInformationEvent):
        cb: ActiveProjectInformationCallback = event.callback

        activeProjectInformation: ActiveProjectInformation = ActiveProjectInformation()
        activeProjectInformation.umlFrame    = self._projectManager.currentFrame
        activeProjectInformation.pyutProject = self._projectManager.currentProject

        cb(activeProjectInformation)

    def _onEditClass(self, event: EditClassEvent):
        pyutClass: PyutClass = event.pyutClass
        umlFrame: UmlDiagramsFrame = self._projectManager.currentFrame

        self.logger.debug(f"Edit: {pyutClass}")

        dlg: DlgEditClass = DlgEditClass(umlFrame, self._eventEngine, pyutClass)
        dlg.ShowModal()
        dlg.Destroy()

    def _onAddShape(self, event: AddShapeEvent):

        oglObject: OglObject = event.shapeToAdd
        umlFrame: UmlDiagramsFrame = self._projectManager.currentFrame
        match oglObject:
            case OglLink() as oglObject:
                self._layoutOglLink(umlFrame=umlFrame, oglLink=cast(OglLink, oglObject))
            case OglSDInstance() as oglObject:
                self._layoutOglSDInstance(diagram=umlFrame.getDiagram(), oglSDInstance=cast(OglSDInstance, oglObject))
            case OglSDMessage() as oglObject:
                self._layoutOglSDMessage(diagram=umlFrame.getDiagram(), oglSDMessage=cast(OglSDMessage, oglObject))
            case _:
                self._layoutAnOglObject(umlFrame=umlFrame, oglObject=oglObject)

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

        cb: FrameSizeCallback = event.callback

        cb(frameSize)

    def _selectedOglObjects(self, event: SelectedOglObjectsEvent):
        umlObjects: UmlObjects = self._projectManager.currentFrame.getUmlObjects()

        selectedObjects: OglObjects = OglObjects([])
        if umlObjects is not None:
            for obj in umlObjects:
                if obj.IsSelected():
                    from core.types.Types import OglObjectType
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
        for document in oglProject.oglDocuments.values():
            oglDocument: OglDocument = cast(OglDocument, document)
            diagramType: DiagramType = DiagramType.toEnum(oglDocument.documentType)
            self._newDiagram(pyutProject=pyutProject, diagramType=diagramType, diagramName=oglDocument.documentTitle)

            newFrame = self._projectManager.currentFrame
            # Don't care what type of diagram since those lists will be empty
            self._layoutOglClasses(umlFrame=newFrame, oglClasses=oglDocument.oglClasses)
            self._layoutOglLinks(umlFrame=newFrame,   oglLinks=oglDocument.oglLinks)
            self._layoutOglNotes(umlFrame=newFrame,   oglNotes=oglDocument.oglNotes)
            self._layoutOglTexts(umlFrame=newFrame,   oglTexts=oglDocument.oglTexts)

            self._layoutOglActors(umlFrame=newFrame,   oglActors=oglDocument.oglActors)
            self._layoutOglUseCases(umlFrame=newFrame, oglUseCases=oglDocument.oglUseCases)

            self._layoutOglSDInstances(umlFrame=newFrame, oglSDInstances=oglDocument.oglSDInstances)
            self._layoutOglSDMessages(umlFrame=newFrame, oglSDMessages=oglDocument.oglSDMessages)

    def _updateApplicationTitle(self):

        # Account for "Untitled" project with no frame
        if self._projectManager.currentFrame is None:
            currentZoom: float = 1.0
        else:
            currentZoom = self._projectManager.currentFrame.GetCurrentZoom()
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

    def _layoutOglClasses(self, umlFrame: UmlDiagramsFrame, oglClasses: OglClasses):
        for oglClass in oglClasses:
            self._layoutAnOglObject(umlFrame=umlFrame, oglObject=oglClass, )

    def _layoutOglLinks(self, umlFrame: UmlDiagramsFrame, oglLinks: OglLinks):

        for link in oglLinks:
            oglLink: OglLink = cast(OglLink, link)
            self._layoutOglLink(umlFrame=umlFrame, oglLink=oglLink)

    def _layoutOglNotes(self, umlFrame: UmlDiagramsFrame, oglNotes: OglNotes):
        for oglNote in oglNotes:
            self._layoutAnOglObject(umlFrame=umlFrame, oglObject=oglNote)

    def _layoutOglTexts(self, umlFrame: UmlDiagramsFrame, oglTexts: OglTexts):
        for oglText in oglTexts:
            self._layoutAnOglObject(umlFrame=umlFrame, oglObject=oglText)

    def _layoutOglActors(self, umlFrame: UmlDiagramsFrame, oglActors: OglActors):
        for oglActor in oglActors:
            self._layoutAnOglObject(umlFrame=umlFrame, oglObject=oglActor)

    def _layoutOglUseCases(self, umlFrame: UmlDiagramsFrame, oglUseCases: OglUseCases):
        for oglUseCase in oglUseCases:
            self._layoutAnOglObject(umlFrame=umlFrame, oglObject=oglUseCase)

    def _layoutOglSDInstances(self, umlFrame: UmlDiagramsFrame, oglSDInstances: OglSDInstances):
        diagram: Diagram = umlFrame.getDiagram()
        for oglSDInstance in oglSDInstances.values():
            self._layoutOglSDInstance(diagram=diagram, oglSDInstance=oglSDInstance)
        umlFrame.Refresh()

    def _layoutOglSDMessages(self, umlFrame: UmlDiagramsFrame, oglSDMessages: OglSDMessages):
        diagram: Diagram = umlFrame.getDiagram()
        for oglSDMessage in oglSDMessages.values():
            self._layoutOglSDMessage(diagram=diagram, oglSDMessage=oglSDMessage)

    def _layoutOglLink(self, umlFrame: UmlDiagramsFrame, oglLink: OglLink):

        self._layoutAnOglObject(umlFrame=umlFrame, oglObject=oglLink)
        # TODO:
        # This is bad mooky here. The Ogl objects were created withing having a Diagram
        # The legacy code deserialized the object while adding them to a frame. This
        # new code deserializes w/o reference to a frame
        # If we don't this the AnchorPoints are not on the diagram and lines ends are not
        # movable.
        if isinstance(oglLink, OglInterface2) is False:
            umlDiagram = umlFrame.GetDiagram()

            umlDiagram.AddShape(oglLink.sourceAnchor)
            umlDiagram.AddShape(oglLink.destinationAnchor)
            controlPoints = oglLink.GetControlPoints()
            for controlPoint in controlPoints:
                umlDiagram.AddShape(controlPoint)

    def _layoutOglSDInstance(self, diagram: Diagram, oglSDInstance: OglSDInstance):
        diagram.AddShape(oglSDInstance)

    def _layoutOglSDMessage(self, diagram: Diagram, oglSDMessage: OglSDMessage):
        diagram.AddShape(oglSDMessage)

    def _layoutAnOglObject(self, umlFrame: UmlDiagramsFrame, oglObject: Union[OglObject, OglInterface2, SelectAnchorPoint, OglLink]):
        x, y = oglObject.GetPosition()
        umlFrame.addShape(oglObject, x, y)

    def _updateProjectManagerWithNewDocument(self, pyutProject: IPyutProject, document: PyutDocumentV2):
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

    def _addNewDocumentToDiagramNotebook(self, newDocument: PyutDocumentV2):
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

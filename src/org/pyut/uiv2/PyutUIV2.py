
from typing import List
from typing import Union
from typing import cast

from logging import Logger
from logging import getLogger
from logging import DEBUG

# noinspection PyPackageRequirements
from deprecated import deprecated

from miniogl.Diagram import Diagram
from miniogl.SelectAnchorPoint import SelectAnchorPoint
from ogl.OglInterface2 import OglInterface2
from ogl.OglLink import OglLink

from ogl.OglObject import OglObject
from oglio.Types import OglClasses
from oglio.Types import OglNotes
from oglio.Types import OglSDInstances
from oglio.Types import OglSDMessages
from oglio.Types import OglTexts
from oglio.Types import OglActors
from oglio.Types import OglUseCases

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

from oglio.Types import OglDocument
from oglio.Types import OglLinks
from oglio.Types import OglProject

from pyutmodel.PyutClass import PyutClass

from org.pyut.PyutUtils import PyutUtils

from org.pyut.dialogs.DlgEditClass import DlgEditClass
from org.pyut.dialogs.DlgEditDocument import DlgEditDocument

from org.pyut.enums.DiagramType import DiagramType

from org.pyut.ui.Actions import ACTION_SELECTOR
from org.pyut.ui.tools.SharedIdentifiers import SharedIdentifiers

from org.pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

from org.pyut.uiv2.IPyutDocument import IPyutDocument
from org.pyut.uiv2.IPyutProject import IPyutProject

from org.pyut.uiv2.IPyutUI import IPyutUI
from org.pyut.uiv2.DiagramNotebook import DiagramNotebook
from org.pyut.uiv2.ProjectManager import ProjectManager
from org.pyut.uiv2.ProjectManager import PyutProjects
from org.pyut.uiv2.ProjectTree import ProjectTree
from org.pyut.uiv2.PyutDocumentV2 import PyutDocumentV2
from org.pyut.uiv2.PyutProjectV2 import PyutProjectV2
from org.pyut.uiv2.PyutProjectV2 import UmlFrameType

from org.pyut.uiv2.eventengine.Events import EVENT_ACTIVE_PROJECT_INFORMATION
from org.pyut.uiv2.eventengine.Events import EVENT_CLOSE_PROJECT
from org.pyut.uiv2.eventengine.Events import EVENT_EDIT_CLASS
from org.pyut.uiv2.eventengine.Events import EVENT_ACTIVE_UML_FRAME
from org.pyut.uiv2.eventengine.Events import EVENT_MINI_PROJECT_INFORMATION
from org.pyut.uiv2.eventengine.Events import EVENT_INSERT_PROJECT
from org.pyut.uiv2.eventengine.Events import EVENT_NEW_DIAGRAM
from org.pyut.uiv2.eventengine.Events import EVENT_NEW_PROJECT
from org.pyut.uiv2.eventengine.Events import EVENT_OPEN_PROJECT
from org.pyut.uiv2.eventengine.Events import EVENT_DELETE_DIAGRAM
from org.pyut.uiv2.eventengine.Events import EVENT_SAVE_PROJECT
from org.pyut.uiv2.eventengine.Events import EVENT_SAVE_PROJECT_AS
from org.pyut.uiv2.eventengine.Events import EVENT_UML_DIAGRAM_MODIFIED

from org.pyut.uiv2.eventengine.Events import EventType
from org.pyut.uiv2.eventengine.Events import ActiveUmlFrameEvent
from org.pyut.uiv2.eventengine.Events import MiniProjectInformationEvent
from org.pyut.uiv2.eventengine.Events import InsertProjectEvent
from org.pyut.uiv2.eventengine.Events import NewDiagramEvent
from org.pyut.uiv2.eventengine.Events import NewProjectEvent
from org.pyut.uiv2.eventengine.Events import OpenProjectEvent
from org.pyut.uiv2.eventengine.Events import SaveProjectAsEvent
from org.pyut.uiv2.eventengine.Events import SaveProjectEvent
from org.pyut.uiv2.eventengine.Events import UMLDiagramModifiedEvent
from org.pyut.uiv2.eventengine.Events import EditClassEvent
from org.pyut.uiv2.eventengine.Events import ActiveProjectInformationEvent

from org.pyut.uiv2.eventengine.MiniProjectInformation import MiniProjectInformation
from org.pyut.uiv2.eventengine.ActiveProjectInformation import ActiveProjectInformation

from org.pyut.uiv2.eventengine.EventEngine import ActiveProjectInformationCallback

from org.pyut.uiv2.eventengine.IEventEngine import IEventEngine

TreeDataType        = Union[PyutProjectV2, PyutDocumentV2]

SASH_POSITION:                 int = 160        # TODO make this a preference and remember it
MAX_NOTEBOOK_PAGE_NAME_LENGTH: int = 12         # TODO make this a preference

NO_DIAGRAM_FRAME: UmlDiagramsFrame = cast(UmlDiagramsFrame, None)
NO_PYUT_PROJECT:  IPyutProject     = cast(IPyutProject, None)
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
        self._eventEngine.registerListener(pyEventBinder=EVENT_DELETE_DIAGRAM, callback=self._onDeleteDiagram)
        self._eventEngine.registerListener(pyEventBinder=EVENT_NEW_PROJECT,     callback=self._onNewProject)
        self._eventEngine.registerListener(pyEventBinder=EVENT_NEW_DIAGRAM,     callback=self._onNewDiagram)
        self._eventEngine.registerListener(pyEventBinder=EVENT_OPEN_PROJECT,    callback=self._onOpenProject)
        self._eventEngine.registerListener(pyEventBinder=EVENT_CLOSE_PROJECT,   callback=self._onCloseProject)
        self._eventEngine.registerListener(pyEventBinder=EVENT_SAVE_PROJECT,    callback=self._onSaveProject)
        self._eventEngine.registerListener(pyEventBinder=EVENT_SAVE_PROJECT_AS, callback=self._onSaveProjectAs)
        self._eventEngine.registerListener(pyEventBinder=EVENT_INSERT_PROJECT,  callback=self._onInsertProject)
        self._eventEngine.registerListener(pyEventBinder=EVENT_UML_DIAGRAM_MODIFIED, callback=self._onDiagramModified)

        self._eventEngine.registerListener(pyEventBinder=EVENT_MINI_PROJECT_INFORMATION,   callback=self._onMiniProjectInformation)
        self._eventEngine.registerListener(pyEventBinder=EVENT_ACTIVE_UML_FRAME, callback=self._onGetActivateUmlFrame)
        self._eventEngine.registerListener(pyEventBinder=EVENT_ACTIVE_PROJECT_INFORMATION, callback=self._onActiveProjectInformation)

        self._eventEngine.registerListener(pyEventBinder=EVENT_EDIT_CLASS, callback=self._onEditClass)

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

    def registerUmlFrame(self, frame: UmlDiagramsFrame):
        """
        Register the current UML Frame

        Args:
            frame:
        """
        self.currentFrame = frame
        self._currentProject = self.getProjectFromFrame(frame)

    def showFrame(self, frame: UmlDiagramsFrame):
        self._frame = frame
        frame.Show()

    def getProjectFromFrame(self, frame: UmlDiagramsFrame) -> IPyutProject:
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

    def newDiagram(self, docType: DiagramType):
        """
        Maintained for PyutXmlV10, until we can fix that;  Probably with oglio

        Args:
            docType:

        Returns:  The created diagram

        """

        return self._newDiagram(self._projectManager.currentProject, diagramType=docType)

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
            self._projectManager.newProject()
            pyutProject = self._projectManager.currentProject

        self._newDiagram(pyutProject=pyutProject, diagramType=diagramType)

    @deprecated(reason='use property .currentProject')
    def getCurrentProject(self) -> IPyutProject:
        """
        Get the current working project

        Returns:
            the current project or None if not found
        """
        return self._projectManager.currentProject

    def isProjectLoaded(self, filename: str) -> bool:
        """
        Args:
            filename:

        Returns:
            `True` if the project is already loaded
        """
        return self._projectManager.isProjectLoaded(filename=filename)

    def _newDiagram(self, pyutProject: IPyutProject, diagramType: DiagramType, diagramName: str = ''):
        """
        Create a new frame on the current project

        Args:
            diagramType:
        """
        document: PyutDocumentV2  = PyutDocumentV2(parentFrame=self._diagramNotebook, docType=diagramType, eventEngine=self._eventEngine)

        if diagramName != '':
            document.title = diagramName

        pyutProject.documents.append(document)

        self._updateProjectManagerWithNewDocument(pyutProject=pyutProject, document=document)
        self._addNewDocumentToDiagramNotebook(newDocument=document)

        self._updateApplicationTitle()

    # def openFile(self, filename, project: IPyutProject = None) -> bool:
    #     """
    #     Args:
    #         filename:
    #         project:
    #
    #     Returns:
    #         `True` if operation succeeded
    #     """
    #     self._projectManager.openProject(filename=filename, project=project)
    #
    #     return True

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

        self._projectManager.currentProject = self.getProjectFromFrame(self._projectManager.currentFrame)
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
            self._projectManager.currentProject  = self.getProjectFromFrame(frame)
            self._projectManager.currentDocument = pyutDocument

            self._projectManager.syncPageFrameAndNotebook(frame=frame)

        elif isinstance(pyutData, PyutProjectV2):
            project: PyutProjectV2 = pyutData
            self._projectManager.currentProject = project
            projectFrames: List[UmlFrameType] = project.getFrames()
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
            currentProject = self.getProjectFromFrame(self.currentFrame)
        if currentProject is None:
            self._displayError(message='No frame to close!')
            return

        # Close the project
        if currentProject.modified is True:
            frame = self._projectManager.currentProject.getFrames()[0]
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
        self._projectManager.currentFrame = NO_DIAGRAM_FRAME

        return self._projectManager.newProject()

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

    def _onInsertProject(self, event: InsertProjectEvent):
        """
        Insert a file into the current project

        Args:
            event: The project filename to insert

        """
        filename: str = event.projectFilename
        # Get current project
        project: IPyutProject = self._projectManager.currentProject

        # Save number of initial documents
        nbInitialDocuments = len(project.documents)

        if not project.insertProject(filename):
            self._displayError("The specified file can't be loaded !")
        else:
            self.__notebookCurrentPage = self._diagramNotebook.GetPageCount()-1
            self._diagramNotebook.SetSelection(self.__notebookCurrentPage)
            # Select first frame as current frame
            if len(project.documents) > nbInitialDocuments:
                self._frame = project.documents[nbInitialDocuments].diagramFrame

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
            self._displayAnOglObject(umlFrame=umlFrame, oglObject=oglClass,)

    def _layoutOglLinks(self, umlFrame: UmlDiagramsFrame, oglLinks: OglLinks):
        for oglLink in oglLinks:
            # TODO:  Special handling for OglInterface2 links
            self._displayAnOglObject(umlFrame=umlFrame, oglObject=oglLink)

    def _layoutOglNotes(self, umlFrame: UmlDiagramsFrame, oglNotes: OglNotes):
        for oglNote in oglNotes:
            self._displayAnOglObject(umlFrame=umlFrame, oglObject=oglNote)

    def _layoutOglTexts(self, umlFrame: UmlDiagramsFrame, oglTexts: OglTexts):
        for oglText in oglTexts:
            self._displayAnOglObject(umlFrame=umlFrame, oglObject=oglText)

    def _layoutOglActors(self, umlFrame: UmlDiagramsFrame, oglActors: OglActors):
        for oglActor in oglActors:
            self._displayAnOglObject(umlFrame=umlFrame, oglObject=oglActor)

    def _layoutOglUseCases(self, umlFrame: UmlDiagramsFrame, oglUseCases: OglUseCases):
        for oglUseCase in oglUseCases:
            self._displayAnOglObject(umlFrame=umlFrame, oglObject=oglUseCase)

    def _layoutOglSDInstances(self, umlFrame: UmlDiagramsFrame, oglSDInstances: OglSDInstances):
        diagram: Diagram = umlFrame.getDiagram()
        for oglSDInstance in oglSDInstances.values():
            diagram.AddShape(oglSDInstance)
        umlFrame.Refresh()

    def _layoutOglSDMessages(self, umlFrame: UmlDiagramsFrame, oglSDMessages: OglSDMessages):
        diagram: Diagram = umlFrame.getDiagram()
        for oglSDMessage in oglSDMessages.values():
            diagram.AddShape(oglSDMessage)

    def _displayAnOglObject(self, umlFrame: UmlDiagramsFrame, oglObject: Union[OglObject, OglInterface2, SelectAnchorPoint, OglLink]):
        x, y = oglObject.GetPosition()
        umlFrame.addShape(oglObject, x, y)

    def _updateProjectManagerWithNewDocument(self, pyutProject: IPyutProject, document: PyutDocumentV2):
        """

        Args:
            pyutProject:
            document:
        """
        self._projectManager.addDocumentNodeToTree(pyutProject=pyutProject, documentNode=document)
        self._projectManager.currentFrame   = document.diagramFrame
        self._projectManager.currentProject = pyutProject
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


from typing import List
from typing import Union
from typing import cast

from logging import Logger
from logging import getLogger

# noinspection PyPackageRequirements
from deprecated import deprecated

from wx import EVT_MENU
from wx import EVT_NOTEBOOK_PAGE_CHANGED
from wx import EVT_TREE_ITEM_RIGHT_CLICK
from wx import EVT_TREE_SEL_CHANGED
from wx import ICON_QUESTION
from wx import ID_ANY
from wx import ID_YES
from wx import YES_NO
from wx import ITEM_NORMAL

from wx import SplitterWindow
from wx import Frame
from wx import TreeEvent
from wx import TreeItemId
from wx import CommandEvent
from wx import Menu
from wx import MessageDialog

from wx import Yield as wxYield

from org.pyut.PyutUtils import PyutUtils
from org.pyut.dialogs.DlgEditDocument import DlgEditDocument

from org.pyut.enums.DiagramType import DiagramType


from org.pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame
from org.pyut.ui.IPyutDocument import IPyutDocument
from org.pyut.ui.IPyutProject import IPyutProject

from org.pyut.uiv2.DiagramNotebook import DiagramNotebook
from org.pyut.uiv2.ProjectManager import ProjectManager
from org.pyut.uiv2.ProjectManager import PyutProjects
from org.pyut.uiv2.ProjectTree import ProjectTree
from org.pyut.uiv2.PyutDocumentV2 import PyutDocumentV2
from org.pyut.uiv2.PyutProjectV2 import PyutProjectV2
from org.pyut.uiv2.PyutProjectV2 import UmlFrameType

TreeDataType = Union[PyutProjectV2, UmlDiagramsFrame]

SASH_POSITION:                 int = 160        # TODO make this a preference and remember it
MAX_NOTEBOOK_PAGE_NAME_LENGTH: int = 12         # TODO make this a preference


class PyutUIV2(SplitterWindow):

    def __init__(self, topLevelWindow: Frame):

        super().__init__(parent=topLevelWindow, id=ID_ANY)

        self.logger: Logger = getLogger(__name__)

        self._parentWindow:    Frame           = topLevelWindow
        self._projectTree:     ProjectTree     = ProjectTree(parentWindow=self)
        self._diagramNotebook: DiagramNotebook = DiagramNotebook(parentWindow=self)

        # Set splitter
        self.SetMinimumPaneSize(20)
        self.SplitVertically(self._projectTree, self._diagramNotebook, SASH_POSITION)

        self._notebookCurrentPageNumber: int                = -1

        # self._projects:                  List[IPyutProject] = []
        # self._currentProject:            IPyutProject       = cast(IPyutProject, None)
        # self._currentFrame:              UmlDiagramsFrame   = cast(UmlDiagramsFrame, None)

        self._projectPopupMenu:          Menu               = cast(Menu, None)
        self._documentPopupMenu:         Menu               = cast(Menu, None)

        self._projectManager: ProjectManager = ProjectManager(projectTree=self._projectTree, diagramNoteBook=self._diagramNotebook)

        self._parentWindow.Bind(EVT_NOTEBOOK_PAGE_CHANGED, self._onDiagramNotebookPageChanged)
        self._parentWindow.Bind(EVT_TREE_SEL_CHANGED,      self._onProjectTreeSelectionChanged)
        self._projectTree.Bind(EVT_TREE_ITEM_RIGHT_CLICK,  self._onProjectTreeRightClick)

    @property
    def currentProject(self) -> IPyutProject:
        return self._projectManager.currentProject

    @currentProject.setter
    def currentProject(self, newProject: IPyutProject):

        self.logger.info(f'{self._diagramNotebook.GetRowCount()=}')
        self._projectManager.currentProject = newProject

        self._notebookCurrentPageNumber = self._diagramNotebook.GetPageCount() - 1
        self._diagramNotebook.SetSelection(self._notebookCurrentPageNumber)

        self.logger.info(f'{self._notebookCurrentPageNumber=}')

    @property
    def currentDocument(self) -> IPyutDocument:
        """
        Get the current document.

        Returns:
            the current document or None if not found
        """
        project: IPyutProject = self._projectManager.currentProject
        if project is None:
            return cast(IPyutDocument, None)
        for document in project.documents:
            if document.diagramFrame is self.currentFrame:
                return document
        return cast(IPyutDocument, None)

    @property
    def currentFrame(self) -> UmlDiagramsFrame:
        return self._projectManager.currentFrame

    @currentFrame.setter
    def currentFrame(self, newFrame: UmlDiagramsFrame):
        self._projectManager.currentFrame = newFrame

    # @property
    # def modified(self) -> bool:
    #     if self._projectManager.currentProject is not None:
    #         return self._projectManager.currentProject.modified
    #     else:
    #         return False
    #
    # @modified.setter
    # def modified(self, theNewValue: bool = True):
    #     """
    #     Set the modified flag of the currently opened project
    #
    #     Args:
    #         theNewValue:
    #     """
    #     if self._projectManager.currentProject is not None:
    #         # mypy does not handle property setters
    #         self._projectManager.currentProject.modified = theNewValue     # type: ignore
    #     # self._mediator.updateTitle()      TODO Fix V2 version

    @property
    def diagramNotebook(self) -> DiagramNotebook:
        """
        This will be removed when we use eventing from the mediator to send messages

        Returns:  The UI component
        """
        return self._diagramNotebook

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
        # for project in self._projects:
        for project in self._projectManager.projects:
            if frame in project.getFrames():
                return project
        return cast(PyutProjectV2, None)

    def newProject(self) -> IPyutProject:
        """
        Returns:  A default empty project
        """
        self.currentFrame   = cast(UmlDiagramsFrame, None)

        return self._projectManager.newProject()

    def newDocument(self, docType: DiagramType) -> IPyutDocument:
        """
        Create a new document;  It is up to the caller to update the PyutProject document list
        It is up to the caller to add it to the notebook

        Args:
            docType:  Type of document

        Returns: The newly created document
        """
        pyutProject: IPyutProject = self._projectManager.currentProject
        if pyutProject is None:
            self._projectManager.newProject()
            pyutProject = self._projectManager.currentProject

        document: PyutDocumentV2  = PyutDocumentV2(parentFrame=self._diagramNotebook, project=pyutProject, docType=docType)

        document.addToTree(self._projectTree, pyutProject.projectTreeRoot)

        self.currentFrame    = document.diagramFrame
        self._currentProject = pyutProject      # TODO do not use property it does a bunch of stuff

        self.currentFrame.Refresh()     # Hmm should I really do this
        wxYield()
        self._notebookCurrentPageNumber  = self._diagramNotebook.GetPageCount() - 1
        self.logger.warning(f'Current notebook page: {self._notebookCurrentPageNumber}')
        # self._diagramNotebook.SetSelection(self._notebookCurrentPageNumber)

        return document

    def closeCurrentProject(self):
        """
        Close the current project

        Returns:
            True if everything is ok
        """
        currentProject: IPyutProject = self._projectManager.currentProject
        if currentProject is None and self.currentFrame is not None:
            currentProject = self.getProjectFromFrame(self.currentFrame)
        if currentProject is None:
            PyutUtils.displayError("No frame to close !", "Error...")
            return False

        # Close the project
        if currentProject.modified is True:
            # frame = self._currentProject.getFrames()[0]
            frame = self._projectManager.currentProject.getFrames()[0]
            frame.SetFocus()
            self.showFrame(frame)

            dlg = MessageDialog(None, "Your project has not been saved. Would you like to save it ?", "Save changes ?", YES_NO | ICON_QUESTION)
            if dlg.ShowModal() == ID_YES:
                self._projectManager.saveProject(projectToSave=self._projectManager.currentProject)

        # Remove the frame in the notebook
        pages = list(range(self._diagramNotebook.GetPageCount()))
        pages.reverse()
        for i in pages:
            pageFrame = self._diagramNotebook.GetPage(i)
            if pageFrame in self._projectManager.currentProject.getFrames():
                self._diagramNotebook.DeletePage(i)

        self._removeProjectFromTree(pyutProject=currentProject)
        self._projectManager.removeProject(self._projectManager.currentProject)

        self.logger.debug(f'{self._projectManager.currentProject.filename=}')

        self.currentFrame = None

        currentProjects: PyutProjects = self._projectManager.projects
        nbrProjects: int = len(currentProjects)
        self.logger.debug(f'{nbrProjects=}')
        if nbrProjects > 0:
            newCurrentProject: IPyutProject = currentProjects[0]
            # self._updateTreeNotebookIfPossible(project=newCurrentProject)
            self._projectManager.updateTreeNotebookIfPossible(project=newCurrentProject)

        # self._mediator.updateTitle()  TODO V2 API update needed  Send event

    @deprecated(reason='use property .currentProject')
    def getCurrentProject(self) -> IPyutProject:
        """
        Get the current working project

        Returns:
            the current project or None if not found
        """
        return self._currentProject

    def isProjectLoaded(self, filename: str) -> bool:
        """
        Args:
            filename:

        Returns:
            `True` if the project is already loaded
        """
        return self._projectManager.isProjectLoaded(filename=filename)

    def saveFile(self):
        self._projectManager.saveProject(projectToSave=self._projectManager.currentProject)

    def openFile(self, filename, project: IPyutProject = None) -> bool:
        """
        Args:
            filename:
            project:

        Returns:
            `True` if operation succeeded
        """
        self._projectManager.openProject(filename=filename, project=project)

        return True

    def removeAllReferencesToUmlFrame(self, umlFrame: UmlDiagramsFrame):
        """
        Remove all my references to a given uml frame

        Args:
            umlFrame:
        """
        # Current frame ?
        if self.currentFrame is umlFrame:
            self.currentFrame = cast(UmlDiagramsFrame, None)

        pageCount: int = self._diagramNotebook.GetPageCount()
        for i in range(pageCount):
            pageFrame = self._diagramNotebook.GetPage(i)
            if pageFrame is umlFrame:
                self._diagramNotebook.DeletePage(i)
                break

    # noinspection PyUnusedLocal
    def _onDiagramNotebookPageChanged(self, event):
        """
        Callback for notebook page changed

        Args:
            event:
        """
        self._notebookCurrentPageNumber = self._diagramNotebook.GetSelection()
        self.logger.info(f'{self._notebookCurrentPageNumber=}')
        self.currentFrame = self._getCurrentFrameFromNotebook()

        # self._mediator.updateTitle()      # TODO to fill out V2
        self._getTreeItemFromFrame(self.currentFrame)

        # Register the current project
        self._currentProject = self.getProjectFromFrame(self.currentFrame)

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
        if isinstance(pyutData, UmlDiagramsFrame):
            frame: UmlDiagramsFrame = pyutData
            self.currentFrame = frame
            # self._currentProject = self.getProjectFromFrame(frame)
            self._projectManager.currentProject = self.getProjectFromFrame(frame)
            self._projectManager.syncPageFrameAndNotebook(frame=frame)

        elif isinstance(pyutData, PyutProjectV2):
            project: PyutProjectV2 = pyutData
            projectFrames: List[UmlFrameType] = project.getFrames()
            if len(projectFrames) > 0:
                self.currentFrame = projectFrames[0]
                self._projectManager.syncPageFrameAndNotebook(frame=self.currentFrame)
                # self._mediator.updateTitle()      TODO: V2 needs update
            self._projectManager.currentProject = project

    def _onProjectTreeRightClick(self, treeEvent: TreeEvent):

        itemId: TreeItemId = treeEvent.GetItem()
        data = self._projectTree.GetItemData(item=itemId)
        self.logger.info(f'Item Data: `{data}`')
        if isinstance(data, IPyutProject):
            self._popupProjectMenu()
        elif isinstance(data, UmlDiagramsFrame):            # TODO  We should put the IPyutDocument on the node
            self._popupProjectDocumentMenu()

    def _popupProjectMenu(self):

        # self._mediator.resetStatusText()      TODO V2 UI;  should send message

        if self._projectPopupMenu is None:
            self.logger.info(f'Create the project popup menu')
            [closeProjectMenuID] = PyutUtils.assignID(1)
            popupMenu: Menu = Menu('Actions')
            popupMenu.AppendSeparator()
            popupMenu.Append(closeProjectMenuID, 'Close Project', 'Remove project from tree', ITEM_NORMAL)
            popupMenu.Bind(EVT_MENU, self._onCloseProject, id=closeProjectMenuID)
            self._projectPopupMenu = popupMenu

        self.logger.info(f'currentProject: `{self._projectManager.currentProject}`')
        self._parentWindow.PopupMenu(self._projectPopupMenu)

    def _popupProjectDocumentMenu(self):

        if self._documentPopupMenu is None:

            self.logger.info(f'Create the document popup menu')

            [editDocumentNameMenuID, removeDocumentMenuID] = PyutUtils.assignID(2)

            popupMenu: Menu = Menu('Actions')
            popupMenu.AppendSeparator()
            popupMenu.Append(editDocumentNameMenuID, 'Edit Document Name', 'Change document name', ITEM_NORMAL)
            popupMenu.Append(removeDocumentMenuID,   'Remove Document',    'Delete it',            ITEM_NORMAL)

            popupMenu.Bind(EVT_MENU, self._onEditDocumentName, id=editDocumentNameMenuID)
            popupMenu.Bind(EVT_MENU, self._onRemoveDocument,   id=removeDocumentMenuID)

            self.__documentPopupMenu = popupMenu

        self.logger.info(f'Current Document: `{self.currentDocument}`')
        self._parentWindow.PopupMenu(self.__documentPopupMenu)

    # noinspection PyUnusedLocal
    def _onCloseProject(self, event: CommandEvent):
        self.closeCurrentProject()

    # noinspection PyUnusedLocal
    def _onEditDocumentName(self, event: CommandEvent):

        self.logger.info(f'{self._notebookCurrentPageNumber=}  {self._diagramNotebook.GetSelection()=}')
        if self._notebookCurrentPageNumber == -1:
            self._notebookCurrentPageNumber = self._diagramNotebook.GetSelection()    # must be default empty project

        currentDocument: IPyutDocument   = self.currentDocument
        dlgEditDocument: DlgEditDocument = DlgEditDocument(parent=self.currentFrame, dialogIdentifier=ID_ANY, document=currentDocument)
        dlgEditDocument.Destroy()

        #
        # TODO can cause
        #     self.__notebook.SetPageText(page=self.__notebookCurrentPage, text=currentDocument.title)
        # wx._core.wxAssertionError: C++ assertion ""((nPage) < GetPageCount())""
        # failed at dist-osx-py38/build/ext/wxWidgets/src/osx/notebook_osx.cpp(120)
        # in SetPageText(): SetPageText: invalid notebook page
        #
        self._diagramNotebook.SetPageText(page=self._notebookCurrentPageNumber, text=currentDocument.title)
        currentDocument.updateTreeText()

    # noinspection PyUnusedLocal
    def _onRemoveDocument(self, event: CommandEvent):
        """
        Invoked from the popup menu in the tree

        Args:
            event:
        """
        project:         IPyutProject  = self._projectManager.currentProject
        currentDocument: IPyutDocument = self.currentDocument
        project.removeDocument(currentDocument)

    def _getCurrentFrameFromNotebook(self):
        """
        Get the current frame in the notebook

        Returns:
        """

        noPage: int = self._notebookCurrentPageNumber
        self.logger.info(f'{noPage=}')
        if noPage == -1:
            return None
        frame = self._diagramNotebook.GetPage(noPage)
        return frame

    def _getTreeItemFromFrame(self, frame: UmlDiagramsFrame) -> TreeItemId:

        projectTree: ProjectTree = self._projectTree

        treeRootItemId: TreeItemId   = projectTree.GetRootItem()
        pyutData:       TreeDataType = projectTree.GetItemData(treeRootItemId)

        self.logger.info(f'{treeRootItemId=} {pyutData=} {frame=}')

        self.logger.info(f'{projectTree.GetCount()=}')
        return treeRootItemId

    def _removeProjectFromTree(self, pyutProject: IPyutProject):
        """
        Remove the project from the tree
        TODO: V2 UI this belongs in the project tree component itself
        Args:
            pyutProject:

        """
        """
        """
        projectTreeRoot: TreeItemId = pyutProject.projectTreeRoot
        self._projectTree.Delete(projectTreeRoot)

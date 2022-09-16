
from typing import List
from typing import Union
from typing import cast

from logging import Logger
from logging import getLogger

from os import path as osPath

# noinspection PyPackageRequirements
from deprecated import deprecated

from wx import EVT_MENU
from wx import EVT_NOTEBOOK_PAGE_CHANGED
from wx import EVT_TREE_ITEM_RIGHT_CLICK
from wx import EVT_TREE_SEL_CHANGED
from wx import ID_ANY
from wx import ITEM_NORMAL
from wx import Menu

from wx import SplitterWindow
from wx import Frame
from wx import TreeEvent
from wx import TreeItemId
from wx import CommandEvent

from wx import Yield as wxYield

from org.pyut.PyutConstants import PyutConstants
from org.pyut.PyutUtils import PyutUtils
from org.pyut.enums.DiagramType import DiagramType
from org.pyut.ui.IPyutDocument import IPyutDocument
from org.pyut.ui.IPyutProject import IPyutProject

from org.pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame
from org.pyut.uiv2.DiagramNotebook import DiagramNotebook
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
        self._projects:                  List[IPyutProject] = []
        self._currentProject:            IPyutProject       = cast(IPyutProject, None)
        self._currentFrame:              UmlDiagramsFrame   = cast(UmlDiagramsFrame, None)
        self._projectPopupMenu:          Menu               = cast(Menu, None)
        self._documentPopupMenu:         Menu               = cast(Menu, None)

        self._parentWindow.Bind(EVT_NOTEBOOK_PAGE_CHANGED, self._onDiagramNotebookPageChanged)
        self._parentWindow.Bind(EVT_TREE_SEL_CHANGED,      self._onProjectTreeSelectionChanged)
        self._projectTree.Bind(EVT_TREE_ITEM_RIGHT_CLICK,  self._onProjectTreeRightClick)

    @property
    def currentProject(self) -> IPyutProject:
        return self._currentProject

    @currentProject.setter
    def currentProject(self, newProject: IPyutProject):

        self.logger.info(f'{self._diagramNotebook.GetRowCount()=}')
        self._currentProject = newProject

        self._notebookCurrentPageNumber = self._diagramNotebook.GetPageCount() - 1
        self._diagramNotebook.SetSelection(self._notebookCurrentPageNumber)

        self.logger.info(f'{self._notebookCurrentPageNumber=}')

    @property
    def currentFrame(self) -> UmlDiagramsFrame:
        return self._currentFrame

    @currentFrame.setter
    def currentFrame(self, newFrame: UmlDiagramsFrame):
        self._currentFrame = newFrame

    @property
    def modified(self) -> bool:
        if self._currentProject is not None:
            return self._currentProject.modified
        else:
            return False

    @modified.setter
    def modified(self, theNewValue: bool = True):
        """
        Set the modified flag of the currently opened project

        Args:
            theNewValue:
        """
        if self._currentProject is not None:
            # mypy does not handle property setters
            self._currentProject.modified = theNewValue     # type: ignore
        # self._mediator.updateTitle()      TODO Fix V2 version

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
        self._currentFrame = frame
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
        for project in self._projects:
            if frame in project.getFrames():
                return project
        return cast(PyutProjectV2, None)

    def newProject(self) -> IPyutProject:
        """
        Begin a new project
        """
        project = PyutProjectV2(PyutConstants.DEFAULT_FILENAME, self._diagramNotebook, self._projectTree, self._projectTree.projectTreeRoot)

        projectTreeRoot: TreeItemId = self._projectTree.addProjectToTree(pyutProject=project)

        project.projectTreeRoot = projectTreeRoot

        self._projects.append(project)
        self._currentProject = project
        self._currentFrame   = cast(UmlDiagramsFrame, None)
        return project

    def newDocument(self, docType: DiagramType) -> IPyutDocument:
        """
        Create a new document;  It is up to the caller to update the PyutProject document list
        It is up to the caller to add it to the notebook

        Args:
            docType:  Type of document

        Returns: The newly created document
        """
        pyutProject: IPyutProject = self._currentProject
        if pyutProject is None:
            self.newProject()
            pyutProject = self.currentProject

        document: PyutDocumentV2  = PyutDocumentV2(parentFrame=self._diagramNotebook, project=pyutProject, docType=docType)

        document.addToTree(self._projectTree, pyutProject.projectTreeRoot)

        self.currentFrame    = document.diagramFrame
        self._currentProject = pyutProject      # TODO do not use property it does a bunch of stuff

        wxYield()
        self._notebookCurrentPageNumber  = self._diagramNotebook.GetPageCount() - 1
        self.logger.info(f'Current notebook page: {self._notebookCurrentPageNumber}')
        # self._diagramNotebook.SetSelection(self._notebookCurrentPageNumber)

        return document

    def closeCurrentProject(self):
        """
        Close the current project

        Returns:
            True if everything is ok
        """
        if self._currentProject is None and self._currentFrame is not None:
            self._currentProject = self.getProjectFromFrame(self._currentFrame)
        if self._currentProject is None:
            PyutUtils.displayError("No frame to close !", "Error...")
            return False

        # Close the file
        # if self._currentProject.modified is True
        #     frame = self._currentProject.getFrames()[0]
        #     frame.SetFocus()
        #     self.showFrame(frame)
        #
        #     dlg = MessageDialog(self.__parent, _("Your project has not been saved. "
        #                                          "Would you like to save it ?"), _("Save changes ?"), YES_NO | ICON_QUESTION)
        #     if dlg.ShowModal() == ID_YES:
        #         if self.saveFile() is False:
        #             return False

        # Remove the frame in the notebook
        pages = list(range(self._diagramNotebook.GetPageCount()))
        pages.reverse()
        for i in pages:
            pageFrame = self._diagramNotebook.GetPage(i)
            if pageFrame in self._currentProject.getFrames():
                self._diagramNotebook.DeletePage(i)

        # self._currentProject.removeFromTree()
        self._removeProjectFromTree(pyutProject=self._currentProject)
        self._projects.remove(self._currentProject)

        self.logger.debug(f'{self._currentProject.filename=}')
        self._currentProject = None
        self._currentFrame = None

        nbrProjects: int = len(self._projects)
        self.logger.debug(f'{nbrProjects=}')
        if nbrProjects > 0:
            self._updateTreeNotebookIfPossible(project=self._projects[0])

        # self._mediator.updateTitle()  TODO V2 API update needed

        return True

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
        for project in self._projects:
            if project.filename == filename:
                return True
        return False

    def openFile(self, filename, project: IPyutProject = None) -> bool:
        """
        Open a file
        TODO:  Fix V2 this does 2 things loads from a file or from a project

        Args:
            filename:
            project:

        Returns:
            `True` if operation succeeded
        """
        self.logger.info(f'{filename=} {project=}')
        # Exit if the file is already loaded
        if self.isProjectLoaded(filename) is True:
            PyutUtils.displayError("The selected file is already loaded !")
            return False

        # Create a new project ?
        if project is None:
            # project = PyutProjectV2(PyutConstants.DEFAULT_FILENAME, self._diagramNotebook, self._projectTree, self._projectTree.projectTreeRoot)
            project = self.newProject()

        # Load the project and add it
        try:
            if not project.loadFromFilename(filename):
                eMsg: str = f'{"The file cannot be loaded !"} - {filename}'
                PyutUtils.displayError(eMsg)
                return False
            self._projects.append(project)
            self._currentProject = project
        except (ValueError, Exception) as e:
            self.logger.error(f"An error occurred while loading the project ! {e}")
            raise e

        success: bool = self._addProjectToNotebook(project)
        self.logger.debug(f'{self._currentFrame=} {self.currentProject=} {self._diagramNotebook.GetSelection()=}')

        return success

    def removeAllReferencesToUmlFrame(self, umlFrame: UmlDiagramsFrame):
        """
        Remove all my references to a given uml frame

        Args:
            umlFrame:
        """
        # Current frame ?
        if self._currentFrame is umlFrame:
            self._currentFrame = cast(UmlDiagramsFrame, None)

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
        self._currentFrame = self._getCurrentFrameFromNotebook()

        # self._mediator.updateTitle()      # TODO to fill out V2
        self._getTreeItemFromFrame(self._currentFrame)

        # Register the current project
        self._currentProject = self.getProjectFromFrame(self._currentFrame)

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
            self._currentFrame = frame
            self._currentProject = self.getProjectFromFrame(frame)
            self._syncPageFrameAndNotebook(frame=frame)

        elif isinstance(pyutData, PyutProjectV2):
            project: PyutProjectV2 = pyutData
            projectFrames: List[UmlFrameType] = project.getFrames()
            if len(projectFrames) > 0:
                self._currentFrame = projectFrames[0]
                self._syncPageFrameAndNotebook(frame=self._currentFrame)
                # self._mediator.updateTitle()      TODO: V2 needs update
            self._currentProject = project

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
            popupMenu.Bind(EVT_MENU, self.__onCloseProject, id=closeProjectMenuID)
            self._projectPopupMenu = popupMenu

        self.logger.info(f'currentProject: `{self._currentProject}`')
        self._parentWindow.PopupMenu(self._projectPopupMenu)

    # noinspection PyUnusedLocal
    def __onCloseProject(self, event: CommandEvent):
        self.closeCurrentProject()

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

    def _addProjectToNotebook(self, project: IPyutProject) -> bool:

        success: bool = True
        self.logger.info(f'{project=}')
        try:
            for document in project.documents:
                diagramTitle: str = document.title
                shortName:    str = self._shortenNotebookPageDiagramName(diagramTitle)
                self._diagramNotebook.AddPage(document.diagramFrame, shortName)

            self._notebookCurrentPageNumber = self._diagramNotebook.GetPageCount()-1
            self._diagramNotebook.SetSelection(self._notebookCurrentPageNumber)

            self._updateTreeNotebookIfPossible(project=project)

        except (ValueError, Exception) as e:
            PyutUtils.displayError(f"An error occurred while adding the project to the notebook {e}")
            success = False

        return success

    def _updateTreeNotebookIfPossible(self, project: IPyutProject):
        """

        Args:
            project:
        """
        project.selectFirstDocument()

        if len(project.documents) > 0:
            self._currentFrame = project.documents[0].diagramFrame
            self._syncPageFrameAndNotebook(frame=self._currentFrame)

    def _syncPageFrameAndNotebook(self, frame: UmlDiagramsFrame):
        """

        Args:
            frame:
        """

        for i in range(self._diagramNotebook.GetPageCount()):
            pageFrame = self._diagramNotebook.GetPage(i)
            if pageFrame is frame:
                self._diagramNotebook.SetSelection(i)
                break

    def _shortenNotebookPageDiagramName(self, diagramTitle: str) -> str:
        """
        Return a shorter filename to display; For file names longer
        than `MAX_NOTEBOOK_PAGE_NAME_LENGTH` this method takes the first
        four characters and the last eight as the shortened file name

        Args:
            diagramTitle:  The diagram name to display

        Returns:
            A short diagram name
        """
        justFileName: str = osPath.split(diagramTitle)[1]
        if len(justFileName) > MAX_NOTEBOOK_PAGE_NAME_LENGTH:
            firstFour: str = justFileName[:4]
            lastEight: str = justFileName[-8:]
            return f'{firstFour}{lastEight}'
        else:
            return justFileName

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

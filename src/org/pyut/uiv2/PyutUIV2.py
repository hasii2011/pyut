
from typing import List
from typing import Union
from typing import cast

from logging import Logger
from logging import getLogger

# noinspection PyPackageRequirements
from deprecated import deprecated

from wx import EVT_NOTEBOOK_PAGE_CHANGED
from wx import ID_ANY

from wx import SplitterWindow
from wx import Frame
from wx import TreeItemId

from org.pyut.PyutConstants import PyutConstants
from org.pyut.ui.PyutProject import PyutProject
from org.pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame
from org.pyut.uiv2.DiagramNotebook import DiagramNotebook
from org.pyut.uiv2.ProjectTree import ProjectTree

TreeDataType = Union[PyutProject, UmlDiagramsFrame]

SASH_POSITION: int = 160        # TODO make this a preference and remember it


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

        self._notebookCurrentPageNumber: int               = -1
        self._projects:                  List[PyutProject] = []
        self._currentProject:            PyutProject       = cast(PyutProject, None)
        self._currentFrame:              UmlDiagramsFrame  = cast(UmlDiagramsFrame, None)

        self._parentWindow.Bind(EVT_NOTEBOOK_PAGE_CHANGED, self._onNotebookPageChanged)

    @property
    def currentProject(self) -> PyutProject:
        return self._currentProject

    @currentProject.setter
    def currentProject(self, newProject: PyutProject):

        self.logger.info(f'{self._diagramNotebook.GetRowCount()=}')
        self._currentProject = newProject

        self._notebookCurrentPageNumber = self._diagramNotebook.GetPageCount() - 1
        self._diagramNotebook.SetSelection(self._notebookCurrentPageNumber)

        self.logger.info(f'{self._notebookCurrentPageNumber=}')

    def getProjectFromFrame(self, frame: UmlDiagramsFrame) -> PyutProject:
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
        return cast(PyutProject, None)

    def newProject(self):
        """
        Begin a new project
        """
        project = PyutProject(PyutConstants.DEFAULT_FILENAME, self._diagramNotebook, self._projectTree, self._projectTree.projectTreeRoot)
        self._projects.append(project)
        self._currentProject = project
        self._currentFrame = None

    @deprecated(reason='use property .currentProject')
    def getCurrentProject(self) -> PyutProject:
        """
        Get the current working project

        Returns:
            the current project or None if not found
        """
        return self._currentProject

    # noinspection PyUnusedLocal
    def _onNotebookPageChanged(self, event):
        """
        Callback for notebook page changed

        Args:
            event:
        """
        self._notebookCurrentPageNumber = self._diagramNotebook.GetSelection()
        self.logger.info(f'{self._notebookCurrentPageNumber=}')
        self._currentFrame = self._getCurrentFrameFromNotebook()

        # self._mediator.updateTitle()
        self._getTreeItemFromFrame(self._currentFrame)

        # Register the current project
        self._currentProject = self.getProjectFromFrame(self._currentFrame)

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

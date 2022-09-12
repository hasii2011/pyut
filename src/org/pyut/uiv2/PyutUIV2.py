
from typing import List
from typing import Union
from typing import cast

from logging import Logger
from logging import getLogger

from os import path as osPath

# noinspection PyPackageRequirements
from deprecated import deprecated

from wx import EVT_NOTEBOOK_PAGE_CHANGED
from wx import ID_ANY

from wx import SplitterWindow
from wx import Frame
from wx import TreeItemId

from wx import Yield as wxYield

from org.pyut.PyutConstants import PyutConstants
from org.pyut.PyutUtils import PyutUtils
from org.pyut.enums.DiagramType import DiagramType

from org.pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame
from org.pyut.uiv2.DiagramNotebook import DiagramNotebook
from org.pyut.uiv2.ProjectTree import ProjectTree
from org.pyut.uiv2.PyutDocumentV2 import PyutDocumentV2
from org.pyut.uiv2.PyutProjectV2 import PyutProjectV2

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

        self._notebookCurrentPageNumber: int               = -1
        self._projects:                  List[PyutProjectV2] = []
        self._currentProject:            PyutProjectV2     = cast(PyutProjectV2, None)
        self._currentFrame:              UmlDiagramsFrame  = cast(UmlDiagramsFrame, None)

        self._parentWindow.Bind(EVT_NOTEBOOK_PAGE_CHANGED, self._onNotebookPageChanged)

    @property
    def currentProject(self) -> PyutProjectV2:
        return self._currentProject

    @currentProject.setter
    def currentProject(self, newProject: PyutProjectV2):

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
            self._currentProject.modified = theNewValue
        # self._mediator.updateTitle()      TODO Fix V2 version

    def registerUmlFrame(self, frame: UmlDiagramsFrame):
        """
        Register the current UML Frame

        Args:
            frame:
        """
        self._currentFrame = frame
        self._currentProject = self.getProjectFromFrame(frame)

    def getProjectFromFrame(self, frame: UmlDiagramsFrame) -> PyutProjectV2:
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

    def newProject(self):
        """
        Begin a new project
        """
        project = PyutProjectV2(PyutConstants.DEFAULT_FILENAME, self._diagramNotebook, self._projectTree, self._projectTree.projectTreeRoot)

        projectTreeRoot: TreeItemId = self._projectTree.addProjectToTree(pyutProject=project)

        project.projectTreeRoot = projectTreeRoot

        self._projects.append(project)
        self._currentProject = project
        self._currentFrame   = None

    def newDocument(self, docType: DiagramType):
        """
        Begin a new document

        Args:
            docType:  Type of document
        """
        pyutProject: PyutProjectV2 = self._currentProject
        if pyutProject is None:
            self.newProject()
            pyutProject = self.currentProject

        document: PyutDocumentV2  = PyutDocumentV2(parentFrame=self._diagramNotebook, project=pyutProject, docType=docType)
        pyutProject.documents.append(document)
        document.addToTree(self._projectTree, pyutProject.projectTreeRoot)

        diagramFrame:    UmlDiagramsFrame = document.diagramFrame

        self.currentFrame   = diagramFrame
        self._currentProject = pyutProject      # TODO do not use property it does a bunch of stuff

        shortName: str = self.__shortenNotebookPageFileName(pyutProject.filename)
        self._diagramNotebook.AddPage(diagramFrame, shortName)
        wxYield()
        self._notebookCurrentPageNumber  = self._diagramNotebook.GetPageCount() - 1
        self.logger.info(f'Current notebook page: {self._notebookCurrentPageNumber}')
        self._diagramNotebook.SetSelection(self._notebookCurrentPageNumber)

    @deprecated(reason='use property .currentProject')
    def getCurrentProject(self) -> PyutProjectV2:
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

    def openFile(self, filename, project: PyutProjectV2) -> bool:
        """
        Open a file

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

        # self._mediator.updateTitle()      # TODO to fill out V2
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

    def _addProjectToNotebook(self, project: PyutProjectV2) -> bool:

        success: bool = True
        try:
            for document in project.getDocuments():
                diagramTitle: str = document.title
                shortName:    str = self.__shortenNotebookPageFileName(diagramTitle)
                self._diagramNotebook.AddPage(document.diagramFrame, shortName)

            self._notebookCurrentPageNumber = self._diagramNotebook.GetPageCount()-1
            self._diagramNotebook.SetSelection(self._notebookCurrentPageNumber)

            self._updateTreeNotebookIfPossible(project=project)

        except (ValueError, Exception) as e:
            PyutUtils.displayError(f"An error occurred while adding the project to the notebook {e}")
            success = False

        return success

    def __shortenNotebookPageFileName(self, filename: str) -> str:
        """
        Return a shorter filename to display; For file names longer
        than `MAX_NOTEBOOK_PAGE_NAME_LENGTH` this method takes the first
        four characters and the last eight as the shortened file name

        Args:
            filename:  The file name to display

        Returns:
            A better file name
        """
        justFileName: str = osPath.split(filename)[1]
        if len(justFileName) > MAX_NOTEBOOK_PAGE_NAME_LENGTH:
            firstFour: str = justFileName[:4]
            lastEight: str = justFileName[-8:]
            return f'{firstFour}{lastEight}'
        else:
            return justFileName

    def _updateTreeNotebookIfPossible(self, project: PyutProjectV2):
        """

        Args:
            project:
        """
        project.selectFirstDocument()

        if len(project.getDocuments()) > 0:
            self._currentFrame = project.getDocuments()[0].diagramFrame
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

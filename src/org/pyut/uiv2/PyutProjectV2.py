
from typing import List
from typing import cast
from typing import TYPE_CHECKING

from os import path as osPath

from logging import Logger
from logging import getLogger

# noinspection PyPackageRequirements
from deprecated import deprecated

from wx import TreeItemId
from wx import BeginBusyCursor
from wx import EndBusyCursor

from org.pyut.PyutUtils import PyutUtils

from org.pyut.preferences.PyutPreferences import PyutPreferences
from org.pyut.uiv2.IPyutDocument import IPyutDocument
from org.pyut.ui.IPyutProject import IPyutProject
from org.pyut.ui.IPyutProject import PyutDocuments
from org.pyut.ui.IPyutProject import UmlFrameType

from org.pyut.ui.Mediator import Mediator
from org.pyut.uiv2.Types import Frames

if TYPE_CHECKING:
    from org.pyut.uiv2.ProjectTree import ProjectTree


class PyutProjectV2(IPyutProject):
    """
    Project : contain multiple documents

    """

    def __init__(self, filename: str, tree: 'ProjectTree', treeRoot: TreeItemId):
        """

        Args:
            filename:       The project file name
            tree:           The tree control
            treeRoot:       Where to root the tree
        """
        super().__init__()
        self.logger:       Logger   = getLogger(__name__)
        self._mediator:    Mediator = Mediator()

        self._documents: PyutDocuments = PyutDocuments([])

        self._filename: str     = filename      # Project filename
        self._modified: bool    = False         # Was the project modified ?
        self._codePath: str     = ""

        self._treeRootParent:  TreeItemId  = treeRoot                 # Parent of the project root entry
        self._tree:            'ProjectTree' = tree                    # Tree I belong to

        self._projectTreeRoot:  TreeItemId = cast(TreeItemId, None)   # Root of this project entry in the tree

    @property
    def filename(self) -> str:
        """
        Returns:  The project's filename
        """
        return self._filename

    @filename.setter
    def filename(self, filename: str):
        """
        Set the project's filename

        Args:
            filename:
        """
        self._filename = filename
        # self.updateTreeText()

    @property
    def codePath(self) -> str:
        return self._codePath

    @codePath.setter
    def codePath(self, newValue: str):
        self._codePath = newValue

    @property
    def modified(self) -> bool:
        """

        Returns:  'True' if it has been else 'False'
        """
        return self._modified

    @modified.setter
    def modified(self, value: bool = True):
        """
        Set that the project has been modified
        Args:
            value:  'True' if it has been else 'False'
        """
        self._modified = value

    @property
    def documents(self) -> PyutDocuments:
        """
        Return the documents

        Returns:  A list of documents
        """
        return self._documents

    @property
    def projectTreeRoot(self) -> TreeItemId:
        """
        A piece of UI information needed to communicate with the UI component

        Returns: The opaque item where this project's documents are display on the UI Tree
        """
        return self._projectTreeRoot

    @projectTreeRoot.setter
    def projectTreeRoot(self, newValue: TreeItemId):
        self._projectTreeRoot = newValue

    @property
    def frames(self) -> Frames:
        """
        Return every frame from the project's documents

        Returns:
            List of frames
        """
        frameList: Frames = Frames([document.diagramFrame for document in self._documents])

        return frameList

    @deprecated(reason='use the "codePath" property')
    def getCodePath(self) -> str:
        """
        Returns: The root path where the corresponding code resides.
        """
        return self._codePath

    @deprecated(reason='use the "codePath" property')
    def setCodePath(self, codePath: str):
        """
        Set the root path where the corresponding code resides.

        Args:
            codePath:
        """
        self._codePath = codePath

    def selectSelf(self):
        self._tree.SelectItem(self._projectTreeRoot)

    @deprecated(reason='Use .documents property')
    def getDocuments(self) -> PyutDocuments:
        """
        Return the documents

        Returns:  A list of documents
        """
        return self._documents

    def deleteDocument(self, document: IPyutDocument):
        self._documents.remove(document)

    def insertProject(self, filename: str) -> bool:
        """
        Insert another project into this one

        Args:
            filename: filename to open

        Returns:
            `True` if the operation succeeded
        """
        # Load the file
        from org.pyut.persistence import IoFile
        BeginBusyCursor()
        io = IoFile.IoFile()

        try:
            io.open(filename, self)
            self._modified = False
        except (ValueError, Exception) as e:
            PyutUtils.displayError(f"Error loading file {e}")
            EndBusyCursor()
            return False
        EndBusyCursor()

        # Update text   TODO caller must ue project manager call
        # self.updateTreeText()

        # Register to mediator
        if len(self._documents) > 0:
            frame = self._documents[0].diagramFrame
            self._mediator.getFileHandling().registerUmlFrame(frame)

        # Return
        return True

    @deprecated(reason='Use .frames property')
    def getFrames(self) -> List[UmlFrameType]:
        """
        Get all the project's frames

        Returns:
            List of frames
        """
        frameList = [document.diagramFrame for document in self._documents]
        return frameList

    def selectFirstDocument(self):

        treeTuple = self._tree.GetFirstChild(self._projectTreeRoot)

        treeDocItem: TreeItemId = treeTuple[0]
        # Make sure this project has some documents
        if treeDocItem.IsOk():
            treeData = self._tree.GetItemData(treeDocItem)
            self.logger.debug(f'{treeData}')
            self._tree.SelectItem(treeDocItem)

    def _justTheFileName(self, filename):
        """
        Return just the file name portion of the fully qualified path

        Args:
            filename:  file name to display

        Returns:
            A better file name
        """
        regularFileName: str = osPath.split(filename)[1]
        if PyutPreferences().displayProjectExtension is False:
            regularFileName = osPath.splitext(regularFileName)[0]

        return regularFileName

    def __repr__(self):
        projectName: str = PyutUtils.extractFileName(self._filename)
        return f'[Project: {projectName} modified: {self._modified}]'

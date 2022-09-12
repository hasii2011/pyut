
from typing import List
from typing import NewType
from typing import Union
from typing import cast

from os import path as osPath

from logging import DEBUG
from logging import Logger
from logging import getLogger

from deprecated import deprecated
from wx import ID_NO
from wx import YES_NO

from wx import MessageDialog
from wx import Notebook
from wx import TreeCtrl
from wx import TreeItemId
from wx import BeginBusyCursor
from wx import EndBusyCursor

from wx import Yield as wxYield

from org.pyut.PyutUtils import PyutUtils

from org.pyut.enums.DiagramType import DiagramType
from org.pyut.general.exceptions.UnsupportedXmlFileFormat import UnsupportedXmlFileFormat
from org.pyut.preferences.PyutPreferences import PyutPreferences

from org.pyut.ui.Mediator import Mediator
from org.pyut.ui.PyutDocument import PyutDocument
from org.pyut.ui.umlframes.UmlClassDiagramsFrame import UmlClassDiagramsFrame
from org.pyut.ui.umlframes.UmlSequenceDiagramsFrame import UmlSequenceDiagramsFrame

# noinspection PyProtectedMember
from org.pyut.general.Globals import _

# Until I figure out how to stop mypy from complaining
# TODO:   This should just be the following:
#          UmlFrameType = Union[UmlClassDiagramsFrame, UmlSequenceDiagramsFrame]
UmlFrameType = NewType('UmlFrameType', Union[UmlClassDiagramsFrame, UmlSequenceDiagramsFrame])  # type: ignore


class PyutProject:
    """
    Project : contain multiple documents

    """

    def __init__(self, filename: str, parentFrame: Notebook, tree: TreeCtrl, treeRoot: TreeItemId):
        """

        Args:
            filename:       The project file name
            parentFrame:
            tree:           The tree control
            treeRoot:       Where to root the tree
        """
        self.logger:       Logger   = getLogger(__name__)
        self._parentFrame: Notebook = parentFrame   # Parent frame
        self._mediator:    Mediator = Mediator()

        self._documents: List[PyutDocument] = []            # List of documents

        self._filename: str     = filename      # Project filename
        self._modified: bool    = False         # Was the project modified ?
        self._codePath: str     = ""
        self._treeRootParent: TreeItemId = treeRoot                 # Parent of the project root entry
        self._treeRoot:       TreeItemId = cast(TreeItemId, None)   # Root of the project entry in the tree
        self._tree:           TreeCtrl   = tree                     # Tree I belong to
        self.addToTree()

    def selectSelf(self):
        self._tree.SelectItem(self._treeRoot)

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
        self.updateTreeText()

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

    def getDocuments(self) -> List[PyutDocument]:
        """
        Return the documents

        Returns:  A list of documents
        """
        return self._documents

    @property
    def codePath(self) -> str:
        return self._codePath

    @codePath.setter
    def codePath(self, newValue: str ):
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

    def addToTree(self):
        """
        Add the project to the project tree
        """
        justTheFileName: str = self._justTheFileName(self._filename)
        self._treeRoot = self._tree.AppendItem(self._treeRootParent, justTheFileName, data=self)
        self._tree.Expand(self._treeRoot)

        # Add the frames
        for document in self._documents:
            document.addToTree(self._tree, self._treeRoot)

    def removeFromTree(self):
        """
        Remove the project from the tree
        """
        self._tree.Delete(self._treeRoot)

    def loadFromFilename(self, filename: str) -> bool:
        """
        Load a project from a file

        Args:
            filename: filename to open

        Returns:
            `True` if the operation succeeded
        """
        # Load the file
        self.logger.info(f'loadFromFilename: {filename=}')
        BeginBusyCursor()
        from org.pyut.persistence.IoFile import IoFile  # Avoid Nuitka cyclical dependency

        io: IoFile = IoFile()
        wxYield()       # to treat the uml frame refresh in newDiagram before loading
        # Load the file
        self._filename = filename
        try:
            io.open(filename, self)
            self._modified = False
        except (ValueError, Exception, UnsupportedXmlFileFormat) as e:
            EndBusyCursor()
            self.logger.error(f"Error loading file: {e}")
            raise e

        EndBusyCursor()
        self.updateTreeText()
        wxYield()

        from org.pyut.ui.PyutUI import PyutUI   # avoid cyclical imports

        if len(self._documents) > 0:
            # self._mediator.getFileHandling().showFrame(self._documents[0].getFrame())
            # self._documents[0].getFrame().Refresh()
            # self._mediator.getFileHandling().showFrame(documentFrame)

            documentFrame: UmlFrameType        = self._documents[0].diagramFrame
            mediator:      Mediator            = self._mediator
            tbh:           PyutUI = mediator.getFileHandling()

            self.logger.debug(f'{documentFrame=}')
            documentFrame.Refresh()
            tbh.showFrame(documentFrame)

            if self.logger.isEnabledFor(DEBUG):
                notebook = tbh.notebook
                self.logger.debug(f'{tbh.currentFrame=} {tbh.currentProject=} {notebook.GetSelection()=}')

            return True
        else:
            return False

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
            PyutUtils.displayError(_(f"Error loading file {e}"))
            EndBusyCursor()
            return False
        EndBusyCursor()

        # Update text
        self.updateTreeText()

        # Register to mediator
        if len(self._documents) > 0:
            frame = self._documents[0].diagramFrame
            self._mediator.getFileHandling().registerUmlFrame(frame)

        # Return
        return True

    def newDocument(self, documentType: DiagramType) -> PyutDocument:
        """
        Create a new document

        Args:
            documentType: The document type to create

        Returns:
            the newly created PyutDocument
        """
        document = PyutDocument(self._parentFrame, self, documentType)
        self._documents.append(document)
        document.addToTree(self._tree, self._treeRoot)
        frame = document.diagramFrame
        self._mediator.getFileHandling().registerUmlFrame(frame)
        return document

    def getFrames(self) -> List[UmlFrameType]:
        """
        Get all the project's frames

        Returns:
            List of frames
        """
        frameList = [document.diagramFrame for document in self._documents]
        return frameList

    def saveXmlPyut(self):
        """
        save the project
        """
        from org.pyut.persistence.IoFile import IoFile
        io: IoFile = IoFile()
        BeginBusyCursor()
        try:
            io.save(self)
            self._modified = False
            self.updateTreeText()
        except (ValueError, Exception) as e:
            PyutUtils.displayError(_(f"An error occurred while saving project {e}"))
        EndBusyCursor()

    def updateTreeText(self):
        """
        Update the tree text for this document
        """
        self._tree.SetItemText(self._treeRoot, self._justTheFileName(self._filename))
        for document in self._documents:
            self.logger.info(f'updateTreeText: {document=}')
            document.updateTreeText()

    def removeDocument(self, document, confirmation=True):
        """
        Remove a given document from the project.

        Args:
            document: PyutDocument to remove from this project
            confirmation:  If `True` ask for confirmation
        """
        frame = document.diagramFrame

        if confirmation:
            self._mediator.getFileHandling().showFrame(frame)

            dlg = MessageDialog(self._mediator.getUmlFrame(), _("Are you sure to remove the document ?"),
                                _("Remove a document from a project"), YES_NO)
            if dlg.ShowModal() == ID_NO:
                dlg.Destroy()
                return
            dlg.Destroy()

        # Remove references

        fileHandling = self._mediator.getFileHandling()
        fileHandling.removeAllReferencesToUmlFrame(frame)

        document.removeFromTree()

        # Remove document from documents list
        self._documents.remove(document)

    def selectFirstDocument(self):

        treeTuple = self._tree.GetFirstChild(self._treeRoot)

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

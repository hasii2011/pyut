from typing import List
from typing import NewType
from typing import Union

from wx import ID_NO
from wx import TreeCtrl
from wx import TreeItemId
from wx import YES_NO

from wx import MessageDialog
from wx import Notebook

from wx import BeginBusyCursor
from wx import EndBusyCursor

from org.pyut.PyutUtils import PyutUtils
from org.pyut.PyutDocument import PyutDocument
from org.pyut.persistence.IoFile import IoFile

from org.pyut.enums.DiagramType import DiagramType

from org.pyut.general.Mediator import getMediator
from org.pyut.general.Globals import _
from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame
from org.pyut.ui.UmlSequenceDiagramsFrame import UmlSequenceDiagramsFrame


def shorterFilename(filename):
    """
    Return a shorter filename to display

    Args:
        filename:  file name to display

    Returns:
        String better file name
    """

    import os
    return os.path.split(filename)[1]


UmlFrameType = NewType('UmlFrameType', Union[UmlClassDiagramsFrame, UmlSequenceDiagramsFrame])


class PyutProject:
    """
    Project : contain multiple documents

    """

    def __init__(self, filename: str, parentFrame: Notebook, tree: TreeCtrl, treeroot: TreeItemId):
        """

        Args:
            filename:       The project file name
            parentFrame:
            tree:           The tree control
            treeroot:       Where to root the tree
        """

        self._parentFrame   = parentFrame   # Parent frame
        self._ctrl          = getMediator()

        self._documents: List[PyutDocument] = []            # List of documents

        self._filename: str     = filename      # Project filename
        self._modified: bool    = False         # Was the project modified ?
        self._treeRootParent = treeroot     # Parent of the project root entry
        self._tree          = tree          # Tree I belong to
        self._treeRoot      = None          # Root of the project entry in the tree
        self._codePath: str      = ""
        self.addToTree()

    def setFilename(self, filename):
        """
        Get the project's filename

        @author C.Dutoit
        @return String : The project filename
        """
        self._filename = filename
        self.updateTreeText()

    def getFilename(self):
        """
        Get the project's filename

        @author C.Dutoit
        @return String : The project filename
        """
        return self._filename

    def getCodePath(self):
        """
        Get the root path where the corresponding code relies.

        @return string
        """
        return self._codePath

    def setCodePath(self, codepath):
        """
        Set the root path where the corresponding code relies.

        @param codepath
        """
        self._codePath = codepath

    def getDocuments(self):
        """
        Return the documents

        @author C.Dutoit
        """
        return self._documents

    def setModified(self, value=True):
        """
        Define the modified attribute

        @author C.Dutoit
        """
        self._modified = value

    def getModified(self):
        """
        Return the modified attribute

        @author C.Dutoit
        """
        return self._modified

    def addToTree(self):
        """
        Add the project to the project tree
        """
        # self._treeRoot = self._tree.AppendItem(self._treeRootParent, shorterFilename(self._filename), data=TreeItemData(self))
        self._treeRoot = self._tree.AppendItem(self._treeRootParent, shorterFilename(self._filename), data=self)
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
        BeginBusyCursor()
        io = IoFile()
        # wx.Yield() # to treat the umlframe refresh in newDiagram before loading
        # Load the file
        self._filename = filename
        try:
            io.open(filename, self)
            self._modified = False
        except (ValueError, Exception) as e:
            EndBusyCursor()
            PyutUtils.displayError(_(f"Error loading file: {e}"))
            return False

        EndBusyCursor()
        # Update text
        self.updateTreeText()

        # Register to mediator
        # if len(self._documents)>0:
        # self._ctrl.registerUMLFrame(self._documents[0].getFrame())
        # print ">>>PyutProject-loadFromFilename-7"
        if len(self._documents) > 0:
            self._ctrl.getFileHandling().showFrame(self._documents[0].getFrame())
            self._documents[0].getFrame().Refresh()
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
            frame = self._documents[0].getFrame()
            self._ctrl.getFileHandling().registerUmlFrame(frame)

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
        frame = document.getFrame()
        self._ctrl.getFileHandling().registerUmlFrame(frame)
        return document

    def getFrames(self) -> List[UmlFrameType]:
        """
        Get all the project's frames

        Returns:
            List of frames
        """
        frameList = [document.getFrame() for document in self._documents]
        return frameList

    def saveXmlPyut(self):
        """
        save the project
        """
        from org.pyut.persistence import IoFile
        io = IoFile.IoFile()
        BeginBusyCursor()
        try:
            io.save(self)
            self._modified = False
            self.updateTreeText()
        except (ValueError, Exception) as e:
            PyutUtils.displayError(_(f"An error occured while saving project {e}"))
        EndBusyCursor()

    def updateTreeText(self):
        """
        Update the tree text for this document
        """
        self._tree.SetItemText(self._treeRoot, shorterFilename(self._filename))
        for document in self._documents:
            document.updateTreeText()

    def removeDocument(self, document, confirmation=True):
        """
        Remove a given document from the project.

        Args:
            document: PyutDocument to remove from this project
            confirmation:  If `True` ask for confirmation
        """

        # Get frame
        frame = document.getFrame()

        # Confirmation
        # self._ctrl.registerUMLFrame(frame)
        if confirmation:
            self._ctrl.getFileHandling().showFrame(frame)
            dlg = MessageDialog(self._parentFrame, _("Are you sure to remove the document ?"), _("Remove a document from a project"), YES_NO)
            if dlg.ShowModal() == ID_NO:
                dlg.Destroy()
                return
            dlg.Destroy()

        # Remove references
        from org.pyut.general import Mediator
        ctrl = Mediator.getMediator()
        fileHandling = ctrl.getFileHandling()
        fileHandling.removeAllReferencesToUmlFrame(frame)

        # Remove frame
        # frame.Close()  # DONE by fileHandling.removeAllRef...
        # self._ctrl.registerUMLFrame(None)

        # Remove from tree
        document.removeFromTree()

        # Remove document from documents list
        self._documents.remove(document)

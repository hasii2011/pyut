
from logging import Logger
from logging import getLogger

from org.pyut.PyutConstants import DiagramsLabels

# from org.pyut.PyutConstants import CLASS_DIAGRAM
# from org.pyut.PyutConstants import SEQUENCE_DIAGRAM
# from org.pyut.PyutConstants import USECASE_DIAGRAM
from org.pyut.enums.DiagramType import DiagramType

from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame
from org.pyut.ui.UmlSequenceDiagramsFrame import UmlSequenceDiagramsFrame

from org.pyut.PyutUtils import PyutUtils


def shorterFilename(filename):
    """
    Return a shorter filename to display

    @param filename file name to display
    @return String better file name
    @since 1.0
    @author C.Dutoit <dutoitc@hotmail.com>
    """
    import os
    return os.path.split(filename)[1]


class PyutDocument:
    """
    Document : Contain a document : frames, properties, ...

    :author: C.Dutoit
    :contact: <dutoitc@hotmail.com>
    :version: $Revision: 1.8 $
    """

    def __init__(self, parentFrame, project, docType: DiagramType):
        """
        Constructor.

        @param docType : Type of document; one cited in PyutConsts.py
        @author C.Dutoit
        """
        self.logger: Logger = getLogger(__name__)
        self._parentFrame    = None
        self._project        = project
        self._treeRoot       = None         # Root of the project entry in the tree
        self._treeRootParent = None         # Parent of the project root entry
        self._tree           = None         # Tree I am belonging to

        self._type: DiagramType = docType

        self.logger.debug(f'Project: {project} PyutDocument using type {docType}')
        if docType == DiagramType.CLASS_DIAGRAM:
            self._title = DiagramsLabels[docType]
            self._frame = UmlClassDiagramsFrame(parentFrame)
        elif docType == DiagramType.SEQUENCE_DIAGRAM:
            self._title = DiagramsLabels[docType]
            self._frame = UmlSequenceDiagramsFrame(parentFrame)
        elif docType == DiagramType.USECASE_DIAGRAM:
            self._title = DiagramsLabels[docType]
            self._frame = UmlClassDiagramsFrame(parentFrame)
        else:
            PyutUtils.displayError(f'Unsupported diagram type; replacing by class diagram: {docType}')
            self._title = DiagramsLabels[DiagramType.CLASS_DIAGRAM]
            self._frame = UmlClassDiagramsFrame(parentFrame)

    def getType(self):
        """
        Return the document's type

        @author C.Dutoit
        @return String : the document's type as string
        """
        return self._type

    def getDiagramTitle(self):
        """
        Return the filename for captions

        @author C.Dutoit
        @return String : the caption
        """
        return self._project.getFilename() + "/" + self._title

    def getFrame(self):
        """
        Return the document's frame

        @author C.Dutoit
        @return xxxFrame this document's frame
        """
        return self._frame

    def addToTree(self, tree, root):
        self._tree = tree
        self._treeRootParent = root
        # Add the project to the project tree
        self._treeRoot = tree.AppendItem(
                         self._treeRootParent,
                         self._title)
        # self._tree.Expand(self._treeRoot)
        # self._tree.SetPyData(self._treeRoot, self._frame)
        self._tree.SetItemData(self._treeRoot, self._frame)

    def updateTreeText(self):
        """
        Update the tree text for this document

        @author C.Dutoit
        """
        self._tree.SetItemText(self._treeRoot, self._title)

    def removeFromTree(self):
        """
        Remove this document.
        """
        # Remove from tree
        self._tree.Delete(self._treeRoot)

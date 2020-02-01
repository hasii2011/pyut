
from logging import Logger
from logging import getLogger

from wx import TreeCtrl
from wx import TreeItemId

from org.pyut.PyutConstants import DiagramsLabels

from org.pyut.enums.DiagramType import DiagramType

from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame
from org.pyut.ui.UmlSequenceDiagramsFrame import UmlSequenceDiagramsFrame

from org.pyut.PyutUtils import PyutUtils


class PyutDocument:
    """
    Document : Contain a document : frames, properties, ...
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

    def getType(self) -> DiagramType:
        """

        Returns:
                The document type
        """
        return self._type

    def getDiagramTitle(self) -> str:
        """

        Returns:
            The diagram caption
        """
        return self._project.getFilename() + "/" + self._title

    def getFrame(self):
        """
        Return the document's frame

        @author C.Dutoit
        @return xxxFrame this document's frame
        """
        return self._frame

    def addToTree(self, tree: TreeCtrl, root: TreeItemId):
        """

        Args:
            tree:   The tree control
            root:   The itemId of the parent root
        """
        self._tree: TreeCtrl = tree
        self._treeRootParent: TreeItemId = root

        # Add the project to the project tree
        self._treeRoot: TreeItemId = tree.AppendItem(self._treeRootParent, self._title)
        # self._tree.Expand(self._treeRoot)
        # self._tree.SetPyData(self._treeRoot, self._frame)
        self._tree.SetItemData(self._treeRoot, self._frame)

    def updateTreeText(self):
        """
        Update the tree text for this document
        """
        self._tree.SetItemText(self._treeRoot, self._title)

    def removeFromTree(self):
        """
        Remove this document.
        """
        self._tree.Delete(self._treeRoot)

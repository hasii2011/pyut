
from typing import cast

from logging import Logger
from logging import getLogger

from wx import TreeCtrl
from wx import TreeItemId

from org.pyut.PyutConstants import DiagramsLabels

from org.pyut.enums.DiagramType import DiagramType

from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame
from org.pyut.ui.UmlDiagramsFrame import UmlDiagramsFrame
from org.pyut.ui.UmlSequenceDiagramsFrame import UmlSequenceDiagramsFrame

from org.pyut.PyutUtils import PyutUtils


class PyutDocument:
    """
    Document : Contain a document : frames, properties, ...
    """
    def __init__(self, parentFrame, project, docType: DiagramType):
        """

        Args:
            parentFrame:    The containing UML or sequence diagram frame
            project:        The project
            docType:        The enumeration value for the diagram type
        """
        from org.pyut.ui.PyutProject import PyutProject

        self.logger:               Logger           = getLogger(__name__)
        self._parentFrame:         UmlDiagramsFrame = cast(UmlDiagramsFrame, None)
        self._project: PyutProject = project

        self._type: DiagramType = docType
        """
        This document's diagram type
        """
        self._treeRoot:       TreeItemId = cast(TreeItemId, None)
        """
        Root of the project entry in the tree
        """
        self._treeRootParent: TreeItemId = cast(TreeItemId, None)
        """
        Parent of the project root entry
        """
        self._tree:           TreeCtrl   = cast(TreeCtrl, None)
        """
        Tree I belong to
        """

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

    def getFullyQualifiedName(self) -> str:
        """

        Returns:
            The diagram's fully qualified file name
        """
        fullyQualifiedName: str = f'{self._project.filename}/{self._title}'
        return fullyQualifiedName

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, theNewValue: str):
        self._title = theNewValue

    def getFrame(self) -> UmlDiagramsFrame:
        """
        Return the document's frame

        Returns:    this document's frame

        """
        return self._frame

    def addToTree(self, tree: TreeCtrl, root: TreeItemId):
        """

        Args:
            tree:   The tree control
            root:   The itemId of the parent root
        """
        self._tree           = tree
        self._treeRootParent = root
        self._treeRoot       = tree.AppendItem(self._treeRootParent, self._title)   # Add the project to the project tree
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

    def __str__(self) -> str:
        from os import path as osPath

        fileName:  str = self._project.filename
        shortName: str = osPath.basename(fileName)
        return f'[{self.title=} {self._type=} {shortName=}]'

    def __repr__(self):
        return self.__str__()

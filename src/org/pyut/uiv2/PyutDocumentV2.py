
from typing import cast
from typing import TYPE_CHECKING

from logging import Logger
from logging import getLogger

from wx import TreeCtrl
from wx import TreeItemId

from org.pyut.enums.DiagramType import DiagramType

from org.pyut.ui.IPyutDocument import IPyutDocument

from org.pyut.ui.umlframes.UmlClassDiagramsFrame import UmlClassDiagramsFrame
from org.pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame
from org.pyut.ui.umlframes.UmlSequenceDiagramsFrame import UmlSequenceDiagramsFrame

from org.pyut.uiv2.DiagramNotebook import DiagramNotebook

from org.pyut.PyutUtils import PyutUtils

from org.pyut.PyutConstants import DiagramsLabels

if TYPE_CHECKING:
    from org.pyut.ui.IPyutProject import IPyutProject


class PyutDocumentV2(IPyutDocument):
    """
    Document : Contain a document : frames, properties, ...
    """
    def __init__(self, parentFrame: DiagramNotebook, project: 'IPyutProject', docType: DiagramType):
        """

        Args:
            parentFrame:    The frame that will parent the UmlDiagramsFrame that we create
            project:        The project
            docType:        The enumeration value for the diagram type
        """
        super().__init__()
        self.logger:       Logger   = getLogger(__name__)

        self._parentFrame: DiagramNotebook = parentFrame
        self._project:     'IPyutProject'   = project       # TODO I should not know this

        self._type:           DiagramType = docType                 # This document's diagram type
        self._treeRoot:       TreeItemId = cast(TreeItemId, None)   # The document entry in the tree
        self._treeRootParent: TreeItemId = cast(TreeItemId, None)   # Project  entry
        self._tree:           TreeCtrl   = cast(TreeCtrl, None)     # The project Tree  TODO get rid of this

        self._diagramFrame:   UmlDiagramsFrame = cast(UmlDiagramsFrame, None)
        self._title:           str              = cast(str, None)

        self.logger.debug(f'Project: {project} PyutDocument using type {docType}')
        if docType == DiagramType.CLASS_DIAGRAM:
            self._title = DiagramsLabels[docType]
            self._diagramFrame = UmlClassDiagramsFrame(parentFrame)
        elif docType == DiagramType.SEQUENCE_DIAGRAM:
            self._title = DiagramsLabels[docType]
            self._diagramFrame = UmlSequenceDiagramsFrame(parentFrame)
        elif docType == DiagramType.USECASE_DIAGRAM:
            self._title = DiagramsLabels[docType]
            self._diagramFrame = UmlClassDiagramsFrame(parentFrame)
        else:
            PyutUtils.displayError(f'Unsupported diagram type; replacing by class diagram: {docType}')
            self._title = DiagramsLabels[DiagramType.CLASS_DIAGRAM]
            self._diagramFrame = UmlClassDiagramsFrame(parentFrame)

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

    @property
    def treeRoot(self) -> TreeItemId:
        """
        Returns: The tree root ItemId for this document's node
        """
        return self._treeRoot

    @treeRoot.setter
    def treeRoot(self, value: TreeItemId):
        self._treeRoot = value

    @property
    def diagramFrame(self) -> UmlDiagramsFrame:
        """
        Return the document's frame

        Returns:    this document's uml frame
        """
        return self._diagramFrame

    def updateTreeText(self):
        """
        Update the tree text for this document
        TODO: Gets removed post V2 UI
        """
        assert False, 'Do not use this method'

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

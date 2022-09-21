
from typing import cast

from logging import Logger
from logging import getLogger

# noinspection PyPackageRequirements
from deprecated import deprecated

from wx import ICON_ERROR
from wx import OK

from wx import TreeItemId
from wx import MessageDialog

from org.pyut.enums.DiagramType import DiagramType

from org.pyut.ui.umlframes.UmlClassDiagramsFrame import UmlClassDiagramsFrame
from org.pyut.ui.umlframes.UmlSequenceDiagramsFrame import UmlSequenceDiagramsFrame

from org.pyut.uiv2.DiagramNotebook import DiagramNotebook
from org.pyut.uiv2.IPyutDocument import IPyutDocument
from org.pyut.uiv2.IPyutProject import UmlFrameType

from org.pyut.PyutConstants import DiagramsLabels


class PyutDocumentV2(IPyutDocument):
    """
    Document : Contains a document : frames, properties, ...
    """
    def __init__(self, parentFrame: DiagramNotebook, docType: DiagramType):

        """

        Args:
            parentFrame:    The frame that will parent the UmlDiagramsFrame that we create
            docType:        The enumeration value for the diagram type
        """
        super().__init__()
        self.logger: Logger   = getLogger(__name__)

        self._parentFrame:    DiagramNotebook = parentFrame
        self._diagramType:    DiagramType     = docType                 # This document's diagram type
        self._treeRoot:       TreeItemId      = cast(TreeItemId, None)   # The document entry in the tree
        self._treeRootParent: TreeItemId      = cast(TreeItemId, None)   # Project  entry

        self._diagramFrame:   UmlFrameType    = cast(UmlFrameType, None)
        self._title:          str             = cast(str, None)

        self._createDiagramFrame()

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
    def diagramFrame(self) -> UmlFrameType:
        """
        Return the document's frame

        Returns:    this document's uml frame
        """
        return self._diagramFrame

    @property
    def diagramType(self) -> DiagramType:
        """
        Returns:
                The document type
        """
        return self._diagramType

    @deprecated(reason='Use .diagramType property')
    def getType(self) -> DiagramType:
        """
        Returns:
                The document type
        """
        return self._diagramType

    def updateTreeText(self):
        assert False, 'Do not use this method'

    def removeFromTree(self):
        assert False, 'Do not use this method'

    def _createDiagramFrame(self):

        docType:     DiagramType     = self._diagramType
        parentFrame: DiagramNotebook = self._parentFrame

        self.logger.debug(f'PyutDocument using type {docType}')
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
            self._displayError(f'Unsupported diagram type; replacing by class diagram: {docType}')
            self._title = DiagramsLabels[DiagramType.CLASS_DIAGRAM]
            self._diagramFrame = UmlClassDiagramsFrame(parentFrame)

    def _displayError(self, message: str):
        booBoo: MessageDialog = MessageDialog(parent=None, message=message, caption='Error', style=OK | ICON_ERROR)
        booBoo.ShowModal()

    def __str__(self) -> str:
        return f'[{self.title=} {self._diagramType=}]'

    def __repr__(self):
        return self.__str__()

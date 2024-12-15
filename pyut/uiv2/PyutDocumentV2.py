
from typing import cast

from logging import Logger
from logging import getLogger

from deprecated import deprecated

from wx import ICON_ERROR
from wx import OK

from wx import TreeItemId
from wx import MessageDialog

from pyut.enums.DiagramType import DiagramType

from pyut.uiv2.IPyutDocument import IPyutDocument
from pyut.uiv2.IPyutProject import UmlFrameType

from pyut.ui.eventengine.IEventEngine import IEventEngine


class PyutDocumentV2(IPyutDocument):
    """
    Document : Contains a document : frames, properties, ...
    """
    def __init__(self, diagramFrame: UmlFrameType, docType: DiagramType, eventEngine: IEventEngine):

        """

        Args:
            diagramFrame:
            docType:        The enumeration value for the diagram type
            eventEngine:    The engine used to communicate with the Pyut UI
        """
        self._diagramFrame: UmlFrameType = diagramFrame

        super().__init__()
        self.logger: Logger   = getLogger(__name__)

        self._diagramType:    DiagramType  = docType                 # This document's diagram type
        self._eventEngine:    IEventEngine = eventEngine
        self._treeRoot:       TreeItemId   = cast(TreeItemId, None)   # The document entry in the tree
        self._treeRootParent: TreeItemId   = cast(TreeItemId, None)   # Project  entry
        self._title:          str          = cast(str, None)

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

    def _displayError(self, message: str):
        booBoo: MessageDialog = MessageDialog(parent=None, message=message, caption='Error', style=OK | ICON_ERROR)
        booBoo.ShowModal()

    def __str__(self) -> str:
        return f'[{self.title=} {self._diagramType=}]'

    def __repr__(self):
        return self.__str__()

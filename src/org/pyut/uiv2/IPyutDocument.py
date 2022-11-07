
from typing import List
from typing import NewType

from abc import ABC
from abc import abstractmethod

from wx import TreeItemId

from pyut.enums.DiagramType import DiagramType
from org.pyut.uiv2.Types import UmlFrameType


class IPyutDocument(ABC):
    """
    Something to fool mypy
    """
    def __init__(self):
        pass

    @property
    @abstractmethod
    def diagramFrame(self) -> UmlFrameType:
        """
        Return the document's frame

        Returns:    this document's uml frame
        """
        pass

    @property
    @abstractmethod
    def title(self) -> str:
        pass

    @title.setter
    @abstractmethod
    def title(self, theNewValue: str):
        pass

    @property
    @abstractmethod
    def treeRoot(self) -> TreeItemId:
        """
        Returns: The tree root ItemId for this document's node
        """
        pass

    @treeRoot.setter
    @abstractmethod
    def treeRoot(self, value: TreeItemId):
        pass

    @property
    @abstractmethod
    def diagramType(self) -> DiagramType:
        """
        Returns:
                The document type
        """
        pass

    @abstractmethod
    def updateTreeText(self):
        """
        Implemented only by legacy Pyut
        """
        pass


PyutDocuments = NewType('PyutDocuments', List[IPyutDocument])

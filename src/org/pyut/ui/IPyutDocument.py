
from typing import List
from typing import NewType

from abc import ABC
from abc import abstractmethod

from wx import TreeItemId

from org.pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame


class IPyutDocument(ABC):
    """
    Something to fool mypy
    """
    def __init__(self):
        pass

    @property               # type: ignore
    @abstractmethod
    def diagramFrame(self) -> UmlDiagramsFrame:
        """
        Return the document's frame

        Returns:    this document's uml frame
        """
        pass

    @property               # type: ignore
    @abstractmethod
    def title(self) -> str:
        pass

    @title.setter           # type: ignore
    @abstractmethod
    def title(self, theNewValue: str):
        pass

    @property               # type: ignore
    @abstractmethod
    def treeRoot(self) -> TreeItemId:
        """
        Returns: The tree root ItemId for this document's node
        """
        pass

    @treeRoot.setter        # type: ignore
    @abstractmethod
    def treeRoot(self, value: TreeItemId):
        pass

    @abstractmethod
    def removeFromTree(self):
        """
        TODO: This does not belong here

        Returns:
        """
        pass

    @abstractmethod
    def updateTreeText(self):
        pass


PyutDocuments = NewType('PyutDocuments', List[IPyutDocument])

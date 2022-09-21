
from typing import List

from abc import ABC
from abc import abstractmethod

from wx import TreeItemId

from org.pyut.ui.IPyutDocument import PyutDocuments
from org.pyut.uiv2.Types import Frames
from org.pyut.uiv2.Types import UmlFrameType


class IPyutProject(ABC):
    """
    Something to fool mypy
    """
    def __init__(self):
        pass

    @property               # type: ignore
    @abstractmethod
    def filename(self) -> str:
        """
        Returns:  The project's filename
        """
        pass

    @filename.setter        # type: ignore
    @abstractmethod
    def filename(self, filename: str):
        """
        Set the project's filename

        Args:
            filename:
        """
        pass

    @property               # type: ignore
    @abstractmethod
    def modified(self) -> bool:
        """
        Returns:  'True' if it has been else 'False'
        """
        pass

    @modified.setter        # type: ignore
    @abstractmethod
    def modified(self, value: bool = True):
        """
        Set that the project has been modified
        Args:
            value:  'True' if it has been else 'False'
        """
        pass

    @property               # type: ignore
    @abstractmethod
    def projectTreeRoot(self) -> TreeItemId:
        """
        A piece of UI information needed to communicate with the UI component

        Returns: The opaque item where this project's documents are display on the UI Tree
        """
        pass

    @projectTreeRoot.setter     # type: ignore
    @abstractmethod
    def projectTreeRoot(self, newValue: TreeItemId):
        pass

    @property           # type: ignore
    @abstractmethod
    def frames(self) -> Frames:
        pass

    @property               # type: ignore
    @abstractmethod
    def documents(self) -> PyutDocuments:
        """
        Return the documents (Not a copy)
        TODO: Is this a bad idea

        Returns:  A list of documents
        """
        pass

    @abstractmethod
    def getFrames(self) -> List[UmlFrameType]:
        """
        Get all the project's frames

        Returns:
            List of frames
        """
        pass

    @abstractmethod
    def selectFirstDocument(self):
        pass

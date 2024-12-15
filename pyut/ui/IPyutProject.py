
from typing import List

from abc import ABC
from abc import abstractmethod

from wx import TreeItemId

from pyut.ui.IPyutDocument import PyutDocuments
from pyut.ui.Types import Frames
from pyut.ui.Types import UmlFrameType


class IPyutProject(ABC):
    """
    Something to fool mypy
    """
    def __init__(self):
        pass

    @property
    @abstractmethod
    def filename(self) -> str:
        """
        Returns:  The project's filename
        """
        pass

    @filename.setter
    @abstractmethod
    def filename(self, filename: str):
        """
        Set the project's filename

        Args:
            filename:
        """
        pass

    @property
    @abstractmethod
    def projectName(self) -> str:
        """
        Truncates to just the file name and less the suffix.

        Returns:   Nice short hane
        """
        pass

    @property
    @abstractmethod
    def codePath(self) -> str:
        pass

    @codePath.setter
    @abstractmethod
    def codePath(self, newValue: str):
        pass

    @property
    @abstractmethod
    def modified(self) -> bool:
        """
        Returns:  'True' if it has been else 'False'
        """
        pass

    @modified.setter
    @abstractmethod
    def modified(self, value: bool = True):
        """
        Set that the project has been modified
        Args:
            value:  'True' if it has been else 'False'
        """
        pass

    @property
    @abstractmethod
    def projectTreeRoot(self) -> TreeItemId:
        """
        A piece of UI information needed to communicate with the UI component

        Returns: The opaque item where this project's documents are display on the UI Tree
        """
        pass

    @projectTreeRoot.setter
    @abstractmethod
    def projectTreeRoot(self, newValue: TreeItemId):
        pass

    @property
    @abstractmethod
    def frames(self) -> Frames:
        pass

    @property
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

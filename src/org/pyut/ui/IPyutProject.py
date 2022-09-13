
from abc import ABC
from abc import abstractmethod

from org.pyut.ui.IPyutDocument import PyutDocuments


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
    def documents(self) -> PyutDocuments:
        """
        Return the documents (Not a copy)
        TODO: Is this a bad idea

        Returns:  A list of documents
        """
        pass


from abc import ABC

from wx import Frame


class IErrorView(ABC):
    """
    Prototypical interface
    """
    def newFatalError(self, msg: str, title: str | None = None, parent: Frame | None = None):
        pass

    def newWarning(self, msg: str, title: str | None = None, parent: Frame | None = None):
        pass

    def newInformation(self, msg: str, title: str | None = None, parent: Frame | None = None):
        pass

    def displayInformation(self, msg: str, title: str | None = None, parent: Frame | None = None):
        pass

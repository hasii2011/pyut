
from abc import ABC

from wx import Window


class IErrorView(ABC):
    """
    Prototypical interface
    """
    def newFatalError(self, msg: str, title: str | None = None, parent: Window | None = None):
        pass

    def newWarning(self, msg: str, title: str | None = None, parent: Window | None = None):
        pass

    def newInformation(self, msg: str, title: str | None = None, parent: Window | None = None):
        pass

    def displayInformation(self, msg: str, title: str | None = None, parent: Window | None = None):
        pass


from abc import ABC

from wx import Window


class IErrorView(ABC):
    """
    Prototypical interface
    """
    def __init__(self):
        pass

    def displayFatalError(self, msg: str, title: str | None = None, parent: Window | None = None):
        pass

    def displayWarning(self, msg: str, title: str | None = None, parent: Window | None = None):
        pass

    def displayInformation(self, msg: str, title: str | None = None, parent: Window | None = None):
        pass

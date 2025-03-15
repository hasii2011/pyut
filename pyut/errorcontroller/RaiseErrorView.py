
from pyut.errorcontroller.IErrorView import IErrorView

from pyut.errorcontroller.PyutException import PyutException


class RaiseErrorView(IErrorView):
    """
    This class is an error view which will raise all errors as exceptions
    """
    def __init__(self):
        super().__init__()

    def displayFatalError(self, msg, title=None, parent=None):
        raise PyutException(f"FATAL ERROR: {title} - {msg}")

    def displayWarning(self, msg, title=None, parent=None):
        raise PyutException(f"WARNING: {title} - {msg}")

    def displayInformation(self, msg, title=None, parent=None):
        raise PyutException(f"INFORMATION: {title} 0 {msg}")

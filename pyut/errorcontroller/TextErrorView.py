
from logging import Logger
from logging import getLogger

from pyut.errorcontroller.IErrorView import IErrorView


class TextErrorView(IErrorView):
    """
    This class is an error view which will display an error as entries
    in the Pyut log file.
    """
    def __init__(self):
        super().__init__()
        self.logger: Logger = getLogger(__name__)

    def displayFatalError(self, msg, title=None, parent=None):

        from pyut.errorcontroller.ErrorManager import ErrorManager  # Avoid cyclical dependency

        if title is None:
            title = 'An error occurred...'
        errMsg: str = ErrorManager.getErrorInfo()

        self.logger.error(f"FATAL ERROR: {title} {errMsg} - parent {parent}")

    def displayWarning(self, msg, title=None, parent=None):
        self.logger.error(f"WARNING: {title} - {msg} - parent {parent}")

    def displayInformation(self, msg, title=None, parent=None):
        self.logger.error(f"INFORMATION: {title} - {msg} - parent {parent}")

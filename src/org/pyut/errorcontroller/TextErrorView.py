
from logging import Logger
from logging import getLogger

from org.pyut.errorcontroller.AbstractErrorView import AbstractErrorView

from org.pyut.general.Globals import _


class TextErrorView(AbstractErrorView):
    """
    This class is an error view which will display error as
    text message box.

    To use it, use the mediator methods:
    ```python
     mediator: Mediator = Mediator()
     ...
     errorManager = mediator.getErrorManager()
     errorManager.changeType(ErrorViewTypes.TEXT_ERROR_VIEW)

     errorManager.newFatalError("This is a message", "...")
     errorManager.newWarning("This is a message", "...")
     errorManager.newInformation("This is a message", "...")
     ```
    """
    def __init__(self):
        self.logger: Logger = getLogger(__name__)

    def newFatalError(self, msg, title=None, parent=None):

        from org.pyut.errorcontroller.ErrorManager import ErrorManager  # Avoid cyclical dependency

        if title is None:
            title = _("An error occurred...")
        errMsg: str = ErrorManager.getErrorInfo()

        self.logger.error(f"FATAL ERROR: {title} {errMsg} - parent {parent}")

    def newWarning(self, msg, title=None, parent=None):
        self.logger.error(f"WARNING: {title} - {msg} - parent {parent}")

    def displayInformation(self, msg, title=None, parent=None):
        self.logger.error(f"INFORMATION: {title} - {msg} - parent {parent}")

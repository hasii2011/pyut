
from logging import Logger
from logging import getLogger

from wx import CENTRE
from wx import ICON_ERROR
from wx import ICON_EXCLAMATION
from wx import ICON_INFORMATION
from wx import MessageDialog
from wx import OK

from org.pyut.errorcontroller.AbstractErrorView import AbstractErrorView

# noinspection PyProtectedMember
from org.pyut.general.Globals import _


class GraphicErrorView(AbstractErrorView):
    """
    This class is an error view which will display error as
    wx message dialogs.

    To use it, use the mediator methods :
    ```python
     mediator: Mediator = Mediator()

     errorManager = mediator.getErrorManager()
     errorManager.changeType(ErrorViewTypes.GRAPHIC_ERROR_VIEW)
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

        errMsg: str = msg + "\n\n"
        errorInfo: str = ErrorManager.getErrorInfo()
        if errorInfo is not None:
            errMsg = f'{errMsg}{ErrorManager.getErrorInfo()}'
        try:
            dlg = MessageDialog(parent, errMsg,  title, OK | ICON_ERROR | CENTRE)
            dlg.ShowModal()
            dlg.Destroy()
        except (ValueError, Exception) as e:
            self.logger.error(f'newFatalError: {e}')

    def newWarning(self, msg, title=None, parent=None):

        if title is None:
            title = _("WARNING...")
        try:
            dlg = MessageDialog(parent, msg, title, OK | ICON_EXCLAMATION | CENTRE)
            dlg.ShowModal()
            dlg.Destroy()
        except (ValueError, Exception) as e:
            self.logger.error(f'newWarning: {e}')

    def newInformation(self, msg, title=None, parent=None):

        if title is None:
            title = _("WARNING...")
        try:
            dlg = MessageDialog(parent, msg, title, OK | ICON_INFORMATION | CENTRE)
            dlg.ShowModal()
            dlg.Destroy()

        except (ValueError, Exception) as e:
            self.logger.error(f'newInformation: {e}')

    def displayInformation(self, msg, title=None, parent=None):
        self.logger.error(f"INFORMATION: {title} - {msg} - parent {parent}")

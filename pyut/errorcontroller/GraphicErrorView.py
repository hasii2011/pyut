
from logging import Logger
from logging import getLogger

from wx import CENTRE
from wx import ICON_ERROR
from wx import ICON_EXCLAMATION
from wx import ICON_INFORMATION
from wx import MessageDialog
from wx import OK

from pyut.errorcontroller.IErrorView import IErrorView


class GraphicErrorView(IErrorView):
    """
    This class is an error view which will display errors as
    wx message dialogs.
    """
    def __init__(self):

        super().__init__()
        self.logger: Logger = getLogger(__name__)

    def displayFatalError(self, msg: str, title=None, parent=None):

        from pyut.errorcontroller.ErrorManager import ErrorManager  # Avoid cyclical dependency

        if title is None:
            title = 'An error occurred...'

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

    def displayWarning(self, msg: str, title=None, parent=None):

        if title is None:
            title = 'WARNING...'
        try:
            dlg = MessageDialog(parent, msg, title, OK | ICON_EXCLAMATION | CENTRE)
            dlg.ShowModal()
            dlg.Destroy()
        except (ValueError, Exception) as e:
            self.logger.error(f'newWarning: {e}')

    def newInformation(self, msg: str, title=None, parent=None):

        if title is None:
            title = 'INFORMATION...'
        try:
            dlg = MessageDialog(parent, msg, title, OK | ICON_INFORMATION | CENTRE)
            dlg.ShowModal()
            dlg.Destroy()

        except (ValueError, Exception) as e:
            self.logger.error(f'newInformation: {e}')

    def displayInformation(self, msg: str, title=None, parent=None):
        self.newInformation(msg=msg, title=title, parent=parent)

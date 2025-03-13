
from logging import Logger
from logging import getLogger

from sys import exc_info

from traceback import extract_tb

from wx import Window

from pyut.errorcontroller.IErrorView import IErrorView
from pyut.errorcontroller.GraphicErrorView import GraphicErrorView
from pyut.errorcontroller.TextErrorView import TextErrorView
from pyut.errorcontroller.RaiseErrorView import RaiseErrorView
from pyut.errorcontroller.ErrorViewTypes import ErrorViewTypes

from pyut.PyutConstants import PyutConstants


class ErrorManager(IErrorView):
    """
    This class handle errors.
    """
    logger: Logger = getLogger(PyutConstants.MAIN_LOGGING_NAME)

    def __init__(self, view=ErrorViewTypes.GRAPHIC_ERROR_VIEW):
        """
        """
        super().__init__()
        if view == ErrorViewTypes.GRAPHIC_ERROR_VIEW:
            self._errorView: IErrorView = GraphicErrorView()
        elif view == ErrorViewTypes.TEXT_ERROR_VIEW:
            self._errorView = TextErrorView()
        elif view == ErrorViewTypes.RAISE_ERROR_VIEW:
            self._errorView = RaiseErrorView()
        else:
            assert False, "ErrorManager: Unknown view type"
        self._errorViewType = view

    @property
    def errorViewType(self):
        return self._errorViewType

    @errorViewType.setter
    def errorViewType(self, view: ErrorViewTypes):

        if view == ErrorViewTypes.GRAPHIC_ERROR_VIEW:
            self._errorView = GraphicErrorView()
        elif view == ErrorViewTypes.TEXT_ERROR_VIEW:
            self._errorView = TextErrorView()
        elif view == ErrorViewTypes.RAISE_ERROR_VIEW:
            self._errorView = RaiseErrorView()

    def newFatalError(self, msg: str = '', title: str | None = '', parent: Window | None = None):
        if msg is None:
            msg = ""
        if title is None:
            title = ""
        ErrorManager.addToLogFile("Fatal error: " + title, msg)
        self._errorView.newFatalError(msg, title, parent)

    def newWarning(self, msg: str, title: str | None = '', parent=None):
        ErrorManager.addToLogFile(f"Warning: {title}", msg)
        self._errorView.newWarning(msg, title, parent)

    def newInformation(self, msg: str, title: str | None = '', parent=None):
        ErrorManager.addToLogFile(f"Info: {title}", msg)
        self._errorView.newInformation(msg, title, parent)

    def displayInformation(self, msg: str, title: str | None = '', parent=None):
        ErrorManager.addToLogFile(f"Info: {title}", msg)
        self._errorView.displayInformation(msg, title, parent)

    @classmethod
    def getErrorInfo(cls) -> str:
        """
        Returns:
            System exception information as a formatted string
        """
        errMsg: str = ''
        if exc_info()[0] is not None:
            errMsg += f'Error : {exc_info()[0]}\n'
        if exc_info()[1] is not None:
            errMsg += f'Msg   : {exc_info()[1]}\n'
        if exc_info()[2] is not None:
            errMsg += 'Trace :\n'
            for el in extract_tb(exc_info()[2]):
                errMsg = errMsg + f'{str(el)}\n'

        return errMsg

    @classmethod
    def addToLogFile(cls, title: str, msg: str):

        cls.logger.error("--------------------------------------------------------------------")
        cls.logger.error(f'{title} - {msg}')

        errMsg: str = ErrorManager.getErrorInfo()
        if errMsg != '':
            cls.logger.error(errMsg)

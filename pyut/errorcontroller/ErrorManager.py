
from logging import Logger
from logging import getLogger

from sys import exc_info

from traceback import extract_tb

from wx import Window

from codeallybasic.SingletonV3 import SingletonV3

from pyut.errorcontroller.GraphicErrorView import GraphicErrorView
from pyut.errorcontroller.IErrorView import IErrorView
from pyut.errorcontroller.RaiseErrorView import RaiseErrorView
from pyut.errorcontroller.TextErrorView import TextErrorView

from pyut.errorcontroller.ErrorViewTypes import ErrorViewTypes

from pyut.PyutConstants import PyutConstants


class ErrorManager(metaclass=SingletonV3):
    """
    This handles errors dependent on the view type:

    To use it instantiate the ErrorManager (it is a Singleton)
    ```python
      ...
      errorManager: ErrorManager = ErrorManager()
      errorManager.errorViewType = ErrorViewTypes.RAISE_ERROR_VIEW | TEXT_ERROR_VIEW | GRAPHIC_ERROR_VIEW

      errorManager.newFatalError("This is a message", "...")
      errorManager.newWarning("This is a message", "...")
      errorManager.newInformation("This is a message", "...")

    ```
    """
    clsLogger: Logger = getLogger(PyutConstants.MAIN_LOGGING_NAME)

    def __init__(self, viewType=ErrorViewTypes.GRAPHIC_ERROR_VIEW):
        """
        """
        if viewType == ErrorViewTypes.GRAPHIC_ERROR_VIEW:
            self._errorView: IErrorView = GraphicErrorView()
        elif viewType == ErrorViewTypes.TEXT_ERROR_VIEW:
            self._errorView = TextErrorView()
        elif viewType == ErrorViewTypes.RAISE_ERROR_VIEW:
            self._errorView = RaiseErrorView()
        else:
            assert False, "ErrorManager: Unknown view type"

        self._errorViewType: ErrorViewTypes = viewType

    @property
    def errorViewType(self):
        return self._errorViewType

    @errorViewType.setter
    def errorViewType(self, view: ErrorViewTypes):

        self._errorViewType = view

        if view == ErrorViewTypes.GRAPHIC_ERROR_VIEW:
            self._errorView = GraphicErrorView()
        elif view == ErrorViewTypes.TEXT_ERROR_VIEW:
            self._errorView = TextErrorView()
        elif view == ErrorViewTypes.RAISE_ERROR_VIEW:
            self._errorView = RaiseErrorView()

    def displayFatalError(self, msg: str = '', title: str | None = '', parent: Window | None = None):
        if msg is None:
            msg = ""
        if title is None:
            title = ""
        ErrorManager.addToLogFile("Fatal error: " + title, msg)
        self._errorView.displayFatalError(msg, title, parent)

    def displayWarning(self, msg: str, title: str | None = '', parent=None):
        ErrorManager.addToLogFile(f"Warning: {title}", msg)
        self._errorView.displayWarning(msg, title, parent)

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

        cls.clsLogger.error("--------------------------------------------------------------------")
        cls.clsLogger.error(f'{title} - {msg}')

        errMsg: str = ErrorManager.getErrorInfo()
        if errMsg != '':
            cls.clsLogger.error(errMsg)

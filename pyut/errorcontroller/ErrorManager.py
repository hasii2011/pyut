
from typing import cast

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

from pyut.errorcontroller.ErrorViewType import ErrorViewType

from pyut.PyutConstants import PyutConstants
from pyut.preferences.PyutPreferences import PyutPreferences


class ErrorManager(metaclass=SingletonV3):
    """
    This class implements the Strategy pattern and handles errors based on the view type:

    To use it instantiate the ErrorManager (it is a Singleton)
    ```python
      ...
      errorManager: ErrorManager = ErrorManager()
      errorManager.errorViewType = ErrorViewType.RAISE_ERROR_VIEW | TEXT_ERROR_VIEW | GRAPHIC_ERROR_VIEW

      errorManager.newFatalError("This is a message", "...")
      errorManager.newWarning("This is a message", "...")
      errorManager.newInformation("This is a message", "...")

    ```
    """
    clsLogger: Logger = getLogger(PyutConstants.MAIN_LOGGING_NAME)

    def __init__(self):
        """
        """
        self._errorViewType: ErrorViewType = cast(ErrorViewType, None)
        self._errorView:     IErrorView    = cast(IErrorView,    None)

        self._preferences:  PyutPreferences = PyutPreferences()
        self.errorViewType: ErrorViewType   = self._preferences.errorViewType

    @property
    def errorViewType(self):
        return self._errorViewType

    @errorViewType.setter
    def errorViewType(self, viewType: ErrorViewType):

        self._errorViewType = viewType

        if viewType == ErrorViewType.GRAPHIC_ERROR_VIEW:
            self._errorView = GraphicErrorView()
        elif viewType == ErrorViewType.TEXT_ERROR_VIEW:
            self._errorView = TextErrorView()
        elif viewType == ErrorViewType.RAISE_ERROR_VIEW:
            self._errorView = RaiseErrorView()
        else:
            assert False, "ErrorManager: Unknown viewType type"

        self._preferences.errorViewType = viewType

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

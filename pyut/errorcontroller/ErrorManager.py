
from logging import Logger
from logging import getLogger

from sys import exc_info

from traceback import extract_tb

from codeallybasic.SingletonV3 import SingletonV3

from pyut.errorcontroller.IErrorView import IErrorView
from pyut.errorcontroller.GraphicErrorView import GraphicErrorView
from pyut.errorcontroller.TextErrorView import TextErrorView
from pyut.errorcontroller.RaiseErrorView import RaiseErrorView
from pyut.errorcontroller.ErrorViewTypes import ErrorViewTypes

from pyut.PyutConstants import PyutConstants


class ErrorManager(metaclass=SingletonV3):
    """
    This class handle errors.
    """
    logger: Logger = getLogger(PyutConstants.MAIN_LOGGING_NAME)

    # noinspection PyAttributeOutsideInit
    def __init__(self, view=ErrorViewTypes.GRAPHIC_ERROR_VIEW):
        """
        """
        self.changeType(view)
        self._view: IErrorView = GraphicErrorView()

    # noinspection PyAttributeOutsideInit
    def changeType(self, view: ErrorViewTypes):

        if view == ErrorViewTypes.GRAPHIC_ERROR_VIEW:
            self._view = GraphicErrorView()
        elif view == ErrorViewTypes.TEXT_ERROR_VIEW:
            self._view = TextErrorView()
        elif view == ErrorViewTypes.RAISE_ERROR_VIEW:
            self._view = RaiseErrorView()

    def newFatalError(self, msg='', title='', parent=None):
        if msg is None:
            msg = ""
        if title is None:
            title = ""
        ErrorManager.addToLogFile("Fatal error: " + title, msg)
        self._view.newFatalError(msg, title, parent)

    def newWarning(self, msg, title='', parent=None):
        ErrorManager.addToLogFile(f"Warning: {title}", msg)
        self._view.newWarning(msg, title, parent)

    def newInformation(self, msg, title='', parent=None):
        ErrorManager.addToLogFile(f"Info: {title}", msg)
        self._view.newInformation(msg, title, parent)

    def displayInformation(self, msg, title='', parent=None):
        ErrorManager.addToLogFile(f"Info: {title}", msg)
        self._view.displayInformation(msg, title, parent)

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


from typing import cast

from logging import Logger
from logging import getLogger

from sys import exc_info

from traceback import extract_tb

from org.pyut.errorcontroller.AbstractErrorView import AbstractErrorView
from org.pyut.errorcontroller.GraphicErrorView import GraphicErrorView
from org.pyut.errorcontroller.TextErrorView import TextErrorView
from org.pyut.errorcontroller.RaiseErrorView import RaiseErrorView
from org.pyut.errorcontroller.ErrorViewTypes import ErrorViewTypes

from org.pyut.PyutConstants import PyutConstants

from org.pyut.general.Singleton import Singleton


class ErrorManager(Singleton):
    """
    This class handle errors.
    """
    clsLogger: Logger = getLogger(PyutConstants.MAIN_LOGGING_NAME)

    def init(self, view=ErrorViewTypes.GRAPHIC_ERROR_VIEW):
        """
        Singleton constructor
        """
        self.changeType(view)
        self._view: AbstractErrorView = GraphicErrorView()

    def changeType(self, view: ErrorViewTypes):

        if view == ErrorViewTypes.GRAPHIC_ERROR_VIEW:
            self._view = GraphicErrorView()
        elif view == ErrorViewTypes.TEXT_ERROR_VIEW:
            self._view = TextErrorView()
        elif view == ErrorViewTypes.RAISE_ERROR_VIEW:
            self._view = RaiseErrorView()
        else:
            self._view = GraphicErrorView()

    def newFatalError(self, msg=None, title=None, parent=None):
        if msg is None:
            msg = ""
        if title is None:
            title = ""
        ErrorManager.addToLogFile("Fatal error: " + title, msg)
        self._view.newFatalError(msg, title, parent)

    def newWarning(self, msg, title=None, parent=None):
        ErrorManager.addToLogFile(f"Warning: {title}", msg)
        self._view.newWarning(msg, title, parent)

    def newInformation(self, msg, title=None, parent=None):
        ErrorManager.addToLogFile(f"Info: {title}", msg)
        self._view.newInformation(msg, title, parent)

    def displayInformation(self, msg, title=None, parent=None):
        ErrorManager.addToLogFile(f"Info: {title}", msg)
        self._view.displayInformation(msg, title, parent)

    @staticmethod
    def getErrorInfo() -> str:
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

        if errMsg == '':
            errMsg = cast(str, None)
        else:
            prependMsg: str = f'The following error occurred : {str(exc_info()[1])}'
            prependMsg += f'\n\n---------------------------\n'
            errMsg = f'{prependMsg}{errMsg}'

        return errMsg

    @staticmethod
    def addToLogFile(title: str, msg: str):

        ErrorManager.clsLogger.info("---------------------------")

        errMsg: str = ErrorManager.getErrorInfo()

        ErrorManager.clsLogger.info(f'{title} - {msg}\n')
        if errMsg is not None:
            ErrorManager.clsLogger.info(errMsg)

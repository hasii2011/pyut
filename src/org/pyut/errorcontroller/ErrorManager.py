
from sys import exc_info

from traceback import extract_tb

from org.pyut.errorcontroller.GraphicErrorView import GraphicErrorView
from org.pyut.errorcontroller.TextErrorView import TextErrorView
from org.pyut.errorcontroller.RaiseErrorView import RaiseErrorView

from org.pyut.errorcontroller.ErrorViewTypes import ErrorViewTypes

from org.pyut.general.Singleton import Singleton

#
#   TODO:  Raise a PyutException(s) instead of the general one
#   TODO:  All these classes need an abstract class to implement
#


def getErrorManager():
    """
    Get the error manager
    """
    return ErrorManager()


def addToLogFile(title, msg):

    import time
    import codecs

    f = codecs.open('errors.log', encoding='utf-8', mode='a')

    f.write("---------------------------\n")
    f.write(str(time.ctime(time.time())))

    errMsg: str = ErrorManager.getErrorInfo()

    f.write(f'{title} - {msg}\n')
    f.write(errMsg)
    f.close()


class ErrorManager(Singleton):
    """
    This class handle all errors.

    :author: C.Dutoit
    :contact: <dutoitc@hotmail.com>
    """

    def init(self, view=ErrorViewTypes.GRAPHIC_ERROR_VIEW):
        """
        Singleton constructor
        """
        self.changeType(view)

    def changeType(self, view: ErrorViewTypes):

        if view == ErrorViewTypes.GRAPHIC_ERROR_VIEW:
            self._view = GraphicErrorView()
        elif view == ErrorViewTypes.TEXT_ERROR_VIEW:
            self._view = TextErrorView()
        elif view == ErrorViewTypes.RAISE_ERROR_VIEW:
            self._view = RaiseErrorView()
        else:
            self._view = GraphicErrorView()

    def newFatalError(self, msg, title=None, parent=None):
        if msg is None:
            msg = u""
        if title is None:
            title = u""
        title = u"" + title
        msg = u"" + msg
        addToLogFile("Fatal error : " + title, msg)
        self._view.newFatalError(msg, title, parent)

    def newWarning(self, msg, title=None, parent=None):
        title = u"" + title
        msg = u"" + msg
        addToLogFile("Warning : " + title, msg)
        self._view.newWarning(msg, title, parent)

    def displayInformation(self, msg, title=None, parent=None):
        title = u"" + title
        msg = u"" + msg
        addToLogFile("Info : " + title, msg)
        self._view.displayInformation(msg, title, parent)

    @staticmethod
    def getErrorInfo() -> str:
        """
        Returns:  System exception information as a formatted string

        """
        errMsg = f'The following error occured : {str(exc_info()[1])}'
        errMsg += f'\n\n---------------------------\n'
        if exc_info()[0] is not None:
            errMsg += f'Error : {exc_info()[0]}\n'
        if exc_info()[1] is not None:
            errMsg += f'Msg   : {exc_info()[1]}\n'
        if exc_info()[2] is not None:
            errMsg += 'Trace :\n'
            for el in extract_tb(exc_info()[2]):
                errMsg = errMsg + f'{str(el)}\n'

        return errMsg

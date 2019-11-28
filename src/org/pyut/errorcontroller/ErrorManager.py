
from logging import Logger
from logging import getLogger

from sys import exc_info

from traceback import extract_tb

from org.pyut.errorcontroller.GraphicErrorView import GraphicErrorView
from org.pyut.experimental.ErrorViewTypes import ErrorViewTypes

from org.pyut.general.Globals import _

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

    title = u"" + title
    msg = u"" + msg
    # f = open("errors.log", "a")
    f = codecs.open('errors.log', encoding='utf-8', mode='a')

    f.write("===========================")
    f.write(str(time.ctime(time.time())))

    errMsg = msg + "\n\n" + _("The following error occurred : %s") % exc_info()[1] + "\n\n---------------------------\n"
    if exc_info()[0] is not None:
        errMsg += "Error : %s" % exc_info()[0] + "\n"
    if exc_info()[1] is not None:
        errMsg += "Msg   : %s" % exc_info()[1] + "\n"
    if exc_info()[2] is not None:
        errMsg += "Trace :\n"
        for el in extract_tb(exc_info()[2]):
            errMsg = errMsg + str(el) + "\n"

    f.write(title + u": " + msg)
    f.write(errMsg)
    f.close()


class TextErrorView:
    """
    This class is an error view which will display error as
    text message box.

    To use it, use the mediator methods :
     - mediator = Mediator.getMediator()
     - mediator.registerErrorManager(GraphicErrorManager())
     - ...
     - errorManager = mediator.getErrorManager()
     - errorManager.newFatalError("This is a message", "...")
     - errorManager.newWarning("This is a message", "...")
     - errorManager.newInformation("This is a message", "...")
     - ...

    @author C.Dutoit
    """
    def __init__(self):
        self.logger: Logger = getLogger(__name__)

    def newFatalError(self, msg, title=None, parent=None):

        if title is None:
            title = _("An error occured...")
        errMsg = msg + "\n\n" + _("The following error occured : %s") % exc_info()[1] + "\n\n---------------------------\n"

        if exc_info()[0] is not None:
            errMsg += "Error : %s" % exc_info()[0] + "\n"
        if exc_info()[1] is not None:
            errMsg += "Msg   : %s" % exc_info()[1] + "\n"
        if exc_info()[2] is not None:
            errMsg += "Trace :\n"
            for el in extract_tb(exc_info()[2]):
                errMsg = errMsg + str(el) + "\n"

        self.logger.error(f"FATAL ERROR: {title} {errMsg} - parent {parent}")

    def newWarning(self, msg, title=None, parent=None):
        self.logger.error(f"WARNING: {title} - {msg} - parent {parent}")

    def displayInformation(self, msg, title=None, parent=None):
        self.logger.error(f"INFORMATION: {title} - {msg} - parent {parent}")


class RaiseErrorView:
    """
    This class is an error view which will raise all errors as
    text message box.

    To use it, use the mediator methods :
     - mediator = Mediator.getMediator()
     - mediator.registerErrorManager(GraphicErrorManager())
     - ...
     - errorManager = mediator.getErrorManager()
     - errorManager.newFatalError("This is a message", "...")
     - errorManager.newWarning("This is a message", "...")
     - errorManager.newInformation("This is a message", "...")
     - ...

    @author C.Dutoit
    """

    def newFatalError(self, msg, title=None, parent=None):
        raise Exception(f"FATAL ERROR: {title} - {msg}")

    def newWarning(self, msg, title=None, parent=None):
        raise Exception(f"WARNING: {title} - {msg}")

    def displayInformation(self, msg, title=None, parent=None):
        raise Exception(f"INFORMATION: {title} 0 {msg}")


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

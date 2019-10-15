
from logging import Logger
from logging import getLogger

from sys import exc_info
from traceback import extract_tb

from wx import NewId

from ErrorManager import getErrorManager
"""
This file is for frequently used pyut utilities.

hasii 
Updated this to avoid a circular dependency this module and mediator;  This module
retrieved the mediator singleton and asked it for its error manager.  Nothing special about that
as the error manager is a singleton;  So I just ask the error manager directly for it

Functions :
    assignID will assign a unique wxID for all the application.

:author: C.Dutoit
:contact: <dutoitc@hotmail.com>
"""

# Assign constants


# noinspection PyUnusedLocal
def assignID(nb):
    """
    Assign and return nb new id.

    @param number  nb : number of unique IDs to return
    @return numbers[] : List of numbers which contain <nb> unique IDs
    @since 1.0
    @author C.Dutoit <dutoitc@hotmail.com>
    """
    # personal reminder : map : return <nb> unique wxID as list
    # explanation in a good phrase : this function return a number <nb> of
    #                                unique IDs, which is a list.
    # Sample use        : [My_Id1, My_Id2, My_Id3] = assignID(3)
    # If this not so long header is not enough explicit, please forgive me or
    # mail me with an update to dutoitc@hotmail.com. thanks
    #
    return [NewId() for x in range(nb)]


def getErrorInfo() -> str:
    """
    Does this belong in the error manager?

    Returns:

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


def displayError(msg, title=None, parent=None):
    """
    Display an error

    @author C.Dutoit
    """
    errMsg = getErrorInfo()

    try:
        em = getErrorManager()
        em.newFatalError(msg, title, parent)
    except (ValueError, Exception) as e:
        eLog: Logger = getLogger(__name__)
        # TODO  I don't this is correct anymore
        eLog.error("Error in PyutUtils/displayError")
        eLog.error(f"Original error message was: {e}")
        eLog.error(errMsg)
        eLog.error("")
        eLog.error("New error is : ")
        errMsg = getErrorInfo()
        eLog.error(errMsg)


def displayWarning(msg, title=None, parent=None):
    """
    Display a warning

    @author C.Dutoit
    """
    # ctrl = getMediator()
    # em = ctrl.getErrorManager()
    em = getErrorManager()

    em.newWarning(msg, title, parent)


def displayInformation(msg, title=None, parent=None):
    """
    Display an information

    @author C.Dutoit
    """
    # ctrl = getMediator()
    # em = ctrl.getErrorManager()
    em = getErrorManager()

    em.newInformation(msg, title, parent)

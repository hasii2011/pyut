
from wx import NewId

from mediator import getMediator
"""
This file is for frequently used pyut utilities.

Functions :
    assignID will assign a unique wxID for all the application.

:author: C.Dutoit
:contact: <dutoitc@hotmail.com>
"""

# Assign constants


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


def getErrorInfo(exc_info):
    import traceback
    errMsg = str(exc_info[1])
    errMsg += "\n\n---------------------------\n"
    if exc_info[0] is not None:
        errMsg += "Error : %s" % exc_info[0] + "\n"
    if exc_info[1] is not None:
        errMsg += "Msg   : %s" % exc_info[1] + "\n"
    if exc_info[2] is not None:
        errMsg += "Trace :\n"
        for el in traceback.extract_tb(exc_info[2]):
            errMsg = errMsg + str(el) + "\n"
    return errMsg


def displayError(msg, title=None, parent=None):
    """
    Display an error

    @author C.Dutoit
    """
    import sys
    errMsg = getErrorInfo(sys.exc_info())

    try:
        ctrl = getMediator()
        em = ctrl.getErrorManager()
        # print "MSG=", msg
        # print "MSG33=", msg.encode("UTF-8")
        # msg = unicode(msg)

        # msg1 = msg.decode("UTF-8", "replace")
        # msg2 = msg1.encode("ISO-8859-1", "replace")
        # msg = msg2
        # msg = msg.decode("UTF-8").encode("UTF-8")
        em.newFatalError(msg, title, parent)
    except (ValueError, Exception) as e:
        print("*********************************************************")
        print("*********************************************************")
        print("*********************************************************")
        print("Error in pyutUtils/displayError")
        print(f"Original error message was: {e}")
        print(errMsg)
        print("")
        print("*********************************************************")
        print("New error is : ")
        errMsg = getErrorInfo(sys.exc_info())
        print(errMsg)
        print("*********************************************************")
        print("*********************************************************")
        print("*********************************************************")


def displayWarning(msg, title=None, parent=None):
    """
    Display a warning

    @author C.Dutoit
    """
    ctrl = getMediator()
    em = ctrl.getErrorManager()
    em.newWarning(msg, title, parent)


def displayInformation(msg, title=None, parent=None):
    """
    Display an information

    @author C.Dutoit
    """
    ctrl = getMediator()
    em = ctrl.getErrorManager()
    em.newInformation(msg, title, parent)


from typing import List

from logging import Logger
from logging import getLogger

from sys import exc_info

from traceback import extract_tb

from os import sep as osSep

from wx import NewIdRef as wxNewIdRef

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


def displayError(msg, title=None, parent=None):
    """
    Display an error

    @author C.Dutoit
    """
    errMsg = PyutUtils.getErrorInfo()
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
        errMsg = PyutUtils.getErrorInfo()
        eLog.error(errMsg)


def displayWarning(msg, title=None, parent=None):
    """
    Display a warning

    @author C.Dutoit
    """
    em = getErrorManager()
    em.newWarning(msg, title, parent)


def displayInformation(msg, title=None, parent=None):
    """
    Display an information

    @author C.Dutoit
    """
    em = getErrorManager()
    em.newInformation(msg, title, parent)


class PyutUtils:
    STRIP_SRC_PATH_SUFFIX:  str = f'{osSep}src'
    STRIP_TEST_PATH_SUFFIX: str = f'{osSep}test'

    _basePath: str = ''

    def __init__(self):
        self.logger: Logger = getLogger(__name__)

    @staticmethod
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

    @staticmethod
    def assignID(numberOfIds: int) -> List[wxNewIdRef]:
        """
        Assign and return numberOfIds

        Sample use        : [Unique_Id1, Unique_Id2, Unique_Id3] = assignID(3)

        Args:
            numberOfIds: number of unique IDs to return

        Returns:  List of numbers which contain <numberOfIds> unique IDs
        """
        retList: List[wxNewIdRef] = []
        x: int = 0
        while x < numberOfIds:
            retList.append(wxNewIdRef())
            x += 1
        return retList

    @classmethod
    def getBasePath(cls) -> str:
        return cls._basePath

    @classmethod
    def setBasePath(cls, newValue: str):
        retPath: str = PyutUtils._stripSrcOrTest(newValue)
        cls._basePath = retPath

    @classmethod
    def _stripSrcOrTest(cls, originalPath: str) -> str:

        if originalPath.endswith(PyutUtils.STRIP_SRC_PATH_SUFFIX):
            retPath: str = originalPath.rstrip(PyutUtils.STRIP_SRC_PATH_SUFFIX)
            retPath = PyutUtils._stripSrcOrTest(retPath)
        elif originalPath.endswith(PyutUtils.STRIP_TEST_PATH_SUFFIX):
            retPath: str = originalPath.rstrip(PyutUtils.STRIP_TEST_PATH_SUFFIX)
            retPath = PyutUtils._stripSrcOrTest(retPath)
        else:
            retPath: str = originalPath

        return retPath

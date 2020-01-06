
from typing import List

from logging import Logger
from logging import getLogger

from os import sep as osSep

from pkg_resources import resource_filename

from wx import NewIdRef as wxNewIdRef

from org.pyut.enums.ResourceTextType import ResourceTextType

from org.pyut.errorcontroller.ErrorManager import ErrorManager
from org.pyut.errorcontroller.ErrorManager import getErrorManager


class PyutUtils:
    """
    This static class is for frequently used pyut utilities.

    hasii
    Updated this to avoid a circular dependency this module and mediator;  This module
    retrieved the mediator singleton and asked it for its error manager.  Nothing special about that
    as the error manager is a singleton;  So I just ask the error manager directly for it
    """

    STRIP_SRC_PATH_SUFFIX:  str = f'{osSep}src'
    STRIP_TEST_PATH_SUFFIX: str = f'{osSep}test'

    RESOURCES_PACKAGE_NAME: str = 'org.pyut.resources'

    _basePath: str = ''

    clsLogger: Logger = getLogger(__name__)

    def __init__(self):

        PyutUtils.logger = getLogger(__name__)

    @staticmethod
    def displayInformation(msg, title=None, parent=None):
        """
        Display information
        """
        em: ErrorManager = getErrorManager()
        em.newInformation(msg, title, parent)

    @staticmethod
    def displayWarning(msg, title=None, parent=None):
        """
        Display a warning
        """
        em: ErrorManager = getErrorManager()
        em.newWarning(msg, title, parent)

    @staticmethod
    def displayError(msg, title=None, parent=None):
        """
        Display an error
        """
        errMsg: str = ErrorManager.getErrorInfo()
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
            errMsg = ErrorManager.getErrorInfo()
            eLog.error(errMsg)

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

    @classmethod
    def retrieveResourceText(cls, textType: ResourceTextType) -> str:
        """
        Look up and retrieve the text associated with the resource type

        Args:
            textType:  The text type from the 'well known' list

        Returns:  A long string
        """
        textFileName = resource_filename(PyutUtils.RESOURCES_PACKAGE_NAME, textType.value)
        cls.clsLogger.debug(f'text filename: {textFileName}')

        objRead = open(textFileName, 'r')

        requestedText: str = objRead.read()

        objRead.close()

        return requestedText

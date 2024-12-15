
from typing import cast
from typing import List
from typing import Tuple

from logging import Logger
from logging import getLogger

from pathlib import Path
from dataclasses import dataclass

from os import sep as osSep

from wx import DisplaySize
from wx import ScreenDC
from wx import Size
from wx import NewIdRef as wxNewIdRef

from codeallybasic.ResourceManager import ResourceManager

from pyut.enums.ResourceTextType import ResourceTextType

from pyut.errorcontroller.ErrorManager import ErrorManager
from pyut.preferences.PyutPreferences import PyutPreferences


@dataclass
class ScreenMetrics:
    screenWidth:  int = 0
    screenHeight: int = 0

    dpiX: int = 0
    dpiY: int = 0


class PyutUtils:
    """
    This static class is for frequently used Pyut utility methods.

    TODO: Utility classes are an anti-pattern
    """

    STRIP_SRC_PATH_SUFFIX:  str = f'{osSep}src'
    STRIP_TEST_PATH_SUFFIX: str = f'{osSep}test'

    RESOURCES_PACKAGE_NAME: str = 'pyut.resources'
    RESOURCES_PATH:         str = f'pyut{osSep}resources'

    RESOURCE_ENV_VAR:       str = 'RESOURCEPATH'

    _basePath: str = ''

    clsLogger: Logger = getLogger(__name__)

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

    @staticmethod
    def extractFileName(fullPath: str) -> str:
        """
        Used to get the filename for a full path.
        Does NOT include the file extension

        Args:
            fullPath:   The fully qualified path

        Returns:
            A string that is the filename without the file extension
        """
        comps: List[str] = fullPath.split('/')      # break up into path components
        pName: str       = comps[len(comps) - 1]    # The filename is the last one
        s:     str       = pName[:-4]               # strip the suffix and the dot ('.')

        return s

    @staticmethod
    def displayInformation(msg, title=None, parent=None):
        """
        Display information
        """
        em: ErrorManager = ErrorManager()
        em.newInformation(msg, title, parent)

    @staticmethod
    def displayWarning(msg, title=None, parent=None):
        """
        Display a warning
        """
        em: ErrorManager = ErrorManager()
        em.newWarning(msg, title, parent)

    @staticmethod
    def displayError(msg, title=None, parent=None):
        """
        Display an error
        """
        errMsg: str = ErrorManager.getErrorInfo()
        try:
            em: ErrorManager = ErrorManager()
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
            retPath = originalPath.rstrip(PyutUtils.STRIP_TEST_PATH_SUFFIX)
            retPath = PyutUtils._stripSrcOrTest(retPath)
        else:
            retPath = originalPath

        return retPath

    @classmethod
    def retrieveResourceText(cls, textType: ResourceTextType) -> str:
        """
        Look up and retrieve the text associated with the resource type

        Args:
            textType:  The text type from the 'well known' list

        Returns:  A long string
        """
        textFileName: str = PyutUtils.retrieveResourcePath(cast(str, textType.value))
        cls.clsLogger.debug(f'text filename: {textFileName}')

        objRead = open(textFileName, 'r')
        requestedText: str = objRead.read()
        objRead.close()

        return requestedText

    @classmethod
    def retrieveResourcePath(cls, bareFileName: str, packageName: str = RESOURCES_PACKAGE_NAME) -> str:
        """
        Args:
            bareFileName:  Simple filename
            packageName:   The package from which to retrieve the resource

        Returns:  The fully qualified filename
        """
        fqFileName: str = ResourceManager.retrieveResourcePath(bareFileName=bareFileName,
                                                               resourcePath=PyutUtils.RESOURCES_PATH,
                                                               packageName=packageName)
        return fqFileName

    @classmethod
    def getResourcePath(cls, packageName: str, fileName: str):

        return cls.retrieveResourcePath(packageName=packageName, bareFileName=fileName)

    @classmethod
    def getScreenMetrics(cls) -> ScreenMetrics:

        scrResolution: Size            = ScreenDC().GetPPI()
        displaySize:   Tuple[int, int] = DisplaySize()

        screenMetrics: ScreenMetrics = ScreenMetrics()

        screenMetrics.screenWidth  = displaySize[0]
        screenMetrics.screenHeight = displaySize[1]

        screenMetrics.dpiX = scrResolution.GetWidth()
        screenMetrics.dpiY = scrResolution.GetHeight()

        return screenMetrics

    @classmethod
    def determineProjectName(cls, filename: str):
        """
        Returns a project name

        TODO: This is a dupe of what is in ProjectTree
        Args:
            filename:  raw file name

        Returns:
            A project name as determined by preferences
        """
        fileNamePath: Path = Path(filename)
        if PyutPreferences().displayProjectExtension is False:
            projectName: str = fileNamePath.stem
        else:
            projectName = fileNamePath.name

        return projectName

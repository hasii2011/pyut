
from typing import Any

from logging import Logger
from logging import getLogger

from glob import glob

from os import chdir
from os import getcwd
from os import sep as osSep

from importlib import import_module

from org.pyut.general.Mediator import Mediator
from org.pyut.general.Mediator import getMediator

from org.pyut.general.exceptions.UnsupportedXmlFileFormat import UnsupportedXmlFileFormat


class PyutXmlFinder:

    PERSISTENCE_PACKAGE: str = 'org.pyut.persistence'
    PERSISTENCE_DIR:     str = f'org{osSep}pyut{osSep}persistence'

    """
    Chunks of code in the source base that are littered all over the place; I'll concentrate them here
    """
    clsLogger: Logger = getLogger(__name__)

    def __init__(self):

        PyutXmlFinder.clsLogger = getLogger(__name__)

    @classmethod
    def getPyutXmlClass(cls, theVersion: int) -> Any:
        """
        Load and return the PyutXml class from the appropriate module that matches the input version

        Args:
            theVersion:  The version of the XML file we want to process

        Returns:  Returns the matching PyutXml`x` class  `Any` type is specified
        although they would be some version of the above;  Creating a TypeVar
        defeats the purpose of dynamic loading since we would have to import
        the specific types
        """
        if theVersion == 1:
            from org.pyut.persistence.PyutXml import PyutXml
            myXml = PyutXml()
        else:
            try:
                module = import_module(f'{PyutXmlFinder.PERSISTENCE_PACKAGE}.PyutXmlV{str(theVersion)}')
                myXml = module.PyutXml()
            except (ValueError, Exception) as e:
                cls.clsLogger.error(f'{e}')
                raise UnsupportedXmlFileFormat(f'Version {theVersion}')

        cls.clsLogger.info(f"Using version {theVersion} of the XML import/exporter")
        return myXml

    @classmethod
    def getLatestXmlVersion(cls) -> int:
        """
        I tend to unroll 'dotted' method call in order to make the code debuggable
        Continue to use .getMediator() so I can mock out the mediator in unit testing
        even though we can just instantiate it directly

        Returns: An integer that is the version number of the latest PyutXml file
        """
        med:     Mediator = getMediator()
        oldpath: str = getcwd()
        appPath: str = med.getAppPath()
        path:    str = f'{appPath}{osSep}{PyutXmlFinder.PERSISTENCE_DIR}'
        chdir(path)

        candidates  = glob("PyutXmlV*.py")
        numbers     = [int(s[8:-3]) for s in candidates]
        lastVersion = max(numbers)

        chdir(oldpath)

        return lastVersion

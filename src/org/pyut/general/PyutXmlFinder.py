
from typing import Any

from logging import Logger
from logging import getLogger

from os import sep as osSep

from org.pyut.general.exceptions.UnsupportedXmlFileFormat import UnsupportedXmlFileFormat


class PyutXmlFinder:

    PERSISTENCE_PACKAGE: str = 'org.pyut.persistence'
    PERSISTENCE_DIR:     str = f'org{osSep}pyut{osSep}persistence'

    ORIGINAL_XML_PROLOG: str = '<?xml version="1.0" ?>'
    FIXED_XML_PROLOG:    str = '<?xml version="1.0" encoding="iso-8859-1"?>'

    LATEST_XML_VERSION:  str = '10'
    """
    Chunks of code in the source base that are littered all over the place; I'll concentrate them here
    """
    clsLogger: Logger = getLogger(__name__)

    def __init__(self):

        PyutXmlFinder.clsLogger = getLogger(__name__)

    @classmethod
    def getPyutXmlClass(cls, theVersion: str) -> Any:
        """
        Load and return the PyutXml class from the appropriate module that matches the input version

        Args:
            theVersion:  The version of the XML file we want to process

        Returns:  Returns the matching PyutXml`x` class  `Any` type is specified
        although, they would be some version of the above;  Creating a TypeVar
        defeats the purpose of dynamic loading since we would have to import
        the specific types
        """
        if theVersion == '10':
            from org.pyut.persistence.PyutXmlV10 import PyutXml  # type: ignore
            myXml = PyutXml()
        else:
            raise UnsupportedXmlFileFormat(f'Version {theVersion}')

        cls.clsLogger.info(f"Using version {theVersion} of the XML import/exporter")
        return myXml

    @classmethod
    def getLatestXmlVersion(cls) -> str:
        """
        No longer do this dynamically
        Returns: A string that is the version number of the latest PyutXml file
        """
        return PyutXmlFinder.LATEST_XML_VERSION

    @classmethod
    def setAsISOLatin(cls, xmlTextToUpdate: str) -> str:
        """
        Add attribute encoding = "iso-8859-1" this is not possible with minidom, so we use pattern matching

        Args:
            xmlTextToUpdate:  Old XML

        Returns:  Updated XML
        """
        retText: str = xmlTextToUpdate.replace(PyutXmlFinder.ORIGINAL_XML_PROLOG, PyutXmlFinder.FIXED_XML_PROLOG)
        return retText

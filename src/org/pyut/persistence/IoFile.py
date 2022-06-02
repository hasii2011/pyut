
from typing import TextIO

from logging import Logger
from logging import getLogger

import zlib
from xml.dom.minicompat import NodeList

from xml.dom.minidom import Document
from xml.dom.minidom import Element
from xml.dom.minidom import parseString

from org.pyut.PyutConstants import PyutConstants
from org.pyut.PyutUtils import PyutUtils

from org.pyut.ui.PyutProject import PyutProject

from org.pyut.general.Lang import Lang
from org.pyut.general.PyutXmlFinder import PyutXmlFinder

# noinspection PyProtectedMember
from org.pyut.general.Globals import _


class IoFile:
    """
    To save data in a compressed file format.

    IoFile is used to save or read Pyut file format who are named *.put.

    Example::
        IoFile = io()
        io.save("myFileName.put", project)  # to save diagram
        io.open("pyFileName.put", project)    # to read file
    """
    def __init__(self):

        self.logger: Logger = getLogger(__name__)

    def save(self, project: PyutProject):
        """
        To save diagram in XML file.  Always, uses the latest version
        """
        lastVersion: str = PyutXmlFinder.getLatestXmlVersion()

        myXml = PyutXmlFinder.getPyutXmlClass(theVersion=lastVersion)
        doc:  Document = myXml.save(project)
        text: str      = doc.toprettyxml()

        updatedText: str = PyutXmlFinder.setAsISOLatin(xmlTextToUpdate=text)
        self.logger.info(f'Document Save: \n{updatedText}')
        byteText   = updatedText.encode()
        compressed = zlib.compress(byteText)

        file = open(project.filename, "wb")
        file.write(compressed)
        file.close()

    def open(self, filename, project):
        """
        To open a compressed file and create diagram.

        Args:
            filename: A fully qualified filename
            project: The project
        """

        Lang.importLanguage()

        suffix:    str = filename[-4:]
        if suffix == PyutConstants.PYUT_EXTENSION:
            try:
                with open(filename, "rb") as dataFile:
                    compressedData: bytes = dataFile.read()
                    # noinspection PyUnresolvedReferences
                    self.logger.info(f'zlib.__version__: {zlib.__version__}')
                    xmlBytes = zlib.decompress(compressedData)    # has b'....' around it
                    xmlString: str = xmlBytes.decode()
                    self.logger.info(f'Document read:\n{xmlString}')
            except (ValueError, Exception) as e:
                self.logger.error(f'open/decompress:  {e}')
                raise e
        elif suffix == PyutConstants.XML_EXTENSION:
            fd:        TextIO = open(filename, "r")
            xmlString: str = fd.read()
            fd.close()
        else:
            PyutUtils.displayError(_(f"This is an unsupported file type: {filename}"))
            return
        dom: Document = parseString(xmlString)

        rootList: NodeList = dom.getElementsByTagName("PyutProject")
        root:     Element = rootList.item(0)
        version:  str     = root.getAttribute("version")
        myXml = PyutXmlFinder.getPyutXmlClass(theVersion=version)

        myXml.open(dom, project)

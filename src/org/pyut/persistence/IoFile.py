
from logging import Logger
from logging import getLogger

from zlib import compress
from zlib import decompress
from zlib import __version__ as zlibVersion     # type: ignore

from xml.dom.minicompat import NodeList

from xml.dom.minidom import Document
from xml.dom.minidom import Element
from xml.dom.minidom import parseString

from org.pyut.PyutConstants import PyutConstants
from org.pyut.PyutUtils import PyutUtils

from org.pyut.general.exceptions.UnsupportedXmlFileFormat import UnsupportedXmlFileFormat
from org.pyut.uiv2.IPyutProject import IPyutProject


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

    def save(self, project: IPyutProject):
        """
        To save diagram in XML file.  Always, uses the latest version
        """
        lastVersion: str = PyutXmlFinder.getLatestXmlVersion()

        myXml = PyutXmlFinder.getPyutXmlClass(theVersion=lastVersion)
        doc:  Document = myXml.save(project)
        text: str      = doc.toprettyxml()

        updatedText: str = PyutXmlFinder.setAsISOLatin(xmlTextToUpdate=text)
        self.logger.info(f'Document Save: \n{updatedText}')
        byteText:   bytes   = updatedText.encode()
        compressed: bytes = compress(byteText)

        with open(project.filename, "wb") as binaryIO:
            binaryIO.write(compressed)

    def open(self, filename, project):
        """
        To open a compressed file and create diagram.

        Args:
            filename: A fully qualified filename
            project: The project
        """
        Lang.importLanguage()

        suffix: str = filename[-4:]
        if suffix == PyutConstants.PYUT_EXTENSION:
            xmlString: str = self._decompressFile(fqFileName=filename)
        elif suffix == PyutConstants.XML_EXTENSION:
            xmlString: str = self._readXmlFile(fqFileName=filename)
        else:
            PyutUtils.displayError(_(f"This is an unsupported file type: {filename}"))
            return
        dom: Document = parseString(xmlString)

        rootList: NodeList = dom.getElementsByTagName("PyutProject")
        root:     Element = rootList.item(0)
        version:  str     = root.getAttribute("version")

        try:
            myXml = PyutXmlFinder.getPyutXmlClass(theVersion=version)
            myXml.open(dom, project)
        except (ValueError, Exception, UnsupportedXmlFileFormat) as e:
            self.logger.error(f'Invalid XML:  {e}')
            raise e

    def _decompressFile(self, fqFileName: str) -> str:

        try:
            with open(fqFileName, "rb") as compressedFile:
                compressedData: bytes = compressedFile.read()
        except (ValueError, Exception) as e:
            self.logger.error(f'decompress open:  {e}')
            raise e
        else:

            self.logger.debug(f'{zlibVersion=}')       # type: ignore
            xmlBytes:  bytes = decompress(compressedData)  # has b'....' around it
            xmlString: str   = xmlBytes.decode()
            self.logger.info(f'Document read:\n{xmlString}')

        return xmlString

    def _readXmlFile(self, fqFileName: str) -> str:
        try:
            with open(fqFileName, 'r') as xmlFile:
                xmlString: str = xmlFile.read()
        except (ValueError, Exception) as e:
            self.logger.error(f'Xml Open:  {e}')
            raise e
        else:
            return xmlString

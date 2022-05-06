
from logging import Logger
from logging import getLogger

from os import getcwd
from os import chdir

import zlib
from typing import TextIO
from xml.dom.minidom import Document
from xml.dom.minidom import parseString

from org.pyut.PyutConstants import PyutConstants
from org.pyut.PyutUtils import PyutUtils

from org.pyut.ui.PyutProject import PyutProject

from org.pyut.enums.DiagramType import DiagramType

from org.pyut.general.Lang import Lang
from org.pyut.general.PyutXmlFinder import PyutXmlFinder

from org.pyut.ui.Mediator import Mediator

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
            filename: The file name
            project: The project
        """
        oldPath:  str      = getcwd()
        mediator: Mediator = Mediator()
        path:     str      = mediator.getAppPath()  # TODO I do not think we need to do this
        chdir(path)                                 #
        
        Lang.importLanguage()
        xmlString: str = ""
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
        elif suffix == PyutConstants.XML_EXTENSION:
            fd:        TextIO = open(filename, "r")
            xmlString: str = fd.read()
            fd.close()
        else:
            PyutUtils.displayError(_(f"This is an unsupported file type: {filename}"))
            return
        dom = parseString(xmlString)

        root = dom.getElementsByTagName("PyutProject")
        if len(root) > 0:
            root = root[0]
            if root.hasAttribute('version'):
                version = root.getAttribute("version")
                myXml = PyutXmlFinder.getPyutXmlClass(theVersion=version)
            else:
                from org.pyut.persistence.PyutXml import PyutXml
                myXml = PyutXml()
            myXml.open(dom, project)
        else:
            # TODO fix this code to use PyutXmlFinder;
            #  I don't think this is used by the Python3 version of this Pyut
            self.logger.warning('***********************************')
            self.logger.warning('Using old code !!!')
            self.logger.warning('***********************************')
            root = dom.getElementsByTagName("Pyut")[0]
            if root.hasAttribute('version'):
                version = root.getAttribute("version")
                self.logger.info(f"Using version {version} of the importer")
                module = __import__("PyutXmlV" + str(version))
                # noinspection PyUnresolvedReferences
                myXml = module.PyutXml()
            else:
                from org.pyut.persistence.PyutXml import PyutXml  # don't like it here but at top of file not recognized -- hasii
                # version = 1
                myXml = PyutXml()
            project.newDocument(DiagramType.CLASS_DIAGRAM)
            umlFrame = project.getDocuments()[0].getFrame()
            myXml.open(dom, umlFrame)

        chdir(oldPath)              # TODO remove this also if above removed

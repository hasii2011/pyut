
from logging import Logger
from logging import getLogger

from os import getcwd
from os import chdir

import zlib

from xml.dom.minidom import Document
from xml.dom.minidom import parseString

from org.pyut.PyutUtils import PyutUtils

from org.pyut.enums.DiagramType import DiagramType

from org.pyut.general.Lang import importLanguage
from org.pyut.general.PyutXmfFinder import PyutXmlFinder

from org.pyut.general.Mediator import getMediator

from org.pyut.general.Globals import _


class IoFile:

    """
    To save data in a compressed file format.

    IoFile is used to save or read Pyut file format who are named *.put.

    Example::
        IoFile = io()
        io.save("myFileName.put", project)  # to save diagram
        io.open("pyFileName.put", project)    # to read file

    :version: $Revision: 1.10 $
    :author:  Deve Roux
    :contact: droux@eivd.ch
    """
    def __init__(self):

        self.logger: Logger = getLogger(__name__)

    def save(self, project):
        """
        To save diagram in XML file.  Always, uses the latest version
        """
        lastVersion: int = PyutXmlFinder.getLatestXmlVersion()

        myXml = PyutXmlFinder.getPyutXmlClass(theVersion=lastVersion)
        doc:  Document = myXml.save(project)
        text: str      = doc.toprettyxml()

        # add attribute encoding = "iso-8859-1" this is not possible with minidom, so we use pattern matching
        updatedText: str = text.replace(r'<?xml version="1.0" ?>', r'<?xml version="1.0" encoding="iso-8859-1"?>')
        self.logger.info(f'Document Save: \n{updatedText}')
        byteText   = updatedText.encode()
        compressed = zlib.compress(byteText)

        file = open(project.getFilename(), "wb")
        file.write(compressed)
        file.close()
        # chdir(oldpath)

    def open(self, filename, project):
        """
        To open a compressed file and create diagram.

        @author Deve Roux
        """
        oldpath = getcwd()
        path = getMediator().getAppPath()
        chdir(path)

        importLanguage()
        xmlString = ""
        if filename[-4:] == ".put":
            try:
                with open(filename, "rb") as dataFile:
                    compressedData: bytes = dataFile.read()
                    self.logger.info(f'zlib.__version__: {zlib.__version__}')
                    xmlBytes = zlib.decompress(compressedData)    # has b'....' around it
                    xmlString: str = xmlBytes.decode()
                    self.logger.info(f'Document read:\n{xmlString}')
            except (ValueError, Exception) as e:
                self.logger.error(f'open:  {e}')
        elif filename[-4:] == ".xml":
            xmlString = open(filename, "r").read()
        else:
            PyutUtils.displayError(_(f"Can't open the unidentified file : {filename}"))
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
            # TODO fix this code to use PyutXmlFinder
            root = dom.getElementsByTagName("Pyut")[0]
            if root.hasAttribute('version'):
                version = root.getAttribute("version")
                self.logger.info(f"Using version {version} of the importer")
                module = __import__("PyutXmlV" + str(version))
                myXml = module.PyutXml()
            else:
                from org.pyut.persistence.PyutXml import PyutXml  # don't like it here but at top of file not recognized -- hasii
                # version = 1
                myXml = PyutXml()
            project.newDocument(DiagramType.CLASS_DIAGRAM)
            umlFrame = project.getDocuments()[0].getFrame()
            myXml.open(dom, umlFrame)

        chdir(oldpath)
        # TODO : put this back
        # except:
        #    #dlg=wxMessageDialog(umlFrame,
        #    #    _("An error occured while while parsing the file ")
        #    #    + str(fileName) + ".",
        #    #    _("Parse Error !"),
        #    #    wxOK | wxICON_ERROR)
        #    #dlg.ShowModal()
        #    #dlg.Destroy()
        #    displayError(_("An error occured while parsing the file") + \
        #                 str(fileName), _("Parse Error !"))

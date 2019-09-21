
from os import getcwd
from os import chdir

from glob import glob
from lang import importLanguage

import zlib

from xml.dom.minidom import parseString


from mediator import getMediator
from pyutUtils import displayError

from PyutConsts import CLASS_DIAGRAM
from PyutXml import PyutXml

from globals import _


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
    def save(self, project):
        """
        To save save diagram in XML file.

        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        oldpath = getcwd()
        path = getMediator().getAppPath()
        chdir(path)

        candidates = glob("PyutXmlV*.py")
        numbers = [int(s[8:-3]) for s in candidates]
        lastVersion = str(max(numbers))

        print("Using version", lastVersion, " of the exporter")
        module = __import__("PyutXmlV" + lastVersion)
        myXml = module.PyutXml()

        doc = myXml.save(project)
        text = doc.toxml()
        # add attribute encoding = "iso-8859-1"
        # this is not possible with minidom, so we use pattern matching
        text = text.replace(r'<?xml version="1.0" ?>', r'<?xml version="1.0" encoding="iso-8859-1"?>')

        compressed = zlib.compress(text)
        file = open(project.getFilename(), "wb")
        file.write(compressed)
        file.close()
        chdir(oldpath)

    def open(self, filename, project):
        """
        To open a compressed file and create diagram.

        @author Deve Roux
        """
        # print "IoFile-1"

        #
        oldpath = getcwd()
        path = getMediator().getAppPath()
        # print "IoFile-2"
        chdir(path)

        # print "IoFile-3"
        importLanguage()
        # print "IoFile-4"
        xmlString = ""
        if filename[-4:]==".put":
            # print "IoFile-5"
            comp = open(filename, "r").read()
            # print "IoFile-6"
            try:
                import zlib
                print(zlib.__version__)
                # print "1"
                import zlib
                xmlString = zlib.decompress(comp)
            except:
                print("EXCEPTION")
            # print xmlString
            # print "IoFile-7"
        elif filename[-4:]==".xml":
            xmlString = open(filename, "rb").read()
        else:
            displayError(_("Can't open the unidentified file : %s") % filename)
            return
        # try:
        # print "IoFile-8"
        dom = parseString(xmlString)

        # Try to load file for version >=5
        # print "IoFile-9"
        root = dom.getElementsByTagName("PyutProject")
        if len(root)>0:
            root = root[0]
            if root.hasAttribute('version'):
                version = root.getAttribute("version")
                print("Using version", version, " of the importer")
                module = __import__("PyutXmlV" + str(version))
                myXml = module.PyutXml()
            else:
                version = 1
                from .PyutXml import PyutXml
                myXml = PyutXml()
            myXml.open(dom, project)
        else:
            root = dom.getElementsByTagName("Pyut")[0]
            if root.hasAttribute('version'):
                version = root.getAttribute("version")
                print("Using version", version, " of the importer")
                module = __import__("PyutXmlV" + str(version))
                myXml = module.PyutXml()
            else:
                version = 1
                myXml = PyutXml()
            project.newDocument(CLASS_DIAGRAM)
            umlFrame = project.getDocuments()[0].getFrame()
            myXml.open(dom, umlFrame)
        #print "IoFile-10"


        os.chdir(oldpath)
        # TODO : put this back
        #except:
        #    #dlg=wxMessageDialog(umlFrame,
        #    #    _("An error occured while while parsing the file ")
        #    #    + str(fileName) + ".",
        #    #    _("Parse Error !"),
        #    #    wxOK | wxICON_ERROR)
        #    #dlg.ShowModal()
        #    #dlg.Destroy()
        #    displayError(_("An error occured while parsing the file") + \
        #                 str(fileName), _("Parse Error !"))


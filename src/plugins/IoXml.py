#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.10 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2002-1-9"

from StringIO import StringIO
from PyutIoPlugin import PyutIoPlugin
#from wxPython.wx import *
from mediator import getMediator
import wx

class IoXml(PyutIoPlugin):
    """
    To save XML file format.

    @version $Revision: 1.10 $
    """
    def getName(self):
        """
        This method returns the name of the plugin.

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.2
        """
        return "IoXml"



    def getAuthor(self):
        """
        This method returns the author of the plugin.

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.2
        """
        return "Deve Roux <droux@eivd.ch>"



    def getVersion(self):
        """
        This method returns the version of the plugin.

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.2
        """
        return "1.0"



    def getInputFormat(self):
        """
        Return a specification tupple.

        @return tupple
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.2
        """
        # return None if this plugin can't read.
        # otherwise, return a tupple with
        # - name of the input format
        # - extension of the input format
        # - textual description of the plugin input format
        # example : return ("Text", "txt", "Tabbed text...")
        return ("XML", "xml", "Pyut XML file")



    def getOutputFormat(self):
        """
        Return a specification tupple.

        @return tupple
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.2
        """
        # return None if this plugin can't write.
        # otherwise, return a tupple with
        # - name of the output format
        # - extension of the output format
        # - textual description of the plugin output format
        # example : return ("Text", "txt", "Tabbed text...")
        return ("XML", "xml", "Pyut XML file")



    def setExportOptions(self):
        """
        Prepare the export.
        This can be used to ask some questions to the user.

        @return Boolean : if False, the export will be cancelled.
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        rep = wx.MessageBox("Do you want pretty xml ?", "Export option",
            style = wx.YES_NO | wx.CANCEL | wx.CENTRE | wx.ICON_QUESTION)
        self.pretty = (rep == wx.YES)
        return rep != wx.CANCEL



    def write(self, oglObjects):
        """
        Write data to filename. Abstract.

        @return True if succeeded, False if error or canceled
        @param OglClass and OglLink [] : list of exported objects
        @author Deve Roux <droux@eivd.ch>
        @since 1.0
        """
        import os
        oldpath = os.getcwd()
        # Ask the user which destination file he wants
        from PyutXmlV2 import PyutXml
        filename=self._askForFileExport()
        if filename=="":
            return False
        path = getMediator().getAppPath()
        os.chdir(path)

        from glob import glob
        candidates = glob("PyutXmlV*.py")
        numbers = [int(s[8:-3]) for s in candidates]
        lastVersion = str(max(numbers))
        print "Using version", lastVersion, " of the exporter"
        module = __import__("PyutXmlV" + lastVersion)
        myXml = module.PyutXml()
        file=open(filename, "w")

        if lastVersion>=5:
            import mediator
            ctrl = mediator.getMediator()
            fileHandling = ctrl.getFileHandling()
            project = fileHandling.getProjectFromOglObjects(oglObjects)
            doc = myXml.save(project)
        else:
            doc = myXml.save(oglObjects)

        if self.pretty:
            text = doc.toprettyxml()
        else:
            text = doc.toxml()

        # add attribute encoding = "iso-8859-1"
        # this is not possible with minidom, so we use pattern matching
        text = text.replace(r'<?xml version="1.0" ?>', 
            r'<?xml version="1.0" encoding="iso-8859-1"?>')

        file.write(text)
        file.close()
        os.chdir(oldpath)
        return True


    #>------------------------------------------------------------------------


    def readOld(self, oglObjects, umlFrame):
        """
        Read data from filename. Abstract.

        @return True if succeeded, False if error or canceled
        @param OglClass and OglLink [] : list of imported objects
        @param UmlFrame : Pyut's UmlFrame
        @author Deve Roux <droux@eivd.ch>
        @since 1.0
        """
        import os
        #Note : xml.dom.minidom must be instancied here, since it redefines
        #the function '_', which is also used for i18n
        from xml.dom.minidom import parse   
        oldpath = os.getcwd()
        path = getMediator().getAppPath()
        os.chdir(path)
        # Ask the user which destination file he wants
        filename=self._askForFileImport()
        if filename=="":
            return False

        dom = parse(StringIO(open(filename).read())) 
        root = dom.getElementsByTagName("Pyut")[0]
        if root.hasAttribute('version'):
            version = root.getAttribute("version")
        else:
            version = 1

        if version == 1:
            from PyutXml import PyutXml
            myXml = PyutXml()
        else:
            module = __import__("PyutXmlV" + str(version))
            myXml = module.PyutXml()

        myXml.open(dom, umlFrame)
        os.chdir(oldpath)
        return True


    #>------------------------------------------------------------------------

    def read(self, oglObjects, umlFrame):
        """
        Read data from filename.

        @return True if succeeded, False if error or canceled
        @param OglClass and OglLink [] : list of imported objects
        @param UmlFrame : Pyut's UmlFrame
        @author C.Dutoit
        """
        # Ask the user which destination file he wants
        filename=self._askForFileImport()
        if filename=="":
            return False

        # Open file
        import mediator
        ctrl = mediator.getMediator()
        fileHandling = ctrl.getFileHandling()
        project = fileHandling.getCurrentProject()
        for document in project.getDocuments():
            project.removeDocument(document, False)
        fileHandling.openFile(filename, project)


    #>------------------------------------------------------------------------

#    def readV2(self):
#        """
#        Read data 
#
        #@return True if succeeded, False if error or canceled
        #@param OglClass and OglLink [] : list of imported objects
        #@param UmlFrame : Pyut's UmlFrame
        #@author C.Dutoit
        #"""
        # Ask the user which destination file he wants
        #filename=self._askForFileImport()
        #if filename=="":
        #    return False
#
#        # Open file
#        import mediator
#        ctrl = mediator.getMediator()
#        fileHandling = ctrl.getFileHandling()
#        fileHandling.openFile(filename)



#fichier = IoXml()
#debug = fichier.open("test.xml")
#debug = []
#fichier.open("test.xml", debug)
#fichier.save("testRW.xml",debug)

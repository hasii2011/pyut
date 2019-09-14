#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.5 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2002-1-9"

from StringIO import StringIO
from PyutXmi import *
from PyutXml import *
from PyutIoPlugin import PyutIoPlugin
import wx

class IoXmi(PyutIoPlugin):
    """
    To save XML file format.

    @version $Revision: 1.5 $
    """
    def getName(self):
        """
        This method returns the name of the plugin.

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.2
        """
        return "IoXmi"



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
        return ("XMI", "xml", "Pyut XMI file")



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
        return ("XMI", "xml", "Pyut XMI file")



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
        # Ask the user which destination file he wants
        filename=self._askForFileExport()
        if filename=="":
            return False
        file=open(filename, "w")

        
        myXml = PyutXml()
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
        return True


    #>------------------------------------------------------------------------


    def read(self, oglObjects, umlFrame):
        """
        Read data from filename. Abstract.

        @return True if succeeded, False if error or canceled
        @param OglClass and OglLink [] : list of imported objects
        @param UmlFrame : Pyut's UmlFrame
        @author Deve Roux <droux@eivd.ch>
        @since 1.0
        """
        from xml.dom.minidom import parse
        
        # Ask the user which destination file he wants
        filename=self._askForFileImport()
        if filename=="":
            return False

        dom = parse(StringIO(open(filename).read())) 

        myXmi = PyutXmi()
        myXmi.open(dom, umlFrame)
        return True



#fichier = IoXml()
#debug = fichier.open("test.xml")
#debug = []
#fichier.open("test.xml", debug)
#fichier.save("testRW.xml",debug)

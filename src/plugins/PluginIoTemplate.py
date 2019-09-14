#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__  = "Laurent Burgbacher <lb@alawa.ch>"
__version__ = "$Revision: 1.3 $"
__date__    = "2002-02-14"

from PyutIoPlugin import PyutIoPlugin

class PluginName(PyutIoPlugin):
    """
    Sample class for input/output plug-ins.

    @author Laurent Burgbacher <lb@alawa.ch>
    @version $Revision: 1.3 $
    """
    def __init__(self, oglObjects, umlFrame):
        """
        Constructor.

        @param String filename : name of the file to save to
        @param OglObject oglObjects : list of ogl objects
        @param UmlFrame umlFrame : the umlframe of pyut
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        PyutIoPlugin.__init__(self, oglObjects, umlFrame)

        # your initializations now



    def getName(self):
        """
        This method returns the name of the plugin.

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.2
        """
        return "No name"



    def getAuthor(self):
        """
        This method returns the author of the plugin.

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.2
        """
        return "No author"



    def getVersion(self):
        """
        This method returns the version of the plugin.

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.2
        """
        return "0.0"



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
        return None



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
        return None



    def setImportOptions(self):
        """
        Prepare the import.
        This can be used to ask some questions to the user.

        @return Boolean : if False, the import will be cancelled.
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        # here, you can open a dialog to ask the user for import options
        # return False if the user wants to cancel at this point
        return True



    def setExportOptions(self):
        """
        Prepare the export.
        This can be used to ask some questions to the user.

        @return Boolean : if False, the export will be cancelled.
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        # here, you can open a dialog to ask the user for export options
        # return False if the user wants to cancel at this point
        return True



    def read(self, file, oglObjects, umlFrame):
        """
        Read data from filename. Abstract.

        @param File file : file to read
        @param OglClass and OglLink [] : list of imported objects
        @param UmlFrame : Pyut's UmlFrame
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        pass



    def write(self, file, oglObjects):
        """
        Write data to filename.

        @param File file : file to write
        @param OglClass and OglLink [] : list of exported objects
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        pass

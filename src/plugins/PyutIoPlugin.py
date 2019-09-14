#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__  = "Laurent Burgbacher <lb@alawa.ch>"
__version__ = "$Revision: 1.9 $"
__date__    = "2002-02-14"
#from wxPython.wx    import * 
from mediator       import *
from PyutPlugin     import PyutPlugin
import os, wx
#wx.FileSelector, wx.DirDialog, \
#wx.OPEN, wx.FILE_MUST_EXIST, wx.SAVE, wx.OVERWRITE_PROMPT, \
#w

class PyutIoPlugin(PyutPlugin):
    """
    Base class for input/output plug-ins.

    If you want to do a new plugin, you must inherit from this class and
    redefine some methods.

    Informational methods
    ---------------------

    These are:
        `getName`
        `getAuthor`
        `getVersion`
        `getInputFormat`
        `getOutputFormat`

    They must be redefined to return a simple string. See their respective doc.

    Interaction methods
    -------------------

    You can ask the user for plugin parameters. If you have to, just redefine
    these methods:
        `setImportOptions`
        `setExportOptions`

    Do whatever you need inside, and return True if all went good, or False
    to cancel the import/export.

    Real work
    ---------

    All the real import/export work is done in:
        `read(self, oglObjects, umlFrame)`
        `write(self, oglObjects)`

    Plugin call
    -----------

    To call a plugin, you need to instantiate it, and call one of:
        `doImport`
        `doExport`

    These two *Template Methods* (Desing patterns) will call what needs to be.

    @author Laurent Burgbacher <lb@alawa.ch>
    @version $Revision: 1.9 $
    """
    def __init__(self, oglObjects, umlFrame):
        """
        Constructor.

        @param OglObject oglObjects : list of ogl objects
        @param UmlFrame umlFrame : the umlframe of pyut
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        PyutPlugin.__init__(self, umlFrame, getMediator())
        self.__oglObjects = oglObjects
        #self.__umlFrame = umlFrame
        #self.__ctrl = getMediator()


    #>------------------------------------------------------------------------

    def getName(self):
        """
        This method returns the name of the plugin.

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        return "No name"


    #>------------------------------------------------------------------------

    def getAuthor(self):
        """
        This method returns the author of the plugin.

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        return "No author"


    #>------------------------------------------------------------------------

    def getVersion(self):
        """
        This method returns the version of the plugin.

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        return "0.0"


    #>------------------------------------------------------------------------

    def getInputFormat(self):
        """
        Return a specification tupple.

        @return tuple
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        # return None if this plugin can't read.
        # otherwise, return a tupple with
        # - name of the input format
        # - extension of the input format
        # - textual description of the plugin input format
        # example : return ("Text", "txt", "Tabbed text...")
        return None


    #>------------------------------------------------------------------------

    def getOutputFormat(self):
        """
        Return a specification tupple.

        @return tuple
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        # return None if this plugin can't write.
        # otherwise, return a tupple with
        # - name of the output format
        # - extension of the output format
        # - textual description of the plugin output format
        # example : return ("Text", "txt", "Tabbed text...")
        return None

    #>------------------------------------------------------------------------


    def setImportOptions(self):
        """
        Prepare the import.
        This can be used to ask some questions to the user.

        @return Boolean : if False, the import will be cancelled.
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        return 1


    #>------------------------------------------------------------------------

    def setExportOptions(self):
        """
        Prepare the export.
        This can be used to ask some questions to the user.

        @return Boolean : if False, the export will be cancelled.
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        return 1


    #>------------------------------------------------------------------------

    def read(self, oglObjects, umlFrame):
        """
        Read data from filename. Abstract.

        @param OglClass and OglLink [] : list of imported objects
        @param UmlFrame : Pyut's UmlFrame
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        pass


    #>------------------------------------------------------------------------

    def write(self, oglObjects):
        """
        Write data to filename. Abstract.

        @param OglClass and OglLink [] : list of exported objects
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        pass



    #>------------------------------------------------------------------------

    def doImport(self):
        """
        Called by Pyut to begin the import process.

        @since 1.4
        """
        # if this plugin can import
        if self.getInputFormat() != None:
            # set user options for import
            if not self.setImportOptions():
                return None

            # read it into the list
            self.read(self.__oglObjects, self._umlFrame)

            # return the new oglObjects list
            return self.__oglObjects
        else:
            return None


    #>------------------------------------------------------------------------

    def doExport(self):
        """
        Called by Pyut to begin the export process.

        @since 1.4
        """
        # if this plugin can export
        if self.getOutputFormat() != None:
            # set user options for export
            if not self.setExportOptions():
                return None

            # write the file
            self.write(self.__oglObjects)

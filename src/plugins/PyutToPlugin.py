#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__  = "C.Dutoit <dutoitc@hotmail.com"
__version__ = "$Revision: 1.5 $"
__date__    = "2002-10-10"
#from wxPython.wx    import * 
from mediator       import *
from PyutPlugin     import PyutPlugin
import os, wx


class PyutToPlugin(PyutPlugin):
    """
    Note : to merge with my PyutToPlugin
    @author C.Dutoit <dutoitc@hotmail.com>
    @version $Revision: 1.5 $
    """
    def __init__(self, umlObjects, umlFrame):
        """
        Constructor.

        @param OglObject umlObjects : list of uml objects
        @param UmlFrame umlFrame : the umlframe of pyut
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        self._umlObjects = umlObjects
        self._umlFrame = umlFrame


    #>------------------------------------------------------------------------

    def getName(self):
        """
        This method returns the name of the plugin.

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        return "Unnamed tool plugin"


    #>------------------------------------------------------------------------

    def getAuthor(self):
        """
        This method returns the author of the plugin.

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        return "anonymous"


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

    def getMenuTitle(self):
        """
        Return a menu title string

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        # Return the menu title as it must be displayed
        return "Untitled plugin"

    #>------------------------------------------------------------------------

    def setOptions(self):
        """
        Prepare the import.
        This can be used to ask some questions to the user.

        @return Boolean : if False, the import will be cancelled.
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        return 1

    #>------------------------------------------------------------------------

    def callDoAction(self):
        """
        This is used internally, don't overload it.

        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        if not self.setOptions():
            return
        self.doAction(self._umlObjects, getMediator().getSelectedShapes(),
            self._umlFrame)

    #>------------------------------------------------------------------------

    def doAction(self, umlObjects, selectedObjects, umlFrame):
        """
        Do the tool's action

        @param OglObject [] umlObjects : list of the uml objects of the diagram
        @param OglObject [] selectedObjects : list of the selected objects
        @param UmlFrame umlFrame : the frame of the diagram
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        pass

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.5 $"
__author__ = "Laurent Burgbacher - lb@alawa.ch"
__date__ = "2002-10-10"

from StringIO import StringIO
from PyutToPlugin import PyutToPlugin
from PyutClass import PyutClass
from OglClass import OglClass
from PyutMethod import PyutMethod
from PyutParam import PyutParam
from PyutField import PyutField
from PyutConsts import *
#from wxPython.wx import *

import os, wx

class ToLayoutSave(PyutToPlugin):
    """
    Python code generation/reverse engineering

    @version $Revision: 1.5 $
    """
    def __init__(self, umlObjects, umlFrame):
        """
        Constructor.

        @param String filename : name of the file to save to
        @param OglObject oglObjects : list of ogl objects
        @param UmlFrame umlFrame : the umlframe of pyut
        """
        PyutToPlugin.__init__(self, umlObjects, umlFrame)
        self._umlFrame = umlFrame

    #>------------------------------------------------------------------------

    def getName(self):
        """
        This method returns the name of the plugin.

        @return string
        @since 1.1
        """
        return "Layout plugin (save)"

    #>------------------------------------------------------------------------

    def getAuthor(self):
        """
        This method returns the author of the plugin.

        @return string
        @since 1.1
        """
        return "Cédric DUTOIT <dutoitc@hotmail.com>"

    #>------------------------------------------------------------------------

    def getVersion(self):
        """
        This method returns the version of the plugin.

        @return string
        @since 1.1
        """
        return "1.0"

    #>------------------------------------------------------------------------

    def getMenuTitle(self):
        """
        Return a menu title string

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        # Return the menu title as it must be displayed
        return "Layout (save)"

    #>------------------------------------------------------------------------

    def setOptions(self):
        """
        Prepare the import.
        This can be used to ask some questions to the user.

        @return Boolean : if False, the import will be cancelled.
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        return True


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
        file = wx.FileSelector(
            "Choose a file name to export layout",
            wildcard = "Layout file (*.lay) |*.lay",
            #default_path = self.__ctrl.getCurrentDir(),
            flags = wx.SAVE | wx.OVERWRITE_PROMPT | wx.CHANGE_DIR
        )

        f=open(file, "w")
        for el in umlObjects:
            f.write(el.getPyutObject().getName() + "," +
                    str(el.GetPosition()[0]) + "," +
                    str(el.GetPosition()[1]) + "," +
                    str(el.GetSize()[0]) + "," +
                    str(el.GetSize()[1]) + "\n")
        f.close()

    #>------------------------------------------------------------------------


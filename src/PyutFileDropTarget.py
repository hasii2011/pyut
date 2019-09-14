#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.4 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2001-11-14"

#from wxPython.wx import *
import wx


################################################################################
class PyutFileDropTarget(wx.FileDropTarget):
    """
    PyutFileDropTarget : File drag-n-drop handling
    @version $Revision: 1.4 $
    """


    #>------------------------------------------------------------------------

    def __init__(self, window):
        """
        Constructor.
        
        @param ??? window : a window containing the function loadFile with
                            a filename wich could be passed in parameter
        @since 1.0
        @author C.Dutoit
        """
        wx.FileDropTarget.__init__(self)
        self.window=window


    #>------------------------------------------------------------------------

    def OnDropFiles(self, x, y, filenames):
        """
        load the first filename received by the user drop action

        @param See wx.Python documentation help
        @since 1.0
        @author C.Dutoit
        """
        self.window.loadByFilename(filenames[0])


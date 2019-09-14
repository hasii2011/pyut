#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.4 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2001-11-14"

#from wxPython.wx import *
import wx

class DlgEditMethod (wx.Dialog):
    """
    dlgEditMethod : Method edition dialog
    @version $Revision: 1.4 $
    """

    #>------------------------------------------------------------------------

    def __init__(self, parent, ID):
        """
        Constructor.

        @since 1.0
        @author C.Dutoit
        """
        wx.Dialog.__init__(self, parent, ID, "Method edition", 
                          wx.DefaultPosition, wx.Size(320, 400))
        self.ShowModal()
        self.Center(wx.BOTH)

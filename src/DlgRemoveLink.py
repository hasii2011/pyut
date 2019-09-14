#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.4 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2002-1-8"

#from wxPython.wx import *
import wx

class DlgRemoveLink(wx.MessageDialog):
    """
    Dialog for the inheritance-interface links rmoval.

    @version $Revision: 1.4 $
    """

    #>------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor.

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """

        wx.MessageDialog.__init__(self, None,\
            _("Are you sure you want to remove this link ?"),
            _("Remove link confirmation"),
            style = wx.YES_NO | wx.ICON_QUESTION | wx.NO_DEFAULT)

    #>------------------------------------------------------------------------

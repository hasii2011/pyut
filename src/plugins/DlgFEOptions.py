#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__version__ = "$Revision: 1.4 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2002-02-23"

from __future__  import nested_scopes
#from wxPython.wx import *
from pyutUtils   import *
from PyutPreferences import *
from OglClass    import *
import lang, wx

class DlgFEOptions(wx.Dialog):
    """
    This is the option dialog for Fast Edit Tool.

    Display current properties and possible values, save modified values.

    :version: $Revision: 1.4 $
    :author: Philippe Waelti
    :contact: pwaelti@eivd.ch
    """
    def __init__(self, parent):
        """
        Constructor.

        @param wx.Window parent Parent
        @param int ID ID
        @author Philippe Waelti <pwaelti@eivd.ch>
        @since 1.0
        """
        wx.Dialog.__init__(self, parent, -1, _("Fast Edit Options"))
        self.__prefs = PyutPreferences()
        self.__initCtrl()

        self.Bind(wx.EVT_CLOSE, self.__OnClose)

    #>------------------------------------------------------------------------

    def __initCtrl(self):
        """
        Initialize the controls.

        @since 1.0
        """
        # IDs
        [
            self.__editorID
        ] = assignID(1)

        GAP = 10

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.__lblEditor = wx.StaticText(self, -1, _("Editor"))
        self.__txtEditor = wx.TextCtrl(self, -1, size=(100,20))
        sizer.Add(self.__lblEditor, 0, wx.ALL, GAP)
        sizer.Add(self.__txtEditor, 0, wx.ALL, GAP)

        hs = wx.BoxSizer(wx.HORIZONTAL)
        btnOk = wx.Button(self, wx.ID_OK, _("&OK"))
        hs.Add(btnOk, 0, wx.ALL, GAP)
        sizer.Add(hs, 0, wx.CENTER)

        self.__changed = 0

        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        sizer.Fit(self)
        sizer.SetSizeHints(self)

        btnOk.SetDefault()

        self.Bind(wx.EVT_TEXT, self.__OnText, id=self.__editorID)
        self.Bind(wx.EVT_BUTTON, self.__OnCmdOk, id=wx.ID_OK)

        self.__setValues()

        self.Center()
        self.ShowModal()

    #>------------------------------------------------------------------------

    def __setValues(self):
        """
        Set the default values to the controls.

        @since 1.0
        """
        def secureStr(x):
            if x is None:
                return ""
            else:
                return x

        self.__txtEditor.SetValue(secureStr(self.__prefs["EDITOR"]))
        self.__txtEditor.SetInsertionPointEnd()


    #>------------------------------------------------------------------------

    def __OnText(self, event):
        """
        Occurs when text entry changes.

        @since 1.0
        """
        self.__changed = 1

    #>------------------------------------------------------------------------

    def __OnClose(self, event):
        """
        Callback.

        @since 1.2
        """
        event.Skip()

    #>------------------------------------------------------------------------

    def __OnCmdOk(self, event):
        """
        Callback.

        @since 1.2
        """
        if self.__changed:
            self.__prefs["EDITOR"] = self.__txtEditor.GetValue()

        self.Close()

    #>------------------------------------------------------------------------

    def getEditor(self):
        """
        Return the editor string.

        @return String editor : Chosen editor
        @since 1.2
        """
        return self.__txtEditor.GetValue()

    #>------------------------------------------------------------------------

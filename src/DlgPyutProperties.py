#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__version__ = "$Revision: 1.7 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2002-02-23"

from __future__  import nested_scopes
#from wxPython.wx import *
from pyutUtils   import *
#from PyutPrefs   import *
from PyutPreferences import *
from OglClass    import *
import lang, wx

class DlgPyutProperties(wx.Dialog):
    """
    This is the properties dialog of Pyut.

    Display current properties and possible values, save modified values.

    To use it from a w.xFrame :
        dlg = DlgProperties(self, -1, PyutPreferences(), Mediator())
        dlg.ShowModal()
        dlg.Destroy()
    
    :version: $Revision: 1.7 $
    :author: C.Dutoit
    :contact: dutoitc@hotmail.com
    """
    def __init__(self, parent, ID, ctrl, prefs):
        """
        Constructor.

        @param wx.Window parent Parent
        @param int ID ID
        @param Mediator ctrl
        @param PyutPrefs prefs
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        wx.Dialog.__init__(self, parent, ID, _("Properties"))
        self.__ctrl = ctrl
        self.__prefs = prefs
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
            self.__autoResizeID, self.__showParamsID, self.__languageID,
            self.__maximizeID, self.__fontSizeID, self.__showTipsID,
        ] = assignID(6)

        GAP = 5

        sizer = wx.BoxSizer(wx.VERTICAL)

        # Maximize
        self.__cbMaximize = wx.CheckBox(self, self.__maximizeID,
           _("&Maximize on startup"))

        # Auto resize
        self.__cbAutoResize = wx.CheckBox(self, self.__autoResizeID,
            _("&Auto resize classes to fit content"))

        # Show Params
        self.__cbShowParams = wx.CheckBox(self, self.__showParamsID,
            _("&Show params in classes"))

        # Show tips
        self.__cbShowTips = wx.CheckBox(self, self.__showTipsID,
            _("Show &Tips on startup"))

        # Font size
#        self.__lblFontSize = wx.StaticText(self, -1, _("Font size"))
#        self.__txtFontSize = wx.TextCtrl(self, self.__fontSizeID)
#        szrFont = wx.BoxSizer(wx.HORIZONTAL)
#        szrFont.Add(self.__lblFontSize, 0, wx.ALL, GAP)
#        szrFont.Add(self.__txtFontSize, 0, wx.ALL, GAP)

        # Language
        #print "   InitCtrl-1"
        self.__lblLanguage = wx.StaticText(self, -1, _("Language"))
        #print "   InitCtrl-a", self.__languageID
        #print lang.LANGUAGES.values()
        self.__cmbLanguage = wx.ComboBox(self, self.__languageID,
            choices = [el[0] for el in lang.LANGUAGES.values()],
            style = wx.CB_READONLY|wx.CB_SORT)
        #print "   InitCtrl-1b"
        szrLanguage = wx.BoxSizer(wx.HORIZONTAL)
        szrLanguage.Add(self.__lblLanguage, 0, wx.ALL, GAP)
        szrLanguage.Add(self.__cmbLanguage, 0, wx.ALL, GAP)
        #print "   InitCtrl-1c"

        sizer.Add(self.__cbAutoResize, 0, wx.ALL, GAP)
        sizer.Add(self.__cbShowParams, 0, wx.ALL, GAP)
        sizer.Add(self.__cbMaximize,   0, wx.ALL, GAP)
        sizer.Add(self.__cbShowTips,   0, wx.ALL, GAP)
#        sizer.Add(szrFont,             0, wx.ALL, GAP)
        sizer.Add(szrLanguage,         0, wx.ALL, GAP)
        #print "   InitCtrl-1d"

        hs = wx.BoxSizer(wx.HORIZONTAL)
        btnOk = wx.Button(self, wx.ID_OK, _("&OK"))
        hs.Add(btnOk, 0, wx.ALL, GAP)
        sizer.Add(hs, 0, wx.CENTER)
        #print "   InitCtrl-2"

        self.__changed = 0

        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        sizer.Fit(self)
        sizer.SetSizeHints(self)

        #print "   InitCtrl-3"
        self.Bind(wx.EVT_CHECKBOX, self.__OnCheckBox, id=self.__autoResizeID)
        self.Bind(wx.EVT_CHECKBOX, self.__OnCheckBox, id=self.__showParamsID)
        self.Bind(wx.EVT_CHECKBOX, self.__OnCheckBox, id=self.__maximizeID)
        self.Bind(wx.EVT_CHECKBOX, self.__OnCheckBox, id=self.__showTipsID)
#       self.Bind( wx.EVT_TEXT(self, self.__fontSizeID, self.__OnFontSizeChange)
        self.Bind(wx.EVT_BUTTON, self.__OnCmdOk, id=wx.ID_OK)

        self.__setValues()
        #print "   InitCtrl-4"

    #>------------------------------------------------------------------------

    def __setValues(self):
        """
        Set the default values to the controls.

        @since 1.0
        """
        def secureInt(x):
            if x is None:
                return 0
            elif x==True or x=="True":
                return 1
            elif x==False or x=="False":
                return 0
            else:
                return int(x)
        self.__cbAutoResize.SetValue(secureInt(self.__prefs["AUTO_RESIZE"]))
        self.__cbShowParams.SetValue(secureInt(self.__prefs["SHOW_PARAMS"]))
        self.__cbMaximize.SetValue(secureInt(self.__prefs["FULL_SCREEN"]))
        self.__cbShowTips.SetValue(secureInt(self.__prefs["SHOW_TIPS_ON_STARTUP"]))
#        self.__txtFontSize.SetValue(self.__prefs["FONT_SIZE"])

        # i18n
        n = self.__prefs["I18N"]
        if n not in lang.LANGUAGES:
            n = lang.DEFAULT_LANG
        self.__cmbLanguage.SetValue(lang.LANGUAGES[n][0])

    #>------------------------------------------------------------------------

    def __OnCheckBox(self, event):
        """
        Callback.

        @since 1.0
        """
        self.__changed = 1
        id = event.GetId()
        val = event.IsChecked()
        if   id == self.__autoResizeID:
            self.__prefs["AUTO_RESIZE"] = val
        elif id == self.__showParamsID:
            self.__ctrl.showParams(val)
            self.__prefs["SHOW_PARAMS"] = val
        elif id == self.__maximizeID:
            self.__prefs["FULL_SCREEN"] = val
        elif id == self.__showTipsID:
            self.__prefs["SHOW_TIPS_ON_STARTUP"] = val

    #>------------------------------------------------------------------------

#    def __OnFontSizeChange(self, event):
#        """
#        Callback.
#
#        @since 1.0
#        """
#        self.__prefs["FONT_SIZE"] = self.__txtFontSize.GetValue()

    #>------------------------------------------------------------------------

    def __OnChoice(self, event):
        """
        Callback.

        @since 1.0
        """
        pass

    #>------------------------------------------------------------------------

    def __OnClose(self, event):
        """
        Callback.

        @since 1.2
        """
        # If language has been changed
        newlanguage = self.__cmbLanguage.GetValue()
        actuallanguage = self.__prefs["I18N"]
        if actuallanguage not in lang.LANGUAGES or \
            newlanguage != lang.LANGUAGES[actuallanguage][0]:
                # Search the key coresponding to the newlanguage
                for i in lang.LANGUAGES.items():
                    if newlanguage == i[1][0]:
                        # Write the key in preferences file
                        self.__prefs["I18N"] = i[0]
                # Dialog must restart Pyut to have the changes
                dlg = wx.MessageDialog(self,
                    _("You must restart application for language changes"),
                    _("Warning"),
                    wx.OK|wx.ICON_EXCLAMATION)
                dlg.ShowModal()
                dlg.Destroy()

        event.Skip()

    #>------------------------------------------------------------------------

    def __OnCmdOk(self, event):
        """
        Callback.

        @since 1.2
        """
        if self.__changed:
            for oglObject in self.__ctrl.getUmlObjects():
                if isinstance(oglObject, OglClass):
                    self.__ctrl.autoResize(oglObject)

        self.Close()

    #>------------------------------------------------------------------------

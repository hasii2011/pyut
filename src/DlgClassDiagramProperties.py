#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__version__ = "$Revision: 1.6 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2002-02-23"

from __future__  import nested_scopes
#from wxPython.wx import *
from pyutUtils   import *
#from PyutPrefs   import *
from PyutPreferences import *
from OglClass    import *
import lang, wx

class DlgClassDiagramProperties(wx.Dialog):
    """
    This is the class diagram properties dialog box

    Display current properties and possible values, save modified values.

    To use it from a wx.Frame :
        dlg = DlgProperties(self, -1, PyutPreferences(), Mediator())
        dlg.ShowModal()
        dlg.Destroy()
    
    :version: $Revision: 1.6 $
    :author: C.Dutoit
    :contact: dutoitc@hotmail.com
    """
    def __init__(self, parent, ID, ctrl):
        """
        Constructor.

        @param wx.Window parent Parent
        @param int ID ID
        @param Mediator ctrl
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        wx.Dialog.__init__(self, parent, ID, _("File properties"))
        self.__ctrl = ctrl
        self.__initCtrl()

        self.Bind(EVT_CLOSE, self.__OnClose)

    #>------------------------------------------------------------------------

    def __initCtrl(self):
        """
        Initialize the controls.

        @since 1.0
        """
        # IDs
        [
            self.__showParamsID, self.__showStereotypeID, self.__showFieldsID,
            self.__showMethodsID] = assignID(4)

        GAP = 5

        sizer = wx.BoxSizer(wx.VERTICAL)

        # Show Params
        self.__cbShowParams = wx.CheckBox(self, self.__showParamsID,
            _("&Show params in classes"))
        self.__cbShowStereotype = wx.CheckBox(self, self.__showStereotypeID,
            _("&Show stereotype in classes"))
        self.__cbShowFields = wx.CheckBox(self, self.__showFieldsID,
            _("&Show fields in classes"))
        self.__cbShowMethods = wx.CheckBox(self, self.__showMethodsID,
            _("&Show methods in classes"))

        # Add params to sizer
        sizer.Add(self.__cbShowParams,     0, wx.ALL, GAP)
        sizer.Add(self.__cbShowStereotype, 0, wx.ALL, GAP)
        sizer.Add(self.__cbShowFields,     0, wx.ALL, GAP)
        sizer.Add(self.__cbShowMethods,    0, wx.ALL, GAP)

        # Add second Vertical sizer
        hs = wx.BoxSizer(wx.HORIZONTAL)
        btnOk = wx.Button(self, wx.ID_OK, _("&OK"))
        hs.Add(btnOk, 0, wx.ALL, GAP)
        sizer.Add(hs, 0, wx.CENTER)

        self.__changed = 0

        # Layout
        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        sizer.Fit(self)
        sizer.SetSizeHints(self)

        # Callbacks
        self.Bind(EVT_CHECKBOX, self.__showParamsID, self.__OnCheckBox)
        self.Bind(EVT_BUTTON, wx.ID_OK, self.__OnCmdOk)

        # Set all values
        self.__setValues()

    #>------------------------------------------------------------------------

    def __setValues(self):
        """
        Set the default values to the controls.

        @since 1.0
        """
        def secureInt(x):
            if x is None:
                return 0
            else:
                return int(x)

    #>------------------------------------------------------------------------

    def __OnCheckBox(self, event):
        """
        Callback.

        @since 1.0
        """
        self.__changed = 1
        id = event.GetId()
        val = event.IsChecked()

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
        event.Skip()

    #>------------------------------------------------------------------------

    def __OnCmdOk(self, event):
        """
        Callback.

        @since 1.2
        """
        #if self.__changed:
        #    for oglObject in self.__ctrl.getUmlObjects():
        #        if isinstance(oglObject, OglClass):
        #            self.__ctrl.autoResize(oglObject)

        self.Close()

    #>------------------------------------------------------------------------

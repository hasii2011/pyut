#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__version__ = "$Revision: 1.7 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2001-11-14"
# C.Dutoit, 20020917, removed OnLoadFile / load file button... (why was it here?)

#from wxPython.wx import *
#from wxPython.html import *
import wx
from pyutUtils import assignID

[ID_LOAD_FILE, ID_BACK, ID_FORWARD, ID_PRINT, ID_VIEW_SOURCE] = assignID(5)

class DlgHelp(wx.Dialog):
    """
    Pyut help dialog frame. Used to show help and navigate through it.

    To use it from a wxFrame :
        dlg = DlgHelp(self, -1, "Pyut Help")
        dlg.Show()
        dlg.destroy()

    :version: $Revision: 1.7 $
    :author: C.Dutoit
    :contact: dutoitc@hotmail.com
    """

    #>------------------------------------------------------------------------

    def __init__(self, parent, ID, title):
        """
        Constructor.

        @since 1.0
        @author C.Dutoit
        """
        import os, wx
        #dialog box
        wx.Dialog.__init__(self, parent, ID, title, wx.DefaultPosition, 
                          wx.Size(720, 520))
        self.Center(wx.BOTH)

        #window
        import wx.html
        self.html = wx.html.HtmlWindow(self, -1, wx.DefaultPosition, wx.Size(720, 520))
        self.html.LoadPage(os.getcwd()+ os.sep + "help" + os.sep + "index.html")

        # Printer
        self.printer=wx.html.HtmlEasyPrinting()

        # Sizer
        self.box = wx.BoxSizer(wx.VERTICAL)
        self.box.Add(self.html, 1, wx.GROW)
        subbox = wx.BoxSizer(wx.HORIZONTAL)

        #buttons
        #btn = wx.Button(self, ID_LOAD_FILE, _("Load file"))
        #EVT_BUTTON(self, ID_LOAD_FILE, self.__OnLoadFile)
        #subbox.Add(btn, 1, wx.GROW | wx.ALL, 2)

        btn = wx.Button(self, ID_BACK, _("Back"))
        self.Bind(wx.EVT_BUTTON, self.__OnBack, id=ID_BACK)
        subbox.Add(btn, 1, wx.GROW | wx.ALL, 2)
        
        btn = wx.Button(self, ID_FORWARD, _("Forward"))
        self.Bind(wx.EVT_BUTTON, self.__OnForward, id=ID_FORWARD)
        subbox.Add(btn, 1, wx.GROW | wx.ALL, 2)

        btn = wx.Button(self, ID_PRINT, _("Print"))
        self.Bind(wx.EVT_BUTTON, self.__OnPrint, id=ID_PRINT)
        subbox.Add(btn, 1, wx.GROW | wx.ALL, 2)

        btn = wx.Button(self, ID_VIEW_SOURCE, _("View Source"))
        self.Bind(wx.EVT_BUTTON, self.__OnViewSource, id=ID_VIEW_SOURCE)
        subbox.Add(btn, 1, wx.GROW | wx.ALL, 2)

        btn = wx.Button(self, wx.ID_OK, _("Exit"))
        subbox.Add(btn, 1, wx.GROW | wx.ALL, 2)

        self.box.Add(subbox, 0, wx.GROW | wx.BOTTOM)
        self.SetSizer(self.box)
        self.SetAutoLayout(True)
        subbox.Fit(self)
        self.box.Fit(self)

        self.OnShowDefault(None)

        self.Show(True)



    #>------------------------------------------------------------------------

    def OnShowDefault(self, event):
        """
        Show default page

        @since 1.1
        @author C.Dutoit
        """
        import os
        name = os.path.join(os.getcwd(), 'help/index.html')
        self.html.LoadPage(name)

    #>------------------------------------------------------------------------

    #def __OnLoadFile(self, event):
        #"""
        #Load a html page
#
        #@since 1.1
        #@author C.Dutoit
        #"""
        #dlg = wx.FileDialog(self, wildcard = '*.htm*', style=wx.OPEN)
        #if dlg.ShowModal()==wx.OK:
            #path = dlg.GetPath()
            #self.html.LoadPage(path)
        #dlg.Destroy()


    #>------------------------------------------------------------------------

    def __OnBack(self, event):
        """
        go one level back; load last page

        @since 1.1
        @author C.Dutoit
        """
        if not self.html.HistoryBack():
            wx.MessageBox(_("No more items in history !"))

    #>------------------------------------------------------------------------

    def __OnForward(self, event):
        """
        go one level forward; load next page

        @since 1.1
        @author C.Dutoit
        """
        if not self.html.HistoryForward():
            wx.MessageBox(_("No more items in history !"))

    #>------------------------------------------------------------------------

    def __OnViewSource(self, event):
        """
        View document source

        @since 1.1
        @author C.Dutoit
        """
        from wx.Python.lib.dialogs import ScrolledMessageDialog
        source = self.html.GetParser().GetSource()
        dlg = wx.ScrolledMessageDialog(self, source, _('HTML Source'))
        dlg.ShowModal()
        dlg.Destroy()


    #>------------------------------------------------------------------------

    def __OnPrint(self, event):
        """
        print the current page

        @since 1.1
        @author C.Dutoit
        """
        self.printer.PrintFile(self.html.GetOpenedPage())



#Dialog box test
if __name__ == "__main__":
    class App(wx.App):
        def OnInit(self):
            frame = wx.Frame(None, -1, "Pyut Help test application")
            self.SetTopWindow(frame)
            self.dlg=DlgHelp(frame,  -1, "Pyut Help")
            return True
    app = App(0)
    app.MainLoop()

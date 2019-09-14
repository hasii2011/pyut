#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.9 $"
__author__ = "C.Dutoit"
__date__ = "2003-02-16"


#from wxPython.wx    import *
import wx
from pyutUtils      import assignID
from PyutPreferences import *
import os

# DEFAULT SIZE
DEFAULT_WIDTH=600
DEFAULT_HEIGHT=100

# Constants
[ID_OK, ID_SET_NEXT_TIP, ID_SET_PREVIOUS_TIP, ID_CHK_SHOW_TIPS] = assignID(4)

# Tips
Tips = [
    _("Welcome in PyUt 1.3 ! You will find some news in this box.\n" +
      "You can activate/desactivate the box display on startup in the " +
      "PyUt preferences dialog box"),
    _("Remember, if you don't submit bugs on http://www.sf.net/projects/pyut, " +
      "we can't correct them. You can also submit features request."),
    _("Since PyUt 1.3, you can split lines in multi-lines.\n" +
      "Select a Line end and press <ins> or <Insert>"),
    _("You can convert a multiline in a spline by pressing <s>"),
    _("You can find more plugins like a MySQL exporter or Design Patterns viewer " +
      "on http://www.sf.net/projects/pyut, section download"),
    _("You can find more tips on PyUt's web site at address http://pyut.sf.net"),
    _("You can submit bugs, features request and support request on " +
      "http://www.sf.net/projects/pyut")
]


##############################################################################

class TipsFrame(wx.Dialog):
    """
    Represents a tips frame, a frame for displaying tips.

    :version: $Revision: 1.9 $
    :author: C.Dutoit
    :contact: dutoitc@hotmail.com
    """
    def __init__(self, parent):
        """
        constructor
        @param wx.Window parent : parent object
        @author C.Dutoit
        """
        # Check
        import sys
        if sys.platform=="win32":
            return None


        # Initialize the dialog box
        wx.Dialog.__init__(self, parent, -1, _("Tips"), 
                          wx.DefaultPosition,
                          wx.Size(DEFAULT_WIDTH, DEFAULT_HEIGHT),
                          style=wx.THICK_FRAME | 
                          wx.SYSTEM_MENU | 
                          wx.CAPTION     | 
                          wx.FRAME_FLOAT_ON_PARENT)
        self.Show()

        # Normalize tips
        import LineSplitter
        ls = LineSplitter.LineSplitter()
        dc = wx.ClientDC(self)
        for i in range(len(Tips)):
            tip = ls.split(Tips[i], dc, DEFAULT_WIDTH*0.8)
            Tips[i]=""
            for line in tip:
                Tips[i]+=line + "\n"
            #tip = ""
            #for line in Tips[i].split("\n"):
                #newLine = ""
                #for word in line.split(" "):
                    #if len(newLine) + len(word) > 59:
                        #tip += newLine + "\n"
                        #newLine = ""
                    #newLine += word + " "
                #tip += newLine
            #Tips[i] = tip

        # Set current tips
        self._prefs = PyutPreferences()
        self._currentTip = self._prefs["CurrentTip"]
        if self._currentTip is None:
            self._currentTip = 0
        else:
            self._currentTip = int(self._currentTip)

        # Add icon
        icon = wx.Icon('img'+os.sep+'tips.bmp',  # Creation the
                      wx.BITMAP_TYPE_BMP)        # application icon
        self.SetIcon(icon)
        self.Center(wx.BOTH)                     # Center on the screen

        # Create controls
        bmp = wx.Bitmap("img" + os.sep + "tips.bmp", wx.BITMAP_TYPE_BMP)
        self._picture = wx.StaticBitmap(self, -1, bmp)
        tip = Tips[self._currentTip]
        self._label = wx.StaticText(self, -1, tip, 
                              size = wx.Size(DEFAULT_WIDTH * 0.8, 
                                            DEFAULT_HEIGHT*0.8),
                              style=wx.ST_NO_AUTORESIZE)
        nextTipButton = wx.Button(self, ID_SET_NEXT_TIP, 
                                 _("&Next tip"))
        previousTipButton = wx.Button(self, ID_SET_PREVIOUS_TIP, 
                                     _("&Previous tip"))
        self._chkShowTips = wx.CheckBox(self, ID_CHK_SHOW_TIPS, 
                                       _("&Show tips at startup"))
        self._chkShowTips.SetValue(not self._prefs["SHOW_TIPS_ON_STARTUP"]=="0")

        # Upper sizer
        upSizer = wx.BoxSizer(wx.HORIZONTAL)
        upSizer.Add(self._picture, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        upSizer.Add(self._label,   1, wx.ALL | wx.ALIGN_CENTER, 5)

        # Lower sizer
        loSizer = wx.BoxSizer(wx.HORIZONTAL)
        loSizer.Add(previousTipButton, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        loSizer.Add(nextTipButton, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        loSizer.Add(wx.Button(self, ID_OK, "&Ok"), 0, wx.ALL | wx.ALIGN_CENTER, 5)

        # Main sizer
        self.SetAutoLayout(True)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(upSizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        mainSizer.Add(self._chkShowTips, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        mainSizer.Add(loSizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        self.SetSizer(mainSizer)
        mainSizer.Fit(self)

        # Events
        self.Bind(wx.EVT_BUTTON, self._onOk, id=ID_OK) 
        self.Bind(wx.EVT_CLOSE, self._onClose)
        self.Bind(wx.EVT_BUTTON, self._onNextTip, id=ID_SET_NEXT_TIP)
        self.Bind(wx.EVT_BUTTON, self._onPreviousTip, id=ID_SET_PREVIOUS_TIP)




    #>------------------------------------------------------------------------

    def _onOk(self, event):
        """
        _onOk : Handle user click on the OK button

        @author C.Dutoit
        """
        # Exit modal mode
        self.Close()
       
    #>------------------------------------------------------------------------

    def _onNextTip(self, event):
        """
        Select and display next tip
        @author C.Dutoit
        """
        self._currentTip = (self._currentTip + 1) % len(Tips)
        self._label.SetLabel(Tips[self._currentTip])

    #>------------------------------------------------------------------------

    def _onPreviousTip(self, event):
        """
        Select and display previous tip
        @author C.Dutoit
        """
        self._currentTip = (self._currentTip - 1) % len(Tips)
        self._label.SetLabel(Tips[self._currentTip])


    #>------------------------------------------------------------------------

    def _onClose(self, event):
        """
        Save state
        @author C.Dutoit
        """
        # Save state
        self._prefs["CurrentTip"] = (self._currentTip + 1) % len(Tips)
        self._prefs["SHOW_TIPS_ON_STARTUP"] = self._chkShowTips.GetValue()
        event.Skip()

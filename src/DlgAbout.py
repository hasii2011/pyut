#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Note : Linux seems not to support SetPointSize on dc... why ?
# Todo : change font;  or find a way to not print each character one after the
#        other (not preatty, with, for eg : WiiW)

__version__ = "$Revision: 1.12 $"
__author__ = "EI6, eivd, Group Dutoit-Roux"
__date__ = "2002-05-25"
#from wxPython.wx import *
import wx
import thread
from pyutUtils import assignID

# Constants
[ID_OK] = assignID(1)
FrameWidth=400          # Canvas width
FrameHeight=300         # and height
x0 = 20                 # Initial x
y0 = 20                 # Initial y
dy=20                   # Y increment

#Text to show. String list.
txtToShow=[
            #"        .S6EEi                                    ",
            #"     6M@     iMM@                                 ",
            #"    Mz   QM    MMl          wQMM     8M           ",
            #"   M     MM    8M         MM 6MM    iMM     M     ",
            #"  M     ,M    BMB :    lB    .Mx    MM   CMMMEW   ",
            #"  M     MMMMMMMCMiMM   MM    MM     MM    BM6.    ",
            #"  M     MB         MM  MW    MM    8Mr    MM      ",
            #"  MMM  MM           M  M    MM     MM     MB      ",
            #"       MM           M.M6    MM  8MMMC  M ,M  Mw   ",
            #"     iMM   .        MMM    MMMMM@ MMMMM  MMMMC    ",
            #"   :MEE@MMMl        MM     CMMl   wMM    zM       ",
            #"                   CM                             ",
            #"                  MM                              ",
            #"             MMMMM                                ",
            "",
            "",
            " About PyUt... or the guys behind the success story...",
            "",
            " Don't forget to visit the Pyut's official web site :",
            "                HTTP://PYUT.SF.NET",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            " PyUt - 1.3 Credits :",
            " ====================",
            " Thierry Gagnebin (professor)",
            "  - Responsible EIVD",
            "",
            "",
            "C.Dutoit (dutoitc@hotmail.com)",
            " - Developer, packager, i18n",
            "",
            "",
            "L.Burgbacher (lb@alawa.ch)",
            " - MiniOgl manager",
            " - Developer",
            "",
            "",
            "P.Waelti (pwaelti@eivd.ch)",
            " - Developer",
            "",
            "",
            "N.Dubois (nicdub@gmx.ch)",
            " - Sugiyama plugin developer",
            "",
            "",
            "J. Frank (private)",
            " - Tester, consultant",
            "",
            "",
            "",
            " Translators",
            " -----------",
            "  - German     : Stefan Drees",
            "  - Danish     : Anders Kastrup J�rgensen",
            "  - French     : C�dric Dutoit",
            "  - Dutch      : GB",
            "  - Portuguese : Fernando Domingues (soon)",
            "  - Spanish    : Alberto Mendez",
            "  - Indonesia  : Bonifatio",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            " PyUt - 1.2 Credits :",
            " ====================",
            " Thierry Gagnebin (professor)",
            "  - Responsible EIVD",
            "",
            "",
            "C.Dutoit (dutoitc@hotmail.com)",
            " - Developer, packager, i18n",
            "",
            "",
            "L.Burgbacher (lb@alawa.ch)",
            " - MiniOgl manager",
            " - Developer",
            "",
            "",
            "P.Waelti (pwaelti@eivd.ch)",
            " - Developer",
            "",
            "",
            "",
            " Translators",
            " -----------",
            "  - German : Stefan Drees"
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            " PyUt 1.1 (March 2002 - July 2002) Credits :",
            " =============================================",
            " Pyut 1.1 was the suite of the group project, ",
            " developed in EIVD, too",
            "",
            " Pyut 1.1 development has taken place ",
            " from March 2002 to July 2002",
            "",
            "",
            "C.Dutoit (dutoitc@hotmail.com)",
            " - Project manager",
            " - Developer",
            "",
            "D.Roux (droux@eivd.ch)",
            " - Co-project manager",
            " - CVS manager",
            " - Configuration manager",
            " - Releases manager",
            " - Developer",
            "",
            "P.Waelti (pwaelti@eivd.ch)",
            " - Documentation manager/writer",
            " - Quality manager",
            " - Developer",
            "",
            "L.Burgbacher (lb@alawa.ch)",
            " - Tests manager",
            " - Developer",
            "",
            "N.Dubois (ndubois@eivd.ch)",
            " - Internationalization",
            " - Developer",
            "",
            "N.Hamadi (nhamadi@eivd.ch)",
            " - Feedback manager",
            " - Developer",
            "",
            "",
            "",
            " Pyut 1.0 (October 2002 - March 2002) has been developing",
            " as group project at EIVD, Yverdon/Switzerland",
            "",
            "PyUt 1.0 Credits :",
            "==================",
            "L.Burgbacher (lb@alawa.ch)",
            " - Project manager",
            " - .exe Packager",
            " - Developer",
            "",
            "P.Waelti (pwaelti@eivd.ch)",
            " - Co-Project manager",
            " - CVS manager",
            " - Developer",
            "",
            "N.Dubois (ndubois@eivd.ch)",
            " - Developer",
            "",
            "C.Dutoit (dutoitc@hotmail.com)",
            " - .rpm/.tar.gz packager",
            " - Developer",
            "",
            "N.Hamadi (nhamadi@eivd.ch)",
            " - Tester",
            " - Developer",
            "",
            "D.Roux (droux@eivd.ch)",
            " - Developer",
            "",
            "",
            "",
            " We would like to thanks",
            "",
            "                     MMMMM                        ",
            "                     MMMMW                        ",
            "",
            "",
            "    .MMMMMMMM:      2BMM  BMBBMMS    MMMX    802SM,",
            "   MMMM    0MMM    MMMMZ  i:MMMMM   7MMMM      MMM ",
            "  MM8M;    :M8MM  iMZBM      M0WM     MMB     ZMM: ",
            " @MZZM7 ;i 2MMMM  MW8M,      M0BM     M8   iMM MMM  ",
            " MWZZ@MaMMM0Sr7Z ,MZWM       @B0M    MM7  MM  MMM   ",
            " M@ZZB8          MB8M:       M0W0M  7MM MMa   MMM   ",
            " SM8Z0M         MM8BM        @W8M,MM   MMM   SMM,   ",
            "  MM0ZMM      SMM8ZW:  M     MWMMM:   MMM   .MMW    ",
            "   ZMMMMMMMMMMM MM@MMMM      MMM;     MMM  MMMMiWM  ",
            "       ;7SSr     :r:         M         ;Z@a  2a;    ",
            "",
            " EIVD : Ecole d'ing�nieurs de l'�tat de Vaud, Yverdon",
            " (http://www.eivd.ch)",
            " to have given us the oportunity to develop PyUt"
           ]


##############################################################################
# Panel update event
#wx.EVT_UPDATE_PANEL = wx.NewEventType()
#
## Panel update event connection with window
#def EVT_UPDATE_PANEL(win, func):
#    win.Connect(-1, -1, wx.EVT_UPDATE_PANEL, func)
#
## Panel update event class
#class UpdatePanelEvent(wx.PyEvent):
#    def __init__(self):
#        wx.PyEvent.__init__(self)
#        self.SetEventType(wx.EVT_UPDATE_PANEL)

##############################################################################
class DlgAbout(wx.Dialog):
    """
    DlgAbout : About box for Pyut.

    Instancied from AppFrame.

    Use it like a normal dialog box ::
        dlg=DlgAbout(self, -1, "")
        dlg.ShowModal()
        dlg.Destroy()

    :author: C.Dutoit
    :contact: <dutoitc@hotmail.com>
    :version: $Revision: 1.12 $
    """

    #>------------------------------------------------------------------------

    def __init__(self, parent, ID, title):
        """
        Constructor.

        @param wxWindow parent : parent window
        @param int ID : wx ID of this frame
        @param String title : Title to display
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        import os
        # Application initialisation
        wx.Dialog.__init__(self, parent, ID, title, wx.DefaultPosition, wx.Size(FrameWidth, FrameHeight))
        icon = wx.Icon('img'+os.sep+'icon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        self.Center(wx.BOTH)

        # Animation panel
        self._panel = wx.Panel(self, -1, size=(FrameWidth, FrameHeight))

        # Picture and text
        import os
        bmp = wx.Bitmap("img" + os.sep + "pyut.bmp", wx.BITMAP_TYPE_BMP)
        self._picture = wx.StaticBitmap(self, -1, bmp)
        self._label = wx.StaticText(self, -1,
                              "2002, The PyUt team.\nPublished under "
                              "the GNU General Public License",
                              style=wx.THICK_FRAME)

        # Main sizer
        self.SetAutoLayout(True)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._picture,                0, wx.ALL | wx.ALIGN_CENTER, 5)
        sizer.Add(self._panel,                  1, wx.ALL | wx.ALIGN_CENTER, 5)
        sizer.Add(self._label,                  0, wx.ALL | wx.ALIGN_CENTER, 5)
        btnOk = wx.Button(self, ID_OK, "&Ok")
        sizer.Add(btnOk, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        self.SetSizer(sizer)
        sizer.Fit(self)

        # Create thread instance
        self._thread = myThread(self._panel, self)


        # Events
        self.Bind(wx.EVT_BUTTON, self._onOk, btnOk)
        self._panel.Bind(wx.EVT_PAINT, self.OnRefreshPanel)
        #TODO self._panel.Bind(wx.EVT_UPDATE_PANEL, self.OnPanelUpdate)
        self.Bind(wx.EVT_CLOSE, self._onOk)



    #>------------------------------------------------------------------------

    def _onOk(self, event):
        """
        _onOk : Handle user click on the OK button

        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        import time
        # Halt task
        self._thread.Stop()
        while self._thread.isRunning():
            time.sleep(0.1)
            wx.Yield()

        # Exit modal mode
        self.EndModal(wx.OK)




    #>------------------------------------------------------------------------

    def ShowModal(self):
        """
        Display this box as modal box

        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._thread.Start()
        wx.Dialog.ShowModal(self)


    #>------------------------------------------------------------------------

    def OnPanelUpdate(self, evt):
        """
        Update panel.

        @since 1.1.2.4
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._panel.Refresh(False)


    #>------------------------------------------------------------------------

    def OnRefreshPanel(self, event):
        """
        Refresh dialog box

        @since 1.1.2.4
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        # constants
        backr = backb = 230     # Background color
        backg = 255
        frontr = frontb = 64    # Foreground color
        frontg = 0
        FADE_IN_LENGTH = 63



        # Init memory buffer
        tdc=wx.MemoryDC()
        tdc.SelectObject(wx.EmptyBitmap(FrameWidth, FrameHeight))
        while not tdc.Ok():
            sleep(0.05)
            tdc=wx.MemoryDC()
            tdc.SelectObject(wx.EmptyBitmap(FrameWidth, FrameHeight))

        # Init drawing
        tdc.BeginDrawing()
        tdc.SetTextForeground(wx.Colour(frontr, frontg, frontb))
        tdc.SetBackground(wx.Brush(wx.Colour(backr, backg, backb), wx.SOLID))
        tdc.Clear()
        font=tdc.GetFont()
        #font.SetFamily(wx.ROMAN)
        font.SetFamily(wx.SWISS)
        font.SetPointSize(12)
        tdc.SetFont(font)

        # Fade-in
        position = self._thread.getPosition()
        if position < FADE_IN_LENGTH:
            n = float(position) / float(FADE_IN_LENGTH)
            r = backr - n * (backr - frontr)
            g = backg - n * (backg - frontg)
            b = backb - n * (backb - frontb)
            r=int(r)
            g=int(g)
            b=int(b)
            tdc.SetTextForeground(wx.Colour(r, g, b))

        # Display text
        for j in range(1,len(txtToShow)):
            # Draw text ?
            if position>FADE_IN_LENGTH:
                y = y0 + j*dy - (position - FADE_IN_LENGTH)
                if y>-dy and y<FrameHeight:
                    tdc.DrawText(txtToShow[j], x0, y)
            else: # Draw initial screen with fade in
                y = y0 + j*dy
                if y>-dy and y<FrameHeight:
                    tdc.DrawText(txtToShow[j], x0, y)


        # end drawing
        tdc.EndDrawing()

        # Show memory dc to current dc (blit)
        dc = wx.PaintDC(self._panel)
        dc.BeginDrawing()
        dc.Blit(0, 0, FrameWidth, FrameHeight, tdc, 0, 0)
        dc.EndDrawing()
        tdc.SelectObject(wx.NullBitmap)





##############################################################################
##############################################################################
class myThread:

    #>------------------------------------------------------------------------
    def __init__(self, win, parent):
        """
        Thread constructor.

        @since 1.1.2.5
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        # Init
        self._win = win
        self._parent = parent
        self._position=0.0            # Current position
        self._keepGoing = self._running = False


    #>------------------------------------------------------------------------
    def getPosition(self):
        """
        Return current position

        @since 1.1.2.5
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        return self._position

    #>------------------------------------------------------------------------

    def Start(self):
        """
        Start the task.

        @since 1.1.2.5
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._keepGoing = self._running = True
        thread.start_new_thread(self.Run, ())


    #>------------------------------------------------------------------------

    def Stop(self):
        """
        Stop the task.

        @since 1.1.2.5
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._keepGoing = False


    #>------------------------------------------------------------------------

    def isRunning(self):
        """
        Test if the task is currently running.

        @since 1.1.2.5
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        return self._running


    #>------------------------------------------------------------------------

    def Run(self):
        """
        main thread, handle text printout

        @since 1.1.2.5
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        import time
        Delay_Unit = 2/100.0   # Delay to wait, in second
        # Note : bug for localisation, so I use 2/100 instead of 0.02 (0,02)
        while self._keepGoing:
            # Change state
            self._position+=1

            # End of text -> re-begin on top
            if self._position > (len(txtToShow)+15) * dy:
                self._position = 0.0



            # Ask for update
            #evt = UpdatePanelEvent()
            #wx.PostEvent(self._win, evt)
            self._parent.OnPanelUpdate(None)

            # Wait
            wx.Yield()
            time.sleep(Delay_Unit)
        self._running = False




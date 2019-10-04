
from logging import Logger
from logging import getLogger

from os import sep as osSep

from pkg_resources import resource_filename

# Todo : change font;  or find a way to not print each character one after the
#        other (not pretty, with, for eg : WiiW)
from wx import ALIGN_CENTER
from wx import ALL
from wx import BITMAP_TYPE_BMP
from wx import BITMAP_TYPE_ICO
from wx import BRUSHSTYLE_SOLID
from wx import BoxSizer
from wx import Brush
from wx import Button
from wx import CAPTION
from wx import BOTH
from wx import Colour
from wx import OK
from wx import VERTICAL
from wx import FONTFAMILY_SWISS

from wx import EVT_BUTTON
from wx import EVT_CLOSE
from wx import EVT_PAINT

from wx import Bitmap
from wx import DefaultPosition
from wx import Dialog
from wx import MemoryDC
from wx import NullBitmap
from wx import PaintDC
from wx import Size
from wx import StaticBitmap
from wx import StaticText
from wx import Icon
from wx import Panel

from wx import Yield as wxYield

import threading

from pyutUtils import assignID
from globals import IMG_PKG

# Constants
[ID_OK] = assignID(1)
FrameWidth  = 400       # Canvas width
FrameHeight = 300       # and height
x0 = 20                 # Initial x
y0 = 20                 # Initial y
dy = 20                 # Y increment

# Text to show. String list.
txtToShow = [
            # "        .S6EEi                                    ",
            # "     6M@     iMM@                                 ",
            # "    Mz   QM    MMl          wQMM     8M           ",
            # "   M     MM    8M         MM 6MM    iMM     M     ",
            # "  M     ,M    BMB :    lB    .Mx    MM   CMMMEW   ",
            # "  M     MMMMMMMCMiMM   MM    MM     MM    BM6.    ",
            # "  M     MB         MM  MW    MM    8Mr    MM      ",
            # "  MMM  MM           M  M    MM     MM     MB      ",
            # "       MM           M.M6    MM  8MMMC  M ,M  Mw   ",
            # "     iMM   .        MMM    MMMMM@ MMMMM  MMMMC    ",
            # "   :MEE@MMMl        MM     CMMl   wMM    zM       ",
            # "                   CM                             ",
            # "                  MM                              ",
            # "             MMMMM                                ",
            "",
            "",
            " About PyUt... or the guys behind the success story...",
            "",
            " Don't forget to visit the Pyut's official web site :",
            "                http://PYUT.SF.NET",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            " PyUt 1.5 Port to Python 3.7 Credits:",
            " ====================",
            " Humberto A. Sanchez II, Consultant, Python Enthusiast",
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


# #############################################################################
# Panel update event
# wx.EVT_UPDATE_PANEL = wx.NewEventType()
#
# # Panel update event connection with window
# def EVT_UPDATE_PANEL(win, func):
#    win.Connect(-1, -1, wx.EVT_UPDATE_PANEL, func)
#
# # Panel update event class
# class UpdatePanelEvent(wx.PyEvent):
#    def __init__(self):
#        wx.PyEvent.__init__(self)
#        self.SetEventType(wx.EVT_UPDATE_PANEL)
# #############################################################################
class DlgAbout(Dialog):
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
    def __init__(self, parent, ID, title):
        """
        Constructor.

        @param  parent : parent window
        @param ID : wx ID of this frame
        @param  title : Title to display
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        super().__init__(parent, ID, title, DefaultPosition, Size(FrameWidth, FrameHeight))

        self.logger: Logger = getLogger(__name__)
        icon = Icon(f'img{osSep}pyut.ico', BITMAP_TYPE_ICO)

        self.SetIcon(icon)
        self.Center(BOTH)

        # Animation panel
        self._panel = Panel(self, -1, size=(FrameWidth, FrameHeight))

        # Picture and text
        # bmp = Bitmap("img" + os.sep + "pyut.bmp", BITMAP_TYPE_BMP)
        fileName = resource_filename(IMG_PKG, 'pyut.bmp')
        bmp = Bitmap(fileName, BITMAP_TYPE_BMP)

        self._picture = StaticBitmap(self, -1, bmp)
        summaryText: str = "2019, The PyUt team and Humberto Sanchez II.\nPublished under the GNU General Public License"
        self._label   = StaticText(self, -1, summaryText, style=CAPTION)

        # Main sizer
        self.SetAutoLayout(True)
        sizer = BoxSizer(VERTICAL)
        sizer.Add(self._picture, 0, ALL | ALIGN_CENTER, 5)
        sizer.Add(self._panel,   1, ALL | ALIGN_CENTER, 5)
        sizer.Add(self._label,   0, ALL | ALIGN_CENTER, 5)

        btnOk = Button(self, ID_OK, "&Ok")
        sizer.Add(btnOk, 0, ALL | ALIGN_CENTER, 5)
        self.SetSizer(sizer)
        sizer.Fit(self)

        # Create thread instance
        self._thread = AboutDialogThread(self._panel, self)

        # Events
        self.Bind(EVT_BUTTON, self._onOk, btnOk)
        self._panel.Bind(EVT_PAINT, self.OnRefreshPanel)
        # TODO self._panel.Bind(wx.EVT_UPDATE_PANEL, self.OnPanelUpdate)
        self.Bind(EVT_CLOSE, self._onOk)

    # noinspection PyUnusedLocal
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
            wxYield()

        # Exit modal mode
        self.EndModal(OK)

    def ShowModal(self):
        """
        Display this box as modal box

        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._thread.Start()
        Dialog.ShowModal(self)

    # noinspection PyUnusedLocal
    def OnPanelUpdate(self, evt):
        """
        Update panel.

        @since 1.1.2.4
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._panel.Refresh(False)

    # noinspection PyUnusedLocal
    def OnRefreshPanel(self, event):
        """
        Refresh dialog box

        @since 1.1.2.4
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        import time
        # constants
        backr = backb = 230     # Background color
        backg = 255
        frontr = frontb = 64    # Foreground color
        frontg = 0
        FADE_IN_LENGTH = 63

        # Init memory buffer
        tdc = MemoryDC()
        tdc.SelectObject(Bitmap(FrameWidth, FrameHeight))
        while not tdc.IsOk():
            time.sleep(0.05)
            tdc = MemoryDC()
            tdc.SelectObject(Bitmap(FrameWidth, FrameHeight))

        # Init drawing
        # tdc.BeginDrawing()
        tdc.SetTextForeground(Colour(frontr, frontg, frontb))
        tdc.SetBackground(Brush(Colour(backr, backg, backb), BRUSHSTYLE_SOLID))
        tdc.Clear()
        font = tdc.GetFont()
        # font.SetFamily(wx.ROMAN)
        font.SetFamily(FONTFAMILY_SWISS)
        font.SetPointSize(12)
        tdc.SetFont(font)

        # Fade-in
        position = self._thread.getPosition()
        if position < FADE_IN_LENGTH:
            n = float(position) / float(FADE_IN_LENGTH)
            r = backr - n * (backr - frontr)
            g = backg - n * (backg - frontg)
            b = backb - n * (backb - frontb)
            r = int(r)
            g = int(g)
            b = int(b)
            tdc.SetTextForeground(Colour(r, g, b))

        # Display text
        for j in range(1, len(txtToShow)):
            # Draw text ?
            if position > FADE_IN_LENGTH:
                y = y0 + j*dy - (position - FADE_IN_LENGTH)
                if -dy < y < FrameHeight:
                    tdc.DrawText(txtToShow[j], x0, y)
            else:   # Draw initial screen with fade in
                y = y0 + j*dy
                if -dy < y < FrameHeight:
                    tdc.DrawText(txtToShow[j], x0, y)

        # end drawing
        # tdc.EndDrawing()

        # Show memory dc to current dc (blit)
        dc = PaintDC(self._panel)
        # dc.BeginDrawing()
        dc.Blit(0, 0, FrameWidth, FrameHeight, tdc, 0, 0)
        # dc.EndDrawing()
        tdc.SelectObject(NullBitmap)


class AboutDialogThread:

    def __init__(self, win, parent):
        """
        Thread constructor.

        @since 1.1.2.5
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        # Init
        self.logger: Logger = getLogger('AboutDialogThread')
        self._win = win
        self._parent = parent
        self._position = 0.0            # Current position
        self._keepGoing = self._running = False

    def getPosition(self):
        """
        Return current position

        @since 1.1.2.5
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        return self._position

    def Start(self):
        """
        Start the task.

        @since 1.1.2.5
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._keepGoing = self._running = True
        # thread.start_new_thread(self.Run, ())
        self.logger.info("Start a new thread")
        x = threading.Thread(target=self.Run, args=())
        x.start()

    def Stop(self):
        """
        Stop the task.

        @since 1.1.2.5
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._keepGoing = False

    def isRunning(self):
        """
        Test if the task is currently running.

        @since 1.1.2.5
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        return self._running

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
            self._position += 1

            # End of text -> re-begin on top
            if self._position > (len(txtToShow)+15) * dy:
                self._position = 0.0
            # Ask for update
            # evt = UpdatePanelEvent()
            # wx.PostEvent(self._win, evt)
            self._parent.OnPanelUpdate(None)
            # Wait
            wxYield()
            time.sleep(Delay_Unit)
        self._running = False

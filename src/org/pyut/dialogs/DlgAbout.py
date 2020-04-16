
from typing import List

from logging import Logger
from logging import getLogger

from pkg_resources import resource_filename

# Todo : change font;  or find a way to not print each character one after the other (not pretty, with, for eg : WiiW)
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
from wx import FONTFAMILY_MODERN
from wx import OK
from wx import VERTICAL


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

from org.pyut.PyutUtils import PyutUtils

from org.pyut.enums.ResourceTextType import ResourceTextType

from org.pyut.general.Globals import IMG_PKG

# Constants
[ID_OK] = PyutUtils.assignID(1)

FrameWidth  = 400       # Canvas width
FrameHeight = 300       # and height
x0 = 20                 # Initial x
y0 = 20                 # Initial y
dy = 20                 # Y increment


class DlgAbout(Dialog):
    """
    DlgAbout : About box for Pyut.

    Instancied from AppFrame.

    Use it like a normal dialog box ::
        dlg=DlgAbout(self, -1, "")
        dlg.ShowModal()
        dlg.Destroy()
    """
    def __init__(self, parent, ID, title):
        """
        Constructor.

        @param  parent : parent window
        @param ID : wx ID of this frame
        @param  title : Title to display
        """
        super().__init__(parent, ID, title, DefaultPosition, Size(FrameWidth, FrameHeight))

        self.logger:  Logger = getLogger(__name__)
        iconFileName: str    = resource_filename(IMG_PKG, 'pyut.ico')
        icon:         Icon   = Icon(iconFileName, BITMAP_TYPE_ICO)

        self.SetIcon(icon)
        self.Center(BOTH)

        longTextStr:      str       = PyutUtils.retrieveResourceText(ResourceTextType.KUDOS_TEXT_TYPE)
        self._textToShow: List[str] = longTextStr.split('\n')
        # Animation panel
        self._panel = Panel(self, -1, size=(FrameWidth, FrameHeight))

        # Picture and text
        # bmp = Bitmap("img" + os.sep + "pyut.bmp", BITMAP_TYPE_BMP)
        fileName = resource_filename(IMG_PKG, 'pyut.bmp')
        bmp = Bitmap(fileName, BITMAP_TYPE_BMP)

        self._picture = StaticBitmap(self, -1, bmp)
        summaryText: str = "2020 The PyUt team and Humberto Sanchez II.\nPublished under the GNU General Public License"
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
        self._thread = AboutDialogThread(self._panel, self, self._textToShow)

        # Events
        self.Bind(EVT_BUTTON, self._onOk, btnOk)
        self._panel.Bind(EVT_PAINT, self.OnRefreshPanel)
        # TODO self._panel.Bind(wx.EVT_UPDATE_PANEL, self.OnPanelUpdate)
        self.Bind(EVT_CLOSE, self._onOk)

    # noinspection PyUnusedLocal
    def _onOk(self, event):
        """
        _onOk : Handle user click on the OK button

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

        """
        self._thread.Start()
        Dialog.ShowModal(self)

    # noinspection PyUnusedLocal
    def OnPanelUpdate(self, evt):
        """
        Update panel.
        """
        self._panel.Refresh(False)

    # noinspection PyUnusedLocal
    def OnRefreshPanel(self, event):
        """
        Refresh dialog box

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

        tdc.SetTextForeground(Colour(frontr, frontg, frontb))
        tdc.SetBackground(Brush(Colour(backr, backg, backb), BRUSHSTYLE_SOLID))
        tdc.Clear()
        font = tdc.GetFont()
        font.SetFamily(FONTFAMILY_MODERN)
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
        for j in range(1, len(self._textToShow)):
            # Draw text ?
            if position > FADE_IN_LENGTH:
                y = y0 + j*dy - (position - FADE_IN_LENGTH)
                if -dy < y < FrameHeight:
                    tdc.DrawText(self._textToShow[j], x0, y)
            else:   # Draw initial screen with fade in
                y = y0 + j*dy
                if -dy < y < FrameHeight:
                    tdc.DrawText(self._textToShow[j], x0, y)

        # end drawing
        # tdc.EndDrawing()

        # Show memory dc to current dc (blit)
        dc = PaintDC(self._panel)
        # dc.BeginDrawing()
        dc.Blit(0, 0, FrameWidth, FrameHeight, tdc, 0, 0)
        # dc.EndDrawing()
        tdc.SelectObject(NullBitmap)


class AboutDialogThread:

    def __init__(self, win, parent, textToShow: List[str]):
        """
        Thread constructor.

        """
        # Init
        self.logger: Logger = getLogger('AboutDialogThread')

        self._textToShow: List[str] = textToShow

        self._win       = win
        self._parent    = parent
        self._position  = 0.0            # Current position
        self._keepGoing = self._running = False

    def getPosition(self):
        """
        Return current position

        """
        return self._position

    def Start(self):
        """
        Start the task.
        """
        self._keepGoing = self._running = True
        # thread.start_new_thread(self.Run, ())
        self.logger.info("Start a new thread")
        x = threading.Thread(target=self.Run, args=())
        x.start()

    def Stop(self):
        """
        Stop the task.
        """
        self._keepGoing = False

    def isRunning(self):
        """
        Test if the task is currently running.
        """
        return self._running

    def Run(self):
        """
        main thread, handle text printout
        """
        import time
        Delay_Unit = 2/100.0   # Delay to wait, in second
        # Note : bug for localisation, so I use 2/100 instead of 0.02 (0,02)
        while self._keepGoing:
            # Change state
            self._position += 1

            # End of text -> restart at top
            if self._position > (len(self._textToShow) + 15) * dy:
                self._position = 0.0
            # Ask for update
            # evt = UpdatePanelEvent()
            # wx.PostEvent(self._win, evt)
            self._parent.OnPanelUpdate(None)
            # Wait
            wxYield()
            time.sleep(Delay_Unit)
        self._running = False

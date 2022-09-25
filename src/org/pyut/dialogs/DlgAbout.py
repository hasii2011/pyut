
from typing import List

from logging import Logger
from logging import getLogger

from sys import platform as sysPlatform

from wx import ALIGN_CENTER
from wx import ALL

from wx import BITMAP_TYPE_ICO
from wx import BRUSHSTYLE_SOLID
from wx import CAPTION
from wx import BOTH
from wx import ColourDatabase
from wx import EVT_TIMER
from wx import FONTFAMILY_TELETYPE
from wx import ID_ANY
from wx import OK
from wx import VERTICAL
from wx import EVT_BUTTON
from wx import EVT_CLOSE
from wx import EVT_PAINT

from wx import Bitmap
from wx import BoxSizer
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
from wx import Brush
from wx import Button
from wx import Colour
from wx import Window
from wx import Timer
from wx import TimerEvent

from wx import Yield as wxYield

from org.pyut.PyutConstants import PyutConstants
from org.pyut.PyutUtils import PyutUtils

from org.pyut.enums.ResourceTextType import ResourceTextType

from org.pyut.general.Globals import IMAGE_RESOURCES_PACKAGE

from org.pyut.resources.img import ImgPyut

[ID_OK] = PyutUtils.assignID(1)

FrameWidth:  int = 425       # Canvas width
FrameHeight: int = 300       # and height

FADE_IN_LENGTH: int = 63

x0: int = 20                 # Initial x
y0: int = 20                 # Initial y
dy: int = 20                 # Y increment


class DlgAbout(Dialog):

    TIMER_UPDATE_MSECS: int = 20
    """
    DlgAbout : About box for Pyut.

    Use it like a normal dialog box
        dlg=DlgAbout(self, -1, "")
        dlg.ShowModal()
        dlg.Destroy()
    """
    def __init__(self, parent: Window, wxID: int, title: str):
        """

        Args:
            parent:     parent window
            wxID:        wx ID of this frame
            title:      Title to display
        """
        super().__init__(parent, wxID, title, DefaultPosition, Size(FrameWidth, FrameHeight))

        self.logger:  Logger = getLogger(__name__)

        if sysPlatform != PyutConstants.THE_GREAT_MAC_PLATFORM:

            fileName: str  = PyutUtils.getResourcePath(packageName=IMAGE_RESOURCES_PACKAGE, fileName='pyut.ico')
            icon:     Icon = Icon(fileName, BITMAP_TYPE_ICO)
            self.SetIcon(icon)

        self.Center(BOTH)

        longTextStr:      str       = PyutUtils.retrieveResourceText(ResourceTextType.KUDOS_TEXT_TYPE)
        self._textToShow: List[str] = longTextStr.split('\n')

        bgWhite: Colour = ColourDatabase().Find('White')
        self.SetBackgroundColour(bgWhite)
        # Animation panel
        self._panel: Panel = Panel(self, ID_ANY, size=(FrameWidth, FrameHeight))

        self._picture: StaticBitmap = StaticBitmap(self, ID_ANY, ImgPyut.embeddedImage.GetBitmap())
        summaryText:   str = "2022 Humberto Sanchez II and the PyUt team.\nGNU AFFERO GENERAL PUBLIC LICENSE"
        self._label:   StaticText   = StaticText(self, ID_ANY, summaryText, style=CAPTION)

        # Main sizer
        self.SetAutoLayout(True)
        sizer = BoxSizer(VERTICAL)
        sizer.Add(self._picture, 0, ALL | ALIGN_CENTER, 5)
        sizer.Add(self._panel,   1, ALL | ALIGN_CENTER, 5)
        sizer.Add(self._label,   0, ALL | ALIGN_CENTER, 5)

        btnOk: Button = Button(self, ID_OK, "&Ok")
        sizer.Add(btnOk, 0, ALL | ALIGN_CENTER, 5)
        self.SetSizer(sizer)
        sizer.Fit(self)

        self._textPosition: int = 0            # Current position

        self._timer: Timer = Timer(self)
        self.Bind(EVT_TIMER, self._onTimer, self._timer)

        self.Bind(EVT_BUTTON, self._onOk, btnOk)
        self._panel.Bind(EVT_PAINT, self.OnRefreshPanel)
        self.Bind(EVT_CLOSE, self._onOk)

    @property
    def textPosition(self) -> int:
        return self._textPosition

    @textPosition.setter
    def textPosition(self, newValue: int):
        self._textPosition = newValue

    # noinspection PyUnusedLocal
    def _onOk(self, event):
        """
        _onOk : Handle user click on the OK button

        """
        self._timer.Stop()
        # import time
        # Halt task
        # self._thread.Stop()
        # while self._thread.isRunning():
        #     time.sleep(0.1)
        #     wxYield()

        # Exit modal mode
        self.EndModal(OK)

    # noinspection PyUnusedLocal
    def _onTimer(self, event: TimerEvent):

        self.textPosition += 1

        # End of text -> restart at top
        if self.textPosition > (len(self._textToShow) + 15) * dy:
            self.textPosition = 0

        self.OnPanelUpdate(None)

        wxYield()

    def ShowModal(self):
        """
        Display this box as modal box

        """
        self._timer.Start(DlgAbout.TIMER_UPDATE_MSECS)

        super().ShowModal()

    # noinspection PyUnusedLocal
    def OnPanelUpdate(self, evt):
        """
        Update panel.
        """
        self.logger.debug('OnPanelUpdate')

        self._panel.Refresh(eraseBackground=False)

    # noinspection PyUnusedLocal
    def OnRefreshPanel(self, event):
        """
        Refresh dialog box

        """
        import time

        backRed:   int = 240
        backGreen: int = 248
        backBlue:  int = 255    # Background color  -- alice blue 240,248,255)

        frontRed:   int = 105
        frontGreen: int = 105
        frontBlue:  int = 105   # Foreground color  -- dim grey

        self.logger.debug(f'Enter OnRefreshPanel')
        # Init memory buffer
        tdc: MemoryDC = MemoryDC()
        tdc.SelectObject(Bitmap(FrameWidth, FrameHeight))
        while not tdc.IsOk():
            time.sleep(0.05)
            tdc = MemoryDC()
            tdc.SelectObject(Bitmap(FrameWidth, FrameHeight))

        tdc.SetTextForeground(Colour(frontRed, frontGreen, frontBlue))
        tdc.SetBackground(Brush(Colour(backRed, backGreen, backBlue), BRUSHSTYLE_SOLID))
        tdc.Clear()
        font = tdc.GetFont()
        font.SetFamily(FONTFAMILY_TELETYPE)
        font.SetPointSize(12)
        tdc.SetFont(font)

        # Fade-in
        position: int = self.textPosition
        if position < FADE_IN_LENGTH:
            n = position // FADE_IN_LENGTH
            r = backRed - n * (backRed - frontRed)
            g = backGreen - n * (backGreen - frontGreen)
            b = backBlue - n * (backBlue - frontBlue)
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

        # Show memory dc to current dc (blit)
        dc = PaintDC(self._panel)
        dc.Blit(0, 0, FrameWidth, FrameHeight, tdc, 0, 0)
        tdc.SelectObject(NullBitmap)
        self.logger.debug(f'Exit OnRefreshPanel')


from typing import List

from os import linesep as osLineSep

from wx import ALIGN_CENTER
from wx import ALL
from wx import Bitmap
from wx import BoxSizer
from wx import Button
from wx import CAPTION
from wx import CheckBox
from wx import ClientDC

from wx import CloseEvent
from wx import CommandEvent
from wx import DefaultPosition
from wx import Dialog
from wx import EVT_BUTTON
from wx import EVT_CLOSE
from wx import FRAME_FLOAT_ON_PARENT
from wx import HORIZONTAL
from wx import ID_ANY

from wx import RESIZE_BORDER
from wx import ST_NO_AUTORESIZE
from wx import SYSTEM_MENU
from wx import STAY_ON_TOP

from wx import Size
from wx import StaticBitmap
from wx import StaticText
from wx import VERTICAL

from org.pyut.PyutUtils import PyutUtils

from org.pyut.general.Globals import WX_SIZER_CHANGEABLE
from org.pyut.general.Globals import WX_SIZER_NOT_CHANGEABLE
from org.pyut.general.LineSplitter import LineSplitter

from org.pyut.dialogs.tips.TipHandler import TipHandler

from org.pyut.preferences.PyutPreferences import PyutPreferences

from pyut.resources.img.ImgTipsFrameTipsLogo import embeddedImage as TipsLogo

from org.pyut.general.Globals import _

# DEFAULT SIZE
DEFAULT_WIDTH  = 600
DEFAULT_HEIGHT = 100

# Constants
[ID_OK, ID_SET_NEXT_TIP, ID_SET_PREVIOUS_TIP, ID_CHK_SHOW_TIPS] = PyutUtils.assignID(4)


class DlgTips(Dialog):

    TIPS_FILENAME: str = 'tips.txt'
    """
    Represents a tips dialog for displaying Pyut features.
    """
    def __init__(self, parent):
        """
        """
        dialogStyle: int  = RESIZE_BORDER | SYSTEM_MENU | CAPTION | FRAME_FLOAT_ON_PARENT | STAY_ON_TOP
        dialogSize:  Size = Size(DEFAULT_WIDTH, DEFAULT_HEIGHT)
        super().__init__(parent, ID_ANY, _("Tips"), DefaultPosition, dialogSize, dialogStyle)

        self._prefs:        PyutPreferences = PyutPreferences()
        self._tipsFileName: str = PyutUtils.retrieveResourcePath(f'{DlgTips.TIPS_FILENAME}')

        self._tipHandler = TipHandler(fqFileName=self._tipsFileName)

        upSizer: BoxSizer = self._buildUpperDialog(self._tipHandler.getCurrentTipText())
        loSizer: BoxSizer = self._buildLowerDialog()

        self.SetAutoLayout(True)

        mainSizer: BoxSizer = BoxSizer(VERTICAL)

        mainSizer.Add(upSizer,           WX_SIZER_NOT_CHANGEABLE, ALL | ALIGN_CENTER, 5)
        mainSizer.Add(self._chkShowTips, WX_SIZER_NOT_CHANGEABLE, ALL | ALIGN_CENTER, 5)
        mainSizer.Add(loSizer,           WX_SIZER_NOT_CHANGEABLE, ALL | ALIGN_CENTER, 5)

        mainSizer.Fit(self)

        self.Center(dir=VERTICAL)
        self.AcceptsFocus()
        self.SetSizer(mainSizer)

        self._bindEventHandlers()

    def _buildUpperDialog(self, tip: str) -> BoxSizer:

        bmp: Bitmap = TipsLogo.GetBitmap()
        self._picture: StaticBitmap = StaticBitmap(self, ID_ANY, bmp)
        self._label:   StaticText   = StaticText(self, ID_ANY, tip, size=Size(DEFAULT_WIDTH * 0.8, DEFAULT_HEIGHT * 0.8), style=ST_NO_AUTORESIZE)

        upSizer: BoxSizer = BoxSizer(HORIZONTAL)
        upSizer.Add(self._picture, WX_SIZER_NOT_CHANGEABLE, ALL | ALIGN_CENTER, 5)
        upSizer.Add(self._label,   WX_SIZER_CHANGEABLE,     ALL | ALIGN_CENTER, 5)

        return upSizer

    def _buildLowerDialog(self) -> BoxSizer:

        nextTipButton:     Button = Button(self, ID_SET_NEXT_TIP, _("&Next tip"))
        previousTipButton: Button = Button(self, ID_SET_PREVIOUS_TIP, _("&Previous tip"))

        loSizer: BoxSizer = BoxSizer(HORIZONTAL)

        loSizer.Add(previousTipButton, WX_SIZER_NOT_CHANGEABLE, ALL | ALIGN_CENTER, 5)
        loSizer.Add(nextTipButton,     WX_SIZER_NOT_CHANGEABLE, ALL | ALIGN_CENTER, 5)
        loSizer.Add(Button(self, ID_OK, "&Ok"), 0, ALL | ALIGN_CENTER, 5)

        self._chkShowTips: CheckBox = CheckBox(self, ID_CHK_SHOW_TIPS, _("&Show tips at startup"))

        showTips: bool = self._prefs.showTipsOnStartup
        self._chkShowTips.SetValue(showTips)

        return loSizer

    def _bindEventHandlers(self):

        self.Bind(EVT_BUTTON, self._onOk, id=ID_OK)
        self.Bind(EVT_CLOSE,  self._onClose)
        self.Bind(EVT_BUTTON, self._onNextTip,     id=ID_SET_NEXT_TIP)
        self.Bind(EVT_BUTTON, self._onPreviousTip, id=ID_SET_PREVIOUS_TIP)

    # noinspection PyUnusedLocal
    def _onOk(self, event: CommandEvent):
        """
        _onOk : Handle user click on the OK button
        """
        # Exit modal mode
        self.Close()

    # noinspection PyUnusedLocal
    def _onNextTip(self, event: CommandEvent):
        """
        Select and display next tip
        """
        self._tipHandler.incrementTipNumber(1)
        self._label.SetLabel(self._getTipText())

    # noinspection PyUnusedLocal
    def _onPreviousTip(self, event: CommandEvent):
        """
        Select and display previous tip
        """
        self._tipHandler.incrementTipNumber(-1)
        self._label.SetLabel(self._getTipText())

    def _onClose(self, event: CloseEvent):
        """
        Save state
        """
        self._prefs.currentTip  = self._tipHandler.currentTipNumber
        self._prefs.showTipsOnStartup = self._chkShowTips.GetValue()
        event.Skip()
        self.Destroy()

    def _getTipText(self) -> str:

        longText: str = self._tipHandler.getCurrentTipText()

        return self.__normalizeTip(longText)

    def __normalizeTip(self, tip: str) -> str:

        dc:    ClientDC     = ClientDC(self)
        ls:    LineSplitter = LineSplitter()
        lines: List[str]    = ls.split(text=tip, dc=dc, textWidth=int(DEFAULT_WIDTH * 0.8))

        splitTip: str = ''
        for line in lines:
            splitTip = f'{splitTip}{line}{osLineSep}'

        return splitTip

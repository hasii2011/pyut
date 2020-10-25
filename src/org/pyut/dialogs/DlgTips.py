
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

from org.pyut.preferences.PyutPreferences import PyutPreferences

from org.pyut.resources.img.ImgTipsFrameTipsLogo import embeddedImage as TipsLogo

from org.pyut.general.Globals import _

# DEFAULT SIZE
DEFAULT_WIDTH  = 600
DEFAULT_HEIGHT = 100

# Constants
[ID_OK, ID_SET_NEXT_TIP, ID_SET_PREVIOUS_TIP, ID_CHK_SHOW_TIPS] = PyutUtils.assignID(4)

# Tips
Tips = [
    _("Welcome in PyUt 6.x ! You will find some news in this box.\n" +
      "You can activate/deactivate the box display on startup in the " +
      "PyUt preferences dialog"),
    _("Remember, if you do not submit bugs at https://github.com/hasii2011/PyUt/issues, " +
      "we can not correct them. You can also submit feature requests."),
    _("Since PyUt 1.3, you can split lines in multi-lines.\n" +
      "Select a Line end and press <ins> or <Insert>"),
    _("You can convert a multiline in a spline by pressing <s>"),
    _("You can find more plugins like a MySQL exporter or Design Patterns viewer " +
      "at https://github.com/hasii2011/PyUt/wiki, section download"),
    _("You can find more tips on the PyUt wiki: https://github.com/hasii2011/PyUt/wiki"),
    _("You can submit bugs, feature requests and support requests at " +
      "https://github.com/hasii2011/PyUt/issues")
]


class DlgTips(Dialog):
    """
    Represents a tips dialog for displaying Pyut features.
    """
    def __init__(self, parent):
        """
        """
        dialogStyle: int  = RESIZE_BORDER | SYSTEM_MENU | CAPTION | FRAME_FLOAT_ON_PARENT | STAY_ON_TOP
        dialogSize:  Size = Size(DEFAULT_WIDTH, DEFAULT_HEIGHT)
        super().__init__(parent, ID_ANY, _("Tips"), DefaultPosition, dialogSize, dialogStyle)

        self._prefs: PyutPreferences = PyutPreferences()

        self._normalizeTips()
        self._safelyRetrieveCurrentTip()

        upSizer: BoxSizer = self._buildUpperDialog(Tips[self._currentTip])
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

    def _normalizeTips(self):

        from org.pyut.general.LineSplitter import LineSplitter
        ls = LineSplitter()
        dc = ClientDC(self)

        for i in range(len(Tips)):
            tip = ls.split(Tips[i], dc, int(DEFAULT_WIDTH * 0.8))
            Tips[i] = ""
            for line in tip:
                Tips[i] += line + "\n"

    def _safelyRetrieveCurrentTip(self):

        self._currentTip: int = self._prefs.currentTip
        if self._currentTip is None:
            self._currentTip = 0
        else:
            self._currentTip = self._currentTip

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
        self._currentTip = (self._currentTip + 1) % len(Tips)
        self._label.SetLabel(Tips[self._currentTip])

    # noinspection PyUnusedLocal
    def _onPreviousTip(self, event: CommandEvent):
        """
        Select and display previous tip

        """
        self._currentTip = (self._currentTip - 1) % len(Tips)
        self._label.SetLabel(Tips[self._currentTip])

    def _onClose(self, event: CloseEvent):
        """
        Save state
        """
        rationalTipNumber: int = (self._currentTip + 1) % len(Tips)

        self._prefs.currentTip  = rationalTipNumber
        self._prefs.showTipsOnStartup = self._chkShowTips.GetValue()
        event.Skip()

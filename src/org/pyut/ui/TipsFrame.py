
from wx import ALIGN_CENTER
from wx import ALL
from wx import Bitmap
from wx import BoxSizer
from wx import Button
from wx import CAPTION
from wx import CheckBox
from wx import ClientDC
from wx import DefaultPosition
from wx import Dialog
from wx import EVT_BUTTON
from wx import EVT_CLOSE
from wx import FRAME_FLOAT_ON_PARENT
from wx import HORIZONTAL

from wx import RESIZE_BORDER
from wx import ST_NO_AUTORESIZE
from wx import SYSTEM_MENU
from wx import STAY_ON_TOP

from wx import Size
from wx import StaticBitmap
from wx import StaticText
from wx import VERTICAL

from org.pyut.PyutUtils import PyutUtils
from org.pyut.PyutPreferences import PyutPreferences

from org.pyut.resources.img.ImgTipsFrameTipsLogo import embeddedImage as TipsLogo

from org.pyut.general.Globals import _

# DEFAULT SIZE
DEFAULT_WIDTH  = 600
DEFAULT_HEIGHT = 100

# Constants
[ID_OK, ID_SET_NEXT_TIP, ID_SET_PREVIOUS_TIP, ID_CHK_SHOW_TIPS] = PyutUtils.assignID(4)

# Tips
Tips = [
    _("Welcome in PyUt 1.4 ! You will find some news in this box.\n" +
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


class TipsFrame(Dialog):
    """
    Represents a tips frame, a frame for displaying tips.

    :version: $Revision: 1.9 $
    :author: C.Dutoit
    :contact: dutoitc@hotmail.com
    """
    def __init__(self, parent):
        """
        """
        # Check
        import sys
        if sys.platform == "win32":
            return

        # Initialize the dialog box
        super().__init__(parent, -1, _("Tips"), DefaultPosition, Size(DEFAULT_WIDTH, DEFAULT_HEIGHT),
                         RESIZE_BORDER | SYSTEM_MENU | CAPTION | FRAME_FLOAT_ON_PARENT | STAY_ON_TOP)

        # Normalize tips
        from org.pyut.general.LineSplitter import LineSplitter
        ls = LineSplitter()
        dc = ClientDC(self)
        for i in range(len(Tips)):
            tip = ls.split(Tips[i], dc, int(DEFAULT_WIDTH * 0.8))
            Tips[i] = ""
            for line in tip:
                Tips[i] += line + "\n"
            # tip = ""
            # for line in Tips[i].split("\n"):
                # newLine = ""
                # for word in line.split(" "):
                    # if len(newLine) + len(word) > 59:
                        # tip += newLine + "\n"
                        # newLine = ""
                    # newLine += word + " "
                # tip += newLine
            # Tips[i] = tip

        # Set current tips
        self._prefs = PyutPreferences()
        self._currentTip = self._prefs[PyutPreferences.CURRENT_TIP]
        if self._currentTip is None:
            self._currentTip = 0
        else:
            self._currentTip = int(self._currentTip)

        # Add icon
        # fileName = resource_filename(IMG_PKG, 'TipsLogo.bmp')
        # icon = Icon(fileName, BITMAP_TYPE_BMP)
        # self.SetIcon(icon)
        # self.Center(BOTH)                     # Center on the screen
        self.Center(dir=VERTICAL)
        self.AcceptsFocus()
        # Create controls
        # bmp: Bitmap = org.pyut.resources.img.ImgTipsFrameTipsLogo.embeddedImage.GetBitmap()
        bmp: Bitmap = TipsLogo.GetBitmap()
        self._picture = StaticBitmap(self, -1, bmp)
        tip = Tips[self._currentTip]
        self._label = StaticText(self, -1, tip, size=Size(DEFAULT_WIDTH * 0.8, DEFAULT_HEIGHT * 0.8), style=ST_NO_AUTORESIZE)

        nextTipButton = Button(self, ID_SET_NEXT_TIP, _("&Next tip"))
        previousTipButton = Button(self, ID_SET_PREVIOUS_TIP, _("&Previous tip"))
        self._chkShowTips = CheckBox(self, ID_CHK_SHOW_TIPS, _("&Show tips at startup"))
        showTips: bool = self._prefs.showTipsOnStartup()
        self._chkShowTips.SetValue(showTips)

        # Upper sizer
        upSizer = BoxSizer(HORIZONTAL)
        upSizer.Add(self._picture, 0, ALL | ALIGN_CENTER, 5)
        upSizer.Add(self._label,   1, ALL | ALIGN_CENTER, 5)

        # Lower sizer
        loSizer = BoxSizer(HORIZONTAL)
        loSizer.Add(previousTipButton, 0, ALL | ALIGN_CENTER, 5)
        loSizer.Add(nextTipButton,     0, ALL | ALIGN_CENTER, 5)
        loSizer.Add(Button(self, ID_OK, "&Ok"), 0, ALL | ALIGN_CENTER, 5)

        # Main sizer
        self.SetAutoLayout(True)
        mainSizer = BoxSizer(VERTICAL)
        mainSizer.Add(upSizer, 0, ALL | ALIGN_CENTER, 5)
        mainSizer.Add(self._chkShowTips, 0, ALL | ALIGN_CENTER, 5)
        mainSizer.Add(loSizer, 0, ALL | ALIGN_CENTER, 5)
        self.SetSizer(mainSizer)
        mainSizer.Fit(self)

        # Events
        self.Bind(EVT_BUTTON, self._onOk, id=ID_OK)
        self.Bind(EVT_CLOSE,  self._onClose)
        self.Bind(EVT_BUTTON, self._onNextTip,     id=ID_SET_NEXT_TIP)
        self.Bind(EVT_BUTTON, self._onPreviousTip, id=ID_SET_PREVIOUS_TIP)

    # noinspection PyUnusedLocal
    def _onOk(self, event):
        """
        _onOk : Handle user click on the OK button

        @author C.Dutoit
        """
        # Exit modal mode
        self.Close()

    # noinspection PyUnusedLocal
    def _onNextTip(self, event):
        """
        Select and display next tip
        @author C.Dutoit
        """
        self._currentTip = (self._currentTip + 1) % len(Tips)
        self._label.SetLabel(Tips[self._currentTip])

    # noinspection PyUnusedLocal
    def _onPreviousTip(self, event):
        """
        Select and display previous tip
        @author C.Dutoit
        """
        self._currentTip = (self._currentTip - 1) % len(Tips)
        self._label.SetLabel(Tips[self._currentTip])

    def _onClose(self, event):
        """
        Save state
        """
        # Save state
        rationalTipNumber: int = (self._currentTip + 1) % len(Tips)
        currentTipNumber:  str = f'{str(rationalTipNumber)}'
        self._prefs[PyutPreferences.CURRENT_TIP] = currentTipNumber
        self._prefs[PyutPreferences.SHOW_TIPS_ON_STARTUP] = self._chkShowTips.GetValue()
        event.Skip()


from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from os import linesep as osLineSep

from wx import ALIGN_LEFT
from wx import Bitmap
from wx import Button
from wx import CANCEL
from wx import CAPTION
from wx import CheckBox
from wx import ClientDC
from wx import CloseEvent
from wx import CommandEvent
from wx import DEFAULT_DIALOG_STYLE
from wx import EVT_BUTTON
from wx import EVT_CLOSE
from wx import ID_ANY
from wx import ID_OK
from wx import OK
from wx import RESIZE_BORDER
from wx import STAY_ON_TOP
from wx import Size

from wx import StaticBitmap
from wx import StaticText
from wx import Window

from wx.lib.sized_controls import SizedDialog
from wx.lib.sized_controls import SizedPanel

from pyut.PyutConstants import PyutConstants

from pyut.PyutUtils import PyutUtils

from pyut.general.LineSplitter import LineSplitter

from pyut.preferences.PyutPreferences import PyutPreferences

from pyut.resources.img.ImgTipsFrameTipsLogo import embeddedImage as TipsLogo

from pyut.ui.dialogs.tips.TipHandler import TipHandler


# DEFAULT SIZE
DEFAULT_WIDTH  = 600
DEFAULT_HEIGHT = 100

# Constants
[ID_SET_NEXT_TIP, ID_SET_PREVIOUS_TIP, ID_CHK_SHOW_TIPS] = PyutUtils.assignID(3)


class DlgTipsV2(SizedDialog):
    def __init__(self, parent: Window):

        dialogStyle: int  = DEFAULT_DIALOG_STYLE | CAPTION | RESIZE_BORDER | STAY_ON_TOP

        super().__init__(parent=parent, id=ID_ANY, title="Tips", style=dialogStyle)

        self.logger: Logger = getLogger(__name__)

        self._prefs:        PyutPreferences = PyutPreferences()
        self._tipsFileName: str             = PyutUtils.retrieveResourcePath(f'{PyutConstants.TIPS_FILENAME}')
        self._tipHandler:   TipHandler      = TipHandler(fqFileName=self._tipsFileName)

        panel: SizedPanel = self.GetContentsPane()

        self._label:       StaticText = cast(StaticText, None)
        self._chkShowTips: CheckBox   = cast(CheckBox, None)

        self._btnOk:       Button     = cast(Button, None)
        self._btnPrevious: Button     = cast(Button, None)
        self._btnNext:     Button     = cast(Button, None)

        self._layoutUpperDialog(parent=panel)
        self._layoutDialogButtonContainer(parent=panel)

        # a little trick to make sure that you can't resize the dialog to
        # less screen space than the controls need
        self.Fit()
        self.SetMinSize(self.GetSize())

        self._bindEventHandlers()

    def _layoutUpperDialog(self, parent: SizedPanel):
        """
            topPanel:  Image and static text widget
            bottomPanel:  The show tips checkbox
        Args:
            parent:  Dialog container
        """
        tipText: str = self._getTipText()

        topPanel: SizedPanel = SizedPanel(parent)
        topPanel.SetSizerType('horizontal')

        bmp: Bitmap = TipsLogo.GetBitmap()
        StaticBitmap(topPanel, ID_ANY, bmp)

        self._label = StaticText(topPanel, ID_ANY, tipText, style=ALIGN_LEFT)

        bottomPanel: SizedPanel = SizedPanel(parent)
        bottomPanel.SetSizerType('horizontal')

        self._chkShowTips = CheckBox(bottomPanel, ID_CHK_SHOW_TIPS, label="&Show tips at startup")

        showTips: bool = self._prefs.showTipsOnStartup
        self._chkShowTips.SetValue(showTips)

    def _layoutDialogButtonContainer(self, parent: SizedPanel):
        """
        Create Ok, Previous Tip and Next Tip buttons;

        Since we want to use a custom button layout, we will not use the
        CreateStdDialogBtnSizer here, we'll create our own panel with
        a horizontal layout and add the buttons to that;

        Args:
            parent:
        """
        buttonPanel: SizedPanel = SizedPanel(parent)
        buttonPanel.SetSizerType('horizontal')
        buttonPanel.SetSizerProps(expand=False, halign='right')  # expand False allows aligning right

        self._btnPrevious = Button(buttonPanel, ID_SET_PREVIOUS_TIP, label='&Previous')
        self._btnNext     = Button(buttonPanel, ID_SET_NEXT_TIP,     label='&Next')
        self._btnOk       = Button(buttonPanel, ID_OK,               label='&Ok')

    def _bindEventHandlers(self):

        self.Bind(EVT_BUTTON, self._onOk,          id=ID_OK)
        self.Bind(EVT_CLOSE,  self._onClose)
        self.Bind(EVT_BUTTON, self._onNextTip,     id=ID_SET_NEXT_TIP)
        self.Bind(EVT_BUTTON, self._onPreviousTip, id=ID_SET_PREVIOUS_TIP)

    # noinspection PyUnusedLocal
    def _onOk(self, event: CommandEvent):
        """
        """
        self._prefs.showTipsOnStartup = self._chkShowTips.GetValue()
        self.SetReturnCode(OK)
        self.EndModal(OK)

    # noinspection PyUnusedLocal
    def _onNextTip(self, event: CommandEvent):
        """
        Select and display the next tip
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

    # noinspection PyUnusedLocal
    def _onClose(self, event: CloseEvent):
        """
        Save state
        """
        self._prefs.currentTip  = self._tipHandler.currentTipNumber
        self._prefs.showTipsOnStartup = self._chkShowTips.GetValue()

        self.EndModal(CANCEL)

    def _getTipText(self) -> str:

        longText: str = self._tipHandler.getCurrentTipText()

        return self._normalizeTip(longText)

    def _normalizeTip(self, tip: str) -> str:

        dc:    ClientDC     = ClientDC(self)
        ls:    LineSplitter = LineSplitter()
        dlgSize: Size = self.GetSize()
        lines: List[str]    = ls.split(text=tip, dc=dc, textWidth=int(dlgSize.width * 0.8))

        splitTip: str = ''
        for line in lines:
            splitTip = f'{splitTip}{line}{osLineSep}'

        return splitTip

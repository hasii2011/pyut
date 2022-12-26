
from logging import Logger
from logging import getLogger

from wx import ALIGN_CENTER_HORIZONTAL
from wx import BOTTOM
from wx import EXPAND

from wx import VERTICAL
from wx import ALL
from wx import OK
from wx import CANCEL

from wx import TextCtrl
from wx import CommandEvent
from wx import StaticText
from wx import BoxSizer

from pyut.dialogs.BaseDlgEdit import BaseDlgEdit
from pyut.uiv2.eventengine.IEventEngine import IEventEngine


class BaseDlgEditText(BaseDlgEdit):

    clsLogger: Logger = getLogger(__name__)

    def __init__(self, parent, eventEngine: IEventEngine, title='',):

        super().__init__(parent, eventEngine=eventEngine, title=title)
        self.SetAutoLayout(True)

    def _setupMainDialogLayout(self, textControl: TextCtrl, label: StaticText = None):

        sizerButtons: BoxSizer = self._createDialogButtons()
        # Sizer for all components
        szrMain: BoxSizer = BoxSizer(VERTICAL)
        if label is not None:
            szrMain.Add(label, 0, BOTTOM, 5)

        szrMain.Add(textControl, 1, EXPAND | BOTTOM, 10)
        szrMain.Add(sizerButtons, 0, ALIGN_CENTER_HORIZONTAL)

        # Border
        szrBorder: BoxSizer = BoxSizer(VERTICAL)
        szrBorder.Add(szrMain, 1, EXPAND | ALL, 10)
        self.SetSizer(szrBorder)
        szrBorder.Fit(self)

    # noinspection PyUnusedLocal
    def _onCmdOk(self, event: CommandEvent):

        self.SetReturnCode(OK)
        self.EndModal(OK)

    # noinspection PyUnusedLocal
    def _onCmdCancel(self, event: CommandEvent):
        """
        Handle click on "Cancel" button.
        """
        self.SetReturnCode(CANCEL)
        self.EndModal(CANCEL)

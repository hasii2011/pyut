
from typing import cast

from logging import Logger
from logging import getLogger

from wx import ALIGN_CENTER_HORIZONTAL
from wx import BOTTOM
from wx import EVT_BUTTON
from wx import EXPAND
from wx import STAY_ON_TOP
from wx import RESIZE_BORDER
from wx import CAPTION
from wx import VERTICAL
from wx import ALL
from wx import OK
from wx import CANCEL
from wx import HORIZONTAL
from wx import RIGHT

from wx import TextCtrl
from wx import Window
from wx import CommandEvent
from wx import StaticText
from wx import BoxSizer
from wx import Button
from wx import Dialog

# noinspection PyProtectedMember
from pyut.general.Globals import _


class BaseDlgEditText(Dialog):

    clsLogger: Logger = getLogger(__name__)

    def __init__(self, parent: Window, dialogIdentifier: int, dialogTitle: str):

        super().__init__(parent, dialogIdentifier, dialogTitle, style=RESIZE_BORDER | CAPTION | STAY_ON_TOP)
        self.SetAutoLayout(True)

    def _createDialogButtons(self) -> BoxSizer:
        """
        Creates the buttons and assigns the handlers

        Returns:
            The container that holds the dialog buttons
        """

        btnOk:     Button = Button(self, OK, _("&Ok"))
        btnCancel: Button = Button(self, CANCEL, _("&Cancel"))

        btnOk.SetDefault()

        self.Bind(EVT_BUTTON, self._onCmdOk,     id=OK)
        self.Bind(EVT_BUTTON, self._onCmdCancel, id=CANCEL)

        sizerButtons: BoxSizer = BoxSizer(HORIZONTAL)
        sizerButtons.Add(btnOk, 0, RIGHT, 10)
        sizerButtons.Add(btnCancel, 0, ALL)

        return sizerButtons

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


from typing import cast

from logging import Logger
from logging import getLogger

from wx import ALIGN_CENTER_HORIZONTAL
from wx import BOTTOM
from wx import BoxSizer
from wx import Button
from wx import Dialog
from wx import EVT_BUTTON
from wx import EXPAND
from wx import StaticText
from wx import TextCtrl
from wx import VERTICAL
from wx import Window
from wx import CommandEvent

from wx import ALL
from wx import OK
from wx import CANCEL
from wx import CAPTION
from wx import HORIZONTAL
from wx import RESIZE_BORDER
from wx import RIGHT

from org.pyut.general.Globals import _


class BaseDlgEditText(Dialog):

    clsLogger: Logger = getLogger(__name__)

    def __init__(self, parent: Window, dialogIdentifier: int, dialogTitle: str):

        super().__init__(parent, dialogIdentifier, dialogTitle, style=RESIZE_BORDER | CAPTION)

        self._returnAction: int = cast(int, None)   # describe how the user exited the dialog box

        self.clsLogger.info(f'{self._returnAction}')

        self.SetAutoLayout(True)

    def getReturnAction(self) -> int:
        """
        Return an information on how the user exited the dialog

        Returns:
            wx.Ok = click on Ok button; wx.Cancel = click on Cancel button
        """
        return self._returnAction

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

        self._returnAction = OK
        # self.Close()
        self.EndModal(OK)

    # noinspection PyUnusedLocal
    def _onCmdCancel(self, event: CommandEvent):
        """
        Handle click on "Cancel" button.
        """
        self._returnAction = CANCEL
        # self.Close()
        self.EndModal(CANCEL)

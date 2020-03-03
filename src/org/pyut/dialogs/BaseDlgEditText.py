
from typing import cast

from logging import Logger
from logging import getLogger

from wx import CANCEL
from wx import CAPTION
from wx import CommandEvent
from wx import Dialog
from wx import OK
from wx import RESIZE_BORDER
from wx import Window


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

    # noinspection PyUnusedLocal
    def _onCmdOk(self, event: CommandEvent):

        self._returnAction = OK
        self.Close()

    # noinspection PyUnusedLocal
    def _onCmdCancel(self, event: CommandEvent):
        """
        Handle click on "Cancel" button.
        """
        self._returnAction = CANCEL
        self.Close()

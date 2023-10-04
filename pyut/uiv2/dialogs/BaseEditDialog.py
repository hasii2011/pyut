
from typing import Callable
from typing import NewType
from typing import cast
from typing import List

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from wx import Button
from wx import CANCEL
from wx import Colour
from wx import DEFAULT_DIALOG_STYLE
from wx import STAY_ON_TOP
from wx import EVT_BUTTON
from wx import EVT_CLOSE
from wx import ID_CANCEL
from wx import ID_OK
from wx import OK

from wx import CommandEvent
from wx import ColourDatabase
from wx import StdDialogButtonSizer
from wx import TextCtrl

from wx.lib.sized_controls import SizedDialog
from wx.lib.sized_controls import SizedPanel


@dataclass
class CustomDialogButton:
    label:    str = ''
    callback: Callable = cast(Callable, None)


CustomDialogButtons = NewType('CustomDialogButtons', List[CustomDialogButton])


class BaseEditDialog(SizedDialog):
    baseDlgLogger: Logger = getLogger(__name__)
    """
    Provides a common place to host duplicate code
    """
    def __init__(self, parent, title=''):

        super().__init__(parent, title=title, style=DEFAULT_DIALOG_STYLE | STAY_ON_TOP)

    def _layoutStandardOkCancelButtonSizer(self):
        """
        Call this last when creating controls;  Will take care of
        adding callbacks for the Ok and Cancel buttons
        """
        buttSizer: StdDialogButtonSizer = self.CreateStdDialogButtonSizer(OK | CANCEL)

        self.SetButtonSizer(buttSizer)
        self.Bind(EVT_BUTTON, self._onOk,    id=ID_OK)
        self.Bind(EVT_BUTTON, self._onClose, id=ID_CANCEL)
        self.Bind(EVT_CLOSE,  self._onClose)

    def _layoutCustomDialogButtonContainer(self, parent: SizedPanel, customButtons: CustomDialogButtons):
        """
        Create Ok and Cancel
        Since we want to use a custom button set, we will not use the
        CreateStdDialogBtnSizer here, we'll just create our own panel with
        a horizontal layout and add the buttons to that

        Args:
            parent:
            customButtons:  Data to create any necessary custom buttons
        """
        buttonPanel: SizedPanel = SizedPanel(parent)
        buttonPanel.SetSizerType('horizontal')
        buttonPanel.SetSizerProps(expand=False, halign='right')  # expand False allows aligning right

        for customButton in customButtons:
            customDialogButton: CustomDialogButton = cast(CustomDialogButton, customButton)
            button:             Button             = Button(buttonPanel, label=customDialogButton.label)
            self.Bind(EVT_BUTTON, customDialogButton.callback, button)

        self._btnCancel = Button(buttonPanel, ID_CANCEL, '&Cancel')
        self._btnOk     = Button(buttonPanel, ID_OK, '&Ok')

        self.Bind(EVT_BUTTON, self._onOk,    self._btnOk)
        self.Bind(EVT_BUTTON, self._onClose, self._btnCancel)

        self._btnOk.SetDefault()

    def _convertNone(self, theString: str):
        """

        Args:
            theString:  the string to possibly convert

        Returns: the same string, if string = None, return an empty string.
        """
        if theString is None:
            theString = ''
        return theString

    # noinspection PyUnusedLocal
    def _onOk(self, event: CommandEvent):
        """
        """
        self.EndModal(OK)

    # noinspection PyUnusedLocal
    def _onClose(self, event: CommandEvent):
        """
        """
        self.EndModal(CANCEL)

    def _indicateEmptyTextCtrl(self, name: TextCtrl):

        self.baseDlgLogger.warning(f'Name is empty!!')
        name.BackgroundColour = ColourDatabase().Find('Red')

    def _indicateNonEmptyTextCtrl(self, name: TextCtrl, normalBackgroundColor: Colour):
        name.BackgroundColour = normalBackgroundColor

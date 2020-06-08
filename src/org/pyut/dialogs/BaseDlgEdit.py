from wx import CANCEL
from wx import CAPTION
from wx import CommandEvent

from wx import ID_ANY
from wx import OK
from wx import RESIZE_BORDER
from wx import STAY_ON_TOP

from wx import Dialog
from wx import Sizer


class BaseDlgEdit(Dialog):

    PROPORTION_CHANGEABLE: int = 1
    CONTAINER_GAP:         int = 3
    VERTICAL_GAP:          int = 2

    """
    Provides a common place to host duplicate code
    """
    def __init__(self, theParent, theWindowId=ID_ANY, theTitle=None, theStyle=RESIZE_BORDER | CAPTION | STAY_ON_TOP, theMediator=None):

        super().__init__(theParent, theWindowId, title=theTitle, style=theStyle)

        self._ctrl = theMediator

    def _createDialogButtonsContainer(self, buttons=OK) -> Sizer:

        hs: Sizer = self.CreateSeparatedButtonSizer(buttons)
        return hs

    def _convertNone (self, theString: str):
        """
        Return the same string, if string = None, return an empty string.

        @param  theString : the string to possibly convert
        """
        if theString is None:
            theString = ''
        return theString

    def _OnCmdOk(self, event: CommandEvent):
        """
        """
        event.Skip(skip=True)
        self.SetReturnCode(OK)
        self.EndModal(OK)

    # noinspection PyUnusedLocal
    def _OnClose(self, event: CommandEvent):
        """
        """
        self.SetReturnCode(CANCEL)
        self.EndModal(CANCEL)

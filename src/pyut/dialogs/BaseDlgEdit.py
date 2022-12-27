
from wx import CANCEL
from wx import CAPTION
from wx import EVT_BUTTON
from wx import EVT_CLOSE
from wx import ID_CANCEL
from wx import ID_OK
from wx import OK
from wx import RESIZE_BORDER
from wx import STAY_ON_TOP

from wx import CommandEvent

from wx.lib.sized_controls import SizedDialog

from pyut.uiv2.eventengine.Events import EventType
from pyut.uiv2.eventengine.IEventEngine import IEventEngine


class BaseDlgEdit(SizedDialog):

    PROPORTION_CHANGEABLE: int = 1
    CONTAINER_GAP:         int = 3
    VERTICAL_GAP:          int = 2

    """
    Provides a common place to host duplicate code
    """
    def __init__(self, parent, eventEngine: IEventEngine, title=''):

        style: int = RESIZE_BORDER | CAPTION | STAY_ON_TOP

        super().__init__(parent, title=title, style=style)

        self._eventEngine: IEventEngine = eventEngine

    def _createStandardOkCancelButtonSizer(self):
        """
        Call this last when creating controls;  Will take care of
        adding callbacks for the Ok and Cancel buttons
        """
        self.SetButtonSizer(self.CreateStdDialogButtonSizer(OK | CANCEL))
        self.Bind(EVT_BUTTON, self._onOk,    id=ID_OK)
        self.Bind(EVT_BUTTON, self._onClose, id=ID_CANCEL)
        self.Bind(EVT_CLOSE,  self._onClose)

    def _convertNone (self, theString: str):
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

    def _markCurrentDiagramAsModified(self):
        """
        """
        self._eventEngine.sendEvent(EventType.UMLDiagramModified)

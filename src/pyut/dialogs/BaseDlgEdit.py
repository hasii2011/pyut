
from wx import CANCEL
from wx import CAPTION
from wx import CommandEvent

from wx import OK
from wx import RESIZE_BORDER
from wx import STAY_ON_TOP

from wx import Dialog
from wx import Sizer

from pyut.uiv2.eventengine.ActiveProjectInformation import ActiveProjectInformation
from pyut.uiv2.eventengine.Events import EventType
from pyut.uiv2.eventengine.IEventEngine import IEventEngine


class BaseDlgEdit(Dialog):

    PROPORTION_CHANGEABLE: int = 1
    CONTAINER_GAP:         int = 3
    VERTICAL_GAP:          int = 2

    """
    Provides a common place to host duplicate code
    """
    def __init__(self, theParent, eventEngine: IEventEngine, title=None, theStyle=RESIZE_BORDER | CAPTION | STAY_ON_TOP):

        # from org.pyut.ui.Mediator import Mediator

        super().__init__(theParent, title=title, style=theStyle)

        self._eventEngine: IEventEngine = eventEngine

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

    def _setProjectModified(self):
        """
        We need to request some information
        """
        self._eventEngine.sendEvent(EventType.ActiveProjectInformation, callback=self.__markProjectAsModified)

    def __markProjectAsModified(self, activeProjectInformation: ActiveProjectInformation):
        """
        Now we can mark the project as modified
        Args:
            activeProjectInformation:
        """

        activeProjectInformation.pyutProject.modified = True

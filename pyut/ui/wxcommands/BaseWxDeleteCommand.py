
from typing import TYPE_CHECKING

from wx import Yield as wxYield

from pyut.ui.wxcommands.BaseWxCommand import BaseWxCommand
from pyut.ui.wxcommands.Types import DoableObjectType

from pyut.ui.eventengine.EventType import EventType
from pyut.ui.eventengine.IEventEngine import IEventEngine

if TYPE_CHECKING:
    from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame


class BaseWxDeleteCommand(BaseWxCommand):

    def __init__(self, name: str, doableObject: DoableObjectType, eventEngine: IEventEngine):

        self._name: str = name

        self._objectToDelete: DoableObjectType = doableObject
        self._eventEngine:    IEventEngine     = eventEngine

        super().__init__(canUndo=True, name=self._name)

        w, h = self._objectToDelete.GetSize()
        x, y = self._objectToDelete.GetPosition()
        self._oglObjWidth:  int = w
        self._oglObjHeight: int = h
        self._oglObjX:      int = x
        self._oglObjY:      int = y

    def GetName(self) -> str:
        """
        Returns the command name.
        """
        return self._name

    def CanUndo(self) -> bool:
        """
        Returns true if the command can be undone, false otherwise.
        """
        return True

    def Do(self) -> bool:
        """
        Override this member method to execute the appropriate action when called.
        """
        self._objectToDelete.Detach()
        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._cbGetActiveUmlFrameForDelete)

        wxYield()
        return True

    def _cbGetActiveUmlFrameForDelete(self, frame: 'UmlDiagramsFrame'):

        from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

        umlFrame: UmlDiagramsFrame = frame
        umlFrame.Refresh()

    def _cbGetActiveUmlFrameForUndoDelete(self, frame: 'UmlDiagramsFrame'):

        from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

        umlFrame: UmlDiagramsFrame = frame
        umlFrame.addShape(self._objectToDelete, x=self._oglObjX, y=self._oglObjY)
        umlFrame.Refresh()

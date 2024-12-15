
from logging import Logger
from logging import getLogger

from wx import Yield as wxYield

from pyutmodelv2.PyutActor import PyutActor

from ogl.OglActor import OglActor

from pyut.ui.wxcommands.BaseWxDeleteCommand import BaseWxDeleteCommand

from pyut.ui.eventengine.Events import EventType
from pyut.ui.eventengine.IEventEngine import IEventEngine


class CommandDeleteOglActor(BaseWxDeleteCommand):

    def __init__(self, oglActor: OglActor, eventEngine: IEventEngine):

        super().__init__(name='Delete Actor', doableObject=oglActor, eventEngine=eventEngine)

        self.logger: Logger = getLogger(__name__)

        self._pyutActor: PyutActor = oglActor.pyutObject

    def Undo(self) -> bool:
        """
        Override this member method to un-execute a previous Do.
        """
        self._objectToDelete = OglActor(self._pyutActor, w=self._oglObjWidth, h=self._oglObjHeight)      # create new
        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._cbGetActiveUmlFrameForUndoDelete)

        wxYield()
        return True

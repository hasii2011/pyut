
from logging import Logger
from logging import getLogger

from wx import Yield as wxYield

from pyutmodelv2.PyutText import PyutText

from ogl.OglText import OglText

from pyut.ui.wxcommands.BaseWxDeleteCommand import BaseWxDeleteCommand

from pyut.uiv2.eventengine.Events import EventType
from pyut.uiv2.eventengine.IEventEngine import IEventEngine


class CommandDeleteOglText(BaseWxDeleteCommand):

    def __init__(self, oglText: OglText, eventEngine: IEventEngine):

        super().__init__(name='Delete Ogl Text', doableObject=oglText, eventEngine=eventEngine)

        self.logger: Logger = getLogger(__name__)

        self._pyutText: PyutText = oglText.pyutObject

    def Undo(self) -> bool:
        """
        Override this member method to un-execute a previous Do.
        """
        self._objectToDelete = OglText(self._pyutText, width=self._oglObjWidth, height=self._oglObjHeight)      # create new
        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._cbGetActiveUmlFrameForUndoDelete)

        wxYield()
        return True

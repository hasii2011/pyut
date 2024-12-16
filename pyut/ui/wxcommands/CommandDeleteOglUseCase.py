
from logging import Logger
from logging import getLogger

from wx import Yield as wxYield

from pyutmodelv2.PyutUseCase import PyutUseCase

from ogl.OglUseCase import OglUseCase

from pyut.ui.eventengine.EventType import EventType
from pyut.ui.eventengine.IEventEngine import IEventEngine

from pyut.ui.wxcommands.BaseWxDeleteCommand import BaseWxDeleteCommand


class CommandDeleteOglUseCase(BaseWxDeleteCommand):

    def __init__(self, oglUseCase: OglUseCase, eventEngine: IEventEngine):

        super().__init__(name='Delete Use Case', doableObject=oglUseCase, eventEngine=eventEngine)

        self.logger: Logger = getLogger(__name__)

        self._pyutUseCase: PyutUseCase = oglUseCase.pyutObject

    def Undo(self) -> bool:
        """
        Override this member method to un-execute a previous Do
        """
        self._objectToDelete = OglUseCase(self._pyutUseCase, w=self._oglObjWidth, h=self._oglObjHeight)      # create new
        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._cbGetActiveUmlFrameForUndoDelete)

        wxYield()
        return True

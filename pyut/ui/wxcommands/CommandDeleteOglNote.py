
from logging import Logger
from logging import getLogger

from pyutmodel.PyutNote import PyutNote
from wx import Yield as wxYield

from ogl.OglNote import OglNote

from pyut.ui.wxcommands.BaseWxDeleteCommand import BaseWxDeleteCommand

from pyut.uiv2.eventengine.Events import EventType
from pyut.uiv2.eventengine.IEventEngine import IEventEngine


class CommandDeleteOglNote(BaseWxDeleteCommand):

    def __init__(self, oglNote: OglNote, eventEngine: IEventEngine):

        super().__init__(name='Delete Note', doableObject=oglNote, eventEngine=eventEngine)

        self.logger: Logger = getLogger(__name__)

        self._pyutNote: PyutNote = oglNote.pyutObject

    def Undo(self) -> bool:
        """
        Override this member method to un-execute a previous Do.
        """
        self._objectToDelete = OglNote(self._pyutNote, w=self._oglObjWidth, h=self._oglObjHeight)      # create new
        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._cbGetActiveUmlFrameForUndoDelete)

        wxYield()
        return True


from typing import cast

from logging import Logger
from logging import getLogger

from pyutmodelv2.PyutActor import PyutActor

from ogl.OglActor import OglActor

from pyut.ui.wxcommands.BaseWxCreateCommand import BaseWxCreateCommand
from pyut.uiv2.eventengine.Events import EventType

from pyut.uiv2.eventengine.IEventEngine import IEventEngine


class CommandCreateOglActor(BaseWxCreateCommand):

    def __init__(self, x: int, y: int, eventEngine: IEventEngine):

        super().__init__(canUndo=True, name='Create Actor', x=x, y=y, eventEngine=eventEngine)

        self.logger: Logger = getLogger(__name__)

    def _createPrototypeInstance(self) -> OglActor:
        """
        Implement required abstract method
        Creates an appropriate actor for the new command

        Returns:    The newly created actor
        """
        pyutActor: PyutActor = PyutActor(actorName=self._oglPreferences.defaultNameActor)

        oglActor:  OglActor  = OglActor(pyutActor)

        return oglActor

    def _placeShapeOnFrame(self):
        """
        Create new self._shape based on saved data
        Place self._shape on the UML frame
        """
        oglActor:  OglActor  = cast(OglActor, self._shape)                 # get old or prototype on first use
        pyutActor: PyutActor = cast(PyutActor, oglActor.pyutObject)

        self._oglObjWidth, self._oglObjHeight = oglActor.GetSize()
        self._shape = OglActor(pyutActor, w=self._oglObjWidth, h=self._oglObjHeight)      # create new one

        self._eventEngine.sendEvent(EventType.EditActor, pyutActor=pyutActor)

        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._cbAddOglObjectToFrame)


from logging import Logger
from logging import getLogger

from wx import Point
from wx import Yield as wxYield

from pyutmodelv2.enumerations.PyutLinkType import PyutLinkType

from pyut.ui.wxcommands.BaseWxLinkCommand import BaseWxLinkCommand
from pyut.ui.eventengine.Events import EventType
from pyut.ui.eventengine.IEventEngine import IEventEngine

from pyut.ui.wxcommands.Types import DoableObjectType


class CommandCreateOglLink(BaseWxLinkCommand):

    def __init__(self, eventEngine: IEventEngine,
                 src: DoableObjectType,
                 dst: DoableObjectType,
                 linkType: PyutLinkType = PyutLinkType.INHERITANCE,
                 srcPoint: Point = None,
                 dstPoint: Point = None):
        """

        Args:
            eventEngine:    A references to the Pyut event engine
            src:            The source UML Object
            dst:            The destination UML Object
            linkType:       The Link Type
            srcPoint:       The source attachment point
            dstPoint:       The destination attachment point
        """
        super().__init__(partialName='Create', linkType=linkType, eventEngine=eventEngine)

        self.logger:       Logger       = getLogger(__name__)

        self._srcOglObject: DoableObjectType = src
        self._dstOglObject: DoableObjectType = dst

        self._srcPoint: Point        = srcPoint
        self._dstPoint: Point        = dstPoint

    def Do(self) -> bool:
        self._link = self._createLink()
        self.logger.info(f'Create: {self._link}')

        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._cbPlaceLink)
        return True

    def Undo(self) -> bool:
        """
        Returns:  True to indicate the undo was done
        """
        self.logger.info(f'Undo Create: {self._link}')

        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._cbDoDeleteLink)

        wxYield()

        return True


from logging import Logger
from logging import getLogger

from wx import Point
from wx import Yield as wxYield

from pyutmodel.PyutLinkType import PyutLinkType
from ogl.OglLink import OglLink

from pyut.ui.wxcommands.BaseWxLinkCommand import BaseWxLinkCommand
from pyut.uiv2.eventengine.Events import EventType

from pyut.uiv2.eventengine.IEventEngine import IEventEngine


class CommandDeleteOglLink(BaseWxLinkCommand):

    def __init__(self, oglLink: OglLink, eventEngine: IEventEngine):

        self._linkType: PyutLinkType = oglLink.pyutObject.linkType

        super().__init__(partialName='Delete', linkType=self._linkType, eventEngine=eventEngine)

        self.logger: Logger = getLogger(__name__)

        self._srcOglObject = oglLink.sourceShape
        self._dstOglObject = oglLink.destinationShape

        sourceAnchorPoint      = oglLink.sourceAnchor
        destinationAnchorPoint = oglLink.destinationAnchor

        srcX, srcY = sourceAnchorPoint.GetPosition()
        dstX, dstY = destinationAnchorPoint.GetPosition()
        self._srcPoint = Point(x=srcX, y=srcY)
        self._dstPoint = Point(x=dstX, y=dstY)

        self._link = oglLink        # Save the link to delete

    def Do(self) -> bool:
        self.logger.info(f'Delete: {self._link}')

        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._cbDoDeleteLink)
        wxYield()

        return True

    def Undo(self) -> bool:

        self._link = self._createLink()

        self.logger.info(f'Undo Delete: {self._link}')

        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._cbPlaceLink)
        wxYield()

        return True


from typing import cast

from logging import Logger
from logging import getLogger

from wx import Point
from wx import Yield as wxYield

from pyutmodelv2.enumerations.PyutLinkType import PyutLinkType

from ogl.OglLink import OglLink
from ogl.OglAssociation import OglAssociation

from pyut.ui.wxcommands.BaseWxLinkCommand import BaseWxLinkCommand
from pyut.ui.eventengine.EventType import EventType

from pyut.ui.eventengine.IEventEngine import IEventEngine


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

        self._controlPoints = oglLink.GetControlPoints()       # in case we have bends
        self._spline        = oglLink.spline

        self._link = oglLink        # Save the link to delete
        if isinstance(self._link, OglAssociation):
            oglAssociation: OglAssociation = cast(OglAssociation, self._link)

            self._pyutLink = oglAssociation.pyutObject

    def Do(self) -> bool:
        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._cbDoDeleteLink)
        wxYield()

        return True

    def Undo(self) -> bool:

        self._link = self._createLink()

        self.logger.info(f'Undo Delete: {self._link.__repr__()}')

        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._cbPlaceLink)
        wxYield()

        return True

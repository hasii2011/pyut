from typing import cast

from logging import Logger
from logging import getLogger

from wx import BLACK_PEN
from wx import RED_PEN
from wx import DC

from miniogl.AttachmentLocation import AttachmentLocation
from miniogl.Common import CommonLine
from miniogl.Common import CommonPoint

from miniogl.SelectAnchorPoint import SelectAnchorPoint
from miniogl.Shape import Shape


class LollipopLine(Shape):

    LOLLIPOP_LINE_LENGTH:   int = 60
    LOLLIPOP_CIRCLE_RADIUS: int = 4

    def __init__(self, destinationAnchor: SelectAnchorPoint):

        super().__init__()

        self.logger:             Logger      = getLogger(__name__)
        self._destinationAnchor: SelectAnchorPoint = cast(SelectAnchorPoint, None)

        if destinationAnchor is not None:
            self._destinationAnchor = destinationAnchor
            destinationAnchor.AddLine(self)

    @property
    def destinationAnchor(self) -> SelectAnchorPoint:
        return self._destinationAnchor

    @destinationAnchor.setter
    def destinationAnchor(self, theNewValue: SelectAnchorPoint):
        self._destinationAnchor = theNewValue

    def lineCoordinates(self) -> CommonLine:

        attachmentPoint: AttachmentLocation = self._destinationAnchor.attachmentPoint

        xDest, yDest = self._destinationAnchor.GetPosition()
        circleX, circleY, xSrc, ySrc = self._calculateWhereToDrawLollipop(attachmentPoint, xDest, yDest)

        return CommonLine(CommonPoint(xSrc, ySrc), CommonPoint(xDest, yDest))

    def Draw(self, dc: DC, withChildren: bool = True):

        if self._selected:
            dc.SetPen(RED_PEN)
        else:
            dc.SetPen(BLACK_PEN)

        xDest, yDest = self._destinationAnchor.GetPosition()
        attachmentPoint: AttachmentLocation = self._destinationAnchor.attachmentPoint

        circleX, circleY, xSrc, ySrc = self._calculateWhereToDrawLollipop(attachmentPoint, xDest, yDest)

        self.logger.debug(f'Source: ({xSrc},{ySrc}) - Dest ({xDest},{yDest})')
        dc.DrawLine(xSrc, ySrc, xDest, yDest)
        dc.DrawCircle(circleX, circleY, LollipopLine.LOLLIPOP_CIRCLE_RADIUS)

    def _calculateWhereToDrawLollipop(self, attachmentPoint, xDest, yDest):
        """

        Args:
            attachmentPoint:
            xDest:
            yDest:

        Returns:  A tuple that is the x,y position of the circle and the end
        of the line
        """

        diagram = self.GetDiagram()
        panel   = diagram.GetPanel()   # to enable debugging and unit tests
        ratio = panel.GetCurrentZoom()

        lollipopLength: int = LollipopLine.LOLLIPOP_LINE_LENGTH * ratio
        self.logger.debug(f'{lollipopLength}')

        if attachmentPoint == AttachmentLocation.EAST:
            xSrc: int = int(xDest + lollipopLength)
            ySrc: int = int(yDest)
            circleX: int = int(xDest + lollipopLength)
            circleY: int = int(yDest)
        elif attachmentPoint == AttachmentLocation.WEST:
            xSrc: int = int(xDest - lollipopLength)
            ySrc: int = int(yDest)
            circleX: int = int(xDest - lollipopLength)
            circleY: int = int(yDest)
        elif attachmentPoint == AttachmentLocation.NORTH:
            xSrc: int = int(xDest)
            ySrc: int = int(yDest - lollipopLength)
            circleX: int = int(xDest)
            circleY: int = int(yDest - lollipopLength)
        else:  # it is South
            xSrc: int = int(xDest)
            ySrc: int = int(yDest + lollipopLength)
            circleX: int = int(xDest)
            circleY: int = int(yDest + lollipopLength)

        return circleX, circleY, xSrc, ySrc

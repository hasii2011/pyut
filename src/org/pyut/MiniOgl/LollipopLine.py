from typing import cast

from logging import Logger
from logging import getLogger

from wx import DC
from wx import Pen
from wx import RED_PEN

from org.pyut.MiniOgl.Common import CommonLine
from org.pyut.MiniOgl.Common import CommonPoint

from org.pyut.MiniOgl.SelectAnchorPoint import SelectAnchorPoint
from org.pyut.MiniOgl.Shape import Shape

from org.pyut.enums.PyutAttachmentPoint import PyutAttachmentPoint


class LollipopLine(Shape):

    LOLLIPOP_LINE_LENGTH:   int = 50
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

        attachmentPoint: PyutAttachmentPoint = self._destinationAnchor.attachmentPoint

        xDest, yDest = self._destinationAnchor.GetPosition()
        circleX, circleY, xSrc, ySrc = self._calculateWhereToDrawLollipop(attachmentPoint, xDest, yDest)

        return CommonLine(CommonPoint(xSrc, ySrc), CommonPoint(xDest, yDest))

    def Draw(self, dc: DC, withChildren: bool = True):

        currentPen: Pen = RED_PEN
        currentPen.SetWidth(2)
        dc.SetPen(currentPen)

        xDest, yDest = self._destinationAnchor.GetPosition()
        attachmentPoint: PyutAttachmentPoint = self._destinationAnchor.attachmentPoint

        circleX, circleY, xSrc, ySrc = self._calculateWhereToDrawLollipop(attachmentPoint, xDest, yDest)

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

        if attachmentPoint == PyutAttachmentPoint.EAST:
            xSrc: int = int(xDest + LollipopLine.LOLLIPOP_LINE_LENGTH)
            ySrc: int = int(yDest)
            circleX: int = int(xDest + LollipopLine.LOLLIPOP_LINE_LENGTH)
            circleY: int = int(yDest)
        elif attachmentPoint == PyutAttachmentPoint.WEST:
            xSrc: int = int(xDest - LollipopLine.LOLLIPOP_LINE_LENGTH)
            ySrc: int = int(yDest)
            circleX: int = int(xDest - LollipopLine.LOLLIPOP_LINE_LENGTH)
            circleY: int = int(yDest)
        elif attachmentPoint == PyutAttachmentPoint.NORTH:
            xSrc: int = int(xDest)
            ySrc: int = int(yDest - LollipopLine.LOLLIPOP_LINE_LENGTH)
            circleX: int = int(xDest)
            circleY: int = int(yDest - LollipopLine.LOLLIPOP_LINE_LENGTH)
        else:  # it is South
            xSrc: int = int(xDest)
            ySrc: int = int(yDest + LollipopLine.LOLLIPOP_LINE_LENGTH)
            circleX: int = int(xDest)
            circleY: int = int(yDest + LollipopLine.LOLLIPOP_LINE_LENGTH)

        return circleX, circleY, xSrc, ySrc

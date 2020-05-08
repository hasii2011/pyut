
from typing import cast

from logging import Logger
from logging import getLogger

from wx import DC
from wx import Pen
from wx import RED_PEN

from org.pyut.MiniOgl.AnchorPoint import AnchorPoint
from org.pyut.MiniOgl.Shape import Shape


class LollipopLine(Shape):

    def __init__(self, destinationAnchor: AnchorPoint):

        super().__init__()

        self.logger:             Logger      = getLogger(__name__)
        self._destinationAnchor: AnchorPoint = cast(AnchorPoint, None)

        if destinationAnchor is not None:
            self._destinationAnchor = destinationAnchor
            destinationAnchor.AddLine(self)

    @property
    def destinationAnchor(self):
        return self._destinationAnchor

    @destinationAnchor.setter
    def destinationAnchor(self, theNewValue: AnchorPoint):
        self._destinationAnchor = theNewValue

    def Draw(self, dc: DC, withChildren: bool = True):

        currentPen: Pen = RED_PEN
        currentPen.SetWidth(2)
        dc.SetPen(currentPen)

        xDest, yDest = self._destinationAnchor.GetPosition()

        xSrc: int = int(xDest - 50)
        ySrc: int = int(yDest)
        dc.DrawLine(xSrc, ySrc, xDest, yDest)

        dc.DrawCircle(xDest, yDest, 4)

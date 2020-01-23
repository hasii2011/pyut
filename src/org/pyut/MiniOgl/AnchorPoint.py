
from logging import Logger
from logging import getLogger

from org.pyut.MiniOgl.LinePoint import LinePoint
from org.pyut.MiniOgl.Shape import Shape


class AnchorPoint(LinePoint):
    """
    This is a point which begins or ends a line.
    It is often anchored to a parent shape, but that's not mandatory.
    """
    def __init__(self, x: float, y: float, parent: Shape = None):
        """

        Args:
            x: x position of the point
            y: y position of the point
            parent:
        """
        super().__init__(x, y, parent)

        self.logger: Logger = getLogger(__name__)

        self.logger.debug(f'AnchorPoint __init__  x: {x}, y: {y} parent: {parent}')
        self._protected:    bool = True  # protected by default
        self._stayInside:   bool = True
        self._stayOnBorder: bool = True
        self.SetDraggable(False)

    def SetStayInside(self, state: bool):
        """
        If True, the point will stay inside the bounds of its parent shape.
        Args:
            state:
        """
        self._stayInside = state

    def GetStayInside(self) -> bool:
        """

        Returns:  `True` if the point stays inside the bounds of its parent shape.
        """
        return self._stayInside

    def SetStayOnBorder(self, state: bool):
        """
        If True, the point will stay on the border of its parent shape.
        Args:
            state:
        """
        self._stayOnBorder = state

    def GetStayOnBorder(self) -> bool:
        """
        Return True if the point stays on the border of its parent shape.

        @return boolean
        """
        return self._stayOnBorder

    def SetPosition(self, x, y):
        """
        Change the position of the anchor point, if it's draggable.

        Args:
            x:
            y:
        """
        if self._draggable:
            if self._parent is not None:

                topLeftX, topLeftY = self._parent.GetTopLeft()
                width, height = self._parent.GetSize()
                width  = abs(width) - 1
                height = abs(height) - 1
                if self._stayInside or self._stayOnBorder:
                    x = self.stayInside(topLeftX, width, x)
                    y = self.stayInside(topLeftY, height, y)
                    if self._stayOnBorder:
                        x, y = self.stickToBorder(topLeftX, topLeftY, width, height, x, y)
                self._x, self._y = self.ConvertCoordToRelative(x, y)
            else:
                self._x = x
                self._y = y

            if self.HasDiagramFrame():
                self.UpdateModel()

    def stayInside(self, low, length, value):
        """
        Return the nearest value in [low, low+length].

        Args:
            low:
            length:
            value:

        Returns: The nearest value
        """
        if value < low:
            value = low
        elif value > low + length:
            value = low + length
        return value

    def stickToBorder(self, ox, oy, width, height, x, y):
        """

        Args:
            ox:
            oy:
            width:
            height:
            x:
            y:

        Returns:  (x, y) on the square (ox, oy, ox+width, oy+height) by
        placing (x,y) on the nearest border.
        """
        left  = x - ox
        right = ox + width - x
        up    = y - oy
        down  = oy + height - y

        choice = {
            left: lambda xLeft, yLeft: (ox, y),
            right: lambda xRight, yRight: (ox + width, y),
            up: lambda xUp, yUp: (x, oy),
            down: lambda xDown, yDown: (x, oy + height),
        }
        lesser = min(left, right, up, down)
        self.logger.debug(f'lesser: {lesser}')
        return choice[lesser](x, y)

    def Detach(self):
        """
        Detach the line and all its line points, including src and dst.
        Also remove self from the parent.
        """
        LinePoint.Detach(self)
        parent = self.GetParent()
        if parent:
            parent.RemoveAnchor(self)

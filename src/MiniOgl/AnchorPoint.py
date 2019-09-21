

from MiniOgl.LinePoint import LinePoint

__all__ = ["AnchorPoint"]


class AnchorPoint(LinePoint):
    """
    This is a point which begins or ends a line.
    It is often anchored to a parent shape, but that's not mandatory.

    Exported methods:
    -----------------

    __init__(self, x, y, parent=None)
        Constructor.
    SetStayInside(self, state)
        If True, the point will stay inside the bounds of its parent shape.
    GetStayInside(self)
        Return True if the point stays inside the bounds of its parent shape.
    SetStayOnBorder(self, state)
        If True, the point will stay on the border of its parent shape.
    GetStayOnBorder(self)
        Return True if the point stays on the border of its parent shape.
    SetPosition(self, x, y)
        Change the position of the anchor point, if it's draggable.
    stayInside(low, length, value)
        Return the nearest value in [low, low+length].
    stickToBorder(ox, oy, width, height, x, y)
        Return (x, y) on the square (ox, oy, ox+width, oy+height) by
    Detach(self)
        Detach the line and all its line points, including src and dst.

    @author Laurent Burgbacher <lb@alawa.ch>
    """
    def __init__(self, x, y, parent=None):
        """
        Constructor.

        @param double x, y : position of the point
        @param Shape parent : parent shape
        """
        #  print ">>>AnchorPoint.init"
        LinePoint.__init__(self, x, y, parent)
        self._protected = True  # protected by default
        self.SetDraggable(False)
        self._stayInside = True
        self._stayOnBorder = True

    def SetStayInside(self, state):
        """
        If True, the point will stay inside the bounds of its parent shape.

        @param state
        """
        self._stayInside = state

    def GetStayInside(self):
        """
        Return True if the point stays inside the bounds of its parent shape.

        @return boolean
        """
        return self._stayInside

    def SetStayOnBorder(self, state):
        """
        If True, the point will stay on the border of its parent shape.

        @param state
        """
        self._stayOnBorder = state

    def GetStayOnBorder(self):
        """
        Return True if the point stays on the border of its parent shape.

        @return boolean
        """
        return self._stayOnBorder

    def SetPosition(self, x, y):
        """
        Change the position of the anchor point, if it's draggable.

        """

        def stayInside(low, length, value):
            """
            Return the nearest value in [low, low+length].
            """
            if value < low:
                value = low
            elif value > low + length:
                value = low + length
            return value

        def stickToBorder(ox, oy, width, height, x, y):
            """
            Return (x, y) on the square (ox, oy, ox+width, oy+height) by
            placing (x, y) on the nearest border.
            """
            left = x - ox
            right = ox + width - x
            up = y - oy
            down = oy + height - y
            choice = {
                left:  lambda x, y: (ox, y),
                right: lambda x, y: (ox + width, y),
                up:    lambda x, y: (x, oy),
                down:  lambda x, y: (x, oy + height),
            }
            lesser = min(left, right, up, down)
            return choice[lesser](x, y)

        if self._draggable:
            if self._parent is not None:

                topLeftX, topLeftY = self._parent.GetTopLeft()
                width, height = self._parent.GetSize()
                width = abs(width) - 1
                height = abs(height) - 1
                if self._stayInside or self._stayOnBorder:
                    x = stayInside(topLeftX, width, x)
                    y = stayInside(topLeftY, height, y)
                    if self._stayOnBorder:
                        x, y = stickToBorder(topLeftX, topLeftY, width, height, x, y)
                self._x, self._y = self.ConvertCoordToRelative(x, y)
            else:
                self._x = x
                self._y = y

            #added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (12.11.2005)
            #updates the model of the anchor point (MVC pattern)
            if self.HasDiagramFrame():
                self.UpdateModel()

    def Detach(self):
        """
        Detach the line and all its line points, including src and dst.
        Also remove self from the parent.
        """
        LinePoint.Detach(self)
        parent = self.GetParent()
        if parent:
            parent.RemoveAnchor(self)

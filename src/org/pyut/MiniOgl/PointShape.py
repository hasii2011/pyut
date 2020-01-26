from org.pyut.MiniOgl.Shape import Shape


class PointShape(Shape):
    """
    A point, which is drawn as a little square (3 pixels wide).

    """
    def __init__(self, x: float, y: float, parent=None):
        """

        Args:
            x:  x position of the point
            y:  y position of the point
            parent:  parent shape
        """
        #  print ">>>PointShape ", x, y
        super().__init__(x, y, parent)
        self._selectZone = 5
        self._visibleWhenSelected = True

    def Draw(self, dc, withChildren=True):
        """
        Draw the point on the dc.

        Args:
            dc:
            withChildren:
        """
        if self._visible or (self._visibleWhenSelected and self._selected):
            Shape.Draw(self, dc, False)
            x, y = self.GetPosition()
            if not self._selected:
                dc.DrawRectangle(x - 1, y - 1, 3, 3)
            else:
                dc.DrawRectangle(x - 3, y - 3, 7, 7)
            if withChildren:
                self.DrawChildren(dc)

    def GetSelectionZone(self):
        """
        Get the selection tolerance zone, in pixels.

        @return float : half of the selection zone.
        """
        return self._selectZone

    def SetSelectionZone(self, halfWidth):
        """
        Set the selection tolerance zone, in pixels.

        @param float halfWidth : half of the selection zone.
        """
        self._selectZone = halfWidth

    def Inside(self, x: float, y: float):
        """

        Args:
            x: x coordinate
            y: y coordinate

        Returns:          `True` if (x, y) is inside the shape.

        """
        ax, ay = self.GetPosition()     # GetPosition always returns absolute position
        zone = self._selectZone
        return (ax - zone < x < ax + zone) and (ay - zone < y < ay + zone)

    def SetVisibleWhenSelected(self, state: bool):
        """
        Set to True if you want the point to always be visible when it's selected.

        @param  state
        """
        self._visibleWhenSelected = state

    def GetVisibleWhenSelected(self):
        """
        Return the "visible when selected flag".

        @return bool True if the shape is always visible when selected
        """
        return self._visibleWhenSelected

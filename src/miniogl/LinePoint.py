
from typing import List

from miniogl.PointShape import PointShape


class LinePoint(PointShape):
    """
    This is a point guiding a line.
    """
    def __init__(self, x: int, y: int, parent=None):
        """

        Args:
            x:  abscissa of point
            y:  ordinate of point
            parent:     parent shape
        """
        #  print ">>>LinePoint ", x, y
        super().__init__(x, y, parent)
        self._lines: List = []    # a list of LineShape(s) passing through this point

    def AddLine(self, line):
        """
        Add a line to this point.

        @param  line
        """
        self._lines.append(line)

    def Detach(self):
        """
        Detach the point from the diagram
        This also removes the point from all the lines it belongs to.
        """
        PointShape.Detach(self)
        for line in self._lines:
            line.Remove(self)
        self._lines = []

    def GetLines(self):
        """
        Get the lines passing through this point.
        Modifying the returned list won't modify the point itself.

        @return LineShape []
        """
        return self._lines[:]

    def RemoveLine(self, line):
        """
        Remove a line from this point.

        @param line
        """
        if line in self._lines:
            self._lines.remove(line)

    def SetMoving(self, state: bool):
        """
        A non-moving shape will be redrawn faster when others are moved.
        See DiagramFrame.Refresh for more information.

        @param  state
        """
        PointShape.SetMoving(self, state)
        for line in self._lines:
            line.SetMoving(state)

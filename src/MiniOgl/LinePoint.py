

from MiniOgl.PointShape import PointShape


class LinePoint(PointShape):
    """
    This is a point guiding a line.


    @author Laurent Burgbacher <lb@alawa.ch>
    """
    def __init__(self, x, y, parent=None):
        """
        Constructor.

        @param double x, y : position of the point
        @param Shape parent : parent shape
        """
        #  print ">>>LinePoint ", x, y
        PointShape.__init__(self, x, y, parent)
        self._lines = []    # a list of LineShape passing through this point

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

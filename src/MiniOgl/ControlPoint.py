

from MiniOgl.LinePoint import LinePoint


class ControlPoint(LinePoint):
    """
    This is a point which guides lines.
    A control point must be linked to a line, it has no life by itself.
    If you remove the last line of a control point, the control point will
    be automatically erased.

    @author Laurent Burgbacher <lb@alawa.ch>
    """
    def __init__(self, x, y, parent=None):
        """
        Constructor.

        @param double x, y : position of the point
        @param Shape parent : parent shape
        """
        LinePoint.__init__(self, x, y, parent)
        self.SetVisible(False)

    def RemoveLine(self, line):
        """
        Remove a line from the point.
        If there are no more lines for this point, it is automatically
        detached.

        @param line line
        """
        super(ControlPoint, self).RemoveLine(line)
        if len(self._lines) == 0:
            self.Detach()

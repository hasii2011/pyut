
from org.pyut.miniogl.LinePoint import LinePoint


class ControlPoint(LinePoint):
    """
    This is a point which guides lines.
    A control point must be linked to a line, it has no life by itself.
    If you remove the last line of a control point, the control point will
    be automatically erased.
    """
    def __init__(self, x: float, y: float, parent=None):
        """

        Args:
            x:  x position of the point
            y:  y position of the point
            parent:     parent Shape
        """
        super().__init__(x, y, parent)
        self.SetVisible(False)

    def RemoveLine(self, line):
        """
        Remove a line from the point.
        If there are no more lines for this point, it is automatically
        detached.

        Args:
            line:   The line to remove
        """
        super(ControlPoint, self).RemoveLine(line)
        if len(self._lines) == 0:
            self.Detach()

    def __repr__(self):
        return f'ControlPoint@ {self._x},{self._y} {self._visible=}'

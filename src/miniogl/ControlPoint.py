
from miniogl.LinePoint import LinePoint


class ControlPoint(LinePoint):
    """
    This is a point which guides lines.
    A control point must be linked to a line, it has no life by itself.

    If you remove the last line of a control point, the control point will
    automatically be erased.
    """
    def __init__(self, x: int, y: int, parent=None):
        """

        Args:
            x:  abscissa of the point
            y:  ordinate of the point
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

    def __eq__(self, other) -> bool:

        if isinstance(other, ControlPoint):
            # noinspection PyProtectedMember
            if self._x == other._x and self._y == other._y and self._id == other._id:
                return True
            else:
                return False
        else:
            return False

    def __repr__(self):
        return f'ControlPoint@ {self._x},{self._y} {self._id=} {self._visible=}'

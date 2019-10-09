
from MiniOgl.PointShape import PointShape


__all__ = ["SizerShape"]


class SizerShape(PointShape):
    """
    A sizer, to resize other shapes.

    Exported methods:
    -----------------

    __init__(self, x, y, parent)
        Constructor.
    SetPosition(self, x, y)
        Change the position of the shape, if it's draggable.
    SetMoving(self, state)
        Set the moving flag.

    @author Laurent Burgbacher <lb@alawa.ch>
    """
    def __init__(self, x, y, parent):
        """
        Constructor.

        @param double x, y : position of the point
        @param Shape parent : parent shape
        """
        #  print ">>>SizerShape", x, y
        PointShape.__init__(self, x, y, parent)
        self._moving = True

    def Draw(self, dc, withChildren=True):
        #  TODO : Remove this. This is for debugging purpose. CD
        PointShape.Draw(self, dc, withChildren)
        # Note : This functions seems to be needed to display anchors
        #        on rectangle when moving them, but not for lines,
        #        single anchors, ...
        pass

    def SetPosition(self, x, y):
        """
        Change the position of the shape, if it's draggable.

        @param  x
        @param y : new position
        """
        self._parent.Resize(self, x, y)
        # the position of the sizer is not changed, because it is relative
        # to the parent

    def SetMoving(self, state):
        """
        Set the moving flag.
        If setting a sizer moving, the parent will also be set moving.

        @param
        @return
        @since 1.0
        """
        PointShape.SetMoving(self, True)
        # a sizer is always moving
        self._parent.SetMoving(state)

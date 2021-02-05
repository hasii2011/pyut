
from typing import cast
from typing import List
from typing import NewType
from typing import Tuple

from logging import Logger
from logging import getLogger
from wx import BLACK_PEN
from wx import DC
from wx import RED_PEN

from org.pyut.miniogl.LinePoint import LinePoint
from org.pyut.miniogl.Shape import Shape
from org.pyut.miniogl.AnchorPoint import AnchorPoint
from org.pyut.miniogl.ControlPoint import ControlPoint

ControlPoints = NewType('ControlPoints', List[ControlPoint])


class LineShape(Shape):
    """
    This is a line, passing through control points.
    The line must begin and end with AnchorPoints, and can be guided by
    ControlPoints.
    """
    clsLogger: Logger = getLogger(__name__)

    def __init__(self, srcAnchor: AnchorPoint, dstAnchor: AnchorPoint):
        """

        Args:
            srcAnchor: the source anchor of the line.
            dstAnchor: the destination anchor of the line.
        """
        super().__init__()
        self._srcAnchor = srcAnchor
        self._dstAnchor = dstAnchor

        self._controls: ControlPoints = cast(ControlPoints, [])
        self._drawArrow = True
        self._arrowSize = 8
        self._spline = False
        if srcAnchor:
            srcAnchor.AddLine(self)
        if dstAnchor:
            dstAnchor.AddLine(self)

    @property
    def sourceAnchor(self) -> AnchorPoint:
        return self._srcAnchor

    @sourceAnchor.setter
    def sourceAnchor(self, theNewValue: AnchorPoint):
        self._srcAnchor = theNewValue

    @property
    def destinationAnchor(self) -> AnchorPoint:
        return self._dstAnchor

    @destinationAnchor.setter
    def destinationAnchor(self, theNewValue: AnchorPoint):
        self._dstAnchor = theNewValue

    def SetSpline(self, state):
        """
        Use a spline instead of a line.

        @param bool state : True for a spline
        """
        self._spline = state

    def GetSpline(self):
        """
        Return True if a spline is drawn instead of a line.

        @return boolean
        """
        return self._spline

    def GetPosition(self):
        """
        Return the absolute position of the shape.
        It's in the diagram's coordinate system.
        For a line, it's the middle control point, or the middle of the two
        middle control points if there's an even number of those.

        @return (double, double)
        """
        points = self.GetSegments()
        middle = len(points) // 2
        if len(points) % 2 == 0:
            # even number of points, take the two at the center
            sx, sy = points[middle-1]
            dx, dy = points[middle]
            return (sx + dx) / 2, (sy + dy) / 2
        else:
            # odd number, take the middle point
            return points[middle]

    def AddControl(self, control: ControlPoint, after: LinePoint = None):
        """
        Add a control point to the line.
        The control point can be appended (last before the destination anchor)
        or inserted after a given control point.

        Args:
            control:  control point to add

            after:  This can be a control point after which to insert. This
            can also be the source of destination anchors. If it's the
            destination anchor, the point will be inserted BEFORE it.

        """
        if after is not None:
            if after is self._srcAnchor:
                self._controls.insert(0, control)
            elif after is self._dstAnchor:
                self._controls.append(control)
            else:
                i = self._controls.index(after)
                self._controls.insert(i+1, control)
        else:
            self._controls.append(control)
        control.AddLine(self)
        # add the point to the diagram so that it can be selected
        if self._diagram is not None:
            self._diagram.AddShape(control)

    def GetDestination(self):
        """
        Get the destination anchor.

        @return AnchorPoint
        """
        return self._dstAnchor

    def SetDestination(self, anchor):
        """
        Set the destination anchor.
        Note that the line must be removed from the previous destination!

        @param anchor
        """
        self._dstAnchor = anchor
        anchor.AddLine(self)

    def SetDrawArrow(self, draw: bool):
        """
        Set to True if you want to have an arrow head at the destination.

        @param  draw
        """
        self._drawArrow = draw

    def GetDrawArrow(self):
        """
        Tells if an arrow head will be drawn.

        @return bool
        """
        return self._drawArrow

    def SetArrowSize(self, size):
        """
        Set the size of the arrow head, in pixels.

        @param  size
        """
        self._arrowSize = size

    def GetArrowSize(self):
        """
        Get the size of the arrow head, in pixels.

        @return double size
        """
        return self._arrowSize

    def GetSource(self):
        """
        Get the source anchor.

        @return AnchorPoint source
        """
        return self._srcAnchor

    def SetSource(self, anchor):
        """
        Set the source anchor.
        Note that the line must be removed from the previous source!

        @param anchor
        """
        self._srcAnchor = anchor
        anchor.AddLine(self)

    def GetSegments(self):
        """
        Return a list of tuples which are the coordinates of the control points.

        Returns:  A list of float tuples

        """
        sp = self._srcAnchor.GetPosition()
        dp = self._dstAnchor.GetPosition()
        # LineShape.clsLogger.debug(f'GetSegments --  sp: {sp} dp: {dp}')
        return [sp] + list(map(lambda x: x.GetPosition(), self._controls)) + [dp]

    def GetControlPoints(self) -> ControlPoints:
        """
        This is a copy of the original list, modifying it won't change the
        line, but modifying the control points will !

        Returns:  a list of the control points.
        """
        return self._controls[:]

    def Draw(self, dc: DC, withChildren: bool = True):
        """
        Draw the line on the dc.

        Args:
            dc:
            withChildren:
        """
        if self._visible:

            super().Draw(dc=dc, withChildren=withChildren)
            line = self.GetSegments()
            if self._selected:
                dc.SetPen(RED_PEN)
            if self._spline:
                dc.DrawSpline(line)
            else:
                dc.DrawLines(line)
            for control in self._controls:
                control.Draw(dc)
            if self._selected:
                self._srcAnchor.Draw(dc)
                self._dstAnchor.Draw(dc)
            dc.SetPen(BLACK_PEN)
            if self._drawArrow:
                u, v = line[-2], line[-1]
                self.DrawArrow(dc, u, v)
            if withChildren:
                LineShape.clsLogger.debug(f'Draw Children')
                self.DrawChildren(dc)

    def DrawBorder(self, dc):
        """
        Draw the border of the shape, for fast rendering.
        """
        self.Draw(dc)

    def DrawArrow(self, dc: DC, u: Tuple[float, float], v: Tuple[float, float]):
        """
        Draw an arrow at the end of the segment uv.

        @param dc
        @param  u: points of the segment
        @param  v: points of the segment
        """
        from math import pi, atan, cos, sin
        pi_6 = pi/6
        points = []
        x1, y1 = u
        x2, y2 = v
        a = x2 - x1
        b = y2 - y1
        if abs(a) < 0.01:   # vertical segment
            if b > 0:
                alpha = -pi/2
            else:
                alpha = pi/2
        else:
            if a == 0:
                alpha = pi/2  # TODO ?
            else:
                alpha = atan(b/a)
        if a > 0:
            alpha += pi
        alpha1 = alpha + pi_6
        alpha2 = alpha - pi_6
        size = self._arrowSize
        points.append((x2 + size * cos(alpha1), y2 + size * sin(alpha1)))
        points.append((x2, y2))
        points.append((x2 + size * cos(alpha2), y2 + size * sin(alpha2)))
        dc.DrawPolygon(points)

    def Detach(self):
        """
        Detach the line and all its line points, including src and dst.
        """
        if self._diagram is not None and not self._protected:
            Shape.Detach(self)
            # while loop, because Detach will remove controls from the list on
            # which we iterate
            while self._controls:
                self._controls[0].Detach()
            self._srcAnchor.RemoveLine(self)
            self._dstAnchor.RemoveLine(self)

    def _removeControl(self, control: ControlPoint):
        """
        Remove a control point from the line.

        Args:
            control:
        """
        if control in self._controls:
            self._controls.remove(control)

    # noinspection PyUnusedLocal
    def _RemoveAnchor(self, anchor):
        """
        Remove an anchor point.

        @param anchor
        """
        self.Detach()

    def RemoveAllControlPoints(self):
        """
        Remove all the control points of the line.
        """
        while self._controls:
            self._removeControl(self._controls[0])

    def Remove(self, point):
        """
        Remove a point from the line, either a anchor or control.
        If the remove point is an anchor, the line itself will be detached.

        Args:
            point: The point
        """
        if isinstance(point, AnchorPoint):
            self._RemoveAnchor(point)
        elif isinstance(point, ControlPoint):
            self._removeControl(point)

    def Inside(self, x, y):
        """
        True if (x, y) is inside the line.
        A tolerance of 4 pixels is used.

        @param  x
        @param  y

        @return bool
        """
        def InsideBoundingBox(x, y, a, b):
            # check if the point (x, y) is inside a box of origin (0, 0) and
            # diagonal (a, b) with a tolerance of 4
            ma, mb = a / 2, b / 2
            if a > 0:
                w = max(4, a - 8)
            else:
                w = min(-4, a + 8)
            if b > 0:
                h = max(4, b - 8)
            else:
                h = min(-4, b + 8)
            topLeftX = ma - w / 2
            topLeftY = mb - h / 2
            i = x > topLeftX
            j = x > topLeftX + w
            k = y > topLeftY
            ll = y > topLeftY + h

            return (i + j) == 1 and (k + ll) == 1

        from math import sqrt

        def InsideSegment(x, y, a, b):
            den = sqrt(a*a + b*b)
            if den != 0.0:
                d = (x*b - y*a) / den
            else:
                return False
            return abs(d) < 4.0

        # go through each segment of the line
        points = [self._srcAnchor] + self._controls + [self._dstAnchor]
        while len(points) > 1:
            x1, y1 = points[0].GetPosition()
            x2, y2 = points[1].GetPosition()
            a, b, xx, yy = x2 - x1, y2 - y1, x - x1, y - y1
            points = points[1:]
            if InsideBoundingBox(xx, yy, a, b) and InsideSegment(xx, yy, a, b):
                return True
        return False

    def SetSelected(self, state: bool = True):
        """
        Select the shape.

        @param  state
        """
        Shape.SetSelected(self, state)
        for ctrl in self._controls:
            ctrl.SetVisible(state)

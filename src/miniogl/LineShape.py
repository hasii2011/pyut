
from typing import List
from typing import NewType
from typing import Tuple
from typing import Union

from logging import Logger
from logging import getLogger

from wx import BLACK_PEN
from wx import DC
from wx import RED_PEN

from miniogl.Common import Common
from miniogl.Common import CommonLine
from miniogl.Common import CommonPoint
from miniogl.LinePoint import LinePoint
from miniogl.Shape import Shape
from miniogl.AnchorPoint import AnchorPoint
from miniogl.ControlPoint import ControlPoint

ControlPoints = NewType('ControlPoints', List[LinePoint])


class LineShape(Shape, Common):
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
        Shape.__init__(self)
        self._srcAnchor: AnchorPoint = srcAnchor
        self._dstAnchor: AnchorPoint = dstAnchor

        self._controls:  ControlPoints = ControlPoints([])
        self._drawArrow: bool = True
        self._arrowSize: int = 8
        self._spline:    bool = False
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
            return (sx + dx) // 2, (sy + dy) // 2
        else:
            # odd number, take the middle point
            return points[middle]

    def AddControl(self, control: ControlPoint, after: Union[ControlPoint, LinePoint] = None):
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

        Returns:  A list of int tuples

        """
        sp = self._srcAnchor.GetPosition()
        dp = self._dstAnchor.GetPosition()
        # LineShape.clsLogger.debug(f'GetSegments --  sp: {sp} dp: {dp}')
        retList = [sp] + list(map(lambda x: x.GetPosition(), self._controls)) + [dp]
        return retList

    def GetControlPoints(self) -> ControlPoints:
        """
        This is a copy of the original list, modifying it won't change the
        line, but modifying the control points will !

        Returns:  a list of the control points.
        """
        return ControlPoints(self._controls[:])

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
                # LineShape.clsLogger.debug(f'Call DrawChildren()')
                self.DrawChildren(dc)

    def DrawBorder(self, dc):
        """
        Draw the border of the shape, for fast rendering.
        """
        self.Draw(dc)

    def DrawArrow(self, dc: DC, u: Tuple[int, int], v: Tuple[int, int]):
        """
        Draw an arrow at the end of the segment uv.

        Args:
            dc:
            u: points of the segment
            v: points of the segment
        """
        from math import pi, atan, cos, sin

        pi_6: float = pi / 6
        x1, y1 = u
        x2, y2 = v
        a = x2 - x1
        b = y2 - y1
        if abs(a) < 0.01:   # vertical segment
            if b > 0:
                alpha: float = -pi / 2
            else:
                alpha = pi / 2
        else:
            if a == 0:
                alpha = pi / 2  # TODO ?
            else:
                alpha = atan(b/a)
        if a > 0:
            alpha += pi
        alpha1: float = alpha + pi_6
        alpha2: float = alpha - pi_6
        size:   int   = self._arrowSize

        points: List[Tuple[int, int]] = [
            (x2 + round(size * cos(alpha1)), y2 + round(size * sin(alpha1))),
            (x2, y2),
            (x2 + round(size * cos(alpha2)), y2 + round(size * sin(alpha2)))
                                         ]

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
        Remove a point from the line, either an anchor or control.
        If the remove point is an anchor, the line itself will be detached.

        Args:
            point: The point
        """
        if isinstance(point, AnchorPoint):
            self._RemoveAnchor(point)
        elif isinstance(point, ControlPoint):
            self._removeControl(point)

    def Inside(self, x: int, y: int) -> bool:
        """
        A tolerance of 4 pixels is used.

        Args:
            x:  abscissa click point
            y:  ordinate click point

        Returns: True if (x, y) is inside the line.
        """
        # Go through each segment of the line
        points: ControlPoints = self._mergeControlPoints()

        while len(points) > 1:

            x1, y1 = points[0].GetPosition()
            x2, y2 = points[1].GetPosition()

            startPoint: CommonPoint = CommonPoint(x=x1, y=y1)
            endPoint:   CommonPoint = CommonPoint(x=x2, y=y2)
            checkLine:  CommonLine  = CommonLine(start=startPoint, end=endPoint)

            clickDiffStartX, clickDiffStartY, diffX, diffY = self.setupInsideCheck(clickPointX=x, clickPointY=y, line=checkLine)
            # points = points[1:]
            points.pop(0)       # do this method instead of above to quiesce mypy

            if self.insideBoundingBox(clickDiffStartX, clickDiffStartY, diffX, diffY) and self.insideSegment(clickDiffStartX, clickDiffStartY, diffX, diffY):
                return True

        return False

    def _mergeControlPoints(self) -> ControlPoints:
        """
        points: ControlPoints = [self._srcAnchor] + self._controls + [self._dstAnchor]
        do this method instead of above to quiesce mypy

        Returns:  All the shape control points
        """
        points: ControlPoints = ControlPoints([])

        points.append(self._srcAnchor)

        for cp in self._controls:
            points.append(cp)

        points.append(self._dstAnchor)

        return points

    def SetSelected(self, state: bool = True):
        """
        Select the shape (default) or not

        Args:
            state:
        """
        Shape.SetSelected(self, state)
        for ctrl in self._controls:
            ctrl.SetVisible(state)

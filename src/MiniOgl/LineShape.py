from MiniOgl.Shape import Shape
from MiniOgl.AnchorPoint import AnchorPoint
from MiniOgl.ControlPoint import ControlPoint

import wx

#
# Copyright 2002, Laurent Burgbacher, Eivd.
# Visit http://www.eivd.ch
#
# This file is part of MiniOgl.
#
# MiniOgl is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# MiniOgl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MiniOgl; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

__author__    = "Laurent Burgbacher, lb@alawa.ch, Eivd"
__copyright__ = "Copyright 2002, Laurent Burgbacher, Eivd"
__license__   = "Released under the terms of the GNU General Public Licence V2"
__date__      = "2002-10-15"
__version__   = "$Id: LineShape.py,v 1.7 2005/03/22 07:56:42 dutoitc Exp $"

__all__ = ["LineShape"]


class LineShape(Shape):
    """
    This is a line, passing through control points.
    The line must begin and end with AnchorPoints, and can be guided by
    ControlPoints.

    Exported methods:
    -----------------

    __init__(self, srcAnchor, dstAnchor)
        Constructor.
    SetSpline(self, state)
        Use a spline instead of a line.
    GetSpline(self)
        Return True if a spline is drawn instead of a line.
    GetPosition(self)
        Return the absolute position of the shape.
    AddControl(self, control, after=None)
        Add a control point to the line.
    GetDestination(self)
        Get the destination anchor.
    SetDestination(self, anchor)
        Set the destination anchor.
    SetDrawArrow(self, draw)
        Set to True if you want to have an arrow head at the destination.
    GetDrawArrow(self)
        Tells if an arrow head will be drawn.
    SetArrowSize(self, size)
        Set the size of the arrow head, in pixels.
    GetArrowSize(self)
        Get the size of the arrow head, in pixels.
    GetSource(self)
        Get the source anchor.
    SetSource(self, anchor)
        Set the source anchor.
    GetSegments(self)
        Return a list of tuples which are the coordinates of the control points.
    GetControlPoints(self)
        Return a list of the control points.
    Draw(self, dc, withChildren=True)
        Draw the line on the dc.
    DrawBorder(self, dc)
        Draw the border of the shape, for fast rendering.
    DrawArrow(self, dc, u, v)
        Draw an arrow at the end of the segment uv.
    Detach(self)
        Detach the line and all its line points, including src and dst.
    RemoveAllControlPoints(self)
        Remove all the control points of the line.
    Remove(self, point)
        Remove a point from the line, either a anchor or control.
    Inside(self, x, y)
        True if (x, y) is inside the line.

    @author Laurent Burgbacher <lb@alawa.ch>
    """
    def __init__(self, srcAnchor, dstAnchor):
        """
        Constructor.

        @param AnchorPoint srcAnchor, dstAnchor : the source and destination
            of the line.
        """
        Shape.__init__(self)
        self._src = srcAnchor
        self._dst = dstAnchor
        self._controls = []
        self._drawArrow = True
        self._arrowSize = 8
        self._spline = False
        if srcAnchor:
            srcAnchor.AddLine(self)
        if dstAnchor:
            dstAnchor.AddLine(self)

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

    def AddControl(self, control, after=None):
        """
        Add a control point to the line.
        The control point can be appended (last before the destination anchor)
        or inserted after a given control point.

        @param ControlPoint control : control point to add. This can
        @param LinePoint after : control point after which to insert. This
            can also be the source of destination anchors. If it's the
            destination anchor, the point will be inserted BEFORE it.
        """
        if after is not None:
            if after is self._src:
                self._controls.insert(0, control)
            elif after is self._dst:
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
        return self._dst

    def SetDestination(self, anchor):
        """
        Set the destination anchor.
        Note that the line must be removed from the previous destination!

        @param AnchorPoint
        """
        self._dst = anchor
        anchor.AddLine(self)

    def SetDrawArrow(self, draw):
        """
        Set to True if you want to have an arrow head at the destination.

        @param bool draw
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

        @param double size
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
        return self._src

    def SetSource(self, anchor):
        """
        Set the source anchor.
        Note that the line must be removed from the previous source!

        @param AnchorPoint
        """
        self._src = anchor
        anchor.AddLine(self)

    def GetSegments(self):
        """
        Return a list of tuples which are the coordinates of the control points.

        @return (double, double) []
        """
        sp = self._src.GetPosition()
        dp = self._dst.GetPosition()
        return [sp] + map(lambda x: x.GetPosition(), self._controls) + [dp]

    def GetControlPoints(self):
        """
        Return a list of the control points.
        This is a copy of the original list, modifying it won't change the
        line, but modifying the control points will !

        @return ControlPoint []
        """
        return self._controls[:]

    def Draw(self, dc, withChildren=True):
        """
        Draw the line on the dc.

        @param wx.DC dc
        """
        if self._visible:
            # changed False to True by C.Dutoit to display cardinality
            #Shape.Draw(self, dc, False)
            Shape.Draw(self, dc, False)
            line = self.GetSegments()
            if self._selected:
                dc.SetPen(wx.RED_PEN)
            if self._spline:
                dc.DrawSpline(line)
            else:
                dc.DrawLines(line)
            for control in self._controls:
                control.Draw(dc)
            if self._selected:
                self._src.Draw(dc)
                self._dst.Draw(dc)
            dc.SetPen(wx.BLACK_PEN)
            if self._drawArrow:
                u, v = line[-2], line[-1]
                self.DrawArrow(dc, u, v)
            if withChildren:
                self.DrawChildren(dc)

    def DrawBorder(self, dc):
        """
        Draw the border of the shape, for fast rendering.
        """
        self.Draw(dc)

    def DrawArrow(self, dc, u, v):
        """
        Draw an arrow at the end of the segment uv.

        @param wx.DC dc
        @param (double, double) u, v : points of the segment
        """
        from math import pi, atan, cos, sin
        pi_6 = pi/6
        points = []
        x1, y1 = u
        x2, y2 = v
        a = x2 - x1
        b = y2 - y1
        if abs(a) < 0.01: # vertical segment
            if b > 0:
                alpha = -pi/2
            else:
                alpha = pi/2
        else:
            if a==0:
                alpha = pi/2 # TODO ?
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
            self._src.RemoveLine(self)
            self._dst.RemoveLine(self)

    def _RemoveControl(self, control):
        """
        Remove a control point from the line.

        @param ControlPoint control
        """
        if control in self._controls:
            self._controls.remove(control)

    def _RemoveAnchor(self, anchor):
        """
        Remove an anchor point.

        @param AnchorPoint anchor
        """
        self.Detach()

    def RemoveAllControlPoints(self):
        """
        Remove all the control points of the line.
        """
        while self._controls:
            self._RemoveControl(self._controls[0])

    def Remove(self, point):
        """
        Remove a point from the line, either a anchor or control.
        If the remove point is an anchor, the line itself will be detached.

        @param LinePoint point
        """
        if isinstance(point, AnchorPoint):
            self._RemoveAnchor(point)
        elif isinstance(point, ControlPoint):
            self._RemoveControl(point)

    def Inside(self, x, y):
        """
        True if (x, y) is inside the line.
        A tolerance of 4 pixels is used.

        @param double x, y
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
            l = y > topLeftY + h

            return (i + j) == 1 and (k + l) == 1

        from math import sqrt
        def InsideSegment(x, y, a, b):
            den = sqrt(a*a + b*b)
            if den != 0.0:
                d = (x*b - y*a) / den
            else:
                return False
            return abs(d) < 4.0

        # go through each segment of the line
        points = [self._src] + self._controls + [self._dst]
        while len(points) > 1:
            x1, y1 = points[0].GetPosition()
            x2, y2 = points[1].GetPosition()
            a, b, xx, yy = x2 - x1, y2 - y1, x - x1, y - y1
            points = points[1:]
            if InsideBoundingBox(xx, yy, a, b) and InsideSegment(xx, yy, a, b):
                return True
        return False

    def SetSelected(self, state=True):
        """
        Select the shape.

        @param bool state
        """
        Shape.SetSelected(self, state)
        for ctrl in self._controls:
            ctrl.SetVisible(state)


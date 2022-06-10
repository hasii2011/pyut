
"""
This is a suite of small classes used to draw RotatableShapes.
Each one represent a simple shape (line, rectangle, circle, ellipse...) or
abstract command (color change).
"""


class VShape:
    """
    Base VShape class.

    """
    def __init__(self):
        self._data = ()

    def Convert(self, angle, x, y):
        T = [
            [1, 0, 0, 1], [0, -1, 1, 0], [-1, 0, 0, -1], [0, 1, -1, 0]
        ]
        nx = T[angle][0] * x + T[angle][1] * y
        ny = T[angle][2] * x + T[angle][3] * y
        return nx, ny

    def SetAngle(self, angle):
        pass

    def Scale(self, scale, data):
        return map(lambda x: x * scale, data)


class VRectangle(VShape):
    def __init__(self, x, y, w, h):
        VShape.__init__(self)
        self._data = (x, y, w, h)

    def SetAngle(self, angle):
        x, y, w, h = self._data
        x, y = self.Convert(angle, x, y)
        w, h = self.Convert(angle, w, h)
        self._data = (x, y, w, h)

    def Draw(self, dc, ox, oy, scale):
        if scale == 1:
            x, y, w, h = self._data
        else:
            x, y, w, h = self.Scale(scale, self._data)
        dc.DrawRectangle(ox + x, oy + y, w, h)


class VEllipse(VShape):
    def __init__(self, x, y, w, h):
        VShape.__init__(self)
        self._data = (x, y, w, h)

    def SetAngle(self, angle):
        x, y, w, h = self._data
        x, y = self.Convert(angle, x, y)
        w, h = self.Convert(angle, w, h)
        self._data = (x, y, w, h)

    def Draw(self, dc, ox, oy, scale):
        if scale == 1:
            x, y, w, h = self._data
        else:
            x, y, w, h = self.Scale(scale, self._data)
        dc.DrawEllipse(ox + x, oy + y, w, h)


class VCircle(VShape):
    def __init__(self, x, y, r):
        VShape.__init__(self)
        self._data = (x, y, r)

    def SetAngle(self, angle):
        x, y, r = self._data
        x, y = self.Convert(angle, x, y)
        self._data = (x, y, r)

    def Draw(self, dc, ox, oy, scale):
        if scale == 1:
            x, y, r = self._data
        else:
            x, y, r = self.Scale(scale, self._data)
        dc.DrawCircle(ox + x, oy + y, r)


class VArc(VShape):
    def __init__(self, x1, y1, x2, y2, xc, yc):
        VShape.__init__(self)
        self._data = (x1, y1, x2, y2, xc, yc)

    def SetAngle(self, angle):
        x1, y1, x2, y2, xc, yc = self._data
        x1, y1 = self.Convert(angle, x1, y1)
        x2, y2 = self.Convert(angle, x2, y2)
        xc, yc = self.Convert(angle, xc, yc)
        self._data = (x1, y1, x2, y2, xc, yc)

    def Draw(self, dc, ox, oy, scale):
        if scale == 1:
            x1, y1, x2, y2, xc, yc = self._data
        else:
            x1, y1, x2, y2, xc, yc = self.Scale(scale, self._data)
        dc.DrawArc(ox + x1, oy + y1, ox + x2, oy + y2, ox + xc, oy + yc)


class VEllipticArc(VShape):
    def __init__(self, x, y, w, h, start, end):
        VShape.__init__(self)
        self._data = (x, y, w, h, start, end)

    def SetAngle(self, angle):
        x, y, w, h, start, end  = self._data
        x, y = self.Convert(angle, x, y)
        w, h = self.Convert(angle, w, h)
        start -= angle * 90
        end -= angle * 90
        self._data = (x, y, w, h, start, end)

    def Draw(self, dc, ox, oy, scale):
        if scale == 1:
            x, y, w, h, start, end  = self._data
        else:
            x, y, w, h = self.Scale(scale, self._data[0:4])
            start, end = self._data[4:]
        dc.DrawEllipticArc(ox + x, oy + y, w, h, start, end)


class VLineLength(VShape):
    def __init__(self, x, y, w, h):
        VShape.__init__(self)
        self._data = (x, y, w, h)

    def SetAngle(self, angle):
        x, y, w, h = self._data
        x, y = self.Convert(angle, x, y)
        w, h = self.Convert(angle, w, h)
        self._data = (x, y, w, h)

    def Draw(self, dc, ox, oy, scale):
        if scale == 1:
            x, y, w, h = self._data
        else:
            x, y, w, h = self.Scale(scale, self._data)
        x, y = ox + x, oy + y
        dc.DrawLine(x, y, x + w, y + h)


class VLineDest(VShape):
    def __init__(self, sx, sy, dx, dy):
        VShape.__init__(self)
        self._data = (sx, sy, dx, dy)

    def SetAngle(self, angle):
        sx, sy, dx, dy = self._data
        sx, sy = self.Convert(angle, sx, sy)
        dx, dy = self.Convert(angle, dx, dy)
        self._data = (sx, sy, dx, dy)

    def Draw(self, dc, ox, oy, scale):
        if scale == 1:
            sx, sy, dx, dy = self._data
        else:
            sx, sy, dx, dy = self.Scale(scale, self._data)
        dc.DrawLine(ox + sx, oy + sy, ox + dx, oy + dy)


class VPolygon(VShape):
    def __init__(self, points):
        VShape.__init__(self)
        self._data = points

    def SetAngle(self, angle):
        new = []
        for x, y in self._data:
            x, y = self.Convert(angle, x, y)
            new.append((x, y))
        self._data = tuple(new)

    def Draw(self, dc, ox, oy, scale):
        if scale == 1:
            points = self._data
        else:
            points = []
            for x, y in self._data:
                points.append(tuple(self.Scale(scale, (x, y))))
        dc.DrawPolygon(points, ox, oy)


class VPen(VShape):
    def __init__(self, pen):
        VShape.__init__(self)
        self._pen = pen

    # noinspection PyUnusedLocal
    def Draw(self, dc, x, y, scale=1):
        dc.SetPen(self._pen)


class VBrush(VShape):
    def __init__(self, brush):
        VShape.__init__(self)
        self._brush = brush

    # noinspection PyUnusedLocal
    def Draw(self, dc, x, y, scale=1):
        dc.SetBrush(self._brush)

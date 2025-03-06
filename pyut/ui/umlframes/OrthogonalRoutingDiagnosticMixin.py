
from typing import List
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from miniogl.MiniOglColorEnum import MiniOglColorEnum
from wx import BLACK_PEN
from wx import Brush
from wx import DC
from wx import PaintDC
from wx import Pen
from wx import Point

from miniogl.DiagramFrame import DiagramFrame


Points      = NewType('Points',      List[Point])
IntegerList = NewType('IntegerList', List[int])


@dataclass
class Rectangle:
    left:   int = 0
    top:    int = 0
    width:  int = 0
    height: int = 0


Rectangles = NewType('Rectangles', List[Rectangle])

REFERENCE_POINT_RADIUS: int = 4


class OrthogonalRoutingDiagnosticMixin:
    """

    """
    def __init__(self):
        self.mixinLogger: Logger = getLogger(__name__)

        self._showReferencePoints: bool = False
        self._showRulers:          bool = False
        self._showRouteGrid:       bool = False

        self._referencePoints:     Points      = cast(Points, None)
        self._horizontalRulers:    IntegerList = cast(IntegerList, None)
        self._verticalRulers:      IntegerList = cast(IntegerList, None)
        self._diagramBounds:       Rectangle   = cast(Rectangle, None)
        self._routeGrid:           Rectangles  = cast(Rectangles, None)

    @property
    def showReferencePoints(self) -> bool:
        raise AttributeError("This property is write-only.")

    @showReferencePoints.setter
    def showReferencePoints(self, value: bool):
        self._showReferencePoints = value

    @property
    def showRulers(self) -> bool:
        raise AttributeError("This property is write-only.")

    @showRulers.setter
    def showRulers(self, value: bool):
        self._showRulers = value

    @property
    def showRouteGrid(self) -> bool:
        raise AttributeError("This property is write-only.")

    @showRouteGrid.setter
    def showRouteGrid(self, showRouteGrid: bool):
        self._showRouteGrid = showRouteGrid

    @property
    def referencePoints(self) -> Points:
        raise AttributeError("This property is write-only.")

    @referencePoints.setter
    def referencePoints(self, points: Points):
        self._referencePoints = points

    @property
    def horizontalRulers(self) -> IntegerList:
        raise AttributeError("This property is write-only.")

    @horizontalRulers.setter
    def horizontalRulers(self, newRulers: IntegerList):
        self._horizontalRulers = newRulers

    @property
    def verticalRulers(self):
        raise AttributeError("This property is write-only.")

    @verticalRulers.setter
    def verticalRulers(self, newRulers: IntegerList):
        self._verticalRulers = newRulers

    @property
    def diagramBounds(self) -> Rectangle:
        raise AttributeError("This property is write-only.")

    @diagramBounds.setter
    def diagramBounds(self, newBounds: Rectangle):
        self._diagramBounds = newBounds

    @property
    def routeGrid(self) -> Rectangles:
        raise AttributeError("This property is write-only.")

    @routeGrid.setter
    def routeGrid(self, routeGrid: Rectangles):
        self._routeGrid = routeGrid

    def OnPaint(self, umlFrame: DiagramFrame):

        if self._showDiagnostics() is True:
            w, h = umlFrame.GetSize()

            mem: DC = umlFrame.CreateDC(False, w, h)
            mem.SetBackground(Brush(umlFrame.GetBackgroundColour()))
            mem.Clear()
            x, y = umlFrame.CalcUnscrolledPosition(0, 0)

            if self._showReferencePoints is True:
                self._drawReferencePoints(dc=mem)
            # if self._showRulers is True:
            #     self._drawRulers(dc=mem)
            # if self._showRouteGrid is True:
            #     self._drawRouteGrid(dc=mem)

            paintDC: PaintDC = PaintDC(self)
            umlFrame.Redraw(mem)
            paintDC.Blit(0, 0, w, h, mem, x, y)

    def _drawReferencePoints(self, dc: DC):
        savePen:   Pen   = dc.GetPen()
        saveBrush: Brush = dc.GetBrush()

        dc.SetPen(BLACK_PEN)
        dc.SetBrush(Brush(MiniOglColorEnum.toWxColor(MiniOglColorEnum.ALICE_BLUE)))

        points: Points = self._referencePoints

        for pt in points:
            point: Point = cast(Point, pt)
            x, y = point.Get()
            dc.DrawCircle(x=x, y=y, radius=REFERENCE_POINT_RADIUS)

        dc.SetPen(savePen)
        dc.SetBrush(saveBrush)

    def _showDiagnostics(self) -> bool:

        show: bool = False

        if self._showReferencePoints is True or self._showRulers is True or self._showRouteGrid is True:
            show = True

        return show

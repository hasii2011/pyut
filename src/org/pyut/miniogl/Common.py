
from typing import Tuple

from dataclasses import dataclass

from math import sqrt


@dataclass
class CommonPoint:

    x: int = 0
    y: int = 0


@dataclass
class CommonLine:

    start: CommonPoint = CommonPoint(0, 0)
    end:   CommonPoint = CommonPoint(0, 0)


class Common:

    CLICK_TOLERANCE: float = 4.0
    """
    A `mix-in` class to share common code currently between a LineShape and a shape that is
    almost a line.  :-)

    """

    def setupInsideCheck(self, clickPointX: int, clickPointY: int, line: CommonLine) -> Tuple[int, int, int, int]:

        x1: int = line.start.x
        y1: int = line.start.y
        x2: int = line.end.x
        y2: int = line.end.y

        diffX: int = x2 - x1
        diffY: int = y2 - y1

        clickDiffStartX: int = clickPointX - x1     # x - x1
        clickDiffStartY: int = clickPointY - y1     # y - y1

        return clickDiffStartX, clickDiffStartY, diffX, diffY

    def insideSegment(self, clickDiffStartX: float, clickDiffStartY: float, diffX: float, diffY: float) -> bool:
        """

        Args:
            clickDiffStartX:
            clickDiffStartY:
            diffX:  Difference between the line's end X coordinate and the start X coordinate
            diffY:  Difference between the line's end Y coordinate and the start Y coordinate

        Returns: `True` if the click points is withing the click tolerance; else `False`
        """
        den: float = sqrt(diffX * diffX + diffY * diffY)

        if den != 0.0:
            d: float = (clickDiffStartX * diffY - clickDiffStartY * diffX) / den
        else:
            return False
        return abs(d) < Common.CLICK_TOLERANCE

    def insideBoundingBox(self, clickDiffStartX: float, clickDiffStartY: float, diffX: float, diffY: float):
        """
        Check if the point (x, y) is inside a box of origin (0, 0) and
        diagonal (a, b) with a tolerance of CLICK_TOLERANCE

        Args:
            clickDiffStartX:
            clickDiffStartY:
            diffX:  Difference between the line's end X coordinate and the start X coordinate
            diffY:  Difference between the line's end Y coordinate and the start Y coordinate

        Returns:  `True` if the click point is in the bounding box else `False`

        """
        ma: float = diffX / 2
        mb: float = diffY / 2

        if diffX > 0:
            w: int = max(4, int(diffX - 8))
        else:
            w = min(-4, int(diffX + 8))

        if diffY > 0:
            h: int = max(4, int(diffY - 8))
        else:
            h = min(-4, int(diffY + 8))

        topLeftX: float = ma - w / 2
        topLeftY: float = mb - h / 2

        i:  bool = clickDiffStartX > topLeftX
        j:  bool = clickDiffStartX > topLeftX + w
        k:  bool = clickDiffStartY > topLeftY
        ll: bool = clickDiffStartY > topLeftY + h

        ans: bool = (i + j) == 1 and (k + ll) == 1
        return ans

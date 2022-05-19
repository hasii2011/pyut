
from typing import cast

from dataclasses import dataclass

from wx import Point

from miniogl.Shape import Shape


@dataclass
class ShapeSelectedEventData:

    shape:    Shape = cast(Shape, None)
    position: Point = cast(Point, None)

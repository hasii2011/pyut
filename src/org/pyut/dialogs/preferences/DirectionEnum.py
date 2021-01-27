
from enum import Enum

from wx import HORIZONTAL
from wx import VERTICAL


class DirectionEnum(Enum):
    """
    A type safe wrapper for wxPython's int values
    """

    Horizontal = HORIZONTAL
    Vertical   = VERTICAL

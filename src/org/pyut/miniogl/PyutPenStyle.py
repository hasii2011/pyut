from enum import Enum

from wx import PENSTYLE_CROSS_HATCH
from wx import PENSTYLE_DOT
from wx import PENSTYLE_DOT_DASH
from wx import PENSTYLE_HORIZONTAL_HATCH
from wx import PENSTYLE_LONG_DASH
from wx import PENSTYLE_SHORT_DASH
from wx import PENSTYLE_SOLID
from wx import PENSTYLE_VERTICAL_HATCH

from wx._core import PenStyle


class PyutPenStyle(Enum):

    SOLID                   = 'Solid'
    DOT                     = 'Dot'
    LONG_DASH               = 'Long Dash'
    SHORT_DASH              = 'Short Dash'
    DOT_DASH                = 'Dot Dash'
    USER_DASH               = 'User Dash'

    CROSS_HATCH             = 'Cross Hatch'
    HORIZONTAL_HATCH        = 'Horizontal Hatch'
    VERTICAL_HATCH          = 'Vertical Hatch'

    @staticmethod
    def toWxPenStyle(penStyleEnum: 'PyutPenStyle') -> PenStyle:

        if penStyleEnum == PyutPenStyle.SOLID:
            wxPenStyle: PenStyle = PENSTYLE_SOLID

        elif penStyleEnum == PyutPenStyle.DOT:
            wxPenStyle: PenStyle = PENSTYLE_DOT

        elif penStyleEnum == PyutPenStyle.LONG_DASH:
            wxPenStyle: PenStyle = PENSTYLE_LONG_DASH

        elif penStyleEnum == PyutPenStyle.SHORT_DASH:
            wxPenStyle: PenStyle = PENSTYLE_SHORT_DASH

        elif penStyleEnum == PyutPenStyle.DOT_DASH:
            wxPenStyle: PenStyle = PENSTYLE_DOT_DASH

        elif penStyleEnum == PyutPenStyle.CROSS_HATCH:
            wxPenStyle: PenStyle = PENSTYLE_CROSS_HATCH

        elif penStyleEnum == PyutPenStyle.HORIZONTAL_HATCH:
            wxPenStyle: PenStyle = PENSTYLE_HORIZONTAL_HATCH

        elif penStyleEnum == PyutPenStyle.VERTICAL_HATCH:
            wxPenStyle: PenStyle = PENSTYLE_VERTICAL_HATCH

        else:
            wxPenStyle: PenStyle = PENSTYLE_SOLID

        return wxPenStyle

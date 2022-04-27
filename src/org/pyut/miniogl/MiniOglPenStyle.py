from enum import Enum

from wx import PENSTYLE_CROSS_HATCH
from wx import PENSTYLE_DOT
from wx import PENSTYLE_DOT_DASH
from wx import PENSTYLE_HORIZONTAL_HATCH
from wx import PENSTYLE_LONG_DASH
from wx import PENSTYLE_SHORT_DASH
from wx import PENSTYLE_SOLID
from wx import PENSTYLE_VERTICAL_HATCH


class MiniOglPenStyle(Enum):

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
    def toWxPenStyle(penStyleEnum: 'MiniOglPenStyle'):

        if penStyleEnum == MiniOglPenStyle.SOLID:
            wxPenStyle = PENSTYLE_SOLID

        elif penStyleEnum == MiniOglPenStyle.DOT:
            wxPenStyle = PENSTYLE_DOT

        elif penStyleEnum == MiniOglPenStyle.LONG_DASH:
            wxPenStyle = PENSTYLE_LONG_DASH

        elif penStyleEnum == MiniOglPenStyle.SHORT_DASH:
            wxPenStyle = PENSTYLE_SHORT_DASH

        elif penStyleEnum == MiniOglPenStyle.DOT_DASH:
            wxPenStyle = PENSTYLE_DOT_DASH

        elif penStyleEnum == MiniOglPenStyle.CROSS_HATCH:
            wxPenStyle = PENSTYLE_CROSS_HATCH

        elif penStyleEnum == MiniOglPenStyle.HORIZONTAL_HATCH:
            wxPenStyle = PENSTYLE_HORIZONTAL_HATCH

        elif penStyleEnum == MiniOglPenStyle.VERTICAL_HATCH:
            wxPenStyle = PENSTYLE_VERTICAL_HATCH

        else:
            wxPenStyle = PENSTYLE_SOLID

        return wxPenStyle

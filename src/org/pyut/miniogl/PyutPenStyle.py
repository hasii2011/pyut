from enum import Enum


class PyutPenStyle(Enum):

    SOLID                   = 'Solid'
    DOT                     = 'Dot'
    LONG_DASH               = 'Long Dash'
    SHORT_DASH              = 'Short Dash'
    DOT_DASH                = 'Dot Dash'
    USER_DASH               = 'User Dash'
    TRANSPARENT             = 'Transparent'
    STIPPLE_MASK_OPAQUE     = 'Stipple Mask Opaque'
    STIPPLE_MASK            = 'Stipple Mask'
    STIPPLE                 = 'Stipple'

    BACKWARD_DIAGONAL_HATCH = 'Backward Hatch'
    CROSS_DIAGONAL_HATCH    = 'Cross Diagonal Hatch'
    FORWARD_DIAGONAL_HATCH  = 'Forward Diagonal Hatch'
    CROSS_HATCH             = 'Cross Hatch'
    HORIZONTAL_HATCH        = 'Horizontal Hatch'
    VERTICAL_HATCH          = 'Vertical Hatch'

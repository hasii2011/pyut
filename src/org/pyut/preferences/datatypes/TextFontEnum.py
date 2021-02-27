
from enum import Enum

from wx import FONTFAMILY_DEFAULT
from wx import FONTFAMILY_MODERN
from wx import FONTFAMILY_ROMAN
from wx import FONTFAMILY_SCRIPT
from wx import FONTFAMILY_SWISS
from wx import FONTFAMILY_TELETYPE


class TextFontEnum(Enum):
    """
    A type safe wrapper for wxPython's Font type integers
    """
    SWISS    = 'Swiss'
    MODERN   = 'Modern'
    ROMAN    = 'Roman'
    SCRIPT   = 'Script'
    TELETYPE = 'Teletype'

    @classmethod
    def toWxType(cls, enumValue: 'TextFontEnum') -> int:

        if enumValue == TextFontEnum.SWISS:
            return FONTFAMILY_SWISS
        elif enumValue == TextFontEnum.MODERN:
            return FONTFAMILY_MODERN
        elif enumValue == TextFontEnum.ROMAN:
            return FONTFAMILY_ROMAN
        elif enumValue == TextFontEnum.SCRIPT:
            return FONTFAMILY_SCRIPT
        elif enumValue == TextFontEnum.TELETYPE:
            return FONTFAMILY_TELETYPE
        else:
            return FONTFAMILY_DEFAULT


from enum import Enum

from wx import FONTFAMILY_DEFAULT
from wx import FONTFAMILY_MODERN
from wx import FONTFAMILY_ROMAN
from wx import FONTFAMILY_SCRIPT
from wx import FONTFAMILY_SWISS
from wx import FONTFAMILY_TELETYPE


class PyutTextFontType(Enum):
    """
    A type safe wrapper for wxPython's Font type integers
    TODO:  Move this to the data model before using externalized data model
    """
    SWISS    = 'Swiss'
    MODERN   = 'Modern'
    ROMAN    = 'Roman'
    SCRIPT   = 'Script'
    TELETYPE = 'Teletype'

    # TODO  This does not belong here; move to a Pyut graphical place
    @classmethod
    def toWxType(cls, enumValue: 'PyutTextFontType') -> int:

        if enumValue == PyutTextFontType.SWISS:
            return FONTFAMILY_SWISS
        elif enumValue == PyutTextFontType.MODERN:
            return FONTFAMILY_MODERN
        elif enumValue == PyutTextFontType.ROMAN:
            return FONTFAMILY_ROMAN
        elif enumValue == PyutTextFontType.SCRIPT:
            return FONTFAMILY_SCRIPT
        elif enumValue == PyutTextFontType.TELETYPE:
            return FONTFAMILY_TELETYPE
        else:
            return FONTFAMILY_DEFAULT

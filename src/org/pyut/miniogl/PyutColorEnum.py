
from enum import Enum

from wx import Colour
from wx import ColourDatabase


class PyutColorEnum(Enum):

    """
    The purpose of this enumeration is to keep wxPython types from getting into
    the user visible portions of the preferences dialog
    """

    BLACK           = 'Black'
    CORNFLOWER_BLUE = 'Cornflower Blue'
    WHITE           = 'White'
    LIGHT_GREY      = 'Light Grey'
    GREEN           = 'Green'
    MEDIUM_BLUE     = 'Medium Blue'
    MIDNIGHT_BLUE   = 'Midnight Blue'
    YELLOW          = 'Yellow'
    SALMON          = 'Salmon'

    @staticmethod
    def toWxColor(colorEnum: 'PyutColorEnum') -> Colour:
        """
        """
        cdb: ColourDatabase = ColourDatabase()
        if colorEnum == PyutColorEnum.BLACK:
            c: Colour = cdb.Find(PyutColorEnum.BLACK.value)
        elif colorEnum == PyutColorEnum.CORNFLOWER_BLUE:
            c = cdb.Find(PyutColorEnum.CORNFLOWER_BLUE.value)
        elif colorEnum == PyutColorEnum.LIGHT_GREY:
            c = cdb.Find(PyutColorEnum.LIGHT_GREY.value)
        elif colorEnum == PyutColorEnum.GREEN:
            c = cdb.Find(PyutColorEnum.GREEN.value)
        elif colorEnum == PyutColorEnum.MEDIUM_BLUE:
            c = cdb.Find(PyutColorEnum.MEDIUM_BLUE.value)
        elif colorEnum == PyutColorEnum.MIDNIGHT_BLUE:
            c = cdb.Find(PyutColorEnum.MIDNIGHT_BLUE.value)
        elif colorEnum == PyutColorEnum.YELLOW:
            c = cdb.Find(PyutColorEnum.YELLOW.value)
        elif colorEnum == PyutColorEnum.SALMON:
            c = cdb.Find(PyutColorEnum.SALMON.value)
        else:
            c = cdb.Find(PyutColorEnum.WHITE.value)

        del cdb
        assert c.IsOk(), 'Developer Error.  Invalid color'
        return c

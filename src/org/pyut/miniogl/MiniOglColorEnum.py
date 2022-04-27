
from enum import Enum

from wx import Colour
from wx import ColourDatabase


class MiniOglColorEnum(Enum):

    """
    The purpose of this enumeration is to keep wxPython types from getting into
    the user visible portions of the preferences dialog
    """

    BLACK             = 'Black'
    CORNFLOWER_BLUE   = 'Cornflower Blue'
    WHITE             = 'White'
    LIGHT_GREY        = 'Light Grey'
    DARK_GREY         = 'Dark Grey'
    DIM_GREY          = 'Dim Grey'
    GREEN             = 'Green'
    MEDIUM_BLUE       = 'Medium Blue'
    MIDNIGHT_BLUE     = 'Midnight Blue'
    LIGHT_BLUE        = 'Light Blue'
    LIGHT_STEEL_BLUE  = 'Light Steel Blue'
    DARK_SLATE_BLUE   = 'Dark Slate Blue'
    MEDIUM_SLATE_BLUE = 'Medium Slate Blue'
    YELLOW            = 'Yellow'
    SALMON            = 'Salmon'

    @staticmethod
    def toWxColor(colorEnum: 'MiniOglColorEnum') -> Colour:
        """
        """
        cdb: ColourDatabase = ColourDatabase()
        if colorEnum == MiniOglColorEnum.BLACK:
            c: Colour = cdb.Find(MiniOglColorEnum.BLACK.value)
        elif colorEnum == MiniOglColorEnum.CORNFLOWER_BLUE:
            c = cdb.Find(MiniOglColorEnum.CORNFLOWER_BLUE.value)
        elif colorEnum == MiniOglColorEnum.LIGHT_GREY:
            c = cdb.Find(MiniOglColorEnum.LIGHT_GREY.value)
        elif colorEnum == MiniOglColorEnum.GREEN:
            c = cdb.Find(MiniOglColorEnum.GREEN.value)
        elif colorEnum == MiniOglColorEnum.MEDIUM_BLUE:
            c = cdb.Find(MiniOglColorEnum.MEDIUM_BLUE.value)
        elif colorEnum == MiniOglColorEnum.MIDNIGHT_BLUE:
            c = cdb.Find(MiniOglColorEnum.MIDNIGHT_BLUE.value)
        elif colorEnum == MiniOglColorEnum.YELLOW:
            c = cdb.Find(MiniOglColorEnum.YELLOW.value)
        elif colorEnum == MiniOglColorEnum.SALMON:
            c = cdb.Find(MiniOglColorEnum.SALMON.value)
        else:
            c = cdb.Find(MiniOglColorEnum.WHITE.value)

        del cdb
        assert c.IsOk(), 'Developer Error.  Invalid color'
        return c


from enum import Enum

from wx import BITMAP_TYPE_BMP
from wx import BITMAP_TYPE_JPEG
from wx import BITMAP_TYPE_PNG
from wx import BITMAP_TYPE_TIFF

# noinspection PyProtectedMember
from wx._core import BitmapType


class WxImageFormat(Enum):

    PNG  = 'png'
    JPG  = 'jpg'
    BMP  = 'bmp'
    TIFF = 'tiff'

    @staticmethod
    def toWxBitMapType(wxImageFormat: 'WxImageFormat') -> BitmapType:

        if wxImageFormat == WxImageFormat.PNG:
            return BITMAP_TYPE_PNG
        elif wxImageFormat == WxImageFormat.JPG:
            return BITMAP_TYPE_JPEG
        elif wxImageFormat == WxImageFormat.BMP:
            return BITMAP_TYPE_BMP
        elif wxImageFormat == WxImageFormat.TIFF:
            return BITMAP_TYPE_TIFF
        else:
            assert False, 'Unhandled WxImageFormat value'

    def __str__(self):
        return self.name.lower()

    def __repr__(self):
        return self.name.lower()

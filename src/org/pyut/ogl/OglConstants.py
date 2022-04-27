
from wx import Bitmap

from org.pyut.ogl.resources.img.Display import embeddedImage as displayImage
from org.pyut.ogl.resources.img.DoNotDisplay import embeddedImage as doNotDisplayImage
from org.pyut.ogl.resources.img.UnSpecified import embeddedImage as unSpecifiedImage


class OglConstants:

    @staticmethod
    def displayMethodsIcon() -> Bitmap:
        bmp: Bitmap = displayImage.GetBitmap()
        return bmp

    @staticmethod
    def doNotDisplayMethodsIcon() -> Bitmap:
        bmp: Bitmap = doNotDisplayImage.GetBitmap()
        return bmp

    @staticmethod
    def unspecifiedDisplayMethodsIcon() -> Bitmap:
        bmp: Bitmap = unSpecifiedImage.GetBitmap()
        return bmp

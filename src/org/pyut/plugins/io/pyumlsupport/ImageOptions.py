
from dataclasses import dataclass

from org.pyut.plugins.io.pyumlsupport.ImageFormat import ImageFormat


@dataclass
class ImageOptions:

    outputFileName: str = ''
    """
    This is a fully qualified file name
    """
    imageWidth:     int = 1280
    imageHeight:    int = 1024
    imageFormat:    ImageFormat = ImageFormat.PNG
    horizontalGap:  int = 60
    verticalGap:    int = 60


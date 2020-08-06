
from dataclasses import dataclass

from pyumldiagrams import Defaults

from org.pyut.plugins.io.pyumlsupport.ImageFormat import ImageFormat


@dataclass
class ImageOptions:

    outputFileName: str = Defaults.DEFAULT_FILE_NAME
    """
    This is a fully qualified file name

    """
    imageWidth:     int = Defaults.DEFAULT_IMAGE_WIDTH
    imageHeight:    int = Defaults.DEFAULT_IMAGE_HEIGHT
    imageFormat:    ImageFormat = ImageFormat.PNG
    horizontalGap:  int = Defaults.DEFAULT_HORIZONTAL_GAP
    verticalGap:    int = Defaults.DEFAULT_VERTICAL_GAP



from typing import Tuple

from logging import Logger
from logging import getLogger

from wx import DC
from wx import FONTSTYLE_NORMAL
from wx import FONTWEIGHT_NORMAL
from wx import Font

from miniogl.Common import Common
from miniogl.AttachmentLocation import AttachmentLocation
from miniogl.SelectAnchorPoint import SelectAnchorPoint
from miniogl.LollipopLine import LollipopLine

from pyutmodel.PyutInterface import PyutInterface
from pyutmodel.PyutObject import PyutObject

from ogl.OglPosition import OglPosition
from ogl.OglTextFontFamily import OglTextFontFamily

from ogl.preferences.OglPreferences import OglPreferences

from ogl.OglUtils import OglUtils


class OglInterface2(LollipopLine, Common):

    ADJUST_AWAY_FROM_IMPLEMENTOR: int = 10

    INTERFACE_FONT_SIZE: int = 12   # TODO:  Make this a preference

    def __init__(self, pyutInterface: PyutInterface,  destinationAnchor: SelectAnchorPoint):

        LollipopLine.__init__(self, destinationAnchor=destinationAnchor)

        self.logger: Logger = getLogger(__name__)

        self._pyutInterface: PyutInterface = pyutInterface

        preferences: OglPreferences = OglPreferences()

        fontStyle:  OglTextFontFamily = preferences.textFontFamily
        fontFamily: int              = OglUtils.oglFontFamilyToWxFontFamily(fontStyle)

        self._defaultFont: Font = Font(OglInterface2.INTERFACE_FONT_SIZE, fontFamily, FONTSTYLE_NORMAL, FONTWEIGHT_NORMAL)

    @property
    def pyutInterface(self) -> PyutInterface:
        return self._pyutInterface

    @pyutInterface.setter
    def pyutInterface(self, theNewValue: PyutInterface):
        self._pyutInterface = theNewValue

    @property
    def pyutObject(self) -> PyutObject:
        """
        Synonym for reverse compatibility

        Returns:  The pyut interface
        """
        return self.pyutInterface

    @pyutObject.setter
    def pyutObject(self, newValue: PyutInterface):
        """
        Synonym for reverse compatibility

        Args:
            newValue: The new PyutInterface object
        """
        self._pyutInterface = newValue

    def Draw(self, dc: DC, withChildren: bool = True):

        super().Draw(dc=dc, withChildren=withChildren)
        dc.SetFont(self._defaultFont)

        xFaceName: str = self.pyutInterface.name

        extentSize: Tuple[int, int] = dc.GetTextExtent(xFaceName)  # width, height

        pixelSize: Tuple[int, int] = self._defaultFont.GetPixelSize()

        textPosition: OglPosition = self._determineInterfaceNamePosition(self._destinationAnchor, pixelSize=pixelSize, textSize=extentSize)

        dc.DrawText(xFaceName, textPosition.x, textPosition.y)

    def Inside(self, clickPointX, clickPointY) -> bool:
        """
        Override Shape.Inside

        Args:
            clickPointX: x click coordinate
            clickPointY: y click coordinate

        Returns:  `True` if (x, y) is inside the shape.
        """
        clickDiffStartX, clickDiffStartY, diffX, diffY = self.setupInsideCheck(clickPointX=clickPointX, clickPointY=clickPointY, line=self.lineCoordinates())

        if self.insideBoundingBox(clickDiffStartX, clickDiffStartY, diffX, diffY) and self.insideSegment(clickDiffStartX, clickDiffStartY, diffX, diffY):
            return True

        return False

    def UpdateFromModel(self):
        super().UpdateFromModel()

    def Remove(self, point):
        """
        Need an empty implementation of this to allow adding of additional interfaces
        on an OglClass;  This confirms I really do not understand the MiniOgl structure

        Args:
            point:
        """
        self.logger.debug(f'{point=}')

    def __repr__(self):

        strMe: str = f'OglInterface2 - "{self._pyutInterface.name}"'
        return strMe

    def __eq__(self, other):

        if isinstance(other, OglInterface2):
            if self._isSameName(other) is True and self._isSameId(other) is True:
                return True
            else:
                return False
        else:
            return False

    def __hash__(self):
        return hash(self._pyutInterface.name) + hash(self.GetID())

    def _isSameName(self, other) -> bool:

        ans: bool = False
        if self.pyutInterface.name == other.pyutInterface.name:
            ans = True
        return ans

    def _isSameId(self, other):

        ans: bool = False
        if self.GetID() == other.GetID():
            ans = True
        return ans

    def _determineInterfaceNamePosition(self, destinationAnchor: SelectAnchorPoint, pixelSize: Tuple[int, int], textSize: Tuple[int, int]) -> OglPosition:

        oglPosition:     OglPosition     = OglPosition()
        attachmentPoint: AttachmentLocation = destinationAnchor.attachmentPoint

        x, y = destinationAnchor.GetPosition()

        fWidth, fHeight = pixelSize
        tWidth, tHeight = textSize

        if attachmentPoint == AttachmentLocation.NORTH:
            y -= (LollipopLine.LOLLIPOP_LINE_LENGTH + (LollipopLine.LOLLIPOP_CIRCLE_RADIUS * 2) + OglInterface2.ADJUST_AWAY_FROM_IMPLEMENTOR)
            x -= (tWidth // 2)
            oglPosition.x = x
            oglPosition.y = y

        elif attachmentPoint == AttachmentLocation.SOUTH:
            y += (LollipopLine.LOLLIPOP_LINE_LENGTH + LollipopLine.LOLLIPOP_CIRCLE_RADIUS + OglInterface2.ADJUST_AWAY_FROM_IMPLEMENTOR)
            x -= (tWidth // 2)
            oglPosition.x = x
            oglPosition.y = y

        elif attachmentPoint == AttachmentLocation.WEST:
            y = y - (fHeight * 2)
            originalX: int = x
            x = x - LollipopLine.LOLLIPOP_LINE_LENGTH - (tWidth // 2)
            while x + tWidth > originalX:
                x -= OglInterface2.ADJUST_AWAY_FROM_IMPLEMENTOR
            oglPosition.x = x
            oglPosition.y = y

        elif attachmentPoint == AttachmentLocation.EAST:
            y = y - (fHeight * 2)
            x = x + round(LollipopLine.LOLLIPOP_LINE_LENGTH * 0.8)
            oglPosition.x = x
            oglPosition.y = y
        else:
            self.logger.warning(f'Unknown attachment point: {attachmentPoint}')
            assert False, 'Unknown attachment point'

        return oglPosition

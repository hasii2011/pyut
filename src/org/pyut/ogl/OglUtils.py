
from logging import Logger
from logging import getLogger
from logging import DEBUG

from wx import FONTFAMILY_DEFAULT
from wx import FONTFAMILY_MODERN
from wx import FONTFAMILY_ROMAN
from wx import FONTFAMILY_SCRIPT
from wx import FONTFAMILY_SWISS
from wx import FONTFAMILY_TELETYPE

from org.pyut.model.OglTextFontType import OglTextFontType
from org.pyut.ogl.OglPosition import OglPosition


class OglUtils:

    clsLogger: Logger = getLogger(__name__)

    @classmethod
    def computeMidPoint(cls, srcPosition: OglPosition, destPosition: OglPosition) -> OglPosition:
        """

        Args:
            srcPosition:        Tuple x,y source position
            destPosition:       Tuple x,y destination position

        Returns:
                A tuple that is the x,y position between `srcPosition` and `destPosition`

            [Reference]: https://mathbitsnotebook.com/Geometry/CoordinateGeometry/CGmidpoint.html
        """
        if OglUtils.clsLogger.isEnabledFor(DEBUG):
            OglUtils.clsLogger.debug(f'{srcPosition=}  {destPosition=}')
        x1 = srcPosition.x
        y1 = srcPosition.y
        x2 = destPosition.x
        y2 = destPosition.y

        midPointX = round(abs(x1 + x2) / 2)
        midPointY = round(abs(y1 + y2) / 2)

        return OglPosition(x=midPointX, y=midPointY)

    @classmethod
    def pyutFontTypeToWxFontType(cls, enumValue: OglTextFontType) -> int:

        if enumValue == OglTextFontType.SWISS:
            return FONTFAMILY_SWISS
        elif enumValue == OglTextFontType.MODERN:
            return FONTFAMILY_MODERN
        elif enumValue == OglTextFontType.ROMAN:
            return FONTFAMILY_ROMAN
        elif enumValue == OglTextFontType.SCRIPT:
            return FONTFAMILY_SCRIPT
        elif enumValue == OglTextFontType.TELETYPE:
            return FONTFAMILY_TELETYPE
        else:
            return FONTFAMILY_DEFAULT

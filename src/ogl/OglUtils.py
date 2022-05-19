
from logging import Logger
from logging import getLogger
from logging import DEBUG
from typing import List
from typing import Tuple

from wx import DC
from wx import FONTFAMILY_DEFAULT
from wx import FONTFAMILY_MODERN
from wx import FONTFAMILY_ROMAN
from wx import FONTFAMILY_SCRIPT
from wx import FONTFAMILY_SWISS
from wx import FONTFAMILY_TELETYPE

from wx import NewIdRef as wxNewIdRef

from ogl.OglTextFontFamily import OglTextFontFamily
from ogl.OglPosition import OglPosition


class OglUtils:

    clsLogger: Logger = getLogger(__name__)

    @staticmethod
    def snapCoordinatesToGrid(x: int, y: int, gridInterval: int) -> Tuple[int, int]:

        xDiff: float = x % gridInterval
        yDiff: float = y % gridInterval

        snappedX: int = round(x - xDiff)
        snappedY: int = round(y - yDiff)

        return snappedX, snappedY

    @classmethod
    def computeMidPoint(cls, srcPosition: OglPosition, dstPosition: OglPosition) -> OglPosition:
        """

        Args:
            srcPosition:        Tuple x,y source position
            dstPosition:       Tuple x,y destination position

        Returns:
                A tuple that is the x,y position between `srcPosition` and `dstPosition`

            [Reference]: https://mathbitsnotebook.com/Geometry/CoordinateGeometry/CGmidpoint.html
        """
        if OglUtils.clsLogger.isEnabledFor(DEBUG):
            OglUtils.clsLogger.debug(f'{srcPosition=}  {dstPosition=}')
        x1 = srcPosition.x
        y1 = srcPosition.y
        x2 = dstPosition.x
        y2 = dstPosition.y

        midPointX = round(abs(x1 + x2) / 2)
        midPointY = round(abs(y1 + y2) / 2)

        return OglPosition(x=midPointX, y=midPointY)

    @classmethod
    def oglFontFamilyToWxFontFamily(cls, enumValue: OglTextFontFamily) -> int:

        if enumValue == OglTextFontFamily.SWISS:
            return FONTFAMILY_SWISS
        elif enumValue == OglTextFontFamily.MODERN:
            return FONTFAMILY_MODERN
        elif enumValue == OglTextFontFamily.ROMAN:
            return FONTFAMILY_ROMAN
        elif enumValue == OglTextFontFamily.SCRIPT:
            return FONTFAMILY_SCRIPT
        elif enumValue == OglTextFontFamily.TELETYPE:
            return FONTFAMILY_TELETYPE
        else:
            return FONTFAMILY_DEFAULT

    @classmethod
    def lineSplitter(cls, text: str, dc: DC, textWidth: int) -> List[str]:
        """
        Split the `text` into lines that fit into `textWidth` pixels.

        Note:  This is a copy of the one in Pyut.  Duplicated here in order to remove the LineSplitter dependency.

        Args:
            text:       The text to split
            dc:         Device Context
            textWidth:  The width of the text in pixels

        Returns:
            A list of strings that are no wider than the input pixel `width`
        """
        splitLines: List[str] = text.splitlines()
        newLines:   List[str] = []

        for line in splitLines:
            words:     List[str] = line.split()
            lineWidth: int       = 0
            newLine:   str       = ""
            for wordX in words:
                word: str = f'{wordX} '

                extentSize: Tuple[int, int] = dc.GetTextExtent(word)        # width, height
                wordWidth:  int             = extentSize[0]
                if lineWidth + wordWidth <= textWidth:
                    newLine = f'{newLine}{word}'
                    lineWidth += wordWidth
                else:
                    newLines.append(newLine[:-1])   # remove last space
                    newLine = word
                    lineWidth = wordWidth

            newLines.append(newLine[:-1])

        return newLines

    @classmethod
    def assignID(cls, numberOfIds: int) -> List[wxNewIdRef]:
        """
        Assign and return numberOfIds

        Sample use        : [Unique_Id1, Unique_Id2, Unique_Id3] = assignID(3)

        Note:  This is a copy of the one in Pyut.  Duplicated here in order to remove the PyutUtils dependency.

        Args:
            numberOfIds: number of unique IDs to return

        Returns:  List of numbers which contain <numberOfIds> unique IDs
        """
        retList: List[wxNewIdRef] = []
        x: int = 0
        while x < numberOfIds:
            retList.append(wxNewIdRef())
            x += 1
        return retList

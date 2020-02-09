
from typing import cast
from typing import List
from typing import NewType
from typing import Tuple


from logging import Logger
from logging import getLogger

from math import pi
from math import atan
from math import cos
from math import sin

from wx import BLACK_BRUSH
from wx import BLACK_PEN
from wx import DC
from wx import FONTFAMILY_DEFAULT
from wx import FONTSTYLE_NORMAL
from wx import FONTWEIGHT_NORMAL
from wx import WHITE_BRUSH

from wx import Font

from org.pyut.MiniOgl.TextShape import TextShape
from org.pyut.MiniOgl.TextShapeModel import TextShapeModel

from org.pyut.ogl.OglLink import OglLink

# label types
[CENTER, SRC_CARD, DEST_CARD] = list(range(3))

TextShapes = NewType('TextShapes', List[TextShape])


class OglAssociation(OglLink):

    TEXT_SHAPE_FONT_SIZE: int = 12

    """
    Graphical link representation of an association, (simple line, no arrow).
    To get a new link,  use the `OglLinkFactory` and specify
    the link type.  .e.g. OGL_ASSOCIATION for an instance of this class.
    """
    def __init__(self, srcShape, pyutLink, dstShape):
        """

        Args:
            srcShape:   Source shape
            pyutLink:   Conceptual links associated with the graphical links.
            dstShape:   Destination shape
        """
        super().__init__(srcShape, pyutLink, dstShape)

        self.logger: Logger = getLogger(__name__)
        # Add labels
        self._labels: TextShapes = cast(TextShapes, {})
        srcPos  = srcShape.GetPosition()
        destPos = dstShape.GetPosition()

        linkLength: float = self._computeLinkLength(srcPosition=srcPos, destPosition=destPos)
        dx, dy            = self._computeDxDy(srcPosition=srcPos, destPosition=destPos)

        # cenLblX = -dy * 5 / linkLength
        # cenLblY = dx * 5 / linkLength
        cenLblX, cenLblY = self._computeMidPoint(srcPosition=srcPos, destPosition=destPos)
        self.logger.info(f'linkLength:  {linkLength:.2f}  cenLblX: {cenLblX:.2f} cenLblY: {cenLblY:.2f} dx: {dx}  dy: {dy}')

        srcLblX = 20 * dx / linkLength     # - dy*5/l
        srcLblY = 20 * dy / linkLength     # + dx*5/l
        dstLblX = -20 * dx / linkLength    # + dy*5/l
        dstLblY = -20 * dy / linkLength    # - dy*5/l

        self._defaultFont = Font(OglAssociation.TEXT_SHAPE_FONT_SIZE, FONTFAMILY_DEFAULT, FONTSTYLE_NORMAL, FONTWEIGHT_NORMAL)

        # Initialize label objects
        self._labels[CENTER]    = self.AddText(cenLblX, cenLblY, "", font=self._defaultFont)
        self._labels[SRC_CARD]  = self._srcAnchor.AddText(srcLblX, srcLblY, "", font=self._defaultFont)
        self._labels[DEST_CARD] = self._dstAnchor.AddText(dstLblX, dstLblY, "", font=self._defaultFont)
        self.updateLabels()
        self.SetDrawArrow(False)

        self.__hackCenterLabelPosition(cenLblX, cenLblY)

    def updateLabels(self):
        """
        Update the labels according to the link.
        """
        def updateTheAssociationLabels(textShape: TextShape, text: str):
            """
            Update the label text;  Empty labels are rendered invisible
            """
            if text.strip() != "":
                textShape.SetText(text)
                textShape.SetVisible(True)
            else:
                textShape.SetVisible(False)

        # update the labels
        updateTheAssociationLabels(self._labels[CENTER],    self._link.getName())
        updateTheAssociationLabels(self._labels[SRC_CARD],  self._link.sourceCardinality)
        updateTheAssociationLabels(self._labels[DEST_CARD], self._link.destinationCardinality)

    def getLabels(self) -> TextShapes:
        """

        Returns:
            The associated text shapes that are used on Association links
        """
        return self._labels

    def Draw(self, dc: DC, withChildren: bool = True):
        """
        Called for the content drawing of links.

        Args:
            dc:     Device context
            withChildren:   draw the children or not
        """
        self.updateLabels()
        OglLink.Draw(self, dc, withChildren)

    def drawLosange(self, dc: DC, filled: bool = False):
        """
        Draw an arrow at the begining of the line.

        Args:
            dc:         The device context
            filled:     True if the losange must be filled, False otherwise

        Note:  Losange is French for 'diamond'
        """
        pi_6 = pi/6
        points = []
        line = self.GetSegments()
        x1, y1 = line[1]
        x2, y2 = line[0]
        a = x2 - x1
        b = y2 - y1
        if abs(a) < 0.01:  # vertical segment
            if b > 0:
                alpha = -pi/2
            else:
                alpha = pi/2
        else:
            if a == 0:
                if b > 0:
                    alpha = pi/2
                else:
                    alpha = 3 * pi / 2
            else:
                alpha = atan(b/a)
        if a > 0:
            alpha += pi
        alpha1 = alpha + pi_6
        alpha2 = alpha - pi_6
        size = 8
        points.append((x2 + size * cos(alpha1), y2 + size * sin(alpha1)))
        points.append((x2, y2))
        points.append((x2 + size * cos(alpha2), y2 + size * sin(alpha2)))
        points.append((x2 + 2*size * cos(alpha),  y2 + 2*size * sin(alpha)))
        dc.SetPen(BLACK_PEN)
        if filled:
            dc.SetBrush(BLACK_BRUSH)
        else:
            dc.SetBrush(WHITE_BRUSH)
        dc.DrawPolygon(points)
        dc.SetBrush(WHITE_BRUSH)

    def __hackCenterLabelPosition(self, cenLblX, cenLblY):
        """
        This code is a hack because I cannot figure out why some "TextShape"s have their
        diagram attribute set and some do not;  Having our diagram attribute set means that the
        model can be updated.
        So I am manually updating here

        Args:
            cenLblX:    center label X position
            cenLblY:    center label Y position

        """
        centerTextShape: TextShape      = self._labels[CENTER]
        model:           TextShapeModel = centerTextShape.GetModel()

        self.logger.info(f'center text position {model.GetPosition()}')
        model.SetPosition(cenLblX, cenLblY)

    @staticmethod
    def _computeMidPoint(srcPosition: Tuple[float, float], destPosition: Tuple[float, float]):
        """

        Args:
            srcPosition:        Tuple x,y source position
            destPosition:       Tuple x,y destination position

        Returns:
                A tuple that is the x,y position between `srcPosition` and `destPosition`

            [Reference]: https://mathbitsnotebook.com/Geometry/CoordinateGeometry/CGmidpoint.html
        """

        x1 = srcPosition[0]
        y1 = srcPosition[1]
        x2 = destPosition[0]
        y2 = destPosition[1]

        midPointX = (x1 + x2) / 2
        midPointY = (y1 + y2) / 2

        return midPointX, midPointY

    def __repr__(self):
        return f'from: {self.getSourceShape()} to: {self.getDestinationShape()}'

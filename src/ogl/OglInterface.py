
from logging import Logger
from logging import getLogger

from wx import DC
from wx import Pen

from wx import PENSTYLE_SHORT_DASH
from wx import PENSTYLE_LONG_DASH
from wx import RED_PEN
from wx import BLACK_PEN
from wx import WHITE_BRUSH

from pyutmodel.PyutLink import PyutLink


from ogl.OglLink import OglLink
from ogl.OglClass import OglClass

# Kind of labels
[CENTER] = list(range(1))


class OglInterface(OglLink):

    clsLogger: Logger = getLogger(__name__)

    """
    Graphical OGL representation of an interface link.
    This class provide the methods for drawing an interface link between
    two classes of an UML diagram. Add labels to an OglLink.
    """
    def __init__(self, srcShape: OglClass, pyutLink: PyutLink, dstShape: OglClass):

        """

        Args:
            srcShape:  Source shape
            pyutLink:  Conceptual links associated with the graphical links.
            dstShape: Destination shape
        """
        super().__init__(srcShape, pyutLink, dstShape)

        self.SetPen(Pen("BLACK", 1, PENSTYLE_LONG_DASH))
        self.SetBrush(WHITE_BRUSH)
        self._labels = {CENTER: self.AddText(0, 0, "")}

        # Initialize labels objects
        self.updateLabels()
        self.SetDrawArrow(True)

    def updateLabels(self):
        """
        Update the labels according to the link.

        @since 1.14
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        def prepareLabel(textShape, text):
            """
            Update a label.

            @author Laurent Burgbacher <lb@alawa.ch>
            """
            # If label should be drawn
            if text.strip() != "":
                textShape.SetText(text)
                # textShape.Show(True)
                textShape.SetVisible(True)
            else:
                # textShape.Show(False)
                textShape.SetVisible(False)

        # Prepares labels
        prepareLabel(self._labels[CENTER], self._link.name)

    def getLabels(self):
        """
        Get the labels.

        @return TextShape []
        @since 1.0
        """
        return self._labels

    def Draw(self, dc: DC, withChildren: bool = False):
        """
        Called for drawing of interface links.
        OglLink drew regular lines
        I need dashed lines for an interface

        Args:
            dc: Device context
            withChildren:   Draw the children or not

        """
        self.updateLabels()
        if self._visible:
            line = self.GetSegments()
            if self._selected:
                dc.SetPen(RED_PEN)

            if self._spline:
                dc.DrawSpline(line)
            else:
                pen: Pen = dc.GetPen()              #
                pen.SetStyle(PENSTYLE_SHORT_DASH)   # This is what is different from OglLink.Draw(..)
                dc.SetPen(pen)                      #
                dc.DrawLines(line)

            for control in self._controls:
                control.Draw(dc)

            if self._selected:
                self._srcAnchor.Draw(dc)
                self._dstAnchor.Draw(dc)
            dc.SetPen(BLACK_PEN)

            if self._drawArrow:
                u, v = line[-2], line[-1]
                self.DrawArrow(dc, u, v)

            if withChildren is True:
                self.DrawChildren(dc)


from logging import Logger
from logging import getLogger

from wx import DC

from wx import Pen
from wx import PENSTYLE_LONG_DASH
from wx import WHITE_BRUSH

from org.pyut.model.PyutLink import PyutLink

from org.pyut.ogl.OglLink import OglLink
from org.pyut.ogl.OglClass import OglClass

# Kind of labels
[CENTER] = list(range(1))


class OglInterface(OglLink):

    clsLogger: Logger = getLogger(__name__)

    """
    Graphical OGL representation of an interface link.
    This class provide the methods for drawing an interface link between
    two classes of an UML diagram. Add labels to an OglLink.
    """
    def __init__(self, srcShape: OglLink, pyutLink: PyutLink, dstShape: OglClass):

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
        prepareLabel(self._labels[CENTER], self._link.getName())

    def getLabels(self):
        """
        Get the labels.

        @return TextShape []
        @since 1.0
        """
        return self._labels

    def Draw(self, dc: DC, withChildren: bool = False):
        """
        Called for contents drawing of links.

        Args:
            dc: Device context
            withChildren:   Draw the children or not

        """
        self.updateLabels()
        OglLink.Draw(self, dc)

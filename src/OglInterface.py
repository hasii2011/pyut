
from wx import ID_YES

from wx import Pen
from wx import PENSTYLE_LONG_DASH
from wx import WHITE_BRUSH

from PyutLink import PyutLink

from OglLink import OglLink
from OglClass import OglClass

from Mediator1 import Mediator

from DlgRemoveLink import DlgRemoveLink

# Kind of labels
[CENTER] = list(range(1))


class OglInterface(OglLink):
    """
    Graphical OGL representation of an interface link.
    This class provide the methods for drawing an interface link between
    two classes of an UML diagram. Add labels to an OglLink.

    @version $Revision: 1.9 $
    """

    def __init__(self, srcShape: OglLink, pyutLink: PyutLink, dstShape: OglClass):
        """
        Constructor.

        @param  srcShape : Source shape
        @param  pyutLink : Conceptual links associated with the graphical links.
        @param  dstShape : Destination shape
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """

        # Init
        OglLink.__init__(self, srcShape, pyutLink, dstShape)

        # Pen
        #self.SetPen(wx.BLACK_DASHED_PEN)
        self.SetPen(Pen("BLACK", 1, PENSTYLE_LONG_DASH))

        # Arrow must be white inside
        self.SetBrush(WHITE_BRUSH)

        # Add labels
        # self._labels = {}
        self._labels = {CENTER: self.AddText(0, 0, "")}

        # Initialize labels objects
        self.updateLabels()

        # Add arrow
        # self.AddArrow(ARROW_ARROW, ARROW_POSITION_END, 15.0)
        self.SetDrawArrow(True)

    def OnLeftClick(self, x, y, keys, attachment):
        """
        Event handler for left mouse click.
        This event handler call the link dialog to edit link properties.

        @param int x : X position
        @param int y : Y position
        @param int keys : ...
        @param int attachment : ...
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        # get the shape
        #  shape = self.GetShape()
        # the canvas wich contain the shape
        # canvas = shape.GetCanvas()

        # Open dialog to edit link
        dlg = DlgRemoveLink()
        rep = dlg.ShowModal()
        dlg.Destroy()
        if rep == ID_YES:  # destroy link
            Mediator().removeLink(self)
        self._diagram.Refresh()

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

    def Draw(self, dc):
        """
        Called for contents drawing of links.

        @param wx.DC dc : Device context
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        self.updateLabels()
        OglLink.Draw(self, dc)

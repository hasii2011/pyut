
from logging import Logger
from logging import getLogger

from wx import BLACK_PEN
from wx import CANCEL
from wx import CENTRE
from wx import ID_OK
from wx import OK
from wx import TextEntryDialog

from MiniOgl.LineShape import LineShape
from MiniOgl.ShapeEventHandler import ShapeEventHandler

from Globals import _

# TODO : Find a way to report moves from AnchorPoints to PyutSDMessage
#
# TODO: Humberto -- This class does not seem to be called; I tried to manually create a sequence
# diagram but did not invoke this class;  However, it is reference by many plugins;  Fix later

# Kind of labels
[CENTER, SRC_CARD, DEST_CARD] = range(3)


class OglSDMessage(LineShape, ShapeEventHandler):
    """
    class for graphical message

    :version: $Revision: 1.16 $
    :author: C.Dutoit
    """

    def __init__(self, srcShape, pyutObject, dstShape):
        """
        Constructor.

        @param OglObject srcShape : Source shape
        @param OglObject dstShape : Destination shape

        @author : Added srcPos and dstPos
        """
        self.logger: Logger = getLogger(__name__)
        self._pyutObject = pyutObject

        srcY = pyutObject.getSrcY() - srcShape.getLifeLineShape().GetPosition()[1]
        dstY = pyutObject.getDstY() - dstShape.getLifeLineShape().GetPosition()[1]

        src = srcShape.getLifeLineShape().AddAnchor(0, srcY)
        dst = dstShape.getLifeLineShape().AddAnchor(0, dstY)

        src.SetStayOnBorder(False)
        dst.SetStayOnBorder(False)
        src.SetStayInside(True)
        dst.SetStayInside(True)
        src.SetVisible(True)
        dst.SetVisible(True)
        src.SetDraggable(True)
        dst.SetDraggable(True)

        self._srcShape = srcShape
        self._dstShape   = dstShape
        self._srcAnchor = src
        self._dstAnchor = dst

        LineShape.__init__(self, src, dst)

        # Pen
        self.SetPen(BLACK_PEN)

        # Add labels
        self._labels = {}
        # self._labels = {CENTER: self.AddText(0, 0, "")}

        # Initialize labels objects
        self.updateLabels()

        # Add arrow
        self.SetDrawArrow(True)

    def updatePositions(self):
        """
        Define the positions on lifeline (y)
        @author C.Dutoit
        """
        # print "OglMessage - updatePositions"
        src = self.GetSource()
        dst = self.GetDestination()
        srcY = self._pyutObject.getSrcY() + src.GetParent().GetSegments()[0][1]
        dstY = self._pyutObject.getDstY() + dst.GetParent().GetSegments()[0][1]
        srcX = 0
        dstX = 0

        src.SetPosition(srcX, srcY)
        dst.SetPosition(dstX, dstY)

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
        prepareLabel(self._labels[CENTER], self._pyutObject.getMessage())

    def getPyutObject(self):
        """
        Return my pyut object
        @author C.Dutoit
        """
        return self._pyutObject

    def getLabels(self):
        """
        Get the labels.

        @return TextShape []
        """
        return self._labels

    def Draw(self, dc,  withChildren=False):
        """
        Called for contents drawing of links.

        @param wx.DC dc : Device context
        @param withChildren

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        self.updateLabels()

        self.logger.debug(f"Draw: Src Pos: '{self.GetSource().GetPosition()}' dest Pos '{self.GetDestination().GetPosition()}'")
        LineShape.Draw(self, dc, withChildren)

    def OnLeftDClick(self, event):
        """
        Callback for left double clicks.
        @author C.Dutoit
        """
        dlg = TextEntryDialog(None, _("Message"), _("Enter message"), self._pyutObject.getMessage(), OK | CANCEL | CENTRE)
        if dlg.ShowModal() == ID_OK:
            self._pyutObject.setMessage(dlg.GetValue())
        dlg.Destroy()

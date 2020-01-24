
from typing import Tuple

from logging import Logger
from logging import getLogger

# from wx import BLACK_PEN
from wx import GREEN_PEN

from wx import CANCEL
from wx import CENTRE
from wx import DC
from wx import ID_OK
from wx import OK
from wx import TextEntryDialog

from org.pyut.MiniOgl.AnchorPoint import AnchorPoint
from org.pyut.MiniOgl.LineShape import LineShape
from org.pyut.MiniOgl.TextShape import TextShape

from org.pyut.PyutSDMessage import PyutSDMessage

from org.pyut.ogl.sd.OglSDInstance import OglSDInstance
from org.pyut.ogl.OglLink import OglLink

from org.pyut.general.Globals import _

# TODO : Find a way to report moves from AnchorPoints to PyutSDMessage
#

[CENTER, SRC_CARD, DEST_CARD] = range(3)


class OglSDMessage(OglLink):
    """
    Class for a graphical message
    """
    def __init__(self, srcShape: OglSDInstance, pyutSDMessage: PyutSDMessage, dstShape: OglSDInstance):
        """

        Args:
            srcShape:   Source shape OglSDInstance
            pyutSDMessage:  PyutSDMessage
            dstShape:   Destination shape OglSDInstance

        """
        self._pyutSDMessage = pyutSDMessage

        dstAnchor, srcAnchor = self._createAnchorPoints(srcShape=srcShape, pyutSDMessage=pyutSDMessage, dstShape=dstShape)

        self._srcAnchor = srcAnchor
        self._dstAnchor = dstAnchor

        super().__init__(srcShape=srcShape, pyutLink=pyutSDMessage, dstShape=dstShape)
        self.logger: Logger = getLogger(__name__)

        self.SetPen(GREEN_PEN)

        linkLength: float = self._computeLinkLength()
        dx, dy            = self._computeDxDy()

        centerMessageX    = -dy * 5 / linkLength
        centerMessageY    = dx * 5 / linkLength

        self._messageLabel: TextShape = self.AddText(centerMessageX, centerMessageY, pyutSDMessage.getMessage())  # font=self._defaultFont

        self.updateMessage()
        self.SetDrawArrow(True)

    def updatePositions(self):
        """
        Define the positions on lifeline (y)
        """
        self.logger.debug(f'OglMessage - updatePositions')
        src = self.GetSource()
        dst = self.GetDestination()
        srcY = self._pyutSDMessage.getSrcY() + src.GetParent().GetSegments()[0][1]
        dstY = self._pyutSDMessage.getDstY() + dst.GetParent().GetSegments()[0][1]
        srcX = 0
        dstX = 0

        src.SetPosition(srcX, srcY)
        dst.SetPosition(dstX, dstY)

    def updateMessage(self):
        """
        Update the message
        """
        text:      str       = self._pyutSDMessage.getMessage()
        textShape: TextShape = self._messageLabel
        # Don't draw blank messages
        if text.strip() != "":
            textShape.SetText(text)
            textShape.SetVisible(True)
        else:
            textShape.SetVisible(False)

    def getPyutObject(self) -> PyutSDMessage:
        """
        override

        Returns: my pyut sd message
        """
        return self._pyutSDMessage

    def Draw(self, dc: DC,  withChildren: bool = True):
        """
        Called for drawing the contents of links.

        Args:
            dc:     Device context
            withChildren:   `True` draw the children
        """
        self.updateMessage()

        self.logger.info(f"Draw: Src Pos: '{self.GetSource().GetPosition()}' dest Pos '{self.GetDestination().GetPosition()}'")
        LineShape.Draw(self, dc, withChildren)

    def OnLeftDClick(self, event):
        """
        Callback for left double clicks.

        """
        dlg = TextEntryDialog(None, _("Message"), _("Enter message"), self._pyutSDMessage.getMessage(), OK | CANCEL | CENTRE)
        if dlg.ShowModal() == ID_OK:
            self._pyutSDMessage.setMessage(dlg.GetValue())
        dlg.Destroy()

    def _createAnchorPoints(self, srcShape: OglSDInstance, dstShape: OglSDInstance, pyutSDMessage: PyutSDMessage) -> Tuple[AnchorPoint, AnchorPoint]:
        """
        Royal ready to heat rice


        Args:
            dstShape:
            srcShape:
            pyutSDMessage

        Returns:  A tuple of anchor points for the source and destination shapes

        """
        srcY: float = pyutSDMessage.getSrcY() - srcShape.getLifeLineShape().GetPosition()[1]
        dstY: float = pyutSDMessage.getDstY() - dstShape.getLifeLineShape().GetPosition()[1]

        srcAnchor: AnchorPoint = srcShape.getLifeLineShape().AddAnchor(0, srcY)
        dstAnchor: AnchorPoint = dstShape.getLifeLineShape().AddAnchor(0, dstY)
        srcAnchor.SetStayOnBorder(False)
        dstAnchor.SetStayOnBorder(False)
        srcAnchor.SetStayInside(True)
        dstAnchor.SetStayInside(True)
        srcAnchor.SetVisible(True)
        dstAnchor.SetVisible(True)
        srcAnchor.SetDraggable(True)
        dstAnchor.SetDraggable(True)

        return dstAnchor, srcAnchor

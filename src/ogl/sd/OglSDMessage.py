
from typing import Tuple

from logging import Logger
from logging import getLogger

from wx import BLACK_PEN

from wx import CANCEL
from wx import CENTRE
from wx import DC
from wx import ID_OK
from wx import OK
from wx import RED_PEN
from wx import TextEntryDialog

from pyutmodel.PyutSDMessage import PyutSDMessage

from miniogl.AnchorPoint import AnchorPoint
from miniogl.TextShape import TextShape

from ogl.OglPosition import OglPosition
from ogl.sd.OglSDInstance import OglSDInstance
from ogl.OglLink import OglLink


# TODO : Find a way to report moves from AnchorPoints to PyutSDMessage


class OglSDMessage(OglLink):
    """
    Class for a graphical message
    """
    clsLogger: Logger = getLogger(__name__)

    def __init__(self, srcShape: OglSDInstance, pyutSDMessage: PyutSDMessage, dstShape: OglSDInstance):
        """

        Args:
            srcShape:   Source shape OglSDInstance
            pyutSDMessage:  PyutSDMessage
            dstShape:   Destination shape OglSDInstance

        """
        self._pyutSDMessage = pyutSDMessage

        super().__init__(srcShape=srcShape, pyutLink=pyutSDMessage, dstShape=dstShape)
        # LineShape.__init__(self, srcAnchor=srcAnchor, dstAnchor=dstAnchor)
        #
        # Override OglLink anchors
        #
        srcAnchor, dstAnchor = self._createAnchorPoints(srcShape=srcShape, pyutSDMessage=pyutSDMessage, dstShape=dstShape)
        srcAnchorPosition = srcAnchor.GetPosition()
        dstAnchorPosition = dstAnchor.GetPosition()

        self._srcAnchor: AnchorPoint = srcAnchor
        self._dstAnchor: AnchorPoint = dstAnchor

        oglSource:      OglPosition = OglPosition.tupleToOglPosition(srcAnchorPosition)
        oglDestination: OglPosition = OglPosition.tupleToOglPosition(dstAnchorPosition)
        linkLength: float = self._computeLinkLength(srcPosition=oglSource, destPosition=oglDestination)
        dx, dy            = self._computeDxDy(srcPosition=oglSource, destPosition=oglDestination)

        centerMessageX: int = round(-dy * 5 // linkLength)
        centerMessageY: int = round(dx * 5 // linkLength)

        self._messageLabel: TextShape = self.AddText(centerMessageX, centerMessageY, pyutSDMessage.getMessage())  # font=self._defaultFont

        self.updateMessage()
        self.SetDrawArrow(True)

    def updatePositions(self):
        """
        Define the positions on lifeline (y)
        """
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

    def Draw(self, dc: DC,  withChildren: bool = False):
        """
        Called for drawing the contents of links.

        Args:
            dc:     Device context
            withChildren:   `True` draw the children
        """
        self.updateMessage()

        srcAnchor, dstAnchor = self.getAnchors()

        srcX, srcY = srcAnchor.GetPosition()
        dstX, dstY = dstAnchor.GetPosition()

        if self._selected is True:
            dc.SetPen(RED_PEN)

        dc.DrawLine(srcX, srcY, dstX, dstY)
        self.DrawArrow(dc, srcAnchor.GetPosition(), dstAnchor.GetPosition())
        self.DrawChildren(dc=dc)

        dc.SetPen(BLACK_PEN)

    def OnLeftDClick(self, event):
        """
        Callback for left double clicks.

        """
        dlg = TextEntryDialog(None, "Message", "Enter message name", self._pyutSDMessage.getMessage(), OK | CANCEL | CENTRE)
        if dlg.ShowModal() == ID_OK:
            self._pyutSDMessage.setMessage(dlg.GetValue())
        dlg.Destroy()

    def _createAnchorPoints(self, srcShape: OglSDInstance, dstShape: OglSDInstance,
                            pyutSDMessage: PyutSDMessage) -> Tuple[AnchorPoint, AnchorPoint]:
        """
        Royal ready to heat rice

        Args:
            dstShape:
            srcShape:
            pyutSDMessage

        Returns:  A tuple of anchor points for the source and destination shapes

        """
        srcY: int = pyutSDMessage.getSrcY() - srcShape.getLifeLineShape().GetPosition()[1]
        dstY: int = pyutSDMessage.getDstY() - dstShape.getLifeLineShape().GetPosition()[1]

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

        return srcAnchor, dstAnchor

    def __repr__(self) -> str:
        msg: str = self._pyutSDMessage.getMessage()
        return f'OglSDMessage[id: {self._id} {msg=}]'

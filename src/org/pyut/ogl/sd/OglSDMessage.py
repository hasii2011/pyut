
from typing import Dict

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

from org.pyut.ogl.OglLink import OglLink

from org.pyut.PyutObject import PyutObject

from org.pyut.general.Globals import _

# TODO : Find a way to report moves from AnchorPoints to PyutSDMessage
#

[CENTER, SRC_CARD, DEST_CARD] = range(3)


class OglSDMessage(OglLink):
    """
    Class for a graphical message
    """
    def __init__(self, srcShape, pyutObject, dstShape):
        """

        Args:
            srcShape:   Source shape OglObject
            pyutObject:
            dstShape:   Destination shape OglObject

        """
        self.logger: Logger = getLogger(__name__)
        self._pyutObject = pyutObject

        srcY: float = pyutObject.getSrcY() - srcShape.getLifeLineShape().GetPosition()[1]
        dstY: float = pyutObject.getDstY() - dstShape.getLifeLineShape().GetPosition()[1]

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

        self._srcShape  = srcShape
        self._dstShape  = dstShape
        self._srcAnchor = srcAnchor
        self._dstAnchor = dstAnchor

        super().__init__(srcShape=srcShape, pyutLink=pyutObject, dstShape=dstShape)

        self.SetPen(GREEN_PEN)
        self._labels: Dict[int, TextShape] = {
            CENTER:     TextShape(x=0, y=0, text='Center'),
            SRC_CARD:   TextShape(x=0, y=0, text='SRC'),
            DEST_CARD:  TextShape(x=0, y=0, text='DEST'),
        }
        self.updateLabels()
        self.SetDrawArrow(True)

    def updatePositions(self):
        """
        Define the positions on lifeline (y)
        """
        self.logger.debug(f'OglMessage - updatePositions')
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

    def getPyutObject(self) -> PyutObject:
        """

        Returns: my pyut object
        """
        return self._pyutObject

    def getLabels(self):
        """
        Get the labels.

        Returns Dict[int, TextShape]
        """
        return self._labels

    def Draw(self, dc: DC,  withChildren: bool = True):
        """
        Called for drawing the contents of links.

        Args:
            dc:     Device context
            withChildren:   `True` draw the children
        """
        self.updateLabels()

        self.logger.debug(f"Draw: Src Pos: '{self.GetSource().GetPosition()}' dest Pos '{self.GetDestination().GetPosition()}'")
        LineShape.Draw(self, dc, withChildren)

    def OnLeftDClick(self, event):
        """
        Callback for left double clicks.

        """
        dlg = TextEntryDialog(None, _("Message"), _("Enter message"), self._pyutObject.getMessage(), OK | CANCEL | CENTRE)
        if dlg.ShowModal() == ID_OK:
            self._pyutObject.setMessage(dlg.GetValue())
        dlg.Destroy()

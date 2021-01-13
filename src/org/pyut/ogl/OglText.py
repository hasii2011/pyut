

from typing import cast

from logging import Logger
from logging import getLogger

from wx import DC
from wx import MouseEvent

from org.pyut.general.LineSplitter import LineSplitter

from org.pyut.model.PyutText import PyutText

from org.pyut.ogl.OglObject import OglObject


class OglText(OglObject):
    """
        Draws resizeable boxes of text with no visible boundaries
    """
    MARGIN: int = 5

    def __init__(self, pyutObject=None, width: int = 125, height: int = 50):    # TODO make default text size a preference
        """
        Args:
            pyutObject: Associated PyutObject
            width:      Initial width
            height:     Initial height
        """
        super().__init__(pyutObject=pyutObject, width=width, height=height)

        self.logger: Logger = getLogger(__name__)

        self._drawFrame = False

    @property
    def pyutText(self) -> PyutText:
        return self._pyutObject

    @pyutText.setter
    def pyutText(self, newValue: PyutText):
        self._pyutObject = newValue

    def OnLeftUp(self, event: MouseEvent):
        """
        Implement this method so we can snap Ogl objects

        Args:
            event:  the mouse event
        """
        super().OnLeftUp(event)

    def Draw(self, dc: DC, withChildren: bool = False):
        """
        Paint handler, draws the content of the shape.

        Args:
            dc:     device context to draw to
            withChildren:   Redraw children or not
        """
        OglObject.Draw(self, dc)
        dc.SetFont(self._defaultFont)

        w, h = self.GetSize()

        baseX, baseY = self.GetPosition()

        dc.SetClippingRegion(baseX, baseY, w, h)

        noteContent = cast(PyutText, self.getPyutObject()).content
        lines = LineSplitter().split(noteContent, dc, w - 2 * OglText.MARGIN)

        x = baseX + OglText.MARGIN
        y = baseY + OglText.MARGIN

        for line in range(len(lines)):
            dc.DrawText(lines[line], x, y + line * (dc.GetCharHeight() + 5))

        # dc.DrawLine(baseX + w - OglText.MARGIN, baseY, baseX + w, baseY + OglText.MARGIN)

        dc.DestroyClippingRegion()

    def __repr__(self):

        strMe: str = f"[OglText - name: '{self._pyutObject.name}' id: '{self._pyutObject._id}']"
        return strMe


from logging import Logger
from logging import getLogger

from wx import Brush
from wx import Colour
from wx import DC

from org.pyut.ogl.OglObject import OglObject
from org.pyut.model.PyutNote import PyutNote
from org.pyut.general.LineSplitter import LineSplitter


class OglNote(OglObject):

    MARGIN: int = 10

    """
    OGL object that represents a UML note in diagrams.
    This class defines OGL object that represents a note. A note may be linked
    with all links except Inheritance and Interface.

    For more instructions about how to create an OGL object, please refer
    to the `OglObject` class.
    """
    def __init__(self, pyutNote=None, w=100, h=50):
        """
        Constructor.

        @param pyutNote : a PyutNote object
        @param  w : Width of the shape
        @param  h : Height of the shape
        @since 1.0
        @author Philippe Waelti<pwaelti@eivd.ch>
        """
        # Init pyutObject (coming from OglObject)
        if pyutNote is None:
            pyutObject = PyutNote()
        else:
            pyutObject = pyutNote
        super().__init__(pyutObject, w, h)

        self.logger: Logger = getLogger(__name__)
        self.SetBrush(Brush(Colour(255, 255, 230)))

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

        try:
            # lines = LineSplitter().split(self.getPyutObject().getName(), dc, w - 2 * MARGIN)
            # noteName = self.getPyutObject().getName()
            noteContent = self.getPyutObject().content
            lines = LineSplitter().split(noteContent, dc, w - 2 * OglNote.MARGIN)
        except (ValueError, Exception) as e:
            self.logger.error(f"Unable to display note - {e}")
            return

        baseX, baseY = self.GetPosition()

        dc.SetClippingRegion(baseX, baseY, w, h)

        x = baseX + OglNote.MARGIN
        y = baseY + OglNote.MARGIN

        for line in range(len(lines)):
            dc.DrawText(lines[line], x, y + line * (dc.GetCharHeight() + 5))

        dc.DrawLine(baseX + w - OglNote.MARGIN, baseY, baseX + w, baseY + OglNote.MARGIN)

        dc.DestroyClippingRegion()

    def __repr__(self):
        pyutNote: PyutNote = self.getPyutObject()
        if pyutNote is None:
            return f'Anonymous Note'
        else:
            return f'{pyutNote._name}'

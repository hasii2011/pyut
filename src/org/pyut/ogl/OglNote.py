
from typing import cast

from logging import Logger
from logging import getLogger

from wx import Brush
from wx import Colour
from wx import DC

from org.pyut.ogl.OglObject import OglObject
from org.pyut.model.PyutNote import PyutNote
from org.pyut.general.LineSplitter import LineSplitter
from org.pyut.preferences.PyutPreferences import PyutPreferences


class OglNote(OglObject):
    """
    This is an OGL object that represents a UML note in diagrams.
    A note may be linked
    with all links except Inheritance and Interface.

    For more instructions about how to create an OGL object, please refer
    to the `OglObject` class.
    """

    MARGIN: int = 10

    def __init__(self, pyutNote=None, w: int = 0, h: int = 0):
        """

        Args:
            pyutNote:   A PyutNote Object
            w:          Default width override
            h:          Default height override
        """

        # Init pyutObject (coming from OglObject)
        if pyutNote is None:
            pyutObject = PyutNote()
        else:
            pyutObject = pyutNote

        width:  int = w
        height: int = h
        prefs: PyutPreferences = PyutPreferences()
        if width == 0:
            width = prefs.noteDimensions.width
        if height == 0:
            height = prefs.noteDimensions.height

        del prefs

        super().__init__(pyutObject, width, height)

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
            noteContent = cast(PyutNote, self.getPyutObject()).content
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
        pyutNote: PyutNote = cast(PyutNote, self.getPyutObject())
        if pyutNote is None:
            return f'Anonymous Note'
        else:
            return f'{pyutNote._name}'

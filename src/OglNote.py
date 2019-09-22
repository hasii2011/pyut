
from logging import Logger
from logging import getLogger

import wx
from OglObject import OglObject
from PyutNote import PyutNote
from LineSplitter import *

MARGIN = 10.0


class OglNote(OglObject):
    """
    OGL object that represent an UML note in diagrams.
    This class defines OGL objects that represents a note. A note may be linked
    with all links except Inheritance and Interface.

    For more instructions about how to create an OGL object, please refer
    to the `OglObject` class.

    :version: $Revision: 1.10 $
    :author: Philippe Waelti
    :contact: pwaelti@eivd.ch
    """

    def __init__(self, pyutNote = None, w = 100, h = 50):
        """
        Constructor.

        @param PyutNote pyutNote : a PyutNote object
        @param float w : Width of the shape
        @param float h : Height of the shape
        @since 1.0
        @author Philippe Waelti<pwaelti@eivd.ch>
        """
        # Init pyutObject (coming from OglObject)
        if pyutNote is None:
            pyutObject = PyutNote()
        else:
            pyutObject = pyutNote

        # Parent class constructor
        # OglObject.__init__(self, pyutObject, w, h)
        super().__init__(pyutObject, w, h)

        self.logger: Logger = getLogger(__name__)
        self.SetBrush(wx.Brush(wx.Colour(255, 255, 230)))

    def Draw(self, dc):
        """
        Paint handler, draws the content of the shape.
        @param wx.DC dc : device context to draw to
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        OglObject.Draw(self, dc)
        dc.SetFont(self._defaultFont)

        w, h = self.GetSize()

        try:
            # lines = LineSplitter().split(self.getPyutObject().getName(), dc, w - 2 * MARGIN)
            noteName = self.getPyutObject().getName()
            lines = LineSplitter().split(noteName, dc, w - 2 * MARGIN)
        except (ValueError, Exception) as e:
            self.logger.error(f"Unable to display note - {e}")
            return

        baseX, baseY = self.GetPosition()

        dc.SetClippingRegion(baseX, baseY, w, h)

        x = baseX + MARGIN
        y = baseY + MARGIN

        for line in range(len(lines)):
            dc.DrawText(lines[line], x, y + line * (dc.GetCharHeight() + 5))

        dc.DrawLine(baseX + w - MARGIN, baseY, baseX + w, baseY + MARGIN)

        dc.DestroyClippingRegion()

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.10 $"
__author__  = "EI5, eivd, Group Burgbacher - Waelti"
__date__    = "2001-12-12"

#from wxPython.wx     import *
#from wxPython.ogl    import *
import wx
from OglObject       import *
from PyutNote        import *
from LineSplitter    import *

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
        OglObject.__init__(self, pyutObject, w, h)
        self.SetBrush(wx.Brush(wx.Colour(255, 255, 230)))

    #>------------------------------------------------------------------

    def Draw(self, dc):#, withChildren=False):
        """
        Paint handler, draws the content of the shape.
        @param wx.DC dc : device context to draw to
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        OglObject.Draw(self, dc)#, withChildren)
        dc.SetFont(self._defaultFont)

        w, h = self.GetSize()

        try:
            lines = LineSplitter().split(\
                    self.getPyutObject().getName(), dc, w - 2 * MARGIN)
        except:
            print "Unable to display note"
            return

        baseX, baseY = self.GetPosition()

        dc.SetClippingRegion(baseX, baseY, w, h)

        x = baseX + MARGIN
        y = baseY + MARGIN

        for line in range(len(lines)):
            dc.DrawText(lines[line], x, y + line * (dc.GetCharHeight() + 5))

        dc.DrawLine(baseX + w - MARGIN, baseY, baseX + w, baseY + MARGIN)


        dc.DestroyClippingRegion()


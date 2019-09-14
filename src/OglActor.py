#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.9 $"
__author__  = "EI5, eivd, Group Burgbacher - Waelti"
__date__    = "2001-12-12"

#from wxPython.wx  import *
#from wxPython.ogl import *
from OglObject    import *
from PyutActor    import *
import wx


MARGIN = 10.0

class OglActor(OglObject):
    """
    OGL object that represent an UML actor in use case diagrams.
    This class defines OGL objects that represents an actor for Use
    Cases diagram. You can just instanciate an OGL actor and add it to
    the diagram, links, resizing, ... are managed by parent class
    `OglObject`.

    For more instructions about how to create an OGL object, please refer
    to the `OglObject` class.

    :version: $Revision: 1.9 $
    :author: Philippe Waelti
    :contact: pwaelti@eivd.ch
    """

    #>------------------------------------------------------------------ 

    def __init__(self, pyutActor = None, w = 80.0, h = 100.0):
        """
        Constructor.
        @param Float w : Width of the shape
        @param Float h : Height of the shape

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        # Init associated PyutObject
        if pyutActor is None:
            pyutObject = PyutActor()
        else:
            pyutObject = pyutActor

        # Super init
        OglObject.__init__(self, pyutObject, w, h)
        self._drawFrame = False

    #>------------------------------------------------------------------ 

    def Draw(self, dc):#, withChildren=False):
        """
        Draw the actor.
        @param wxDC dc : Device context

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        OglObject.Draw(self, dc)#, withChildren)
        # Get current font
        dc.SetFont(self._defaultFont)

        # Gets the minimum bounding box for the shape
        width, height = self.GetSize()

        # Calculate the top center of the shape
        x, y = self.GetPosition()

        # drawing is restricted in the specified region of the device
        dc.SetClippingRegion(x, y, width, height)

        # Our sweet actor size
        actorWidth  = width
        actorHeight = 0.8 * (height - 2.0 * MARGIN) # 80 % of total height
        sizer = min(actorHeight, actorWidth)

        # Draw our actor head
        centerX = x + width / 2
        centerY = y + height / 2

        x = centerX - 0.2 * sizer
        y += MARGIN
        dc.DrawEllipse(x, y, 0.4 * sizer, 0.4 * sizer)

        # Draw body and arms
        x = centerX
        y += 0.4 * sizer
        dc.DrawLine(x, y, x, y + 0.3 * actorHeight)
        dc.DrawLine(x - 0.25 * actorWidth, y + 0.15 * actorHeight,
                    x + 0.25 * actorWidth, y + 0.15 * actorHeight)

        # And the feet
        y += 0.3 * actorHeight
        dc.DrawLine(x, y, x - 0.25 * actorWidth, y + 0.3 * actorHeight)
        dc.DrawLine(x, y, x + 0.25 * actorWidth, y + 0.3 * actorHeight)

        # Draw our buddy name
        textWidth, textHeight = dc.GetTextExtent(self.getPyutObject().getName())
        y = centerY + 0.5 * height - MARGIN - 0.1 * actorHeight
        dc.DrawText(self.getPyutObject().getName(), x - 0.5 * textWidth, y)
        dc.DestroyClippingRegion()


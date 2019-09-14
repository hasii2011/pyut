#!/usr/bin/env python
#
# Copyright 2002, Laurent Burgbacher, Eivd.
# Visit http://www.eivd.ch
#
# This file is part of MiniOgl.
#
# MiniOgl is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# MiniOgl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MiniOgl; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

__author__    = "Laurent Burgbacher, lb@alawa.ch, Eivd"
__copyright__ = "Copyright 2002, Laurent Burgbacher, Eivd"
__license__   = "Released under the terms of the GNU General Public Licence V2"
__date__      = "2002-10-15"
__version__   = "$Id: TextShape.py,v 1.5 2006/02/04 22:01:01 dutoitc Exp $"

from __future__                import division
#from wxPython.wx               import *
from Shape                     import Shape
from RectangleShape            import RectangleShape
import wx
from TextShapeModel            import *

__all__ = ["TextShape"]

class TextShape(RectangleShape):
    """
    A text shape that can be attached to another shape (or be standalone).

    Exported methods:
    -----------------

    __init__(self, x, y, text, parent=None)
        Constructor.
    Attach(self, diagram)
        Don't use this method, use Diagram.AddShape instead !!!
    GetText(self)
        Get the text of the shape.
    SetText(self, text)
        Set the text of the shape.
    SetTextBackground(self, colour)
        Set the text background color.
    GetTextBackground(self)
        Get the text background color.
    Draw(self, dc, withChildren=True)
        Draw the text on the dc.
    DrawBorder(self, dc)
        Draw the border of the shape, for fast rendering.
    GetColor(self)
        Get the color of the text.
    SetColor(self, color)
        Set the color of the text.

    @author Laurent Burgbacher <lb@alawa.ch>
    """
    def __init__(self, x, y, text, parent=None):
        """
        Constructor.

        @param double x, y : position of the point
        @param string text : the text of the shape
        @param Shape parent : parent shape
        """
        RectangleShape.__init__(self, x, y, 0, 0, parent)
        self._text = None
        self._color = wx.BLACK
        self.SetText(text)
        self._drawFrame = False
        self._resizable = False
        self._textBack = wx.WHITE    # text background colour

    #>------------------------------------------------------------------------

    def Attach(self, diagram):
        """
        Don't use this method, use Diagram.AddShape instead !!!
        Attach the shape to a diagram.
        When you create a new shape, you must attach it to a diagram before
        you can see it. This method is used internally by Diagram.AddShape.

        @param Diagram diagram
        """
        RectangleShape.Attach(self, diagram)
        self._textBack = self._diagram.GetPanel().GetBackgroundColour()

    #>------------------------------------------------------------------------

    def GetText(self):
        """
        Get the text of the shape.

        @return string
        """
        return self._text

    #>------------------------------------------------------------------------

    def SetText(self, text):
        """
        Set the text of the shape.

        @param string text
        """
        self._text = text
        self._width, self._height = wx.MemoryDC().GetTextExtent(text)

    #>------------------------------------------------------------------------

    def SetTextBackground(self, colour):
        """
        Set the text background color.

        @param wx.Colour
        """
        self._textBack = colour

    #>------------------------------------------------------------------------

    def GetTextBackground(self):
        """
        Get the text background color.

        @return wx.Colour
        """
        return self._textBack

    #>------------------------------------------------------------------------

    def Draw(self, dc, withChildren=True):
        """
        Draw the text on the dc.

        @param wx.DC dc
        """
        if self._visible:
            RectangleShape.Draw(self, dc, False)
            dc.SetTextForeground(self._color)
            dc.SetBackgroundMode(wx.SOLID)
            dc.SetTextBackground(self._textBack)
            x, y = self.GetPosition()
            dc.DrawText(self._text, x, y)
            if withChildren:
                self.DrawChildren(dc)

    #>------------------------------------------------------------------------

    def DrawBorder(self, dc):
        """
        Draw the border of the shape, for fast rendering.

        @param wx.DC dc
        """
        if self._selected:
            RectangleShape.DrawBorder(self, dc)
        else:
            Shape.DrawBorder(self, dc)

    #>------------------------------------------------------------------ 

    def GetColor(self):
        """
        Get the color of the text.

        @return wx.Colour
        """
        return self._color

    #>------------------------------------------------------------------ 

    def SetColor(self, color):
        """
        Set the color of the text.

        @param wx.Colour
        """
        self._color = color

    #>------------------------------------------------------------------------

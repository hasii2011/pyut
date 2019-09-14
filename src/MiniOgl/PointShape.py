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
__version__   = "$Id: PointShape.py,v 1.6 2004/12/10 23:31:59 dutoitc Exp $"

from __future__                import division
#from wxPython.wx               import *
from Shape                     import Shape

__all__ = ["PointShape"]

class PointShape(Shape):
    """
    A point, which is drawn as a little square (3 pixels wide).

    Exported methods:
    -----------------

    __init__(self, x, y, parent=None)
        Constructor.
    Draw(self, dc, withChildren=True)
        Draw the point on the dc.
    GetSelectionZone(self)
        Get the selection tolerance zone, in pixels.
    SetSelectionZone(self, halfWidth)
        Set the selection tolerance zone, in pixels.
    Inside(self, x, y)
        True if (x, y) is inside the point, according to the selection zone.
    SetVisibleWhenSelected(self, state)
        Set to True if you want the point to always be visible when it's
    GetVisibleWhenSelected(self)
        Return the "visible when selected flag".

    @author Laurent Burgbacher <lb@alawa.ch>
    """
    def __init__(self, x, y, parent=None):
        """
        Constructor.

        @param double x, y : position of the point
        @param Shape parent : parent shape
        """
        #print ">>>PointShape ", x, y
        Shape.__init__(self, x, y, parent)
        self._selectZone = 5
        self._visibleWhenSelected = True

    #>------------------------------------------------------------------------

    def Draw(self, dc, withChildren=True):
        """
        Draw the point on the dc.

        @param wxDC dc
        """
        if self._visible or (self._visibleWhenSelected and self._selected):
            Shape.Draw(self, dc, False)
            x, y = self.GetPosition()
            if not self._selected:
                dc.DrawRectangle(x - 1, y - 1, 3, 3)
            else:
                dc.DrawRectangle(x - 3, y - 3, 7, 7)
            if withChildren:
                self.DrawChildren(dc)

    #>------------------------------------------------------------------------

    def GetSelectionZone(self):
        """
        Get the selection tolerance zone, in pixels.

        @return float : half of the selection zone.
        """
        return self._selectZone

    #>------------------------------------------------------------------------

    def SetSelectionZone(self, halfWidth):
        """
        Set the selection tolerance zone, in pixels.

        @param float halfWidth : half of the selection zone.
        """
        self._selectZone = halfWidth

    #>------------------------------------------------------------------------

    def Inside(self, x, y):
        """
        True if (x, y) is inside the point, according to the selection zone.

        @param double x, y
        @return bool
        """
        ax, ay = self.GetPosition() # GetPosition always returns absolute pos
        zone = self._selectZone
        return (ax - zone < x < ax + zone) and (ay - zone < y < ay + zone)

    #>------------------------------------------------------------------------

    def SetVisibleWhenSelected(self, state):
        """
        Set to True if you want the point to always be visible when it's
        selected.

        @param bool state
        """
        self._visibleWhenSelected = state

    #>------------------------------------------------------------------------

    def GetVisibleWhenSelected(self):
        """
        Return the "visible when selected flag".

        @return bool True if the shape is always visible when selected
        """
        return self._visibleWhenSelected

    #>------------------------------------------------------------------------

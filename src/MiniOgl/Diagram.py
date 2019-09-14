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
__version__   = "$Id: Diagram.py,v 1.10 2006/02/04 22:01:01 dutoitc Exp $"

from __future__                import division
#from wxPython.wx               import *
import wx



__all__ = ["Diagram"]

class Diagram(object):
    """
    A diagram contains shapes and is responsible to manage them.
    It can be saved to a file, and loaded back. It knows every shapes that
    can be clicked (selected, moved...).

    Exported methods:
    -----------------

    __init__(self, panel)
        Constructor.
    AddShape(self, shape)
        Add a shape to the diagram.
    DeleteAllShapes(self)
        Delete all shapes in the diagram.
    RemoveShape(self, shape)
        Remove a shape from the diagram. Use Shape.Detach() instead!
    GetShapes(self)
        Return a list of the shapes in the diagram.
    GetParentShapes(self)
        Return a list of the parent shapes in the diagram.
    GetPanel(self)
        Return the panel associated with this diagram.
    MoveToFront(self, shape)
        Move the given shape to the end of the display list => last drawn.
    MoveToBack(self, shape)
        Move the given shape to the start of the display list => first drawn.

    @author Laurent Burgbacher <lb@alawa.ch>
    """
    def __init__(self, panel):
        """
        Constructor.

        @param wx.Panel panel : the panel on which to draw
        """
        self._panel = panel
        self._shapes = []       # all selectable shapes
        self._parentShapes = [] # all first level shapes

    #>------------------------------------------------------------------------

    def AddShape(self, shape, withModelUpdate = True):
        """
        Add a shape to the diagram.
        This is the correct way to do it. Don't use Shape.Attach(diagram)!

        @param Shape shape : the shape to add
        """
        #print "Diagram.AddShape => ", shape
        if shape not in self._shapes:
            self._shapes.append(shape)
        if shape not in self._parentShapes and shape.GetParent() is None:
            self._parentShapes.append(shape)
        #print "-----------"
        #print "   Diagram.AddShape : "
        #print "      shapes => ", self._shapes
        #print "      parentShapes => ", self._parentShapes
        shape.Attach(self)

        #added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (12.11.2005)
        #makes the shape's model (MVC pattern) have the right values depending on
        #the diagram frame state.
        if withModelUpdate:
            shape.UpdateModel()

    #>------------------------------------------------------------------------

    def DeleteAllShapes(self):
        """
        Delete all shapes in the diagram.
        """
        while self._shapes:
            self._shapes[0].Detach()
        self._shapes = []
        self._parentShapes = []

    #>------------------------------------------------------------------------

    def RemoveShape(self, shape):
        """
        Remove a shape from the diagram. Use Shape.Detach() instead!
        This also works, but it not the better way.

        @param Shape shape
        """
        if shape in self._shapes:
            self._shapes.remove(shape)
        if shape in self._parentShapes:
            self._parentShapes.remove(shape)

    #>------------------------------------------------------------------------

    def GetShapes(self):
        """
        Return a list of the shapes in the diagram.
        It is a copy of the original. You cannot detach or add shapes to the
        diagram this way.

        @return Shape []
        """
        return self._shapes[:]

    #>------------------------------------------------------------------------

    def GetParentShapes(self):
        """
        Return a list of the parent shapes in the diagram.
        It is a copy of the original. You cannot detach or add shapes to the
        diagram this way.

        @return Shape []
        """
        return self._parentShapes[:]

    #>------------------------------------------------------------------------

    def GetPanel(self):
        """
        Return the panel associated with this diagram.

        @return DiagramFrame
        """
        return self._panel

    #>------------------------------------------------------------------------

    def MoveToFront(self, shape):
        """
        Move the given shape to the end of the display list => last drawn.

        @param Shape shape : shape to move
        """
        shapes = [shape] + shape.GetAllChildren()
        for s in shapes:
            self._shapes.remove(s)
        self._shapes = self._shapes + shapes

    #>------------------------------------------------------------------------

    def MoveToBack(self, shape):
        """
        Move the given shape to the start of the display list => first drawn.

        @param Shape shape : shape to move
        """
        shapes = [shape] + shape.GetAllChildren()
        for s in shapes:
            self._shapes.remove(s)
        self._shapes = shapes + self._shapes

    #>------------------------------------------------------------------------

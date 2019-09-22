import wx
from MiniOgl.ShapeModel import *

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
__version__   = "$Id: Shape.py,v 1.8 2006/02/04 22:01:01 dutoitc Exp $"


__all__ = ["Shape"]

# Setting this to 1 will display a little label for each Shape.
DEBUG = 0


class Shape(object):
    """
    Shape is the basic graphical block. It is also the view in
    a MVC pattern, so it has has a relative model (ShapeModel).

    Exported methods:
    -----------------

    __init__(self, x=0.0, y=0.0, parent=None)
        Constructor.
    SetPen(self, pen)
        Set the pen used to draw the shape.
    GetPen(self)
        Get the pen used to draw the shape.
    SetBrush(self, brush)
        Set the brush used to draw the shape.
    GetBrush(self)
        Get the brush used to draw the shape.
    GetID(self)
        Get the ID number of the shape.
    SetID(self, id)
        Set the ID of the shape. This can be used when loading a shape.
    SetOrigin(self, x, y)
        Set the origin of the shape, from its upper left corner.
    GetOrigin(self)
        Get the origin of the shape, from its upper left corner.
    AppendChild(self, child)
        Append a child to this shape.
    GetAllChildren(self)
        Get all the children of this shape, recursively.
    GetChildren(self)
        Get the children of this shape.
    AddAnchor(self, x, y, anchorType=None)
        Add an anchor point to the shape.
    AddAnchorObject(self, anchor)
        Add an anchor point directly.
    RemoveAllAnchors(self)
        Remove all anchors of the shape.
    RemoveAnchor(self, anchor)
        Remove an anchor.
    AddText(self, x, y, text)
        Add a text shape to the shape.
    Attach(self, diagram)
        Don't use this method, use Diagram.AddShape instead !!!
    Detach(self)
        Detach the shape from its diagram.
    Draw(self, dc, withChildren=True)
        Draw the shape.
    DrawChildren(self, dc)
        Draw the children of this shape.
    DrawBorder(self, dc)
        Draw the border of the shape, for fast rendering.
    DrawAnchors(self, dc)
        Draw the anchors of the shape.
    DrawHandles(self, dc)
        Draw the handles (selection points) of the shape.
    GetAnchors(self)
        Return a list of the anchors of the shape.
    GetParent(self)
        Get the parent of this shape.
    SetParent(self, parent)
        Set the parent of this shape.
    GetPosition(self)
        Return the absolute position of the shape.
    GetTopLeft(self)
        Get the coords of the top left point in diagram coords.
    GetSize(self)
        Get the size of the shape.
    ConvertCoordToRelative(self, x, y)
        Convert absolute coordinates to relative ones.
    GetRelativePosition(self)
        Return the position of the shape, relative to it's parent.
    Inside(self, x, y)
        True if (x, y) is inside the shape.
    IsDraggable(self)
        True if the shape can be dragged.
    IsProtected(self)
        True if the shape is protected.
    IsSelected(self)
        True if the shape is selected.
    IsVisible(self)
        True if the shape is visible.
    SetSelected(self, state=True)
        Select the shape.
    IsMoving(self)
        Return the "moving" state of a shape.
    SetMoving(self, state)
        A non-moving shape will be redrawn faster when others are moved.
    SetDraggable(self, drag)
        If False, the shape won't be movable.
    SetPosition(self, x, y)
        Change the position of the shape, if it's draggable.
    SetRelativePosition(self, x, y)
        Set the position of the shape, relative to the parent.
    SetProtected(self, bool)
        Protect the shape against deletion (Detach).
    SetSize(self, w, h)
        Set the size of the shape.
    SetVisible(self, bool)
        Set the shape visible or not.
    __repr__(self)
        String representation.
    GetDiagram(self)
        Return the diagram associated with this shape.

    @author Laurent Burgbacher <lb@alawa.ch>
    """

    ID = 0 # internal ID number

    def __init__(self, x=0.0, y=0.0, parent=None):
        """
        Constructor.
        If a parent is given, the position is relative to the parent's
        origin.

        @param double x, y : position of the shape on the diagram
        """
        self._x = x                 # shape position (view)
        self._y = y                 # shape position (view)
        self._ox = 0.0              # origin position (view)
        self._oy = 0.0              # origin position (view)
        self._parent = parent       # parent shape
        self._selected = False      # is the shape selected ?
        self._anchors = []          # anchors of the shape
        self._visible = True        # is the shape visible ?
        self._draggable = True      # can the shape be dragged ?
        self._moving = False        # is this shape moving now ?
        self._diagram = None        # associated diagram
        self._protected = False     # to protect against deletion
        self._children = []         # children shapes
        self._privateChildren = []  # private children, not saved
        self._pen = wx.BLACK_PEN     # pen to use
        self._brush = wx.WHITE_BRUSH # brush to use

        #  added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (12.11.2005)
        self._model = ShapeModel(self) # model of the shape (MVC pattern)

        self._id = Shape.ID     # unique ID number
        Shape.ID += 1
        if DEBUG:
            from TextShape import TextShape
            from LineShape import LineShape
            if not isinstance(self, (TextShape, LineShape)):
                t = self.AddText(0, -10, str(self._id))
                t.SetColor(wx.RED)

    def SetPen(self, pen):
        """
        Set the pen used to draw the shape.

        @param wx.Pen pen
        """
        self._pen = pen

    def GetPen(self):
        """
        Get the pen used to draw the shape.

        @return wx.Pen
        """
        return self._pen

    def SetBrush(self, brush):
        """
        Set the brush used to draw the shape.

        @param wx.Brush brush
        """
        self._brush = brush

    def GetBrush(self):
        """
        Get the brush used to draw the shape.

        @return wx.Brush
        """
        return self._brush

    def GetID(self):
        """
        Get the ID number of the shape.

        @return int
        """
        return self._id

    def SetID(self, id):
        """
        Set the ID of the shape. This can be used when loading a shape.

        @param int id
        """
        self._id = id
        Shape.ID = max(self._id + 1, Shape.ID)

    def SetOrigin(self, x, y):
        """
        Set the origin of the shape, from its upper left corner.

        @param double x, y : new origin
        """
        self._ox, self._oy = x, y

    def GetOrigin(self):
        """
        Get the origin of the shape, from its upper left corner.

        @return double x, y : origin
        """
        return self._ox, self._oy

    def AppendChild(self, child):
        """
        Append a child to this shape.
        This doesn't add it to the diagram, but it will be drawn by the parent.

        @param Shape child
        """
        child.SetParent(self)
        self._children.append(child)

    def GetAllChildren(self):
        """
        Get all the children of this shape, recursively.

        @return Shape []
        """
        shapes = []
        for child in self._children:
            shapes.append(child.GetAllChildren())
        return shapes

    def GetChildren(self):
        """
        Get the children of this shape.
        Not recursively, only get first level children.
        It's a copy of the original list, modifying it won't modify the
        original.

        @return Shape []
        """
        return self._children[:]

    def AddAnchor(self, x, y, anchorType=None):
        """
        Add an anchor point to the shape.
        A line can be linked to it. The anchor point will stay bound to the
        shape and move with it. It is protected against deletion (by default)
        and not movable by itself.

        @param double x, y : position of the new point, relative to the
            origin of the shape
        @param class anchorType : class to use as anchor point, or None for
            default (AnchorPoint)
        @return AnchorPoint : the created anchor
        """
        from MiniOgl.AnchorPoint import AnchorPoint     # I don't like in module imports but there is a cyclical dependency somewhere
        if anchorType is None:
            anchorType = AnchorPoint
        p = anchorType(x, y, self)
        p.SetProtected(True)
        self._anchors.append(p)
        if self._diagram is not None:
            self._diagram.AddShape(p)
        # if the shape is not yet attached to a diagram, the anchor points
        # will be attached when Attach is called on the shape.
        return p

    def AddAnchorObject(self, anchor):
        """
        Add an anchor point directly.

        @param anchor
        """
        self._anchors.append(anchor)

    def RemoveAllAnchors(self):
        """
        Remove all anchors of the shape.
        """
        while self._anchors:
            self.RemoveAnchor(self._anchors[0])

    def RemoveAnchor(self, anchor):
        """
        Remove an anchor.

        @param AnchorPoint anchor
        """
        if anchor in self._anchors:
            self._anchors.remove(anchor)

    def AddText(self, x, y, text):
        """
        Add a text shape to the shape.

        @param double x, y : position of the text, relative to the
            origin of the shape
        @param String text : text to add
        @return TextShape : the created shape
        """
        t = self._CreateTextShape(x, y, text)
        self._children.append(t)
        return t

    def _AddPrivateText(self, x, y, text):
        """
        Add a text shape, putting it in the private children of the shape.
        It won't be saved !!! This is used in constructor of child classes.

        @param double x, y : position of the text, relative to the
            origin of the shape
        @param String text : text to add
        @return TextShape : the created shape
        """
        t = self._CreateTextShape(x, y, text)
        self._privateChildren.append(t)
        return t

    def _CreateTextShape(self, x, y, text):
        """
        Create a text shape and add it to the diagram.

        @param double x, y : position of the text, relative to the
            origin of the shape
        @param String text : text to add
        @return TextShape : the created shape
        """
        from TextShape import TextShape
        t = TextShape(x, y, text, self)
        if self._diagram is not None:
            self._diagram.AddShape(t)
        if DEBUG:
            print("Text", t, "added")
        return t

    def Attach(self, diagram):
        """
        Don't use this method, use Diagram.AddShape instead !!!
        Attach the shape to a diagram.
        When you create a new shape, you must attach it to a diagram before
        you can see it. This method is used internally by Diagram.AddShape.

        @param Diagram diagram
        """
        self._diagram = diagram
        # add the anchors and the children
        map(lambda x: diagram.AddShape(x), self._anchors + self._children
            + self._privateChildren)

    def Detach(self):
        """
        Detach the shape from its diagram.
        This is the way to delete a shape. All anchor points are also
        removed, and link lines too.
        """
        # do not detach a protected shape
        if DEBUG:
            print("In shape.Detach with", self)
        if self._diagram is not None and not self._protected:
            if DEBUG:
                print("passed first condition")

            #  added by P. Dabrowski to ensure that the model is not
            #  attached anymore to this view.
            self.GetModel()._views.remove(self)

            diagram = self._diagram
            self._diagram = None
            diagram.RemoveShape(self)
            # detach the anchors + children
            while self._anchors:
                child = self._anchors[0]
                child.SetProtected(False)
                child.Detach()
                child.SetProtected(True)
            for child in self._children + self._privateChildren:
                child.SetProtected(False)
                child.Detach()
                child.SetProtected(True)
            if DEBUG:
                print("now, the shapes are", diagram.GetShapes())

    def Draw(self, dc, withChildren=True):
        """
        Draw the shape.
        For a shape, only the anchors are drawn. Nothing is drawn if the
        shape is set invisible.
        For children classes, the main classes would normally call it's
        parent's Draw method, passing withChildren = False, and finally
        calling itself the DrawChildren method.

        @param wx.DC dc
        @param boolean withChildren : draw the children or not
        """
        #C.Dutoit debug
        #print withChildren
        #import traceback
        #traceback.print_stack()
        #print "-----------------"

        if self._visible:
            dc.SetPen(self._pen)
            dc.SetBrush(self._brush)
            if withChildren:
                self.DrawChildren(dc)

        if self._selected:
            dc.SetPen(wx.RED_PEN) # CD
            self.DrawHandles(dc)

    def DrawChildren(self, dc):
        """
        Draw the children of this shape.

        @param wx.DC dc
        """
        if self._visible:
            for child in self._children + self._anchors + self._privateChildren:
                child.Draw(dc)

    def DrawBorder(self, dc):
        """
        Draw the border of the shape, for fast rendering.

        @param wx.DC dc
        """
        pass

    def DrawAnchors(self, dc):
        """
        Draw the anchors of the shape.

        @param wx.DC dc
        """
        #  print "Shape.DrawAnchors; shape=", self, ", anchors=", self._anchors
        map(lambda x: x.Draw(dc), self._anchors)

    def DrawHandles(self, dc):
        """
        Draw the handles (selection points) of the shape.
        A shape has no handles, because it has no size.

        @param wx.DC dc
        """
        pass

    def GetAnchors(self):
        """
        Return a list of the anchors of the shape.

        @return AnchorPoint []
        """
        return self._anchors[:]

    def GetParent(self):
        """
        Get the parent of this shape.

        @return Shape parent
        """
        return self._parent

    def SetParent(self, parent):
        """
        Set the parent of this shape.

        @param Shape parent
        """
        self._parent = parent

    def GetPosition(self):
        """
        Return the absolute position of the shape.
        It's in the diagram's coordinate system.

        @return (double, double)
        """
        if self._parent is not None:
            x, y = self._parent.GetPosition()
            return self._x + x, self._y + y
        else:
            return self._x, self._y

    def GetTopLeft(self):
        """
        Get the coords of the top left point in diagram coords.

        @return (double, double)
        """
        x, y = self.GetPosition()
        x -= self._ox
        y -= self._oy
        return x, y

    def GetSize(self):
        """
        Get the size of the shape.

        @return (double, double)
        """
        return 0.0, 0.0

    def ConvertCoordToRelative(self, x, y):
        """
        Convert absolute coordinates to relative ones.
        Relative coordinates are coordinates relative to the origin of the
        shape.

        @return (double, double)
        """
        if self._parent is not None:
            ox, oy = self._parent.GetPosition()
            x -= ox
            y -= oy
        return x, y

    def GetRelativePosition(self):
        """
        Return the position of the shape, relative to it's parent.

        @return (double, double)
        """
        return self._x, self._y

    def Inside(self, x, y):
        """
        True if (x, y) is inside the shape.

        @return bool
        """
        return False


    def IsDraggable(self):
        """
        True if the shape can be dragged.

        @return bool
        """
        return self._draggable

    def IsProtected(self):
        """
        True if the shape is protected.

        @return bool
        """
        return self._protected

    def IsSelected(self):
        """
        True if the shape is selected.

        @return bool
        """
        return self._selected

    def IsVisible(self):
        """
        True if the shape is visible.

        @return bool
        """
        return self._visible

    def SetSelected(self, state=True):
        """
        Select the shape.

        @param bool state
        """
        self._selected = state

    def IsMoving(self):
        """
        Return the "moving" state of a shape.
        See SetMoving.
        """
        return self._moving

    def SetMoving(self, state):
        """
        A non-moving shape will be redrawn faster when others are moved.
        See DiagramFrame.Refresh for more information.

        @param bool state
        """
        self._moving = state
        for shape in self._children:
            shape.SetMoving(state)
        for anchor in self._anchors:
            anchor.SetMoving(state)

    def SetDraggable(self, drag):
        """
        If False, the shape won't be movable.

        @param bool
        """
        self._draggable = drag

    def SetPosition(self, x, y):
        """
        Change the position of the shape, if it's draggable.

        @param double x, y : new position
        """
        if self._draggable:
            if self._parent is not None:
                self._x, self._y = self.ConvertCoordToRelative(x, y)
            else:
                self._x = x
                self._y = y

            #added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (12.11.2005)
            # if the shape is attached to a diagramFrame, it means that
            # the model will be initialized correctly.
            #(Avoid a null pointer error).
            if self.HasDiagramFrame():
                self.UpdateModel()

    def SetRelativePosition(self, x, y):
        """
        Set the position of the shape, relative to the parent.
        Only works if the shape is draggable.

        @param double x, y : new position
        """
        if self._draggable:
            self._x = x
            self._y = y

    def SetProtected(self, bool):
        """
        Protect the shape against deletion (Detach).

        @param bool bool
        """
        self._protected = bool

    def SetSize(self, w, h):
        """
        Set the size of the shape.

        @param double w, h : width and height of the shape
        """
        pass

    def SetVisible(self, bool):
        """
        Set the shape visible or not.

        @param bool bool
        """
        self._visible = bool

    def __repr__(self):
        """
        String representation.

        @return String
        """
        return object.__repr__(self) + " : " + str(self._id)

    def GetDiagram(self):
        """
        Return the diagram associated with this shape.

        @return Diagram
        """
        return self._diagram

    def UpdateFromModel(self):
        """
        Added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (12.11.2005)

        Updates the shape position from the model in the light of a
        change of state of the diagram frame (here it's only for the zoom)
        """

        #Get the coords of the model (ShapeModel)
        mx, my = self.GetModel().GetPosition()

        #Get the offsets and the ratio between the shape (view) and the
        #shape model (ShapeModel) given by the frame where the shape
        #is displayed.
        ratio = self.GetDiagram().GetPanel().GetCurrentZoom()
        dx = self.GetDiagram().GetPanel().GetXOffset()
        dy = self.GetDiagram().GetPanel().GetYOffset()

        #calculation of the shape (view) coords in the light of the
        #offsets and ratio
        x = (ratio * mx) + dx
        y = (ratio * my) + dy

        #assign the new coords to the shape (view). DON'T USE SetPosition(),
        #because there is a call to UpdateModel() in that method.
        if self._parent is not None:
            self._x, self._y = self.ConvertCoordToRelative(x, y)
        else:
            self._x = x
            self._y = y

    def UpdateModel(self):
        """
        Added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (12.11.2005)
        Updates the coords of the model (ShapeModel) when the Shape (view)
        is deplaced.
        """

        #  get the associated model (ShapeModel)
        model = self.GetModel()

        #Get the offsets and the ratio between the shape (view) and the
        #shape model (ShapeModel) given by the frame where the shape
        #is displayed.
        ratio = self.GetDiagram().GetPanel().GetCurrentZoom()
        dx = self.GetDiagram().GetPanel().GetXOffset()
        dy = self.GetDiagram().GetPanel().GetYOffset()

        #  get the coords of this shape
        x, y = self.GetPosition()

        #calculation of the model coords in the light of the
        #offsets and ratio and assignement.
        mx = (x - dx)/ratio
        my = (y - dy)/ratio
        model.SetPosition(mx, my)

        #change also the position of the model of the children,
        #because when we move the parent children setposition isn't called
        #and so their updatemodel isn't called
        for child in self._anchors : #  + self.GetAllChildren():
            cx, cy = child.GetPosition()
            cmx = (cx - dx) / ratio
            cmy = (cy - dy) / ratio
            child.GetModel().SetPosition(cmx, cmy)

    def GetModel(self):
        """
        Added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (12.11.2005)
        @return the model of the shape (MVC pattern)
        """
        return self._model

    def SetModel(self, modelShape):
        """
        Added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (12.11.2005)
        Set the specified model associated to this shape (MVC pattern)

        @param modelShape ShapeModel  : model to set
        """
        self._model = modelShape

    def HasDiagramFrame(self):
        """
        Added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (12.11.2005)

        @return true if the shape has a diagram and if this diagram has
        a diagram frame.
        """
        if self.GetDiagram() is not None:
            return self.GetDiagram().GetPanel() is not None
        else:
            return False

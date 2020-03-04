
from typing import Union
from typing import Tuple

from logging import Logger
from logging import getLogger
from logging import DEBUG as pythonDebugLoggingLevel

from wx import BLACK_PEN
from wx import Brush
from wx import DC
from wx import Font
from wx import Pen
from wx import RED
from wx import RED_PEN
from wx import WHITE_BRUSH

from org.pyut.MiniOgl.ShapeModel import ShapeModel


class Shape:
    """
    Shape is the basic graphical block. It is also the view in
    a MVC pattern, so it has has a relative model (ShapeModel).
    """

    ID = 0  # internal ID number
    clsLogger: Logger = getLogger(__name__)

    def __init__(self, x: float = 0.0, y: float = 0.0, parent=None):
        """
        If a parent is given, the position is relative to the parent's origin.

        Args:
            x: position of the shape on the diagram
            y: position of the shape on the diagram
            parent:
        """
        self._x: float = x      # shape position (view)
        self._y: float = y      # shape position (view)
        self._ox: float = 0.0   # origin position (view)
        self._oy: float = 0.0   # origin position (view)

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

        self._pen:   Pen   = BLACK_PEN    # pen to use
        self._brush: Brush = WHITE_BRUSH  # brush to use

        self._model = ShapeModel(self)  # model of the shape (MVC pattern)

        self._id = Shape.ID     # unique ID number
        Shape.ID += 1
        if self.clsLogger.level == pythonDebugLoggingLevel:
            from org.pyut.MiniOgl.TextShape import TextShape
            from org.pyut.MiniOgl.LineShape import LineShape
            if not isinstance(self, (TextShape, LineShape)):
                t: Union[TextShape, LineShape] = self.AddText(0, -10, str(self._id))
                t.SetColor(RED)

    def SetPen(self, pen: Pen):
        """
        Set the pen used to draw the shape.

        @param pen
        """
        self._pen = pen

    def GetPen(self):
        """
        Get the pen used to draw the shape.

        @return wx.Pen
        """
        return self._pen

    def SetBrush(self, brush: Brush):
        """
        Set the brush used to draw the shape.

        @param brush
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

    def SetID(self, theId):
        """
        Set the ID of the shape. This can be used when loading a shape.

        @param theId
        """
        self._id = theId
        Shape.ID = max(self._id + 1, Shape.ID)

    def SetOrigin(self, x: float, y: float):
        """
        Set the origin of the shape, from its upper left corner.

        @param  x  new origin
        @param  y new origin
        """
        self._ox, self._oy = x, y

    def GetOrigin(self):
        """
        Get the origin of the shape, from its upper left corner.

        @return double x, y : origin
        """
        return self._ox, self._oy

    def AppendChild(self, child: "Shape"):
        """
        Append a child to this shape.
        This doesn't add it to the diagram, but it will be drawn by the parent.

        @param  child
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

        @param double x : position of the new point, relative to the origin of the shape
        @param double y : position of the new point, relative to the origin of the shape
        @param class anchorType : class to use as anchor point, or None for default (AnchorPoint)

        @return AnchorPoint : the created anchor
        """
        from org.pyut.MiniOgl.AnchorPoint import AnchorPoint     # I don't like in module imports but there is a cyclical dependency somewhere

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

        @param  anchor
        """
        if anchor in self._anchors:
            self._anchors.remove(anchor)

    def AddText(self, x: float, y: float, text: str, font: Font = None):
        """
        Add a text shape to the shape.
        Args:
            x : position of the text, relative to the origin of the shape
            y : position of the text, relative to the origin of the shape
            text : text to add
            font: font to use

        Returns:
            The created shape
        """
        t = self._CreateTextShape(x, y, text, font=font)
        self._children.append(t)

        return t

    def _AddPrivateText(self, x: float, y: float, text: str, font: Font = None):
        """
        Add a text shape, putting it in the private children of the shape.
        It won't be saved !!! This is used in constructor of child classes.

        Args:
            x,: position of the text, relative to the origin of the shape
            y : position of the text, relative to the origin of the shape
            text: text to add
            font: font to use

        Returns:  TextShape : the created shape
        """
        t = self._CreateTextShape(x, y, text, font=font)
        self._privateChildren.append(t)
        return t

    def _CreateTextShape(self, x: float, y: float, text: str, font: Font = None):
        """
        Create a text shape and add it to the diagram.

        Args:
            x,: position of the text, relative to the origin of the shape
            y : position of the text, relative to the origin of the shape
            text: text to add
            font: font to use

        Returns:  TextShape : the created shape

        """
        from org.pyut.MiniOgl.TextShape import TextShape
        t = TextShape(x, y, text, self, font=font)
        if self._diagram is not None:
            self._diagram.AddShape(t)
        self.clsLogger.debug(f"Text: {t} added")
        return t

    def Attach(self, diagram):
        """
        Don't use this method, use Diagram.AddShape instead !!!
        Attach the shape to a diagram.
        When you create a new shape, you must attach it to a diagram before
        you can see it. This method is used internally by Diagram.AddShape.

        @param  diagram
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
        self.clsLogger.debug(f"In shape.Detach with: {self}")
        if self._diagram is not None and not self._protected:
            self.clsLogger.debug(f"passed first condition")

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

            # self.clsLogger.debug("now, the shapes are", diagram.GetShapes())

    def Draw(self, dc: DC, withChildren: bool = True):
        """
        Draw the shape.
        For a shape, only the anchors are drawn. Nothing is drawn if the
        shape is set invisible.
        For children classes, the main classes would normally call it's
        parent's Draw method, passing withChildren = False, and finally
        calling itself the DrawChildren method.

        Args:
            dc:             wxPython device context
            withChildren:   draw the children or not
        """

        if self._visible:
            dc.SetPen(self._pen)
            dc.SetBrush(self._brush)
            if withChildren:
                self.DrawChildren(dc)

        if self._selected:
            dc.SetPen(RED_PEN)
            self.DrawHandles(dc)

    def DrawChildren(self, dc: DC):
        """
        Draw the children of this shape.

        Args:
            dc:
        """
        if self._visible:
            for child in self._children + self._anchors + self._privateChildren:
                child.Draw(dc)

    def DrawBorder(self, dc):
        """
        Draw the border of the shape, for fast rendering.

        @param dc
        """
        pass

    def DrawAnchors(self, dc):
        """
        Draw the anchors of the shape.

        @param dc
        """
        #  print "Shape.DrawAnchors; shape=", self, ", anchors=", self._anchors
        map(lambda x: x.Draw(dc), self._anchors)

    def DrawHandles(self, dc: DC):
        """
        Draw the handles (selection points) of the shape.
        A shape has no handles, because it has no size.

        @param  dc
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

    def SetParent(self, parent: 'Shape'):
        """
        Set the parent of this shape.

        @param parent
        """
        self._parent = parent

    def GetPosition(self) -> Tuple[float, float]:
        """
        Return the absolute position of the shape.
        It is in the diagram's coordinate system.

        Returns: An x,y tuple

        """
        if self._parent is not None:
            x, y = self._parent.GetPosition()
            return self._x + x, self._y + y
        else:
            return self._x, self._y

    def GetTopLeft(self):
        """
        Get the coordinates of the top left point in diagram coordinates.

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

    def Inside(self, x, y) -> bool:
        """

        Args:
            x: x coordinate
            y: y coordinate

        Returns:          `True` if (x, y) is inside the shape.
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

        @param state
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

        @param state
        """
        self._moving = state
        for shape in self._children:
            shape.SetMoving(state)
        for anchor in self._anchors:
            anchor.SetMoving(state)

    def SetDraggable(self, drag):
        """
        If False, the shape won't be movable.

        @param drag
        """
        self._draggable = drag

    def SetPosition(self, x: float, y: float):
        """
        Change the position of the shape, if it's draggable.

        @param x
        @param y
        """
        if self._draggable:
            if self._parent is not None:
                self._x, self._y = self.ConvertCoordToRelative(x, y)
            else:
                self._x = x
                self._y = y

            # added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (12.11.2005)
            #  if the shape is attached to a diagramFrame, it means that
            #  the model will be initialized correctly.
            # (Avoid a null pointer error).
            if self.HasDiagramFrame():
                self.UpdateModel()

    def SetRelativePosition(self, x: float, y: float):
        """
        Set the position of the shape, relative to the parent.
        Only works if the shape is draggable.

        @param x
        @param y
        """
        if self._draggable:
            self._x = x
            self._y = y

    def SetProtected(self, newValue: bool):
        """
        Protect the shape against deletion (Detach).

        @param newValue
        """
        self._protected = newValue

    def SetSize(self, w: float, h: float):
        """
        Set the size of the shape.

        @param  w, width
        @param h : height of the shape
        """
        pass

    def SetVisible(self, theNewValue: bool):
        """
        Set the shape visible or not.

        @param theNewValue
        """
        self._visible = theNewValue

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

        # Get the coordinates of the model (ShapeModel)
        mx, my = self.GetModel().GetPosition()

        # Get the offsets and the ratio between the shape (view) and the
        # shape model (ShapeModel) given by the frame where the shape
        # is displayed.
        ratio = self.GetDiagram().GetPanel().GetCurrentZoom()
        dx = self.GetDiagram().GetPanel().GetXOffset()
        dy = self.GetDiagram().GetPanel().GetYOffset()

        # calculation of the shape (view) coordinates in the light of the offsets and ratio
        x = (ratio * mx) + dx
        y = (ratio * my) + dy

        # assign the new coordinates to the shape (view). DON'T USE SetPosition(),
        # because there is a call to UpdateModel() in that method.
        if self._parent is not None:
            self._x, self._y = self.ConvertCoordToRelative(x, y)
        else:
            self._x = x
            self._y = y

    def UpdateModel(self):
        """
        Added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (12.11.2005)
        Updates the coordinates of the model (ShapeModel) when the Shape (view)
        is moved.
        """

        #  get the associated model (ShapeModel)
        model = self.GetModel()

        # Get the offsets and the ratio between the shape (view) and the
        # shape model (ShapeModel) given by the frame where the shape
        # is displayed.
        ratio = self.GetDiagram().GetPanel().GetCurrentZoom()
        dx = self.GetDiagram().GetPanel().GetXOffset()
        dy = self.GetDiagram().GetPanel().GetYOffset()

        #  get the coordinates of this shape
        x, y = self.GetPosition()

        # calculation of the model coordinates in the light of the
        # offsets and ratio and assignment.
        mx = (x - dx)/ratio
        my = (y - dy)/ratio
        model.SetPosition(mx, my)

        # change also the position of the model of the children,
        # because when we move the parent children set position is not called
        # and so their update model is not called
        for child in self._anchors:
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

        @param modelShape : model to set
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

    def __repr__(self):
        """
        String representation.

        @return String
        """
        return object.__repr__(self) + " : " + str(self._id)


from typing import cast
from typing import List

from logging import Logger
from logging import getLogger

import wx

from MiniOgl.Diagram import Diagram
from MiniOgl.ShapeEventHandler import ShapeEventHandler
from MiniOgl.SizerShape import SizerShape
from MiniOgl.ControlPoint import ControlPoint
from MiniOgl.RectangleShape import RectangleShape

__all__ = ["DiagramFrame"]

DEBUG = 0  # set to 1 to have some debug info in the terminal

LEFT_MARGIN     = 0
RIGHT_MARGIN    = 1
TOP_MARGIN      = 2
BOTTOM_MARGIN   = 3


class DiagramFrame(wx.ScrolledWindow):
    """
    A frame to draw simulation diagrams.
    This frame also manage all mouse events.
    It has a Diagram automatically associated.


    @author Laurent Burgbacher <lb@alawa.ch>
    """
    def __init__(self, parent: wx.Window):
        """
        Constructor.

        @param parent window
        """
        super().__init__(parent)

        self.logger: Logger = getLogger(__name__)

        self._diagram = Diagram(self)

        self.__keepMoving       = False
        self._selectedShapes    = []        # list of the shapes that are selected
        self._lastMousePosition = None
        self._selector          = None      # rectangle selector shape
        self._clickedShape      = None      # last clicked shape
        self._moving            = False     # a drag has been initiated

        self._xOffset = 0.0     # abscissa offset between the view and the model
        self._yOffset = 0.0     # ordinate offset between the view and the model
        self._zoomStack = []    # cstore all zoom factors applied

        self._zoomLevel = 0             # number of zoom factors applied
        self._maxZoomFactor = 6         # can zoom in beyond 600%
        self._minZoomFactor = 0.2       # can zoom out beyond 20%
        self._defaultZoomFactor = 1.5   # used when only a point is selected

        # margins define a perimeter around the work area that must remains
        # blank and hidden. if we scroll beyond the limits, the diagram is
        # resized.
        DEFAULT_MARGIN_VALUE = 100
        self._leftMargin = DEFAULT_MARGIN_VALUE
        self._rightMargin = DEFAULT_MARGIN_VALUE
        self._topMargin = DEFAULT_MARGIN_VALUE
        self._bottomMargin = DEFAULT_MARGIN_VALUE
        self._isInfinite = False    # to know if the frame is infinite or not

        # paint related
        w, h = self.GetSize()
        self.__workingBitmap    = wx.Bitmap(w, h)   # double buffering
        self.__backgroundBitmap = wx.Bitmap(w, h)

        DEFAULT_FONT_SIZE = 12
        self._defaultFont = wx.Font(DEFAULT_FONT_SIZE, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.SetBackgroundColour(wx.WHITE)

        # Mouse events
        self.Bind(wx.EVT_LEFT_DOWN,     self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP,       self.OnLeftUp)
        self.Bind(wx.EVT_LEFT_DCLICK,   self.OnLeftDClick)
        self.Bind(wx.EVT_MIDDLE_DOWN,   self.OnMiddleDown)
        self.Bind(wx.EVT_MIDDLE_UP,     self.OnMiddleUp)
        self.Bind(wx.EVT_MIDDLE_DCLICK, self.OnMiddleDClick)
        self.Bind(wx.EVT_RIGHT_DOWN,    self.OnRightDown)
        self.Bind(wx.EVT_RIGHT_UP,      self.OnRightUp)
        self.Bind(wx.EVT_RIGHT_DCLICK,  self.OnRightDClick)
        self.Bind(wx.EVT_PAINT,         self.OnPaint)

    def getEventPosition(self, event: wx.MouseEvent):
        """
        Return the position of a click in the diagram.

        @param  event : mouse event

        @return (int, int) : x, y
        """

        x, y = self._ConvertEventCoords(event)  # Updated by CD, 20041005
        return x, y

    def GenericHandler(self, event: wx.MouseEvent, methodName: str):
        """
        This handler finds the shape at event coords and dispatch the event.
        The handler will receive an event with coords already unscrolled.

        @param wx.Event event : original event
        @param string methodName : name of the method to invoke in the
            event handler of the shape
        @return Shape : the clicked shape
        """
        if DEBUG:
            self.logger.info(f"Generic for: {methodName}")
        x, y = self.getEventPosition(event)
        self.logger.info(f'GenericHandler - {methodName} x,y: {x},{y}')
        shape = self.FindShape(x, y)
        event.m_x, event.m_y = x, y
        # event.SetX(x)
        # event.SetY(y)
        # if the shape found is a ShapeEventHandler
        if shape and isinstance(shape, ShapeEventHandler):
            getattr(shape, methodName)(event)
        else:
            event.Skip()
        return shape

    def OnLeftDown(self, event: wx.MouseEvent):
        """
        Callback for left down events on the diagram.

        @param  event
        """
        if DEBUG:
            self.logger.info("DiagramFrame.OnLeftDown")

        # First, call the generic handler for OnLeftDown
        shape = self.GenericHandler(event, "OnLeftDown")
        self._clickedShape = shape  # store the last clicked shape
        if not event.GetSkipped():
            return
        if shape is None:
            self._BeginSelect(event)
            return

        # manage click and drag
        x, y = event.GetX(), event.GetY()
        # print "OnLeftDown, event=(%s, %s); %s; (%s, %s))" % (event.GetX(), event.GetY(), event.GetPosition(), x, y)
        self._lastMousePosition = (x, y)

        if not event.ControlDown() and not shape.IsSelected():
            shapes = self._diagram.GetShapes()
            shapes.remove(shape)
            if isinstance(shape, SizerShape):
                # don't deselect the parent of a sizer
                # or its sizers would be detached
                shapes.remove(shape.GetParent())
            elif isinstance(shape, ControlPoint):
                # don't deselect the line of a control point
                for line in shape.GetLines():
                    shapes.remove(line)
            # don't call DeselectAllShapes, because we must ensure that
            # sizers won't be deselected (because they're detached when they're
            # deselected)
            # deselect all other shapes
            for s in shapes:
                s.SetSelected(False)
                s.SetMoving(False)

            self._selectedShapes = [shape]
            shape.SetSelected(True)
            shape.SetMoving(True)
            self._clickedShape = None
            self.Refresh()

        self.Bind(wx.EVT_MOTION, self.OnMove)

    def _BeginSelect(self, event: wx.MouseEvent):
        """
        Create a selector box and manage it.

        @param  event
        """
        if not event.ControlDown():
            self.DeselectAllShapes()
        x, y = event.GetX(), event.GetY() # event position has been modified
        self._selector = rect = RectangleShape(x, y, 0, 0)
        rect.SetDrawFrame(True)
        rect.SetBrush(wx.TRANSPARENT_BRUSH)
        rect.SetMoving(True)
        self._diagram.AddShape(rect)
        self.PrepareBackground()
        self.Bind(wx.EVT_MOTION, self._OnMoveSelector)

    def _OnMoveSelector(self, event: wx.MouseEvent):
        """
        Callback for the selector box.

        @param  event
        """
        if self._selector is not None:
            x, y = self.getEventPosition(event)
            x0, y0 = self._selector.GetPosition()
            self._selector.SetSize(x - x0, y - y0)
            self.Refresh(False)

    def OnLeftUp(self, event: wx.MouseEvent):
        """
        Callback for left up events.

        @param event
        """
        # manage the selector box
        if self._selector is not None:
            self.Bind(wx.EVT_MOTION, self._NullCallback)
            rect = self._selector
            x, y = rect.GetPosition()
            w, h = rect.GetSize()
            for shape in self._diagram.GetShapes():
                x0, y0 = shape.GetTopLeft()
                w0, h0 = shape.GetSize()
                if shape.GetParent() is None and \
                   rect.Inside(x0, y0) and \
                   rect.Inside(x0 + w0, y0) and \
                   rect.Inside(x0, y0 + h0) and \
                   rect.Inside(x0 + w0, y0 + h0):
                    shape.SetSelected(True)
                    shape.SetMoving(True)
                    self._selectedShapes.append(shape)
            rect.Detach()
            self._selector = None
        if not self._moving and self._clickedShape:
            clicked = self._clickedShape
            if not event.ControlDown():
                self.DeselectAllShapes()
                self._selectedShapes = [clicked]
                clicked.SetSelected(True)
                clicked.SetMoving(True)
            else:
                sel = not clicked.IsSelected()
                clicked.SetSelected(sel)
                clicked.SetMoving(sel)
                if sel and clicked not in self._selectedShapes:
                    self._selectedShapes.append(clicked)
                elif not sel and clicked in self._selectedShapes:
                    self._selectedShapes.remove(clicked)
            self._clickedShape = None
            self.Refresh()

        self._moving = False

        # normal event management
        self.GenericHandler(event, "OnLeftUp")
        if not self.__keepMoving:
            self.Bind(wx.EVT_MOTION, self._NullCallback)
            self.Refresh()

    def OnDrag(self, event: wx.MouseEvent):
        """
        Callback to drag the selected shapes.

        @param  event
        """
        x, y = event.GetX(), event.GetY()
        if not self._moving:
            self.PrepareBackground()
        self._moving = True
        clicked = self._clickedShape
        if clicked and not clicked.IsSelected():
            self._selectedShapes.append(clicked)
            clicked.SetSelected(True)
            clicked.SetMoving(True)
        self._clickedShape = None
        for shape in self._selectedShapes:
            parent = shape.GetParent()
            if parent is not None and parent.IsSelected() and not isinstance(shape, SizerShape):
                continue
            ox, oy = self._lastMousePosition
            dx, dy = x - ox, y - oy
            sx, sy = shape.GetPosition()
            shape.SetPosition(sx + dx, sy + dy)

        self.Refresh(False)
        self._lastMousePosition = (x, y)

    def OnMove(self, event: wx.MouseEvent):
        """
        Callback for mouse movements.

        @param  event
        """
        event.m_x, event.m_y = self.getEventPosition(event)
        self.OnDrag(event)

    def OnLeftDClick(self, event: wx.MouseEvent):
        """
        Callback for left double clicks.

        @param  event
        """
        self.GenericHandler(event, "OnLeftDClick")
        self._clickedShape = None
        if not self.__keepMoving:
            self.Bind(wx.EVT_MOTION, self._NullCallback)

    def OnMiddleDown(self, event: wx.MouseEvent):
        """
        Callback.

        @param  event
        """
        self.GenericHandler(event, "OnMiddleDown")

    def OnMiddleUp(self, event: wx.MouseEvent):
        """
        Callback.

        @param  event
        """
        self.GenericHandler(event, "OnMiddleUp")

    def OnMiddleDClick(self, event: wx.MouseEvent):
        """
        Callback.

        @param  event
        """
        self.GenericHandler(event, "OnMiddleDClick")

    def OnRightDown(self, event: wx.MouseEvent):
        """
        Callback.

        @param  event
        """
        self.GenericHandler(event, "OnRightDown")

    def OnRightUp(self, event: wx.MouseEvent):
        """
        Callback.

        @param  event
        """
        self.GenericHandler(event, "OnRightUp")

    def OnRightDClick(self, event: wx.MouseEvent):
        """
        Callback.

        @param  event
        """
        # DEBUG
        import wx
        # import wx.py as py
        crustWin = wx.Dialog(self, -1, "PyCrust", (0, 0), (640, 480))
        # win = py.crust.Crust(crustWin)
        crustWin.Show()
        self.GenericHandler(event, "OnRightDClick")

    def GetDiagram(self):
        """
        Return the diagram associated with this panel.

        @return Diagram
        """
        return self._diagram

    def SetDiagram(self, diagram):
        """
        Set a new diagram for this panel.

        @param diagram
        """
        self._diagram = diagram

    from MiniOgl.Shape import Shape

    def FindShape(self, x: int, y: int):
        """
        Return the shape at (x, y).

        @param x : coord
        @param y : coord

        @return Shape : found shape or None
        """
        found = None
        shapes = self._diagram.GetShapes()
        shapes.reverse()    # to select the one at the top
        for shape in shapes:
            if shape.Inside(x, y):
                if DEBUG:
                    self.logger.info(f"Inside: {shape}")
                found = shape
                break   # only select the first one
        return found

    def DeselectAllShapes(self):
        """
        Deselect all shapes in the frame.
        """
        for shape in self._diagram.GetShapes():
            shape.SetSelected(False)
            shape.SetMoving(False)
        self._selectedShapes = []

    def GetSelectedShapes(self):
        """
        Get the selected shapes.
        Beware, this is the list of the frame, but other shapes could be
        selected and not declared to the frame.

        @return Shape []
        """
        return self._selectedShapes

    def SetSelectedShapes(self, shapes: List[Shape]):
        """
        Set the list of selected shapes.

        @param shapes
        """
        self._selectedShapes = shapes

    def KeepMoving(self, keep):
        """
        Tell the frame to continue capturing the mouse movements.
        Even after a mouse up event.

        @param bool keep : True to continue capturing mouse move events
        """
        self.__keepMoving = keep
        if not keep:
            self.Bind(wx.EVT_MOTION, self._NullCallback)

    def Refresh(self, eraseBackground=True, rect=None):
        """
        This refresh is done imediately, not through an event.

        @param bool eraseBackground : if False, the stored background is used
        @param wx.Rect rect : not used
        """
        if eraseBackground:
            self.Redraw()
        else:
            self.RedrawWithBackground()

    def SaveBackground(self, dc):
        """
        Save the given dc as the new background image.

        @param wx.DC dc : the dc to save
        """
        w, h = self.GetSize()
        bb = self.__backgroundBitmap
        if (bb.GetWidth(), bb.GetHeight()) != (w, h):
            bb = self.__backgroundBitmap = wx.Bitmap(w, h)
        mem = wx.MemoryDC()
        mem.SelectObject(bb)

        if wx.__version__ > "2.3.2":
            x, y = self.CalcUnscrolledPosition(0, 0)
            mem.Blit(0, 0, w, h, dc, x, y)
        else:
            mem.Blit(0, 0, w, h, dc, 0, 0)
        mem.SelectObject(wx.NullBitmap)

    def LoadBackground(self, dc: wx.DC, w: int, h: int):
        """
        Load the background image in the given dc.

        Args:
            dc:
            w:
            h:

        Returns:

        """
        mem = wx.MemoryDC()
        mem.SelectObject(self.__backgroundBitmap)
        dc.Blit(0, 0, w, h, mem, 0, 0)
        mem.SelectObject(wx.NullBitmap)

    def ClearBackground(self):
        """
        Clear the background image.
        """
        dc = wx.MemoryDC()
        bb = self.__backgroundBitmap
        w, h = self.GetSize()
        if (bb.GetWidth(), bb.GetHeight()) != (w, h):
            bb = self.__backgroundBitmap = wx.EmptyBitmap(w, h)
        dc.SelectObject(bb)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        dc.SelectObject(wx.NullBitmap)

    def CreateDC(self, loadBackground: bool, w: int, h: int) -> wx.DC:
        """
        Create a DC, load the background on demand.

        @param loadBackground
        @param w : width of the frame.
        @param h :  height of the frame.

        @return wx.DC
        """
        dc = wx.MemoryDC()
        bm = self.__workingBitmap
        # cache the bitmap, to avoid creating a new at each refresh.
        # only recreate it if the size of the window has changed
        if (bm.GetWidth(), bm.GetHeight()) != (w, h):
            bm = self.__workingBitmap = wx.Bitmap(w, h)
        dc.SelectObject(bm)
        if loadBackground:
            self.LoadBackground(dc, w, h)
        else:
            dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
            dc.Clear()
        self.PrepareDC(dc)

        return dc

    def PrepareBackground(self):
        """
        Redraw the screen without movable shapes, store it as the background.
        """
        self.Redraw(cast(wx.DC, None), True, True, False)

    def RedrawWithBackground(self):
        """
        Redraw the screen using the background.
        """
        self.Redraw(cast(wx.DC, None), True, False, True)

    def Redraw(self, dc=None, full=True, saveBackground=False, useBackground=False):
        """
        Refresh the diagram graphically.
        If a dc is given, use it. Otherwise, a double buffered dc is used.

        @param wx.DC dc : if None, a default dc will be created
        @param bool full : if 0, only draws the borders of shapes
        @param bool saveBackground : if True, the background will be saved
        @param bool useBackground : if True, the background will be used
        """
        needBlit = False
        w, h = self.GetSize()

        if dc is None:
            dc = self.CreateDC(useBackground, w, h)
            needBlit = True

        dc.SetFont(self._defaultFont)

        shapes = self._diagram.GetShapes()

        if full:
            # first time, need to create the background
            if saveBackground:
                # first, draw every non moving shapes
                for shape in shapes:
                    if not shape.IsMoving():
                        shape.Draw(dc)
                # save the background
                self.SaveBackground(dc)
                # draw every moving shapes
                for shape in shapes:
                    if shape.IsMoving():
                        shape.Draw(dc)
            if useBackground:
                # draw every moving shapes
                for shape in shapes:
                    if shape.IsMoving():
                        shape.Draw(dc)
            else:  # don't use background
                # draw all shapes
                for shape in shapes:
                    shape.Draw(dc)
        else:  # not full
            for shape in shapes:
                shape.DrawBorder(dc)
                shape.DrawAnchors(dc)

        if needBlit:
            #  MODIFIED BY C.DUTOIT : Added wx.Python test
            client = wx.ClientDC(self)

            if wx.__version__ > "2.3.2":
                x, y = self.CalcUnscrolledPosition(0, 0)
                client.Blit(0, 0, w, h, dc, x, y)
            else:
                client.Blit(0, 0, w, h, dc, 0, 0)

    # noinspection PyUnusedLocal
    def OnPaint(self, event: wx.PaintEvent):
        """
        Callback.
        Refresh the screen when a paint event is issued by the system.

        @param event
        """
        dc = wx.PaintDC(self)
        w, h = self.GetSize()
        mem = self.CreateDC(False, w, h)
        mem.SetBackground(wx.Brush(self.GetBackgroundColour()))
        mem.Clear()
        self.Redraw(mem)

        if wx.__version__ > "2.3.2":
            x, y = self.CalcUnscrolledPosition(0, 0)
            dc.Blit(0, 0, w, h, mem, x, y)
        else:
            dc.Blit(0, 0, w, h, mem, 0, 0)

    def _NullCallback(self, evt):
        pass

    def _ConvertEventCoords(self, event):
        xView, yView = self.GetViewStart()
        xDelta, yDelta = self.GetScrollPixelsPerUnit()
        return event.GetX() + (xView * xDelta), event.GetY() + (yView * yDelta)

    def GetCurrentZoom(self):
        """
        added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (11.11.2005)
        @return the global current zoom factor.
        """
        zoom = 1.0
        for z in self._zoomStack:
            zoom *= z
        return zoom

    def GetXOffset(self):
        """
        added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (11.11.2005)
        @return the x offset between the model an the view of the shapes (MVC)
        """
        return self._xOffset

    def GetYOffset(self):
        """
        added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (11.11.2005)
        @return the y offset between the model an the view of the shapes (MVC)
        """
        return self._yOffset

    def SetXOffset(self, offset):
        """
        added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (11.11.2005)
        Set the x offset between the model an the view of the shapes (MVC)
        """
        self._xOffset = offset

    def SetYOffset(self, offset):
        """
        added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (11.11.2005)
        Set the y offset between the model an the view of the shapes (MVC)
        """
        self._yOffset = offset

    def SetDefaultZoomFactor(self, factor):
        """
        added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (11.11.2005)
        Set the default zoom factor (1 = 100%)
        """
        self._defaultZoomFactor = factor

    def SetMaxZoomFactor(self, factor):
        """
        added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (11.11.2005)
        Set the maximal zoom factor that can be reached (1 = 100%)
        """
        self._maxZoomFactor = factor

    def GetDefaultZoomFactor(self):
        """
        added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (11.11.2005)
        @return the default zoom factor. (1 = 100%)
        """
        return self._defaultZoomFactor

    def GetMaxZoomFactor(self):
        """
        added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (11.11.2005)
        @return the maximal zoom factor that can be reached. (1 = 100%)
        """
        return self._maxZoomFactor

    def SetMinZoomFactor(self, factor):
        """
        added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (11.11.2005)
        Set the minimal zoom factor that can be reached. (1 = 100%)
        """
        self._minLevelZoom = factor

    def GetMinZoomFactor(self):
        """
        added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (11.11.2005)
        @return the minimal zoom factor that can be reached. (1 = 100%)
        """
        return self._minZoomFactor

    def DoZoomIn(self, ax, ay, width=0, height=0):
        """
        added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (11.11.2005)

        Do the "zoom in" fitted on the selected area or with a default factor
        and the clicked point as central point of the zoom.
        The maximal zoom that can be reached is :

            self.GetMaxLevelZoom() * self.GetDefaultZoomFactor()

        If the maximal zoom level is reached, then the shapes are just centered
        on the selected area or on the clicked point.

        @param ax        :  abscissa of the upper left corner of the selected
                            area or abscissa of the central point of the zoom

        @param ay        :  ordinate of the upper left corner of the selected
                            area or ordinate of the central point of the zoom

        @param width    :   width of the selected area for the zoom

        @param height   :   height of the selected area for the zoom
        """

        # number of pixels per unit of scrolling
        xUnit, yUnit = self.GetScrollPixelsPerUnit()

        # position of the upper left corner of the client area
        # (work area that is visible) in scroll units.
        viewStartX, viewStartY = self.GetViewStart()

        # Get the client and virtual size of the work area, where
        # the client size is the size of the work area that is
        # visible and the virtual is the whole work area's size.
        clientWidth, clientHeight = self.GetClientSize()
        virtualWidth, virtualHeight = self.GetVirtualSize()

        # maximal zoom factor that can be applied
        # maxZoomFactor = self.GetMaxLevelZoom() * self.GetDefaultZoomFactor()
        maxZoomFactor = self.GetMaxZoomFactor()

        # transform event coords to get them relative to the upper left corner of
        # the virual screen (avoid the case where that corner is on a shape and
        # get its coords relative to the client view).
        if ax >= viewStartX * xUnit and ay >= viewStartY * yUnit:
            x = ax
            y = ay
        else:
            x = ax + viewStartX * xUnit
            y = ay + viewStartY * yUnit

        # to get the upper left corner of the zoom selected area in the
        # case where we select first the bottom right corner.
        if width < 0:
            x = x - width
        if height < 0:
            y = y - height

        # init the zoom's offsets and factor
        # zoomFactor = 1
        # dx = 0
        # dy = 0

        # if there is no selected area but a clicked point, a default
        # zoom is performed with the clicked point as center.
        if width == 0 or height == 0:
            zoomFactor = self.GetDefaultZoomFactor()
            # check if the zoom factor that we are to apply combined with the
            # previous ones won't be beyond the maximal zoom. If it's the case,
            # we proceed to the calculation of the zoom factor that allows to
            # exactly reach the maximal zoom.
            maxZoomReached = maxZoomFactor <= (self.GetCurrentZoom() * zoomFactor)
            if maxZoomReached:
                zoomFactor = maxZoomFactor/self.GetCurrentZoom()
            # if the view is reduced, we just eliminate the
            # last zoom out performed
            if self._zoomLevel < 0:
                self._zoomStack.pop()
                self._zoomLevel += 1
            else:
                if zoomFactor > 1.0:
                    self._zoomStack.append(zoomFactor)
                    self._zoomLevel += 1

            # calculation of the upper-left corner of a zoom area whose
            # size is the half of the diagram frame and which is centred
            # on the clicked point. This calculation is done in the way to
            # get the zoom area centred in the middle of the virtual screen.
            dx = virtualWidth/2 - x
            dy = virtualHeight/2 - y

        else:
            # to be sure to get all the shapes in the selected zoom area
            if width > height:
                zoomFactor = clientWidth / abs(width)
            else:
                zoomFactor = clientHeight / abs(height)

            # check if the zoom factor that we are to apply combined with the
            # previous ones won't be beyond the maximal zoom. If it's the case,
            # we proceed to the calculation of the zoom factor that allows to
            # exactly reach the maximal zoom.
            maxZoomReached = maxZoomFactor <= self.GetCurrentZoom() * zoomFactor
            if maxZoomReached:
                zoomFactor = maxZoomFactor/self.GetCurrentZoom()

            # calculation of the upper-left corner of a zoom area whose
            # size is the half of the diagram frame and which is centred
            # on the clicked point. This calculation is done in the way to
            # get the zoom area centred in the middle of the virtual screen.
            dx = virtualWidth/2 - x - (clientWidth / zoomFactor / 2.0)
            dy = virtualHeight/2 - y - (clientHeight / zoomFactor / 2.0)

            # we have to check if the "zoom in" on a reduced view produce
            # an other less reduced view or an elarged view. For this, we
            # get the global current zoom, multiply by the zoom factor to
            # obtain only one zoom factor.
            if self._zoomLevel < 0:

                globalFactor = zoomFactor * self.GetCurrentZoom()
                self._zoomStack = []
                self._zoomStack.append(globalFactor)

                if globalFactor < 1.0:
                    self._zoomLevel = -1    # the view is still reduced
                elif globalFactor > 1.0:
                    self._zoomLevel = 1     # the view is enlarged
                else:
                    self._zoomLevel = 0     # the zoom in is just equal to all the zoom out previously applied
            else:
                if zoomFactor > 1.0:
                    self._zoomStack.append(zoomFactor)
                    self._zoomLevel += 1

        # set the offsets between the model and the view
        self.SetXOffset((self.GetXOffset() + dx) * zoomFactor)
        self.SetYOffset((self.GetYOffset() + dy) * zoomFactor)

        # updates the shapes (view) position and dimensions from
        # their models in the light of the new zoom factor and offsets.
        for shape in self.GetDiagram().GetShapes():
            shape.UpdateFromModel()

        # resize the virutal screen in order to match with the zoom
        virtualWidth = (virtualWidth) * zoomFactor
        virtualHeight = (virtualHeight) * zoomFactor
        virtualSize = wx.Size(virtualWidth, virtualHeight)
        self.SetVirtualSize(virtualSize)

        # perform the scrolling in the way to have the zoom area visible
        # and centred on the virutal screen.
        scrollX = (virtualWidth - clientWidth) /2 / xUnit
        scrollY = (virtualHeight - clientHeight) /2 /yUnit
        self.Scroll(scrollX, scrollY)

    def DoZoomOut(self, ax: int, ay: int):

        """
        added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (11.11.2005)

        Do the 'zoom out' in the way to have the clicked point (ax, ay) as
        the central point of new view.
        If one or many 'zoom in' where performed before, then we just suppress the
        last one from the zoom stack. Else, we add the default zoom factor inversed
        to the stack.

        @param ax  abscissa of the clicked point
        @param ay  ordinate of the clicked point
        """

        # number of pixels per unit of scrolling
        xUnit, yUnit = self.GetScrollPixelsPerUnit()

        # position of the upper left corner of the client area
        # (work area that is visible) in scroll units.
        viewStartX, viewStartY = self.GetViewStart()

        # Get the client and virtual size of the work area, where
        # the client size is the size of the work area that is
        # visible and the virtual is the whole work area's size.
        clientWidth, clientHeight = self.GetClientSize()
        virtualWidth, virtualHeight = self.GetVirtualSize()

        # transform event coords to get them relative to the upper left corner of
        # the virual screen (avoid the case where that corner is on a shape and
        # get its coords relative to the shape).
        if ax >= viewStartX * xUnit and ay >= viewStartY * yUnit :
            x = ax
            y = ay
        else:
            x = ax + viewStartX * xUnit
            y = ay + viewStartY * yUnit

        # calculation of the upper-left corner of a zoom area whose
        # size is the half of the diagram frame and which is centred
        # on the clicked point. This calculation is done in the way to
        # get the zoom area centred in the middle of the virtual screen.
        dx = virtualWidth/2 - x
        dy = virtualHeight/2 - y

        minZoomFactor = self.GetMinZoomFactor()
        minZoomReached = False

        # if the view is elarged, then we just remove the last
        # zoom in factor that has been applied. Else, we apply
        # the default one inversed.
        if self._zoomLevel > 0:
            zoomFactor = 1/self._zoomStack.pop()
            self._zoomLevel -= 1
        else:
            zoomFactor = 1/self.GetDefaultZoomFactor()
            # check if minimal zoom has been reached
            minZoomReached = minZoomFactor >= (self.GetCurrentZoom() * zoomFactor)
            if not minZoomReached:
                self._zoomStack.append(zoomFactor)
                self._zoomLevel -= 1
            else:
                zoomFactor = minZoomFactor / self.GetCurrentZoom()
                if zoomFactor != 1:
                    self._zoomStack.append(zoomFactor)
                    self._zoomLevel -= 1

        # set the offsets between the view and the model of the
        # each shape on this diagram frame.
        self.SetXOffset((self.GetXOffset() + dx) * zoomFactor)
        self.SetYOffset((self.GetYOffset() + dy) * zoomFactor)

        # updates the shapes (view) position and dimensions from
        # their model in the light of the new zoom factor and offsets.
        for shape in self.GetDiagram().GetShapes():
            shape.UpdateFromModel()

        # resize the virutal screen in order to match with the zoom
        virtualWidth  = virtualWidth * zoomFactor
        virtualHeight = virtualHeight * zoomFactor
        virtualSize = wx.Size(virtualWidth, virtualHeight)
        self.SetVirtualSize(virtualSize)

        # perform the scrolling in the way to have the zoom area visible
        # and centred on the virutal screen.
        scrollX = (virtualWidth - clientWidth) /2 / xUnit
        scrollY = (virtualHeight - clientHeight) /2 /yUnit
        self.Scroll(scrollX, scrollY)

    def SetMargins(self, left, right, top, bottom):
        """
        added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (11.11.2005
        set the size of the margins that can't be reached by the
        scrollbars if the frame is infinite.
        """
        self._leftMargin = left
        self._topMargin = top
        self._bottomMargin = bottom
        self._rightMargin = right

    def GetMargins(self):
        """
        added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (11.11.2005
        @return the size of the margins that can't be reached by the
        scrollbars if the frame is infinite.
        """
        return self._leftMargin, self._rightMargin, self._topMargin, self._bottomMargin

    def SetInfinite(self, infinite: bool = False):
        """
        added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (11.11.2005
        Set this diagram frame as infinite work area. The result is that the
        virtual size is elarged when the scrollbar reached the specified
        margins (see SetMargins). When we set this as true, the scrollbars
        are moved in the middle of their scale.

        @param infinite    : shows if the work area is infinite or not.
        """

        self._isInfinite = infinite

        if infinite:
            # place all the shape in an area centered on the infinite work area
            vWidth, vHeight = self.GetVirtualSize()
            cWidth, cHeight = self.GetClientSize()
            # get the number of pixels per scroll unit
            xUnit, yUnit = self.GetScrollPixelsPerUnit()

            # get the number of scroll unit
            noUnitX = (vWidth-cWidth) / xUnit
            noUnitY = (vHeight-cHeight) / yUnit

            # set the scrollbars position in the middle of their scale
            self.Scroll(noUnitX / 2, noUnitY / 2)

    def IsInfinite(self) -> bool:
        """
        added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (11.11.2005
        @return this frame is infinite.
        """
        return self._isInfinite

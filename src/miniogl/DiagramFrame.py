
from typing import Tuple
from typing import cast
from typing import List

from logging import Logger
from logging import getLogger

from wx import Colour
from wx import Rect
from wx import WHITE

from wx import EVT_LEFT_DCLICK
from wx import EVT_LEFT_DOWN
from wx import EVT_LEFT_UP
from wx import EVT_MIDDLE_DCLICK
from wx import EVT_MIDDLE_DOWN
from wx import EVT_MIDDLE_UP
from wx import EVT_MOTION
from wx import EVT_PAINT
from wx import EVT_RIGHT_DCLICK
from wx import EVT_RIGHT_DOWN
from wx import EVT_RIGHT_UP

from wx import FONTFAMILY_DEFAULT
from wx import FONTSTYLE_NORMAL
from wx import FONTWEIGHT_NORMAL
from wx import ID_ANY
from wx import SUNKEN_BORDER
from wx import TRANSPARENT_BRUSH

from wx import Bitmap
from wx import EmptyBitmap
from wx import Brush
from wx import ClientDC
from wx import DC
from wx import Dialog
from wx import PaintDC
from wx import PaintEvent
from wx import ScrolledWindow
from wx import Size
from wx import MemoryDC
from wx import MouseEvent
from wx import NullBitmap
from wx import Font
from wx import Window
from wx import Pen
from wx import PenInfo

# I know it is there
# noinspection PyUnresolvedReferences
from wx.core import PenStyle

from miniogl.Shape import Shape

from miniogl.Diagram import Diagram
from miniogl.MiniOglColorEnum import MiniOglColorEnum
from miniogl.MiniOglPenStyle import MiniOglPenStyle
from miniogl.ShapeEventHandler import ShapeEventHandler
from miniogl.SizerShape import SizerShape
from miniogl.ControlPoint import ControlPoint
from miniogl.RectangleShape import RectangleShape

from ogl.preferences.OglPreferences import OglPreferences

from miniogl.DlgDebugDiagramFrame import DlgDebugDiagramFrame


class DiagramFrame(ScrolledWindow):

    diagramFrameLogger: Logger = getLogger(__name__)

    """
    A frame to draw simulation diagrams.
    This frame also manage all mouse events.
    It has a Diagram automatically associated.
    """
    def __init__(self, parent: Window):
        """

        Args:
            parent:  parent window
        """
        super().__init__(parent, style=SUNKEN_BORDER)

        self._diagram = Diagram(self)

        self.__keepMoving:    bool        = False
        self._selectedShapes: List[Shape] = []        # list of the shapes that are selected

        self._lastMousePosition: Tuple[int, int] = cast(Tuple[int, int], None)
        self._selector:          RectangleShape  = cast(RectangleShape, None)     # rectangle selector shape

        self._clickedShape: Shape = cast(Shape, None)      # last clicked shape
        self._moving:       bool  = False     # a drag has been initiated

        self._xOffset:   float       = 0.0   # abscissa offset between the view and the model
        self._yOffset:   float       = 0.0   # ordinate offset between the view and the model
        self._zoomStack: List[float] = []    # store all zoom factors applied

        self._zoomLevel = 0             # number of zoom factors applied
        self._maxZoomFactor = 6         # can zoom in beyond 600%
        self._minZoomFactor = 0.2       # can zoom out beyond 20%
        self._defaultZoomFactor = 1.5   # used when only a point is selected

        # margins define a perimeter around the work area that must remains
        # blank and hidden. if we scroll beyond the limits, the diagram is
        # resized.
        # self._leftMargin   = DEFAULT_MARGIN_VALUE
        # self._rightMargin  = DEFAULT_MARGIN_VALUE
        # self._topMargin    = DEFAULT_MARGIN_VALUE
        # self._bottomMargin = DEFAULT_MARGIN_VALUE
        self._isInfinite = False    # to know if the frame is infinite or not

        # paint related
        w, h = self.GetSize()
        self.__workingBitmap    = Bitmap(w, h)   # double buffering
        self.__backgroundBitmap = Bitmap(w, h)

        DEFAULT_FONT_SIZE = 12
        self._defaultFont = Font(DEFAULT_FONT_SIZE, FONTFAMILY_DEFAULT, FONTSTYLE_NORMAL, FONTWEIGHT_NORMAL)
        self.SetBackgroundColour(WHITE)
        self._prefs: OglPreferences = OglPreferences()

        # Mouse events
        self.Bind(EVT_LEFT_DOWN,     self.OnLeftDown)
        self.Bind(EVT_LEFT_UP,       self.OnLeftUp)
        self.Bind(EVT_LEFT_DCLICK,   self.OnLeftDClick)
        self.Bind(EVT_MIDDLE_DOWN,   self.OnMiddleDown)
        self.Bind(EVT_MIDDLE_UP,     self.OnMiddleUp)
        self.Bind(EVT_MIDDLE_DCLICK, self.OnMiddleDClick)
        self.Bind(EVT_RIGHT_DOWN,    self.OnRightDown)
        self.Bind(EVT_RIGHT_UP,      self.OnRightUp)
        self.Bind(EVT_RIGHT_DCLICK,  self.OnRightDClick)
        self.Bind(EVT_PAINT,         self.OnPaint)

        if self._prefs.debugDiagramFrame is True:

            self._debugDialog: DlgDebugDiagramFrame = DlgDebugDiagramFrame(self, ID_ANY)
            self._debugDialog.startMonitor()
            self._debugDialog.Show(True)

    def getEventPosition(self, event: MouseEvent):
        """
        Return the position of a click in the diagram.

        @param  event : mouse event

        @return (int, int) : x, y
        """

        x, y = self._ConvertEventCoordinates(event)  # Updated by CD, 20041005
        return x, y

    def GenericHandler(self, event: MouseEvent, methodName: str):
        """
        This handler finds the shape at event coordinates and dispatches the event.
        The handler will receive an event with coordinates already scrolled.

        Args:
            event:      The original event
            methodName: Name of the method to invoke in the event handler of the shape

        Returns:  The clicked shape
        """
        x, y = self.getEventPosition(event)
        shape = self.FindShape(x, y)
        event.m_x, event.m_y = x, y

        self.diagramFrameLogger.debug(f'GenericHandler - `{shape=}` `{methodName=}` x,y: {x},{y}')
        # if the shape found is a ShapeEventHandler
        if shape is not None and isinstance(shape, ShapeEventHandler):
            getattr(shape, methodName)(event)
        else:
            event.Skip()

        return shape

    def OnLeftDown(self, event: MouseEvent):
        """
        Callback for left down events on the diagram.

        Args:
            event:
        """
        self.diagramFrameLogger.debug("DiagramFrame.OnLeftDown")

        # First, call the generic handler for OnLeftDown
        shape: ShapeEventHandler = self.GenericHandler(event, "OnLeftDown")
        self._clickedShape = cast(Shape, shape)  # store the last clicked shape
        if not event.GetSkipped():
            self.diagramFrameLogger.debug(f'{event.GetSkipped()=}')
            return
        if shape is None:
            self._BeginSelect(event)
            return

        # manage click and drag
        x, y = event.GetX(), event.GetY()
        self._lastMousePosition = (x, y)

        realShape: Shape = cast(Shape, shape)
        if not event.ControlDown() and not realShape.IsSelected():
            shapes = self._diagram.GetShapes()
            shapes.remove(shape)
            if isinstance(shape, SizerShape):
                # don't deselect the parent of a sizer
                # or its sizer's would be detached
                shapes.remove(shape.GetParent())
            elif isinstance(shape, ControlPoint):
                # don't deselect the line of a control point
                self.diagramFrameLogger.debug(f'{shape=}')
                for line in shape.GetLines():
                    shapes.remove(line)
            # do not call DeselectAllShapes, because we must ensure that
            # the sizer won't be deselected (because they are detached when they are deselected)
            # deselect every other shape
            for s in shapes:
                s.SetSelected(False)
                s.SetMoving(False)

            self._selectedShapes = [cast(Shape, shape)]
            cast(Shape, shape).SetSelected(True)
            cast(Shape, shape).SetMoving(True)
            self._clickedShape = cast(Shape, None)
            self.Refresh()

        self.Bind(EVT_MOTION, self.OnMove)

    def OnLeftUp(self, event: MouseEvent):
        """
        Callback for left up events.

        Args:
            event:
        """
        if self._selector is not None:
            self.Bind(EVT_MOTION, self._NullCallback)
            self.diagramFrameLogger.debug(f'{self._selector=}')
            rect = self._selector

            for shape in self._diagram.GetShapes():
                x0, y0 = shape.GetTopLeft()
                w0, h0 = shape.GetSize()

                if shape.GetParent() is None and self._isShapeInRectangle(rect, x0=x0, y0=y0, w0=w0, h0=h0):
                    shape.SetSelected(True)
                    shape.SetMoving(True)
                    self._selectedShapes.append(shape)
            rect.Detach()
            self._selector = cast(RectangleShape, None)
        if not self._moving and self._clickedShape:
            self.diagramFrameLogger.debug(f'{self._moving} {self._clickedShape}')
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
            self._clickedShape = cast(Shape, None)
            self.Refresh()

        self._moving = False

        # normal event management
        self.GenericHandler(event, "OnLeftUp")
        if not self.__keepMoving:
            self.Bind(EVT_MOTION, self._NullCallback)
            self.Refresh()

    def OnDrag(self, event: MouseEvent):
        """
        Callback to drag the selected shapes.

        Args:
            event:
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
        self._clickedShape = cast(Shape, None)
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

    def OnMove(self, event: MouseEvent):
        """
        Callback for mouse movements.

        @param  event
        """
        event.m_x, event.m_y = self.getEventPosition(event)
        self.OnDrag(event)

    def OnLeftDClick(self, event: MouseEvent):
        """
        Callback for left double clicks.

        Args:
            event:
        """

        self.GenericHandler(event, "OnLeftDClick")
        self._clickedShape = cast(Shape, None)
        if not self.__keepMoving:
            self.Bind(EVT_MOTION, self._NullCallback)

    def OnMiddleDown(self, event: MouseEvent):
        """
        Callback.

        @param  event
        """
        self.GenericHandler(event, "OnMiddleDown")

    def OnMiddleUp(self, event: MouseEvent):
        """
        Callback.

        @param  event
        """
        self.GenericHandler(event, "OnMiddleUp")

    def OnMiddleDClick(self, event: MouseEvent):
        """
        Callback.

        @param  event
        """
        self.GenericHandler(event, "OnMiddleDClick")

    def OnRightDown(self, event: MouseEvent):
        """
        Callback.

        @param  event
        """
        self.GenericHandler(event, "OnRightDown")

    def OnRightUp(self, event: MouseEvent):
        """
        Callback.

        @param  event
        """
        self.GenericHandler(event, "OnRightUp")

    def OnRightDClick(self, event: MouseEvent):
        """
        Args:
            event:
        """
        crustWin = Dialog(self, -1, "PyCrust", (0, 0), (640, 480))
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

    def FindShape(self, x: int, y: int):
        """
        Return the shape at (x, y).

        Args:
            x: coordinate
            y: coordinate

        Returns:  The shape that was found under the coordinates or None
        """
        self.diagramFrameLogger.debug(f'FindShape: @{x},{y}')
        found = None
        shapes = self._diagram.GetShapes()
        # self.clsLogger.debug(f'{shapes=}')
        shapes.reverse()    # to select the one at the top
        for shape in shapes:
            if shape.Inside(x, y):
                self.diagramFrameLogger.debug(f"Inside: {shape}")
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

    def Refresh(self, eraseBackground: bool = True, rect: Rect = None):
        """
        not used
        Args:
            eraseBackground:    if False, the stored background is used
            rect:               not used
        """

        # self.clsLogger.warning(f'Refresh - {eraseBackground=}')
        if eraseBackground:
            self.Redraw()
        else:
            self.RedrawWithBackground()

    def SaveBackground(self, dc: DC):
        """

        Args:
            dc: The DC to save
        """
        w, h = self.GetSize()
        bb = self.__backgroundBitmap
        if (bb.GetWidth(), bb.GetHeight()) != (w, h):
            bb = self.__backgroundBitmap = Bitmap(w, h)
        mem = MemoryDC()
        mem.SelectObject(bb)

        x, y = self.CalcUnscrolledPosition(0, 0)
        mem.Blit(0, 0, w, h, dc, x, y)

        mem.SelectObject(NullBitmap)

    def LoadBackground(self, dc: DC, w: int, h: int):
        """
        Load the background image in the given dc.

        Args:
            dc:
            w:
            h:
        """
        mem = MemoryDC()
        mem.SelectObject(self.__backgroundBitmap)
        dc.Blit(0, 0, w, h, mem, 0, 0)
        mem.SelectObject(NullBitmap)

    def ClearBackground(self):
        """
        Clear the background image.
        """
        dc = MemoryDC()
        bb = self.__backgroundBitmap
        w, h = self.GetSize()
        if (bb.GetWidth(), bb.GetHeight()) != (w, h):
            bb = self.__backgroundBitmap = EmptyBitmap(w, h)
        dc.SelectObject(bb)
        dc.SetBackground(Brush(self.GetBackgroundColour()))
        dc.Clear()
        dc.SelectObject(NullBitmap)

    def CreateDC(self, loadBackground: bool, w: int, h: int) -> DC:
        """
        Create a DC, load the background on demand.

        @param loadBackground
        @param w : width of the frame.
        @param h :  height of the frame.

        @return DC
        """
        dc = MemoryDC()
        bm = self.__workingBitmap
        # cache the bitmap, to avoid creating a new at each refresh.
        # only recreate it if the size of the window has changed
        if (bm.GetWidth(), bm.GetHeight()) != (w, h):
            bm = self.__workingBitmap = Bitmap(w, h)
        dc.SelectObject(bm)
        if loadBackground:
            self.LoadBackground(dc, w, h)
        else:
            dc.SetBackground(Brush(self.GetBackgroundColour()))
            dc.Clear()
        self.PrepareDC(dc)

        return dc

    def PrepareBackground(self):
        """
        Redraw the screen without movable shapes, store it as the background.
        """
        self.Redraw(cast(DC, None), True, True, False)

    def RedrawWithBackground(self):
        """
        Redraw the screen using the background.
        """
        self.Redraw(cast(DC, None), True, False, True)

    def Redraw(self, dc: DC = None, full: bool = True, saveBackground: bool = False, useBackground: bool = False):
        """
        Refresh the diagram.
        If a DC is given, use it. Otherwise, use a double buffered DC.

        Args:
            dc:     If None, a default dc is created
            full:   If False, only draw the shape borders.
            saveBackground: If True, save the background
            useBackground:  If True, use the background
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
                # first, draw every non-moving shapes
                for shape in shapes:
                    if not shape.IsMoving():
                        shape.Draw(dc)
                # save the background
                self.SaveBackground(dc)
                # draw every moving shape
                for shape in shapes:
                    if shape.IsMoving():
                        shape.Draw(dc)

            # x, y = self.CalcUnScrolledPosition(0, 0)
            if useBackground:
                # draw every moving shapes
                for shape in shapes:
                    if shape.IsMoving():
                        shape.Draw(dc)
                # TODO: This code belongs in OnPaint
                # if self._prefs.backgroundGridEnabled is True:
                #     self._drawGrid(memDC=dc, width=w, height=h, startX=x, startY=y)
            else:  # don't use background
                # draw all shapes
                for shape in shapes:
                    shape.Draw(dc)
                # TODO: This code belongs in OnPaint
                # if self._prefs.backgroundGridEnabled is True:
                #     self._drawGrid(memDC=dc, width=w, height=h, startX=x, startY=y)
        else:  # not full
            for shape in shapes:
                shape.DrawBorder(dc)
                shape.DrawAnchors(dc)

        if needBlit:
            client = ClientDC(self)

            x, y = self.CalcUnscrolledPosition(0, 0)
            client.Blit(0, 0, w, h, dc, x, y)

    # noinspection PyUnusedLocal
    def OnPaint(self, event: PaintEvent):
        """
        Refresh the screen when a paint event is issued by the system.

        Args:
            event:
        """
        dc = PaintDC(self)
        w, h = self.GetSize()
        mem = self.CreateDC(False, w, h)
        mem.SetBackground(Brush(self.GetBackgroundColour()))
        mem.Clear()

        x, y = self.CalcUnscrolledPosition(0, 0)
        #
        # self.clsLogger.warning(f'OnPaint - {w=}, {h=} {x=} {y=}')
        # Paint events don't seem to be generated when Pyut is built for deployment;  So code duplicated in .Redraw()
        #
        if self._prefs.backgroundGridEnabled is True:
            self._drawGrid(memDC=mem, width=w, height=h, startX=x, startY=y)
        self.Redraw(mem)

        dc.Blit(0, 0, w, h, mem, x, y)

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

        Returns: the x offset between the model and the shapes view (MVC)

        """
        return self._xOffset

    def GetYOffset(self):
        """
        added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (11.11.2005)
        @return the y offset between the model and the view of the shapes (MVC)
        """
        return self._yOffset

    def SetXOffset(self, offset):
        """
        added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (11.11.2005)
        Set the x offset between the model and the view of the shapes (MVC)
        """
        self._xOffset = offset

    def SetYOffset(self, offset):
        """
        added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (11.11.2005)
        Set the y offset between the model and the view of the shapes (MVC)
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

        # transform event coordinates to get them relative to the upper left corner of
        # the virtual screen (avoid the case where that corner is on a shape and
        # get its coordinates relative to the client view).
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

            # we have to check if the "zoom in" on a reduced view produces
            # another less reduced view or an enlarged view. For this, we
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

        # resize the virtual screen in order to match with the zoom
        virtualWidth  = virtualWidth * zoomFactor
        virtualHeight = virtualHeight * zoomFactor
        virtualSize = Size(virtualWidth, virtualHeight)
        self.SetVirtualSize(virtualSize)

        # perform the scrolling in the way to have the zoom area visible
        # and centred on the virtual screen.
        scrollX = (virtualWidth - clientWidth) // 2 // xUnit
        scrollY = (virtualHeight - clientHeight) // 2 // yUnit
        self.Scroll(scrollX, scrollY)

    def DoZoomOut(self, ax: int, ay: int):
        """
        Do the 'zoom out' in the way to have the clicked point (ax, ay) as
        the central point of new view.
        If one or many 'zoom in' where performed before, then we just suppress the
        last one from the zoom stack. Else, we add the default inverted zoom factor
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

        # transform event coordinates to get them relative to the upper left corner of
        # the virtual screen (avoid the case where that corner is on a shape and
        # get its coordinates relative to the shape).
        if ax >= viewStartX * xUnit and ay >= viewStartY * yUnit:
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
        # minZoomReached = False        not used

        # if the view is enlarged, then we just remove the last
        # zoom in factor that has been applied. Else, we apply
        # the default one in inverted.
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

        # set the offsets between the view and the model for
        # each shape on this diagram frame.
        self.SetXOffset((self.GetXOffset() + dx) * zoomFactor)
        self.SetYOffset((self.GetYOffset() + dy) * zoomFactor)

        # updates the shapes (view) position and dimensions from
        # their model in the light of the new zoom factor and offsets.
        for shape in self.GetDiagram().GetShapes():
            shape.UpdateFromModel()

        # resize the virtual screen in order to match with the zoom
        virtualWidth  = virtualWidth * zoomFactor
        virtualHeight = virtualHeight * zoomFactor
        virtualSize = Size(virtualWidth, virtualHeight)
        self.SetVirtualSize(virtualSize)

        # perform the scrolling in the way to have the zoom area visible
        # and centred on the virtual screen.
        scrollX = (virtualWidth - clientWidth) // 2 // xUnit
        scrollY = (virtualHeight - clientHeight) // 2 // yUnit
        self.Scroll(scrollX, scrollY)

    def SetInfinite(self, infinite: bool = False):
        """
        Set this diagram frame as an infinite work area. The result is that the
        virtual size is enlarged when the scrollbar reaches the specified
        margins (see `SetMargins`). When we set this as `True`, the scrollbars
        are moved to the middle of their scale.

        Args:
            infinite:   If `True` the work area is infinite
        """
        self._isInfinite = infinite

        if infinite is True:
            # place all the shapes in an area centered on the infinite work area
            vWidth, vHeight = self.GetVirtualSize()
            cWidth, cHeight = self.GetClientSize()
            # get the number of pixels per scroll unit
            xUnit, yUnit = self.GetScrollPixelsPerUnit()

            # get the number of scroll unit
            noUnitX = (vWidth-cWidth) / xUnit
            noUnitY = (vHeight-cHeight) / yUnit

            if self._prefs.centerDiagram is True:
                self.Scroll(noUnitX / 2, noUnitY / 2)   # set the scrollbars position in the middle of their scale
            else:
                self.Scroll(0, 0)

    def _BeginSelect(self, event: MouseEvent):
        """
        Create a selector box and manage it.

        @param  event
        """
        if not event.ControlDown():
            self.DeselectAllShapes()
        x, y = event.GetX(), event.GetY()   # event position has been modified

        rect: RectangleShape = RectangleShape(x, y, 0, 0)
        self._selector = rect
        rect.SetDrawFrame(True)
        rect.SetBrush(TRANSPARENT_BRUSH)
        rect.SetMoving(True)
        self._diagram.AddShape(rect)
        self.PrepareBackground()
        self.Bind(EVT_MOTION, self._OnMoveSelector)

    def _OnMoveSelector(self, event: MouseEvent):
        """
        Callback for the selector box.

        @param  event
        """
        if self._selector is not None:
            x, y = self.getEventPosition(event)
            x0, y0 = self._selector.GetPosition()
            self._selector.SetSize(x - x0, y - y0)
            self.Refresh(False)

    def _NullCallback(self, evt):
        pass

    def _ConvertEventCoordinates(self, event):
        xView, yView = self.GetViewStart()
        xDelta, yDelta = self.GetScrollPixelsPerUnit()
        return event.GetX() + (xView * xDelta), event.GetY() + (yView * yDelta)

    def _drawGrid(self, memDC: DC, width: int, height: int, startX: int, startY: int):

        # self.clsLogger.info(f'{width=} {height=} {startX=} {startY=}')
        savePen = memDC.GetPen()

        newPen: Pen = self._getGridPen()
        memDC.SetPen(newPen)

        self._drawHorizontalLines(memDC=memDC, width=width, height=height, startX=startX, startY=startY)
        self._drawVerticalLines(memDC=memDC,   width=width, height=height, startX=startX, startY=startY)
        memDC.SetPen(savePen)

    def _drawHorizontalLines(self, memDC: DC, width: int, height: int, startX: int, startY: int):

        x1:   int = 0
        x2:   int = startX + width
        stop: int = height + startY
        step: int = self._prefs.backgroundGridInterval
        for movingY in range(startY, stop, step):
            # self.clsLogger.info(f'{x1=} {movingY=} - {x2=} {movingY=}')
            memDC.DrawLine(x1, movingY, x2, movingY)

    def _drawVerticalLines(self, memDC: DC, width: int, height: int, startX: int, startY: int):

        y1:   int = 0
        y2:   int = startY + height
        stop: int = width + startX
        step: int = self._prefs.backgroundGridInterval

        for movingX in range(startX, stop, step):
            memDC.DrawLine(movingX, y1, movingX, y2)

    def _getGridPen(self) -> Pen:

        gridLineColor: Colour   = MiniOglColorEnum.toWxColor(self._prefs.gridLineColor)
        gridLineStyle: PenStyle = MiniOglPenStyle.toWxPenStyle(self._prefs.gridLineStyle)

        pen:           Pen    = Pen(PenInfo(gridLineColor).Style(gridLineStyle).Width(1))

        return pen

    def _isShapeInRectangle(self, rect: RectangleShape, x0: float, y0: float, w0: float, h0: float) -> bool:

        ans: bool = False
        if rect.Inside(x0, y0) and rect.Inside(x0 + w0, y0) and rect.Inside(x0, y0 + h0) and rect.Inside(x0 + w0, y0 + h0):
            ans = True

        return ans

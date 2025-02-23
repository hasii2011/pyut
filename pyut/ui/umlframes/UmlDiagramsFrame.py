
from typing import Callable
from typing import cast

from logging import Logger
from logging import getLogger

from sys import maxsize

from miniogl.MiniOglColorEnum import MiniOglColorEnum
from wx import EVT_CHAR
from wx import WXK_BACK
from wx import WXK_DELETE
from wx import WXK_DOWN
from wx import WXK_UP
from wx import WXK_INSERT

from wx import KeyEvent
from wx import Notebook

from ogl.OglClass import OglClass
from ogl.OglObject import OglObject

from ogl.events.OglEvents import EVT_CREATE_LOLLIPOP_INTERFACE
from ogl.events.OglEvents import EVT_DIAGRAM_FRAME_MODIFIED
from ogl.events.OglEvents import EVT_SHAPE_SELECTED
from ogl.events.OglEvents import EVT_CUT_OGL_CLASS
from ogl.events.OglEvents import EVT_REQUEST_LOLLIPOP_LOCATION

from ogl.events.OglEvents import ShapeSelectedEvent
from ogl.events.OglEvents import CutOglClassEvent
from ogl.events.OglEvents import DiagramFrameModifiedEvent
from ogl.events.OglEvents import RequestLollipopLocationEvent
from ogl.events.OglEvents import CreateLollipopInterfaceEvent

from ogl.events.ShapeSelectedEventData import ShapeSelectedEventData

from ogl.preferences.OglPreferences import OglPreferences

from pyut.ui.eventengine.Events import DarkModeChangedEvent
from pyut.ui.eventengine.Events import EVENT_DARK_MODE_CHANGED
from pyut.ui.umlframes.UmlFrame import UmlFrame

from pyut.ui.eventengine.Events import EVENT_ADD_OGL_DIAGRAM
from pyut.ui.eventengine.Events import EVENT_ADD_PYUT_DIAGRAM
from pyut.ui.eventengine.EventType import EventType
from pyut.ui.eventengine.IEventEngine import IEventEngine

from pyutplugins.ExternalTypes import ObjectBoundaries


class UmlDiagramsFrame(UmlFrame):
    """
    ClassFrame : class diagram frame.

    This class is a frame where we can draw Class diagrams.

    It is used by UmlClassDiagramsFrame
    """

    KEY_CODE_DELETE:       int = WXK_DELETE
    KEY_CODE_BACK:         int = WXK_BACK
    KEY_CODE_INSERT:       int = WXK_INSERT
    KEY_CODE_CAPITAL_I:    int = ord('I')
    KEY_CODE_LOWER_CASE_I: int = ord('i')
    KEY_CODE_CAPITAL_S:    int = ord('S')
    KEY_CODE_LOWER_CASE_S: int = ord('s')
    KEY_CODE_UP:           int = WXK_UP
    KEY_CODE_DOWN:         int = WXK_DOWN

    def __init__(self, parent: Notebook, eventEngine: IEventEngine):
        """
        This class sits at the crux between the underlying OGL layer and the overarching
        Pyut UI.  Thus, it registers to listen for Ogl Events
        and where necessary uses the PyutUI event engine to forward events

        Args:
            parent: wx.Window parent window;  In practice this is always wx.Notebook instance
            eventEngine: Pyut event engine
        """
        self.umlDiagramFrameLogger: Logger = getLogger(__name__)

        super().__init__(parent, eventEngine=eventEngine)

        self._eventEngine.registerListener(pyEventBinder=EVENT_ADD_PYUT_DIAGRAM,  callback=self._onAddPyutDiagram)
        self._eventEngine.registerListener(pyEventBinder=EVENT_ADD_OGL_DIAGRAM,   callback=self._onAddOglDiagram)
        self._eventEngine.registerListener(pyEventBinder=EVENT_DARK_MODE_CHANGED, callback=self._onDarkModeChanged)

        self._oglEventEngine.registerListener(EVT_SHAPE_SELECTED,            self._onShapeSelected)
        self._oglEventEngine.registerListener(EVT_CUT_OGL_CLASS,             self._onCutOglClassShape)
        self._oglEventEngine.registerListener(EVT_DIAGRAM_FRAME_MODIFIED,    self._onDiagramFrameModified)
        self._oglEventEngine.registerListener(EVT_REQUEST_LOLLIPOP_LOCATION, self._onRequestLollipopLocation)
        self._oglEventEngine.registerListener(EVT_CREATE_LOLLIPOP_INTERFACE, self._onCreateLollipopInterface)

        self.Bind(EVT_CHAR, self._onProcessKeyboard)

    @property
    def objectBoundaries(self) -> ObjectBoundaries:
        """

        Return object boundaries (coordinates)

        """
        minX: int = maxsize
        maxX: int = -maxsize
        minY: int = maxsize
        maxY: int = -maxsize

        # Get boundaries
        for shapeObject in self._diagram.shapes:
            # Get object limits
            ox1, oy1 = shapeObject.GetPosition()
            ox2, oy2 = shapeObject.GetSize()
            ox2 += ox1
            oy2 += oy1

            # Update min-max
            minX = min(minX, ox1)
            maxX = max(maxX, ox2)
            minY = min(minY, oy1)
            maxY = max(maxY, oy2)

        # Return values
        return ObjectBoundaries(minX=minX, minY=minY, maxX=maxX, maxY=maxY)

    def undo(self):
        """
        Undo the last operation on this frame
        """
        self._commandProcessor.Undo()

    def redo(self):
        """
        Redo the last operation on this frame
        """
        self._commandProcessor.Redo()

    def OnClose(self):
        """
        Closing handler (must be called explicitly).

        Returns: True if the close succeeded
        """
        self.Destroy()
        return True

    def _onProcessKeyboard(self, event: KeyEvent):
        """
        Process the keyboard events.
        TODO:  Build the callable dictionary once and use it here.  This code builds it every time the
        user presses a key.  Eeks;

        Args:
            event:  The wxPython key event
        """
        c: int = event.GetKeyCode()
        # print(f'{WXK_DELETE=} {WXK_BACK=} {WXK_INSERT=}')
        match c:
            case UmlDiagramsFrame.KEY_CODE_DELETE:
                self._onCutShape()
            case UmlDiagramsFrame.KEY_CODE_BACK:
                self._onCutShape()
            case UmlDiagramsFrame.KEY_CODE_INSERT:
                self._insertSelectedShape()
            case UmlDiagramsFrame.KEY_CODE_LOWER_CASE_I:
                self._insertSelectedShape()
            case UmlDiagramsFrame.KEY_CODE_CAPITAL_I:
                self._insertSelectedShape()
            case UmlDiagramsFrame.KEY_CODE_LOWER_CASE_S:
                self._toggleSpline()
            case UmlDiagramsFrame.KEY_CODE_INSERT:
                self._toggleSpline()
            case UmlDiagramsFrame.KEY_CODE_DOWN:
                self._moveSelectedShapeDown()
            case UmlDiagramsFrame.KEY_CODE_UP:
                self._moveSelectedShapeUp()
            case _:
                self.umlDiagramFrameLogger.warning(f'Key code not supported: {c}')
                event.Skip()

    def _onCutShape(self):
        self._eventEngine.sendEvent(EventType.CutShapes)

    def _onShapeSelected(self, event: ShapeSelectedEvent):
        """

        Args:
            event:   Event which contains data on the selected shape
        """
        shapeSelectedData: ShapeSelectedEventData = event.shapeSelectedData

        selectedOglObject: OglObject = cast(OglObject, shapeSelectedData.shape)

        if self._actionHandler.actionWaiting:
            self.umlDiagramFrameLogger.debug(f'{shapeSelectedData=}')
            self._actionHandler.shapeSelected(self, selectedOglObject, shapeSelectedData.position)

    def _onCutOglClassShape(self, cutOglClassEvent: CutOglClassEvent):
        """
        Ogl Event handler
        Args:
            cutOglClassEvent:
        """
        selectedOglClass: OglClass = cutOglClassEvent.selectedShape
        self._eventEngine.sendEvent(EventType.DeSelectAllShapes)

        selectedOglClass.selected = True
        self._eventEngine.sendEvent(EventType.CutShape, shapeToCut=selectedOglClass)

    # noinspection PyUnusedLocal
    def _onDiagramFrameModified(self, event: DiagramFrameModifiedEvent):
        """
        Receives the diagram frame modified event from the Ogl Layer.  We
        have to forward a Pyut specific event
        Args:
            event:
        """
        self._eventEngine.sendEvent(EventType.UMLDiagramModified)

    def _onRequestLollipopLocation(self, event: RequestLollipopLocationEvent):

        shape = event.shape
        self._actionHandler.requestLollipopLocation(self, shape)

    def _onCreateLollipopInterface(self, event: CreateLollipopInterfaceEvent):

        attachmentPoint = event.attachmentPoint
        implementor     = event.implementor
        self.umlDiagramFrameLogger.info(f'{attachmentPoint=} {implementor=}')

        self._actionHandler.createLollipopInterface(self, implementor=implementor, attachmentAnchor=attachmentPoint)

    def _onDarkModeChanged(self, event: DarkModeChangedEvent):
        oglPreferences: OglPreferences = OglPreferences()
        darkMode:       bool           = event.darkMode

        if darkMode is True:
            self.SetBackgroundColour(MiniOglColorEnum.toWxColor(oglPreferences.darkModeBackGroundColor))
        else:
            self.SetBackgroundColour(MiniOglColorEnum.toWxColor(oglPreferences.backGroundColor))

        self.Refresh()
        event.Skip(skip=True)   # Let other frames change their color

    def _toggleSpline(self):

        from ogl.OglLink import OglLink

        selected = self.selectedShapes
        self.umlDiagramFrameLogger.info(f'Selected Shape: {selected}')
        for shape in selected:
            if isinstance(shape, OglLink):
                shape.spline = (not shape.spline)
        self.Refresh()

    def _moveSelectedShapeUp(self):
        """
        Move the selected shape one level up in z-order
        """
        self._moveSelectedShapeZOrder(self.diagram.MoveToFront)

    def _moveSelectedShapeDown(self):
        """
        Move the selected shape one level down in z-order
        """
        self._moveSelectedShapeZOrder(self.diagram.MoveToBack)

    def _insertSelectedShape(self):
        """
        is this really useful?
        """
        from miniogl.LinePoint import LinePoint
        from miniogl.ControlPoint import ControlPoint

        selectedShapes = self.selectedShapes
        if len(selectedShapes) == 1:

            selectedShape = selectedShapes.pop()
            if isinstance(selectedShape, LinePoint):
                px, py = selectedShape.GetPosition()
                # add a control point and make it child of the shape if it's a
                # self link
                line = selectedShape.lines[0]
                if line.sourceAnchor.parent is line.destinationAnchor.parent:
                    cp = ControlPoint(0, 0, line.sourceAnchor.parent)
                    cp.SetPosition(px + 20, py + 20)
                else:
                    cp = ControlPoint(px + 20, py + 20)

                line.AddControl(cp, selectedShape)
                self.diagram.AddShape(cp)
                self.Refresh()

    def _moveSelectedShapeZOrder(self, callback: Callable):
        """
        Move the selected shape one level in z-order

        Args:
            callback:
        """
        from ogl.OglObject import OglObject

        selected = self.selectedShapes
        if len(selected) > 0:
            for oglObject in selected:
                if isinstance(oglObject, OglObject):
                    callback(oglObject)
        self.Refresh()

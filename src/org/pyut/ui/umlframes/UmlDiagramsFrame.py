
from typing import Callable

from logging import Logger
from logging import getLogger

from wx import EVT_CHAR
from wx import WXK_BACK
from wx import WXK_DELETE
from wx import WXK_DOWN
from wx import WXK_UP
from wx import WXK_INSERT

from wx import KeyEvent
from wx import Notebook

from ogl.OglClass import OglClass

from ogl.events.OglEventEngine import OglEventEngine

from ogl.events.OglEvents import EVT_CREATE_LOLLIPOP_INTERFACE
from ogl.events.OglEvents import EVT_PROJECT_MODIFIED
from ogl.events.OglEvents import EVT_SHAPE_SELECTED
from ogl.events.OglEvents import EVT_CUT_OGL_CLASS
from ogl.events.OglEvents import EVT_REQUEST_LOLLIPOP_LOCATION

from ogl.events.OglEvents import ShapeSelectedEvent
from ogl.events.OglEvents import CutOglClassEvent
from ogl.events.OglEvents import ProjectModifiedEvent
from ogl.events.OglEvents import RequestLollipopLocationEvent
from ogl.events.OglEvents import CreateLollipopInterfaceEvent

from ogl.events.ShapeSelectedEventData import ShapeSelectedEventData

from org.pyut.ui.umlframes.UmlFrame import UmlFrame

from pyut.uiv2.eventengine.Events import EVENT_ADD_OGL_DIAGRAM
from pyut.uiv2.eventengine.Events import EVENT_ADD_PYUT_DIAGRAM
from pyut.uiv2.eventengine.Events import EventType
from pyut.uiv2.eventengine.IEventEngine import IEventEngine


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
        self.umlDiagramFrameLogger: Logger       = getLogger(__name__)

        super().__init__(parent, eventEngine=eventEngine)

        self._eventEngine.registerListener(pyEventBinder=EVENT_ADD_PYUT_DIAGRAM, callback=self._onAddPyutDiagram)
        self._eventEngine.registerListener(pyEventBinder=EVENT_ADD_OGL_DIAGRAM,  callback=self._onAddOglDiagram)

        self._oglEventEngine: OglEventEngine = OglEventEngine(listeningWindow=self)

        self._oglEventEngine.registerListener(EVT_SHAPE_SELECTED,            self._onShapeSelected)
        self._oglEventEngine.registerListener(EVT_CUT_OGL_CLASS,             self._onCutOglClassShape)
        self._oglEventEngine.registerListener(EVT_PROJECT_MODIFIED,          self._onProjectModified)
        self._oglEventEngine.registerListener(EVT_REQUEST_LOLLIPOP_LOCATION, self._onRequestLollipopLocation)
        self._oglEventEngine.registerListener(EVT_CREATE_LOLLIPOP_INTERFACE, self._onCreateLollipopInterface)

        self.Bind(EVT_CHAR, self._onProcessKeyboard)

    @property
    def eventEngine(self) -> OglEventEngine:
        return self._oglEventEngine

    # noinspection PyUnusedLocal
    def OnClose(self, force=False):
        """
        Closing handler (must be called explicitly).

        Args:
            force:

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
                self.logger.warning(f'Key code not supported: {c}')
                event.Skip()

    def _onCutShape(self):
        self._eventEngine.sendEvent(EventType.CutShapes)

    def _onShapeSelected(self, event: ShapeSelectedEvent):
        """
        In practice this is only used on UML Class diagrams when the user
        wants to create links between classes;  For example, associations and inheritance
        x
        Args:
            event:   Event which contains data on the selected shape
        """

        shapeSelectedData: ShapeSelectedEventData = event.shapeSelectedData

        if self._actionHandler.actionWaiting:
            self.umlDiagramFrameLogger.debug(f'{shapeSelectedData=}')
            self._actionHandler.shapeSelected(self, shapeSelectedData.shape, shapeSelectedData.position)

    def _onCutOglClassShape(self, cutOglClassEvent: CutOglClassEvent):
        """
        Ogl Event handler
        Args:
            cutOglClassEvent:

        """
        selectedOglClass: OglClass = cutOglClassEvent.selectedShape
        self._eventEngine.sendEvent(EventType.DeSelectAllShapes)

        selectedOglClass.SetSelected(True)
        self._eventEngine.sendEvent(EventType.CutShape, shapeToCut=selectedOglClass)

    # noinspection PyUnusedLocal
    def _onProjectModified(self, event: ProjectModifiedEvent):
        """
        Receives the project modified event from the Ogl Layer.  We
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

    def _toggleSpline(self):

        from ogl.OglLink import OglLink

        selected = self.GetSelectedShapes()
        self.logger.info(f'Selected Shape: {selected}')
        for shape in selected:
            if isinstance(shape, OglLink):
                shape.SetSpline(not shape.GetSpline())
        self.Refresh()

    def _moveSelectedShapeUp(self):
        """
        Move the selected shape one level up in z-order
        """
        self._moveSelectedShapeZOrder(self.GetDiagram().MoveToFront)

    def _moveSelectedShapeDown(self):
        """
        Move the selected shape one level down in z-order
        """
        self._moveSelectedShapeZOrder(self.GetDiagram().MoveToBack)

    def _insertSelectedShape(self):
        """
        is this really useful?
        """

        from miniogl.LinePoint import LinePoint
        from miniogl.ControlPoint import ControlPoint

        selectedShapes = self.GetSelectedShapes()
        if len(selectedShapes) == 1:

            selectedShape = selectedShapes.pop()
            if isinstance(selectedShape, LinePoint):
                px, py = selectedShape.GetPosition()
                # add a control point and make it child of the shape if it's a
                # self link
                line = selectedShape.GetLines()[0]
                if line.GetSource().GetParent() is line.GetDestination().GetParent():
                    cp = ControlPoint(0, 0, line.GetSource().GetParent())
                    cp.SetPosition(px + 20, py + 20)
                else:
                    cp = ControlPoint(px + 20, py + 20)

                line.AddControl(cp, selectedShape)
                self.GetDiagram().AddShape(cp)
                self.Refresh()

    def _moveSelectedShapeZOrder(self, callback: Callable):
        """
        Move the selected shape one level in z-order

        Args:
            callback:

        """
        from ogl.OglObject import OglObject

        selected = self.GetSelectedShapes()
        if len(selected) > 0:
            for oglObject in selected:
                if isinstance(oglObject, OglObject):
                    callback(oglObject)
        self.Refresh()

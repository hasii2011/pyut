
from logging import Logger
from logging import getLogger

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
from org.pyut.uiv2.eventengine.Events import EventType
from org.pyut.uiv2.eventengine.IEventEngine import IEventEngine


class UmlDiagramsFrame(UmlFrame):
    """
    ClassFrame : class diagram frame.

    This class is a frame where we can draw Class diagrams.

    It is used by UmlClassDiagramsFrame
    """

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

        super().__init__(parent, -1)    # TODO Fix this sending in -1 for a frame

        self._eventEngine:    IEventEngine   = eventEngine
        self._oglEventEngine: OglEventEngine = OglEventEngine(listeningWindow=self)

        self._oglEventEngine.registerListener(EVT_SHAPE_SELECTED,            self._onShapeSelected)
        self._oglEventEngine.registerListener(EVT_CUT_OGL_CLASS,             self._onCutOglClassShape)
        self._oglEventEngine.registerListener(EVT_PROJECT_MODIFIED,          self._onProjectModified)
        self._oglEventEngine.registerListener(EVT_REQUEST_LOLLIPOP_LOCATION, self._onRequestLollipopLocation)
        self._oglEventEngine.registerListener(EVT_CREATE_LOLLIPOP_INTERFACE, self._onCreateLollipopInterface)

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
        self.cleanUp()
        self.Destroy()
        return True

    def _onShapeSelected(self, event: ShapeSelectedEvent):
        """
        In practice this is only used on UML Class diagrams when the user
        wants to create links between classes;  For example, associations and inheritance
        x
        Args:
            event:   Event which contains data on the selected shape
        """

        shapeSelectedData: ShapeSelectedEventData = event.shapeSelectedData

        if self._mediator.actionWaiting():
            self.umlDiagramFrameLogger.debug(f'{shapeSelectedData=}')
            self._mediator.shapeSelected(shapeSelectedData.shape, shapeSelectedData.position)

    def _onCutOglClassShape(self, cutOglClassEvent: CutOglClassEvent):

        selectedOglClass: OglClass = cutOglClassEvent.selectedShape
        self._mediator.deselectAllShapes()
        selectedOglClass.SetSelected(True)
        self._mediator.cutSelectedShapes()

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
        self._mediator.requestLollipopLocation(shape)

    def _onCreateLollipopInterface(self, event: CreateLollipopInterfaceEvent):

        attachmentPoint = event.attachmentPoint
        implementor     = event.implementor
        self.umlDiagramFrameLogger.info(f'{attachmentPoint=} {implementor=}')

        self._mediator.createLollipopInterface(implementor=implementor, attachmentAnchor=attachmentPoint)

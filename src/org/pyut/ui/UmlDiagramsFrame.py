from logging import Logger
from logging import getLogger

from wx import Notebook

from org.pyut.ogl.OglClass import OglClass

from org.pyut.ogl.events.OglEvents import EVT_SHAPE_SELECTED
from org.pyut.ogl.events.OglEvents import EVT_CUT_OGL_CLASS
from org.pyut.ogl.events.OglEvents import EVT_REQUEST_LOLLIPOP_LOCATION

from org.pyut.ogl.events.OglEvents import ShapeSelectedEvent
from org.pyut.ogl.events.OglEvents import CutOglClassEvent
from org.pyut.ogl.events.OglEvents import RequestLollipopLocationEvent

from org.pyut.ogl.events.ShapeSelectedEventData import ShapeSelectedEventData

from org.pyut.ui.UmlFrame import UmlFrame


class UmlDiagramsFrame(UmlFrame):

    """
    ClassFrame : class diagram frame.

    This class is a frame where we can draw Class diagrams.

    It is used by UmlClassDiagramsFrame
    """
    umlDiagramFrameLogger: Logger = getLogger(__name__)

    def __init__(self, parent: Notebook):
        """

        Args:
            parent: wx.Window parent window;  In practice this is always wx.Notebook instance
        """

        super().__init__(parent, -1)    # TODO Fix this sending in -1 for a frame

        print(f'{type(EVT_SHAPE_SELECTED)=}')
        self.Bind(EVT_SHAPE_SELECTED, self._onShapeSelected)
        self.Bind(EVT_CUT_OGL_CLASS,  self._onCutOglClassShape)
        self.Bind(EVT_REQUEST_LOLLIPOP_LOCATION, self._onRequestLollipopLocation)

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

        if self._ctrl.actionWaiting():
            UmlDiagramsFrame.umlDiagramFrameLogger.debug(f'{shapeSelectedData=}')
            self._ctrl.shapeSelected(shapeSelectedData.shape, shapeSelectedData.position)

    def _onCutOglClassShape(self, cutOglClassEvent: CutOglClassEvent):

        selectedOglClass: OglClass = cutOglClassEvent.selectedShape
        self._ctrl.deselectAllShapes()
        selectedOglClass.SetSelected(True)
        self._ctrl.cutSelectedShapes()

    def _onRequestLollipopLocation(self, event: RequestLollipopLocationEvent):

        shape = event.shape
        self._ctrl.requestLollipopLocation(shape)

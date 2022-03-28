from logging import Logger
from logging import getLogger

from wx import Notebook

from org.pyut.ogl.events.OglEvents import EVT_SHAPE_SELECTED
from org.pyut.ogl.events.OglEvents import ShapeSelectedEvent
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

        self.Bind(EVT_SHAPE_SELECTED, self._onShapeSelected)

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

        shapeSelectedData: ShapeSelectedEventData = event.shapeSelectedData

        if self._ctrl.actionWaiting():
            UmlDiagramsFrame.umlDiagramFrameLogger.debug(f'{shapeSelectedData=}')
            self._ctrl.shapeSelected(shapeSelectedData.shape, shapeSelectedData.position)

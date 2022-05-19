
from typing import List
from typing import NewType
from typing import Union

from logging import Logger
from logging import getLogger

# noinspection PyPackageRequirements
from deprecated import deprecated

from wx import EVT_CHAR
from wx import EVT_CLOSE
from wx import EVT_PAINT

from wx import BeginBusyCursor
from wx import EndBusyCursor
from wx import MouseEvent
from wx import Notebook

from org.pyut.ogl.OglInterface2 import OglInterface2
from org.pyut.ogl.OglObject import OglObject
from org.pyut.ogl.OglLink import OglLink

from org.pyut.ogl.sd.OglSDMessage import OglSDMessage

from miniogl.Constants import SKIP_EVENT
from miniogl.DiagramFrame import DiagramFrame

from org.pyut.ui.Mediator import ACTION_ZOOM_IN
from org.pyut.ui.Mediator import Mediator

from org.pyut.PyutUtils import PyutUtils

from org.pyut.history.HistoryManager import HistoryManager

from org.pyut.experimental.GraphicalHandler import GraphicalHandler

# noinspection PyProtectedMember
from org.pyut.general.Globals import _

from org.pyut.ui.UmlFrameShapeHandler import UmlFrameShapeHandler

#  DEFAULT_WIDTH = 1280
#  DEFAULT_WIDTH = 5120
DEFAULT_WIDTH = 3000
A4_FACTOR:    float = 1.41

UmlObject  = Union[OglObject, OglLink, OglSDMessage, OglInterface2]
UmlObjects = NewType('UmlObjects', List[UmlObject])


class UmlFrame(UmlFrameShapeHandler):
    """
    Represents a canvas for drawing diagrams.
    It provides all the methods to add new classes, notes, links...
    It also routes some click events to the mediator. See the `OnLeftDown`
    method.
    """
    PIXELS_PER_UNIT_X: int = 20
    PIXELS_PER_UNIT_Y: int = 20

    def __init__(self, parent: Notebook, frame):
        """

        Args:
            parent: The parent window
            frame:  The uml frame
        """
        super().__init__(parent)

        self.logger: Logger = getLogger(__name__)

        self._mediator: Mediator = Mediator()

        self.maxWidth:  int  = DEFAULT_WIDTH
        self.maxHeight: int = int(self.maxWidth / A4_FACTOR)  # 1.41 is for A4 support

        nbrUnitsX: int = int(self.maxWidth / UmlFrame.PIXELS_PER_UNIT_X)
        nbrUnitsY: int = int(self.maxHeight / UmlFrame.PIXELS_PER_UNIT_Y)
        initPosX:  int = 0
        initPosY:  int = 0
        self.SetScrollbars(UmlFrame.PIXELS_PER_UNIT_X, UmlFrame.PIXELS_PER_UNIT_Y, nbrUnitsX, nbrUnitsY, initPosX, initPosY, False)

        self._frame = frame
        self._historyManager: HistoryManager = HistoryManager(self)

        # Close event
        self.Bind(EVT_CLOSE, self.evtClose)
        self.Bind(EVT_PAINT, self.OnPaint)
        self.Bind(EVT_CHAR, self._mediator.processChar)

        self.SetInfinite(True)

        self._defaultCursor = self.GetCursor()

    @property
    def historyManager(self) -> HistoryManager:
        """
        Read-only as this is created on the frame initialization.

        Returns:  The frame's history manager.
        """
        return self._historyManager

    def setCodePath(self, path):
        """
        Set the code path
        DEPRECATED
        @author C.Dutoit
        """
        project = self._mediator.getFileHandling().getProjectFromFrame(self)
        if project is not None:
            project.setCodePath(path)
        else:
            print("Passing setCodePath in UmlFrame-setCodePath")

    def displayDiagramProperties(self):
        """
        Display class diagram properties
        @author C.Dutoit
        """
        PyutUtils.displayError(_("Not yet implemented !"))

    def cleanUp(self):
        """
        Clean up object references before quitting.

        @since 1.23
        @author Laurent Burgbacher <lb@alawa.ch>
        @modified C.Dutoit <dutoitc@hotmail.com>
            Added clean destroy code
        """
        self._mediator = None
        self._frame = None

    # noinspection PyUnusedLocal
    def evtClose(self, event):
        """
        Clean close, event handler on EVT_CLOSE

        @since 1.35.2.8
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._historyManager.destroy()

        self.cleanUp()
        self.Destroy()

    def OnLeftDown(self, event):
        """
        Manage a left down mouse event.
        If there's an action pending in the mediator, give it the event, else
        let it go to the next handler.

        @param  event
        @since 1.4
        @author L. Burgbacher <lb@alawa.ch>
        """

        if self._mediator.actionWaiting():
            x, y = self.CalcUnscrolledPosition(event.GetX(), event.GetY())
            skip = self._mediator.doAction(x, y)

            if self._mediator.getCurrentAction() == ACTION_ZOOM_IN:
                DiagramFrame._BeginSelect(self, event)

            if skip == SKIP_EVENT:
                DiagramFrame.OnLeftDown(self, event)

        else:
            DiagramFrame.OnLeftDown(self, event)

    def OnLeftUp(self, event):
        """
        Added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (11.11.2005)
        to make the right action if it is a selection or a zoom.
        """
        if self._mediator.getCurrentAction() == ACTION_ZOOM_IN:
            width, height = self._selector.GetSize()
            x, y = self._selector.GetPosition()
            self._selector.Detach()
            self._selector = None
            self.DoZoomIn(x, y, width, height)
            self.Refresh()
            self._mediator.updateTitle()
        else:

            DiagramFrame.OnLeftUp(self, event)

    def OnLeftDClick(self, event: MouseEvent):
        """
        Manage a left double click mouse event.

        Args:
            event:
        """

        x, y = self.CalcUnscrolledPosition(event.GetX(), event.GetY())
        self._mediator.editObject(x, y)
        DiagramFrame.OnLeftDClick(self, event)

    def newDiagram(self):
        """
        Remove all shapes, get a brand new empty diagram.

        @since 1.31
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        self._diagram.DeleteAllShapes()
        self.Refresh()

    def getDiagram(self):
        """
        Return the diagram of this frame.

        @return wx.Diagram
        @since 1.23
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        return self._diagram

    def addPyutHierarchy(self):
        """
        Calls addHierarchy with the Pyut class list.
        """
        import org.pyut.experimental.PyutModelClasses as pdc

        BeginBusyCursor()

        gh: GraphicalHandler = GraphicalHandler(umlFrame=self, maxWidth=self.maxWidth, historyManager=self._historyManager)
        gh.addHierarchy(pdc.PyutClassNames)

        EndBusyCursor()

    def addOglHierarchy(self):
        """
        Calls addHierarchy with the Ogl class list.
        """
        import org.pyut.experimental.PyutModelClasses as pdc

        BeginBusyCursor()

        gh: GraphicalHandler = GraphicalHandler(umlFrame=self, maxWidth=self.maxWidth, historyManager=self._historyManager)
        gh.addHierarchy(pdc.OglClassNames)

        EndBusyCursor()

    def getUmlObjects(self) -> UmlObjects:
        """
        Retrieve UML objects from the UML Frame

        Returns:  The Uml objects on this diagram
        """
        umlObjects: UmlObjects = UmlObjects([])

        for s in self._diagram.GetShapes():
            if isinstance(s, (OglObject, OglLink, OglSDMessage, OglInterface2)):
                umlObjects.append(s)

        return umlObjects

    def getWidth(self):
        """

        Returns:  The frame width

        """
        return self.maxWidth

    def getHeight(self):
        """

        Returns: The frame height
        """
        return self.maxHeight

    # def getObjectsBoundaries(self):
    #     """
    #     TODO:  This appears to be an unused method
    #
    #     Return object boundaries (coordinates)
    #
    #     @since 1.35.2.25
    #     @author C.Dutoit <dutoitc@hotmail.com>
    #     """
    #     infinite = 1e9
    #     minx     = infinite
    #     maxX     = -infinite
    #     miny     = infinite
    #     maxy     = -infinite
    #
    #     # Get boundaries
    #     for shapeObject in self._diagram.GetShapes():
    #         # Get object limits
    #         ox1, oy1 = shapeObject.GetPosition()
    #         ox2, oy2 = shapeObject.GetSize()
    #         ox2 += ox1
    #         oy2 += oy1
    #
    #         # Update min-max
    #         minx = min(minx, ox1)
    #         maxX = max(maxX, ox2)
    #         miny = min(miny, oy1)
    #         maxy = max(maxy, oy2)
    #
    #     # Return values
    #     return minx, miny, maxX, maxy

    def getUmlObjectById(self, objectId: int):
        """
        Added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (20.11.2005)
        @param objectId    :   id for which we want to get an object

        @return the uml object that has the specified id. If there is no
        matching object, None is returned.
        """

        for shape in self.GetDiagram().GetShapes():
            if isinstance(shape, (OglObject, OglLink)):
                if shape.pyutObject.id == objectId:
                    return shape
        return None

    @deprecated('Use the historyManager property')
    def getHistory(self):
        """
        """
        return self._historyManager

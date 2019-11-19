
from logging import Logger
from logging import getLogger

from wx import BeginBusyCursor
from wx import EVT_CHAR
from wx import EVT_CLOSE
from wx import EVT_PAINT
from wx import EndBusyCursor
from wx import MouseEvent

from org.pyut.ogl.OglObject import OglObject

from org.pyut.ogl.OglLink import OglLink
from OglSDMessage import OglSDMessage

from MiniOgl.Constants import SKIP_EVENT
from MiniOgl.DiagramFrame import DiagramFrame

from Mediator import ACTION_ZOOM_IN
from Mediator import getMediator

from org.pyut.PyutUtils import PyutUtils

from org.pyut.history.HistoryManager import HistoryManager

from org.pyut.experimental.GraphicalHandler import GraphicalHandler

from org.pyut.general.Globals import _

from org.pyut.ui.UmlFrameShapeHandler import UmlFrameShapeHandler

#  DEFAULT_WIDTH = 1280
#  DEFAULT_WIDTH = 5120
DEFAULT_WIDTH = 3000


class UmlFrame(UmlFrameShapeHandler):
    """
    Represents a canvas for drawing diagrams.
    It provides all the methods to add new classes, notes, links...
    It also routes some click events to the mediator. See the `OnLeftDown`
    method.

    :version: $Revision: 1.22 $
    :author: L. Burgbacher
    :contact: lb@alawa.ch
    """
    def __init__(self, parent, frame):
        """
        constructor
        @param wx.Window parent : parent object
        @param frame : parent frame object
        @since 1.0
        @author N. hamadi (hamadi12@yahoo.fr)
        @modified L. Burgbacher <lb@alawa.ch>
            added event processing
            added mediator support
            bind with OglClass to create new classes
        """

        super().__init__(parent)

        self.logger: Logger = getLogger(__name__)

        self._ctrl = getMediator()
        self.maxWidth  = DEFAULT_WIDTH
        self.maxHeight = int(self.maxWidth / 1.41)  # 1.41 is for A4 support

        # set a scrollbar
        self.SetScrollbars(20, 20, self.maxWidth/20, self.maxHeight/20)

        self._frame = frame
        self._history = HistoryManager(self)

        # Close event
        self.Bind(EVT_CLOSE, self.evtClose)
        self.Bind(EVT_PAINT, self.OnPaint)
        self.Bind(EVT_CHAR, self._ctrl.processChar)

        self.SetInfinite(True)

        self._defaultCursor = self.GetCursor()

    def setCodePath(self, path):
        """
        Set the code path
        DEPRECATED
        @author C.Dutoit
        """
        project = self._ctrl.getFileHandling().getProjectFromFrame(self)
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
        self._ctrl = None
        self._frame = None

    # noinspection PyUnusedLocal
    def evtClose(self, event):
        """
        Clean close, event handler on EVT_CLOSE

        @since 1.35.2.8
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._history.destroy()

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

        if self._ctrl.actionWaiting():
            x, y = self.CalcUnscrolledPosition(event.GetX(), event.GetY())
            skip = self._ctrl.doAction(x, y)

            if self._ctrl.getCurrentAction() == ACTION_ZOOM_IN:
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
        if self._ctrl.getCurrentAction() == ACTION_ZOOM_IN:
            width, height = self._selector.GetSize()
            x, y = self._selector.GetPosition()
            self._selector.Detach()
            self._selector = None
            self.DoZoomIn(x, y, width, height)
            self.Refresh()
            self._ctrl.updateTitle()
        else:

            DiagramFrame.OnLeftUp(self, event)

    def OnLeftDClick(self, event: MouseEvent):
        """
        Manage a left double click mouse event.

        @param  event
        @since 1.22
        @author L. Burgbacher <lb@alawa.ch>
        """
        x, y = self.CalcUnscrolledPosition(event.GetX(), event.GetY())
        self._ctrl.editObject(x, y)
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
        import PyutDataClasses as pdc

        BeginBusyCursor()

        gh: GraphicalHandler = GraphicalHandler(umlFrame=self, maxWidth=self.maxWidth, historyManager=self._history)
        gh.addHierarchy(pdc.display)

        EndBusyCursor()

    def addOglHierarchy(self):
        """
        Calls addHierarchy with the Ogl class list.
        """
        import PyutDataClasses as pdc

        BeginBusyCursor()

        gh: GraphicalHandler = GraphicalHandler(umlFrame=self, maxWidth=self.maxWidth, historyManager=self._history)
        gh.addHierarchy(pdc.displayOgl)

        EndBusyCursor()

    def getUmlObjects(self):
        """
        To know all OglObject.

        @since 1.19
        @author L. Burgbacher <lb@alawa.ch>
        """
        # umlObjs = [s for s in self._diagram.GetShapes() if isinstance(s, (OglObject, OglLink, OglSDMessage))]
        umlObjs = []
        for s in self._diagram.GetShapes():
            if isinstance(s, (OglObject, OglLink, OglSDMessage)):
                umlObjs.append(s)
        return umlObjs

    def getWidth(self):
        """
        Knowing Width.

        @since 1.19
        @author Deve Roux <droux@eivd.ch>
        """
        return self.maxWidth

    def getHeight(self):
        """
        Knowing Height.

        @since 1.19
        @author Deve Roux <droux@eivd.ch>
        """
        return self.maxHeight

    def getObjectsBoundaries(self):
        """
        Return object boundaries (coordinates)

        @since 1.35.2.25
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        infinite = 1e9
        minx     = infinite
        maxx     = -infinite
        miny     = infinite
        maxy     = -infinite

        # Get boundaries
        for shapeObject in self._diagram.GetShapes():
            # Get object limits
            ox1, oy1 = shapeObject.GetPosition()
            ox2, oy2 = shapeObject.GetSize()
            ox2 += ox1
            oy2 += oy1

            # Update min-max
            minx = min(minx, ox1)
            maxx = max(maxx, ox2)
            miny = min(miny, oy1)
            maxy = max(maxy, oy2)

        # Return values
        return minx, miny, maxx, maxy

    def getUmlObjectById(self, objectId: int):
        """
        Added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (20.11.2005)
        @param objectId    :   id for which we want to get an object

        @return the uml object that has the specified id. If there is no
        matching object, None is returned.
        """

        for shape in self.GetDiagram().GetShapes():
            if isinstance(shape, (OglObject, OglLink)):
                if shape.getPyutObject().getId() == objectId:
                    return shape
        return None

    def getHistory(self):
        """
        Added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (20.11.2005)
        @return the history associated to this frame
        """
        return self._history

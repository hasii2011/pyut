
from typing import List
from typing import NewType
from typing import Union
from typing import cast

from logging import Logger
from logging import getLogger

from wx import EVT_CLOSE
from wx import EVT_PAINT

from wx import BeginBusyCursor
from wx import EndBusyCursor
from wx import MouseEvent
from wx import Notebook
from wx import CommandProcessor

from miniogl.Constants import SKIP_EVENT
from miniogl.DiagramFrame import DiagramFrame
from miniogl.RectangleShape import RectangleShape

from ogl.OglInterface2 import OglInterface2
from ogl.OglObject import OglObject
from ogl.OglLink import OglLink
from ogl.OglActor import OglActor

from ogl.OglClass import OglClass
from ogl.OglNote import OglNote
from ogl.OglText import OglText
from ogl.OglUseCase import OglUseCase

from ogl.sd.OglSDInstance import OglSDInstance
from ogl.sd.OglSDMessage import OglSDMessage

from pyut.ui.ActionHandler import ActionHandler
from pyut.ui.Action import Action

from pyut.PyutUtils import PyutUtils

from pyut.experimental.GraphicalHandler import GraphicalHandler

from pyut.ui.umlframes.UmlFrameShapeHandler import UmlFrameShapeHandler

from pyut.ui.eventengine.Events import AddOglDiagramEvent
from pyut.ui.eventengine.Events import AddPyutDiagramEvent
from pyut.ui.eventengine.IEventEngine import IEventEngine

A4_FACTOR:    float = 1.41

UmlObject  = Union[OglClass, OglLink, OglNote, OglText, OglSDMessage, OglSDInstance, OglActor, OglUseCase, OglInterface2]
UmlObjects = NewType('UmlObjects', List[UmlObject])


class UmlFrame(UmlFrameShapeHandler):
    """
    Represents a canvas for drawing diagrams.
    It provides all the methods to add new classes, notes, and links.
    """
    PIXELS_PER_UNIT_X: int = 20
    PIXELS_PER_UNIT_Y: int = 20

    clsUmlFrameLogger: Logger = getLogger(__name__)

    def __init__(self, parent: Notebook, eventEngine: IEventEngine):
        """

        Args:
            parent: The parent window
        """
        from pyut.ui.EditObjectHandler import EditObjectHandler

        super().__init__(parent)

        self.logger:            Logger           = UmlFrame.clsUmlFrameLogger
        self._eventEngine:      IEventEngine     = eventEngine
        self._commandProcessor: CommandProcessor = CommandProcessor()

        self._actionHandler:     ActionHandler     = ActionHandler(eventEngine=eventEngine)
        self._editObjectHandler: EditObjectHandler = EditObjectHandler(eventEngine=eventEngine)

        self.maxWidth:  int  = self._preferences.virtualWindowWidth
        self.maxHeight: int = int(self.maxWidth / A4_FACTOR)  # 1.41 is for A4 support

        nbrUnitsX: int = int(self.maxWidth / UmlFrame.PIXELS_PER_UNIT_X)
        nbrUnitsY: int = int(self.maxHeight / UmlFrame.PIXELS_PER_UNIT_Y)
        initPosX:  int = 0
        initPosY:  int = 0
        self.SetScrollbars(UmlFrame.PIXELS_PER_UNIT_X, UmlFrame.PIXELS_PER_UNIT_Y, nbrUnitsX, nbrUnitsY, initPosX, initPosY, False)

        # Close event
        self.Bind(EVT_CLOSE, self.evtClose)
        self.Bind(EVT_PAINT, self.OnPaint)

        self.SetInfinite(True)

        self._defaultCursor = self.GetCursor()

    @property
    def commandProcessor(self) -> CommandProcessor:
        return self._commandProcessor

    @property
    def umlObjects(self) -> UmlObjects:
        """
        Retrieve UML objects from the UML Frame

        Returns:  The Uml objects on this diagram
        """
        umlObjects: UmlObjects = UmlObjects([])

        for s in self._diagram.shapes:
            # This is a duplicate of the UmlObject, since I cannot use NewType
            if isinstance(s, (OglClass, OglLink, OglNote, OglText, OglSDMessage, OglSDInstance, OglActor, OglUseCase, OglInterface2)):
                umlObjects.append(s)

        return umlObjects

    # noinspection PyUnusedLocal
    def setCodePath(self, path: str):
        """
        Set the code path

        Args:
            path:
        """
        assert False, 'This method is unsupported'
        # project = self._mediator.getFileHandling().getProjectFromFrame(self)
        # if project is not None:
        #     project.setCodePath(path)
        # else:
        #     self._logger.info("Passing setCodePath in UmlFrame-setCodePath")

    def displayDiagramProperties(self):
        """
        Display class diagram properties
        """
        PyutUtils.displayError('Not yet implemented !')

    # noinspection PyUnusedLocal
    def evtClose(self, event):
        """
        Clean close, event handler on EVT_CLOSE

        Args:
            event:
        """
        # self._historyManager.destroy()
        self.Destroy()

    def OnLeftDown(self, event: MouseEvent):
        """
        Manage a left down mouse event.
        If there's an action pending in the action handler, give it the event, else
        let it go to the next handler.
        """
        if self._actionHandler.actionWaiting:
            x, y = self.CalcUnscrolledPosition(event.GetX(), event.GetY())

            skip = self._actionHandler.doAction(self, x, y)

            if self._actionHandler.currentAction == Action.ZOOM_IN:
                DiagramFrame._BeginSelect(self, event)

            if skip == SKIP_EVENT:
                DiagramFrame.OnLeftDown(self, event)
        else:
            super().OnLeftDown(event)

    def OnLeftUp(self, event: MouseEvent):
        """
        To make the right action if it is a selection or a zoom.
        """
        if self._actionHandler.currentAction == Action.ZOOM_IN:
            width, height = self._selector.GetSize()
            x, y = self._selector.GetPosition()
            self._selector.Detach()
            self._selector = cast(RectangleShape, None)
            self.DoZoomIn(x, y, width, height)
            self.Refresh()

            self._actionHandler.updateTitle()
        else:
            super().OnLeftUp(event)

    def OnLeftDClick(self, event: MouseEvent):
        """
        Manage a left double-click mouse event.

        Args:
            event:
        """
        x, y = self.CalcUnscrolledPosition(event.GetX(), event.GetY())
        self.logger.debug(f'leftDoubleClick - {x},{y}')

        self._editObjectHandler.editObject(x, y)

        super().OnLeftDClick(event)

    def clearDiagram(self):
        """
        Remove all shapes
        """
        self._diagram.DeleteAllShapes()
        self.Refresh()

    def getDiagram(self):
        """
        Returns this frame's diagram

        Returns:  wx.Diagram
        """
        return self._diagram

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

    def getUmlObjectById(self, objectId: int) -> UmlObject | None:
        """

        Args:
            objectId:  The id of the object we want

        Returns:  The uml object that has the specified id.
        If no matching object is found, this method returns `None`
        """

        for shape in self.diagram.shapes:
            if isinstance(shape, (OglClass, OglLink, OglObject)):
                if shape.pyutObject.id == objectId:
                    return cast(UmlObject, shape)
        return cast(UmlObject, None)

    # noinspection PyUnusedLocal
    def _onAddPyutDiagram(self, event: AddPyutDiagramEvent):
        """
        Calls addHierarchy with the Pyut class list.
        """
        from pyut.experimental import PyutModelClasses

        BeginBusyCursor()

        gh: GraphicalHandler = GraphicalHandler(umlFrame=self, eventEngine=self._eventEngine, maxWidth=self.maxWidth)
        gh.addHierarchy(PyutModelClasses.PyutClassNames)

        EndBusyCursor()

    # noinspection PyUnusedLocal
    def _onAddOglDiagram(self, event: AddOglDiagramEvent):
        """
        Calls addHierarchy with the Ogl class list.
        """
        from pyut.experimental import PyutModelClasses

        BeginBusyCursor()

        gh: GraphicalHandler = GraphicalHandler(umlFrame=self, eventEngine=self._eventEngine, maxWidth=self.maxWidth)
        gh.addHierarchy(PyutModelClasses.OglClassNames)

        EndBusyCursor()

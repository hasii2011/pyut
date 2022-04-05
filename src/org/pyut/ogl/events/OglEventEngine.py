
from typing import Callable

from logging import Logger
from logging import getLogger

from wx import Point
from wx import PostEvent
from wx import Window
from wx import PyEventBinder

from org.pyut.general.Singleton import Singleton
from org.pyut.miniogl.Shape import Shape

from org.pyut.ogl.events.IEventEngine import IEventEngine
from org.pyut.ogl.events.OglEvents import CutOglClassEvent
from org.pyut.ogl.events.OglEvents import ProjectModifiedEvent
from org.pyut.ogl.events.OglEvents import RequestLollipopLocationEvent
from org.pyut.ogl.events.OglEvents import ShapeSelectedEvent
from org.pyut.ogl.events.ShapeSelectedEventData import ShapeSelectedEventData


class OglEventEngine(IEventEngine):
    """
    The rationale for this class is to isolate the underlying implementation
    of events.  Currently, it depends on the wxPython event loop.  This leaves
    it open to other implementations;

    Get one of these for each Window you want to listen on
    """
    def __init__(self, listeningWindow: Window):

        self._listeningWindow: Window = listeningWindow
        self.logger: Logger = getLogger(__name__)

    def registerListener(self, event: PyEventBinder, callback: Callable):
        self._listeningWindow.Bind(event, callback)

    def sendSelectedShapeEvent(self, shape: Shape, position: Point):

        eventData:     ShapeSelectedEventData = ShapeSelectedEventData(shape=shape, position=position)
        selectedEvent: ShapeSelectedEvent     = ShapeSelectedEvent(shapeSelectedData=eventData)

        PostEvent(dest=self._listeningWindow, event=selectedEvent)

    def sendCutShapeEvent(self, shapeToCut: Shape):
        cutOglClassEvent: CutOglClassEvent = CutOglClassEvent(selectedShape=shapeToCut)
        PostEvent(dest=self._listeningWindow, event=cutOglClassEvent)

    def sendProjectModifiedEvent(self):
        eventToPost: ProjectModifiedEvent = ProjectModifiedEvent()
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def sendRequestLollipopLocationEvent(self, requestShape: Shape):
        eventToPost: RequestLollipopLocationEvent = RequestLollipopLocationEvent(shape=requestShape)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

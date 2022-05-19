
from typing import Callable
from typing import TYPE_CHECKING

from logging import Logger
from logging import getLogger

from wx import Point
from wx import PostEvent
from wx import Window
from wx import PyEventBinder

from ogl.events.InvalidKeywordException import InvalidKeywordException

if TYPE_CHECKING:
    from miniogl.SelectAnchorPoint import SelectAnchorPoint
    from ogl.OglClass import OglClass

from miniogl.Shape import Shape

from ogl.events.IEventEngine import IEventEngine
from ogl.events.OglEventType import OglEventType
from ogl.events.OglEvents import CreateLollipopInterfaceEvent
from ogl.events.OglEvents import CutOglClassEvent
from ogl.events.OglEvents import ProjectModifiedEvent
from ogl.events.OglEvents import RequestLollipopLocationEvent
from ogl.events.OglEvents import ShapeSelectedEvent
from ogl.events.ShapeSelectedEventData import ShapeSelectedEventData

CUT_OGL_CLASS_PARAMETER:                    str = 'shapeToCut'
REQUEST_LOLLIPOP_LOCATION_PARAMETER:        str = 'requestShape'
SELECTED_SHAPE_PARAMETER:                   str = 'selectedShape'
SELECTED_SHAPE_POSITION_PARAMETER:          str = 'selectedShapePosition'
CREATE_LOLLIPOP_IMPLEMENTOR_PARAMETER:      str = 'implementor'
CREATE_LOLLIPOP_ATTACHMENT_POINT_PARAMETER: str = 'attachmentPoint'


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

    def sendEvent(self, eventType: OglEventType, **kwargs):
        """
        CutOglClass: shapeToCut

        Args:
            eventType:
            **kwargs:

        """

        if eventType == OglEventType.ProjectModified:
            self._sendProjectModifiedEvent()

        elif eventType == OglEventType.RequestLollipopLocation:
            try:
                requestShape: Shape = kwargs[REQUEST_LOLLIPOP_LOCATION_PARAMETER]
                self._sendRequestLollipopLocationEvent(requestShape=requestShape)
            except KeyError:
                eMsg: str = f'Invalid keyword parameter.  Use `{REQUEST_LOLLIPOP_LOCATION_PARAMETER}`'
                raise InvalidKeywordException(eMsg)

        elif eventType == OglEventType.CutOglClass:
            try:
                shapeToCut = kwargs[CUT_OGL_CLASS_PARAMETER]
                self._sendCutShapeEvent(shapeToCut=shapeToCut)
            except KeyError:
                eMsg2: str = f'Invalid keyword parameter.  Use `{CUT_OGL_CLASS_PARAMETER}`'
                raise InvalidKeywordException(eMsg2)

        elif eventType == OglEventType.ShapeSelected:
            try:
                shape:    Shape = kwargs[SELECTED_SHAPE_PARAMETER]
                position: Point = kwargs[SELECTED_SHAPE_POSITION_PARAMETER]
                self._sendSelectedShapeEvent(shape=shape, position=position)
            except KeyError:
                eMsg3: str = f'Invalid keywords requires `{SELECTED_SHAPE_PARAMETER}` and `{SELECTED_SHAPE_POSITION_PARAMETER}`'
                raise InvalidKeywordException(eMsg3)

        elif eventType == OglEventType.CreateLollipopInterface:
            try:
                implementor:     OglClass          = kwargs[CREATE_LOLLIPOP_IMPLEMENTOR_PARAMETER]
                attachmentPoint: SelectAnchorPoint = kwargs[CREATE_LOLLIPOP_ATTACHMENT_POINT_PARAMETER]
                self._sendCreateLollipopInterfaceEvent(implementor=implementor, attachmentPoint=attachmentPoint)
            except KeyError:
                eMsg4: str = f'Invalid keywords requires `{CREATE_LOLLIPOP_IMPLEMENTOR_PARAMETER}` and `{CREATE_LOLLIPOP_ATTACHMENT_POINT_PARAMETER}`'
                raise InvalidKeywordException(eMsg4)

    def _sendSelectedShapeEvent(self, shape: Shape, position: Point):

        eventData:     ShapeSelectedEventData = ShapeSelectedEventData(shape=shape, position=position)
        selectedEvent: ShapeSelectedEvent     = ShapeSelectedEvent(shapeSelectedData=eventData)

        PostEvent(dest=self._listeningWindow, event=selectedEvent)

    def _sendCutShapeEvent(self, shapeToCut: Shape):
        cutOglClassEvent: CutOglClassEvent = CutOglClassEvent(selectedShape=shapeToCut)
        PostEvent(dest=self._listeningWindow, event=cutOglClassEvent)

    def _sendProjectModifiedEvent(self):
        eventToPost: ProjectModifiedEvent = ProjectModifiedEvent()
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendRequestLollipopLocationEvent(self, requestShape: Shape):
        eventToPost: RequestLollipopLocationEvent = RequestLollipopLocationEvent(shape=requestShape)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendCreateLollipopInterfaceEvent(self, implementor: 'OglClass', attachmentPoint: 'SelectAnchorPoint'):

        eventToPost: CreateLollipopInterfaceEvent = CreateLollipopInterfaceEvent(implementor=implementor, attachmentPoint=attachmentPoint)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

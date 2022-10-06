
from typing import Callable

from logging import Logger
from logging import getLogger

from wx import PostEvent
from wx import PyEventBinder
from wx import TreeItemId
from wx import Window

from org.pyut.enums.DiagramType import DiagramType
from org.pyut.uiv2.eventengine.Events import CutShapeEvent
from org.pyut.uiv2.eventengine.Events import EventType
from org.pyut.uiv2.eventengine.Events import InsertProjectEvent
from org.pyut.uiv2.eventengine.Events import NewDiagramEvent
from org.pyut.uiv2.eventengine.Events import OpenProjectEvent
from org.pyut.uiv2.eventengine.Events import UpdateApplicationStatusEvent
from org.pyut.uiv2.eventengine.Events import UpdateApplicationTitleEvent
from org.pyut.uiv2.eventengine.Events import UpdateTreeItemNameEvent

from org.pyut.uiv2.eventengine.IEventEngine import IEventEngine

NEW_NAME_PARAMETER:       str = 'newName'
DIAGRAM_TYPE_PARAMETER:   str = 'diagramType'
TREE_ITEM_ID_PARAMETER:   str = 'treeItemId'

NEW_FILENAME_PARAMETER:              str = 'newFilename'
CURRENT_FRAME_ZOOM_FACTOR_PARAMETER: str = 'currentFrameZoomFactor'
PROJECT_MODIFIED_PARAMETER:          str = 'projectModified'

APPLICATION_STATUS_MSG_PARAMETER:    str = 'applicationStatusMsg'

INSERT_PROJECT_FILENAME_PARAMETER:   str = 'projectFilename'
OPEN_PROJECT_FILENAME_PARAMETER:     str = INSERT_PROJECT_FILENAME_PARAMETER

SHAPE_TO_CUT_PARAMETER: str = 'shapeToCut'


class EventEngine(IEventEngine):
    """
    The rationale for this class is to isolate the underlying implementation
    of events.  Currently, it depends on the wxPython event loop.  This leaves
    it open to other implementations;

    Get one of these for each Window you want to listen on
    In practice, Pyut always listens on the top level application Frame

    Additionally, when UI components on different parts of the UI hierarchy need to communicate with
    each other, they should use the eventing mechanism rather than incestuously embedding references
    to each other (after all we are Republicans, not Demo-rats
    """

    def __init__(self, listeningWindow: Window):

        self._listeningWindow: Window = listeningWindow
        self.logger:           Logger = getLogger(__name__)

    def registerListener(self, pyEventBinder: PyEventBinder, callback: Callable):
        self._listeningWindow.Bind(pyEventBinder, callback)

    def sendEvent(self, eventType: EventType, **kwargs):

        match eventType:

            case EventType.UpdateTreeItemName:
                self._sendUpdateTreeItemNameEvent(**kwargs)
            case EventType.UpdateApplicationTitle:
                self._sendNewTitleEvent(**kwargs)
            case EventType.UpdateApplicationStatus:
                self._sendUpdateApplicationStatusEvent(**kwargs)
            case EventType.NewDiagram:
                self._sendNewDiagramEvent(**kwargs)
            case EventType.NewProject:
                self._simpleSendEvent(eventType=eventType)
            case EventType.DeleteDiagram:
                self._simpleSendEvent(eventType=eventType)
            case EventType.CloseProject:
                self._simpleSendEvent(eventType=eventType)
            case EventType.SaveProject:
                self._simpleSendEvent(eventType=eventType)
            case EventType.SaveProjectAs:
                self._simpleSendEvent(eventType=eventType)
            case EventType.UMLDiagramModified:
                self._simpleSendEvent(eventType=eventType)
            case EventType.UpdateRecentProjects:
                self._simpleSendEvent(eventType=eventType)
            case EventType.InsertProject:
                self._sendInsertProjectEvent(**kwargs)
            case EventType.OpenProject:
                self._sendOpenProjectEvent(**kwargs)
            case EventType.SelectAllShapes:
                self._simpleSendEvent(eventType=eventType)
            case EventType.DeSelectAllShapes:
                self._simpleSendEvent(eventType=eventType)
            case EventType.CopyShapes:
                self._simpleSendEvent(eventType=eventType)
            case EventType.PasteShapes:
                self._simpleSendEvent(eventType=eventType)
            case EventType.Undo:
                self._simpleSendEvent(eventType=eventType)
            case EventType.Redo:
                self._simpleSendEvent(eventType=eventType)
            case EventType.CutShape:
                self._sendCutShapeEvent(**kwargs)
            case EventType.CutShapes:
                self._simpleSendEvent(eventType=eventType)
            case EventType.AddOglDiagram:
                self._simpleSendEvent(eventType=eventType)
            case EventType.AddPyutDiagram:
                self._simpleSendEvent(eventType=eventType)
            case _:
                assert False, f'Unknown event type: `{eventType}`'

    def _sendUpdateTreeItemNameEvent(self, **kwargs):

        newName: str = kwargs[NEW_NAME_PARAMETER]
        treeItemId: TreeItemId = kwargs[TREE_ITEM_ID_PARAMETER]

        eventToPost: UpdateTreeItemNameEvent = UpdateTreeItemNameEvent(newName=newName, treeItemId=treeItemId)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendNewTitleEvent(self, **kwargs):
        newFilename:            str   = kwargs[NEW_FILENAME_PARAMETER]
        currentFrameZoomFactor: float = kwargs[CURRENT_FRAME_ZOOM_FACTOR_PARAMETER]
        projectModified:        bool  = kwargs[PROJECT_MODIFIED_PARAMETER]
        eventToPost: UpdateApplicationTitleEvent = UpdateApplicationTitleEvent(newFilename=newFilename,
                                                                               currentFrameZoomFactor=currentFrameZoomFactor,
                                                                               projectModified=projectModified)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendUpdateApplicationStatusEvent(self, **kwargs):
        newMessage:  str = kwargs[APPLICATION_STATUS_MSG_PARAMETER]

        eventToPost: UpdateApplicationStatusEvent = UpdateApplicationStatusEvent(applicationStatusMsg=newMessage)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendInsertProjectEvent(self, **kwargs):

        projectFilename: str                = kwargs[INSERT_PROJECT_FILENAME_PARAMETER]
        eventToPost:     InsertProjectEvent = InsertProjectEvent(projectFilename=projectFilename)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendOpenProjectEvent(self, **kwargs):

        projectFilename: str              = kwargs[OPEN_PROJECT_FILENAME_PARAMETER]
        eventToPost:     OpenProjectEvent = OpenProjectEvent(projectFilename=projectFilename)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendNewDiagramEvent(self, **kwargs):

        diagramType: DiagramType     = kwargs[DIAGRAM_TYPE_PARAMETER]
        eventToPost: NewDiagramEvent = NewDiagramEvent(diagramType=diagramType)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _simpleSendEvent(self, eventType: EventType):
        eventToPost = eventType.commandEvent
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendCutShapeEvent(self, **kwargs):
        shapeToCut = kwargs[SHAPE_TO_CUT_PARAMETER]
        eventToPost: CutShapeEvent = CutShapeEvent(shapeToCut=shapeToCut)
        PostEvent(dest=self._listeningWindow, event=eventToPost)


from logging import Logger
from logging import getLogger
from typing import Callable

from wx import PostEvent
from wx import PyEventBinder
from wx import TreeItemId
from wx import Window

from org.pyut.uiv2.eventengine.Events import EventType
from org.pyut.uiv2.eventengine.Events import NewProjectEvent
from org.pyut.uiv2.eventengine.Events import UpdateApplicationTitleEvent
from org.pyut.uiv2.eventengine.Events import UpdateTreeItemNameEvent
from org.pyut.uiv2.eventengine.IEventEngine import IEventEngine

NEW_NAME_PARAMETER:       str = 'newName'
TREE_ITEM_ID_PARAMETER:   str = 'treeItemId'
PLUGIN_PROJECT_PARAMETER: str = 'pluginProject'

NEW_FILENAME_PARAMETER:              str = 'newFilename'
CURRENT_FRAME_ZOOM_FACTOR_PARAMETER: str = 'currentFrameZoomFactor'
PROJECT_MODIFIED_PARAMETER:          str = 'projectModified'


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

    def registerListener(self, event: PyEventBinder, callback: Callable):
        self._listeningWindow.Bind(event, callback)

    def sendEvent(self, eventType: EventType, **kwargs):

        if eventType == EventType.UpdateTreeItemName:
            newName:    str        = kwargs[NEW_NAME_PARAMETER]
            treeItemId: TreeItemId = kwargs[TREE_ITEM_ID_PARAMETER]
            self._sendUpdateTreeItemNameEvent(newName=newName, treeItemId=treeItemId)
        elif eventType == EventType.UpdateApplicationTitle:
            self._sendNewTitleEvent(**kwargs)

        elif eventType == EventType.NewProject:
            self._sendNewProjectEvent()
        else:
            assert False, f'Unknown event type: {eventType}'

    def _sendUpdateTreeItemNameEvent(self, newName: str, treeItemId: TreeItemId):
        eventToPost: UpdateTreeItemNameEvent = UpdateTreeItemNameEvent(newName=newName, treeItemId=treeItemId)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendNewTitleEvent(self, **kwargs):
        newFilename:             str  = kwargs[NEW_FILENAME_PARAMETER]
        currentFrameZoomFactor: float = kwargs[CURRENT_FRAME_ZOOM_FACTOR_PARAMETER]
        projectModified:        bool  = kwargs[PROJECT_MODIFIED_PARAMETER]
        eventToPost: UpdateApplicationTitleEvent = UpdateApplicationTitleEvent(newFilename=newFilename,
                                                                               currentFrameZoomFactor=currentFrameZoomFactor,
                                                                               projectModified=projectModified)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendNewProjectEvent(self):
        eventToPost: NewProjectEvent = NewProjectEvent()
        PostEvent(dest=self._listeningWindow, event=eventToPost)

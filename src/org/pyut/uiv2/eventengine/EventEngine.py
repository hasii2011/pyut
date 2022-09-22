
from logging import Logger
from logging import getLogger
from typing import Callable

from wx import PostEvent
from wx import PyEventBinder
from wx import TreeItemId
from wx import Window

from core.types.Types import PluginProject

from tests.scaffoldv2.eventengine.EventType import EventType
from tests.scaffoldv2.eventengine.Events import LoadProjectEvent
from tests.scaffoldv2.eventengine.Events import NewProjectEvent
from tests.scaffoldv2.eventengine.IEventEngine import IEventEngine

NEW_NAME_PARAMETER:     str = 'newName'
TREE_ITEM_ID_PARAMETER: str = 'treeItemId'
PLUGIN_PROJECT_PARAMETER: str = 'pluginProject'


class EventEngine(IEventEngine):
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

    def sendEvent(self, eventType: EventType, **kwargs):

        if eventType == EventType.UpdateTreeItemName:
            newName:    str        = kwargs[NEW_NAME_PARAMETER]
            treeItemId: TreeItemId = kwargs[TREE_ITEM_ID_PARAMETER]
            self._sendUpdateTreeItemNameEvent(newName=newName, treeItemId=treeItemId)
        elif eventType == EventType.LoadProjectEvent:
            pluginProject: PluginProject = kwargs[PLUGIN_PROJECT_PARAMETER]
            self._sendLoadProjectEvent(pluginProject=pluginProject)
        elif eventType == EventType.NewProject:
            self._sendNewProjectEvent()

    def _sendUpdateTreeItemNameEvent(self, newName: str, treeItemId: TreeItemId):
        pass

    def _sendNewProjectEvent(self):
        eventToPost: NewProjectEvent = NewProjectEvent()
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendLoadProjectEvent(self, pluginProject: PluginProject):
        eventToPost: LoadProjectEvent = LoadProjectEvent(pluginProject=pluginProject)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

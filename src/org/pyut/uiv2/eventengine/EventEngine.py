from typing import Any
from typing import Callable

from logging import Logger
from logging import getLogger

from wx import PostEvent
from wx import PyEventBinder
from wx import TreeItemId
from wx import Window

from org.pyut.enums.DiagramType import DiagramType
from org.pyut.uiv2.eventengine.CurrentProjectInformation import CurrentProjectInformation
from org.pyut.uiv2.eventengine.Events import CutShapeEvent
from org.pyut.uiv2.eventengine.Events import EventType
from org.pyut.uiv2.eventengine.Events import GetActiveUmlFrameEvent
from org.pyut.uiv2.eventengine.Events import GetProjectInformationEvent
from org.pyut.uiv2.eventengine.Events import InsertProjectEvent
from org.pyut.uiv2.eventengine.Events import NewDiagramEvent
from org.pyut.uiv2.eventengine.Events import OpenProjectEvent
from org.pyut.uiv2.eventengine.Events import SelectToolEvent
from org.pyut.uiv2.eventengine.Events import SetToolActionEvent
from org.pyut.uiv2.eventengine.Events import UpdateApplicationStatusEvent
from org.pyut.uiv2.eventengine.Events import UpdateApplicationTitleEvent
from org.pyut.uiv2.eventengine.Events import UpdateTreeItemNameEvent

from org.pyut.uiv2.eventengine.IEventEngine import IEventEngine

NEW_NAME_PARAMETER:     str = 'newName'
DIAGRAM_TYPE_PARAMETER: str = 'diagramType'
TREE_ITEM_ID_PARAMETER: str = 'treeItemId'
SHAPE_TO_CUT_PARAMETER: str = 'shapeToCut'
TOOL_ID_PARAMETER:      str = 'toolId'
ACTION_PARAMETER:       str = 'action'
NEW_FILENAME_PARAMETER: str = 'newFilename'

PROJECT_MODIFIED_PARAMETER:          str = 'projectModified'
CURRENT_FRAME_ZOOM_FACTOR_PARAMETER: str = 'currentFrameZoomFactor'
APPLICATION_STATUS_MSG_PARAMETER:    str = 'applicationStatusMsg'
INSERT_PROJECT_FILENAME_PARAMETER:   str = 'projectFilename'
OPEN_PROJECT_FILENAME_PARAMETER:     str = INSERT_PROJECT_FILENAME_PARAMETER
CALLBACK_PARAMETER:                  str = 'callback'

# EventCallback = NewType('EventCallback', Callable[[CurrentProjectInformation], None])
ProjectInformationCallback = Callable[[CurrentProjectInformation], None]
ActiveUmlFrameCallback     = Callable[[Any], None]


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
        self.logger: Logger = getLogger(__name__)

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
            case EventType.InsertProject:
                self._sendInsertProjectEvent(**kwargs)
            case EventType.OpenProject:
                self._sendOpenProjectEvent(**kwargs)
            case EventType.CutShape:
                self._sendCutShapeEvent(**kwargs)
            case EventType.SelectTool:
                self._sendSelectToolEvent(**kwargs)
            case EventType.SetToolAction:
                self._sendSetToolActionEvent(**kwargs)
            case EventType.GetProjectInformation:
                self._sendGetProjectInformationRequestEvent(**kwargs)
            case EventType.GetActiveUmlFrame:
                self._sendGetActiveUmlFrameEvent(**kwargs)

            case EventType.NewProject | EventType.DeleteDiagram | EventType.CloseProject | EventType.SaveProject | EventType.SaveProjectAs | \
                    EventType.UMLDiagramModified | EventType.UpdateRecentProjects | EventType.SelectAllShapes | EventType.DeSelectAllShapes | \
                    EventType.CopyShapes | EventType.PasteShapes | EventType.Undo | EventType.Redo | EventType.CutShapes | \
                    EventType.AddOglDiagram | EventType.AddPyutDiagram:
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
        newMessage: str = kwargs[APPLICATION_STATUS_MSG_PARAMETER]

        eventToPost: UpdateApplicationStatusEvent = UpdateApplicationStatusEvent(applicationStatusMsg=newMessage)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendInsertProjectEvent(self, **kwargs):

        projectFilename: str = kwargs[INSERT_PROJECT_FILENAME_PARAMETER]
        eventToPost: InsertProjectEvent = InsertProjectEvent(projectFilename=projectFilename)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendOpenProjectEvent(self, **kwargs):

        projectFilename: str = kwargs[OPEN_PROJECT_FILENAME_PARAMETER]
        eventToPost: OpenProjectEvent = OpenProjectEvent(projectFilename=projectFilename)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendNewDiagramEvent(self, **kwargs):

        diagramType: DiagramType = kwargs[DIAGRAM_TYPE_PARAMETER]
        eventToPost: NewDiagramEvent = NewDiagramEvent(diagramType=diagramType)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _simpleSendEvent(self, eventType: EventType):
        eventToPost = eventType.commandEvent
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendCutShapeEvent(self, **kwargs):
        shapeToCut = kwargs[SHAPE_TO_CUT_PARAMETER]
        eventToPost: CutShapeEvent = CutShapeEvent(shapeToCut=shapeToCut)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendSelectToolEvent(self, **kwargs):

        toolId: int = kwargs[TOOL_ID_PARAMETER]
        eventToPost: SelectToolEvent = SelectToolEvent(toolId=toolId)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendSetToolActionEvent(self, **kwargs):
        action: int = kwargs[ACTION_PARAMETER]
        eventToPost: SetToolActionEvent = SetToolActionEvent(action=action)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendGetProjectInformationRequestEvent(self, **kwargs):

        cb:          ProjectInformationCallback = kwargs[CALLBACK_PARAMETER]
        eventToPost: GetProjectInformationEvent = GetProjectInformationEvent(callback=cb)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendGetActiveUmlFrameEvent(self, **kwargs):

        cb:          ActiveUmlFrameCallback = kwargs[CALLBACK_PARAMETER]
        eventToPost: GetActiveUmlFrameEvent = GetActiveUmlFrameEvent(callback=cb)
        PostEvent(dest=self._listeningWindow, event=eventToPost)
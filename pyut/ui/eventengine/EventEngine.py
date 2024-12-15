
from typing import Any
from typing import Callable

from logging import Logger
from logging import getLogger
from typing import Dict
from typing import NewType

from wx import CommandEvent
from wx import PostEvent
from wx import PyEventBinder
from wx import TreeItemId
from wx import Window

from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.PyutNote import PyutNote
from pyutmodelv2.PyutText import PyutText
from pyutmodelv2.PyutActor import PyutActor
from pyutmodelv2.PyutUseCase import PyutUseCase
from pyutmodelv2.PyutInterface import PyutInterfaces

from ogl.OglObject import OglObject
from ogl.OglClass import OglClass
from ogl.OglInterface2 import OglInterface2

from pyutplugins.ExternalTypes import CurrentProjectCallback
from pyutplugins.ExternalTypes import FrameInformationCallback

from pyut.enums.DiagramType import DiagramType

from pyut.uiv2.IPyutProject import IPyutProject
from pyut.ui.eventengine.Events import AddOglDiagramEvent
from pyut.ui.eventengine.Events import AddPyutDiagramEvent
from pyut.ui.eventengine.Events import AddShapeEvent
from pyut.ui.eventengine.Events import AssociateEditMenuEvent
from pyut.ui.eventengine.Events import ClassNameChangedEvent
from pyut.ui.eventengine.Events import CloseProjectEvent
from pyut.ui.eventengine.Events import CopyShapesEvent
from pyut.ui.eventengine.Events import CutShapesEvent
from pyut.ui.eventengine.Events import DeSelectAllShapesEvent
from pyut.ui.eventengine.Events import DeleteDiagramEvent
from pyut.ui.eventengine.Events import EditActorEvent
from pyut.ui.eventengine.Events import EditInterfaceEvent
from pyut.ui.eventengine.Events import EditNoteEvent
from pyut.ui.eventengine.Events import EditTextEvent
from pyut.ui.eventengine.Events import EditUseCaseEvent
from pyut.ui.eventengine.Events import GetLollipopInterfacesEvent
from pyut.ui.eventengine.Events import FrameInformationEvent
from pyut.ui.eventengine.Events import NewNamedProjectEvent
from pyut.ui.eventengine.Events import NewProjectDiagramEvent
from pyut.ui.eventengine.Events import NewProjectEvent
from pyut.ui.eventengine.Events import OverrideProgramExitPositionEvent
from pyut.ui.eventengine.Events import OverrideProgramExitSizeEvent
from pyut.ui.eventengine.Events import PasteShapesEvent
from pyut.ui.eventengine.Events import RedoEvent
from pyut.ui.eventengine.Events import RefreshFrameEvent
from pyut.ui.eventengine.Events import RequestCurrentProjectEvent
from pyut.ui.eventengine.Events import SaveProjectAsEvent
from pyut.ui.eventengine.Events import SaveProjectEvent
from pyut.ui.eventengine.Events import SelectAllShapesEvent
from pyut.ui.eventengine.Events import SelectedOglObjectsEvent
from pyut.ui.eventengine.Events import UMLDiagramModifiedEvent
from pyut.ui.eventengine.Events import UndoEvent
from pyut.ui.eventengine.Events import UpdateEditMenuEvent
from pyut.ui.eventengine.Events import UpdateRecentProjectsEvent

from pyut.ui.eventengine.eventinformation.MiniProjectInformation import MiniProjectInformation
from pyut.ui.eventengine.eventinformation.ActiveProjectInformation import ActiveProjectInformation
from pyut.ui.eventengine.eventinformation.NewProjectDiagramInformation import NewProjectDiagramInformation

from pyut.ui.eventengine.Events import EditClassEvent
from pyut.ui.eventengine.Events import ActiveProjectInformationEvent
from pyut.ui.eventengine.Events import CutShapeEvent
from pyut.ui.eventengine.Events import EventType
from pyut.ui.eventengine.Events import ActiveUmlFrameEvent
from pyut.ui.eventengine.Events import MiniProjectInformationEvent
from pyut.ui.eventengine.Events import InsertProjectEvent
from pyut.ui.eventengine.Events import NewDiagramEvent
from pyut.ui.eventengine.Events import OpenProjectEvent
from pyut.ui.eventengine.Events import SelectToolEvent
from pyut.ui.eventengine.Events import SetToolActionEvent
from pyut.ui.eventengine.Events import UpdateApplicationStatusEvent
from pyut.ui.eventengine.Events import UpdateApplicationTitleEvent
from pyut.ui.eventengine.Events import UpdateTreeItemNameEvent

from pyut.ui.eventengine.IEventEngine import IEventEngine


NEW_NAME_PARAMETER:     str = 'newName'
DIAGRAM_TYPE_PARAMETER: str = 'diagramType'
TREE_ITEM_ID_PARAMETER: str = 'treeItemId'
SHAPE_TO_CUT_PARAMETER: str = 'shapeToCut'
SHAPE_TO_ADD_PARAMETER: str = 'shapeToAdd'
TOOL_ID_PARAMETER:      str = 'toolId'
ACTION_PARAMETER:       str = 'action'
NEW_FILENAME_PARAMETER: str = 'newFilename'

IMPLEMENTOR_PARAMETER:         str = 'implementor'
PYUT_INTERFACE_PARAMETER:      str = 'pyutInterface'
PYUT_INTERFACE_NAME_PARAMETER: str = 'pyutInterfaceName'

COMMAND_PROCESSOR_PARAMETER:         str = 'commandProcessor'
PROJECT_MODIFIED_PARAMETER:          str = 'projectModified'
CURRENT_FRAME_ZOOM_FACTOR_PARAMETER: str = 'currentFrameZoomFactor'
APPLICATION_STATUS_MSG_PARAMETER:    str = 'applicationStatusMsg'
INSERT_PROJECT_FILENAME_PARAMETER:   str = 'projectFilename'
OPEN_PROJECT_FILENAME_PARAMETER:     str = INSERT_PROJECT_FILENAME_PARAMETER
NEW_PROJECT_FROM_FILENAME_PARAMETER: str = OPEN_PROJECT_FILENAME_PARAMETER
CALLBACK_PARAMETER:                  str = 'callback'
PYUT_CLASS_PARAMETER:                str = 'pyutClass'
PYUT_NOTE_PARAMETER:                 str = 'pyutNote'
PYUT_TEXT_PARAMETER:                 str = 'pyutText'
PYUT_ACTOR_PARAMETER:                str = 'pyutActor'
PYUT_USE_CASE_PARAMETER:             str = 'pyutUseCase'

OGL_INTERFACE2_PARAMETER:            str = 'oglInterface2'

PROJECT_FILENAME_PARAMETER:                str = INSERT_PROJECT_FILENAME_PARAMETER
NEW_PROJECT_DIAGRAM_INFORMATION_PARAMETER: str = 'newProjectDiagramInformation'

OLD_CLASS_NAME_PARAMETER: str = 'oldClassName'
NEW_CLASS_NAME_PARAMETER: str = 'newClassName'
OVERRIDE_PARAMETER:       str = 'override'

MiniProjectInformationCallback    = Callable[[MiniProjectInformation], None]
ActiveUmlFrameCallback            = Callable[[Any], None]                       # Figure out appropriate type for callback
ActiveProjectInformationCallback  = Callable[[ActiveProjectInformation], None]
NewNamedProjectCallback           = Callable[[IPyutProject], None]
GetLollipopInterfacesCallback     = Callable[[PyutInterfaces], None]            # Figure out appropriate type for callback

EventEnumToType = NewType('EventEnumToType', Dict[EventType, CommandEvent])

SimpleEvents: EventEnumToType = EventEnumToType({
    EventType.NewProject:         NewProjectEvent,
    EventType.DeleteDiagram:      DeleteDiagramEvent,
    EventType.CloseProject:       CloseProjectEvent,
    EventType.SaveProject:        SaveProjectEvent,
    EventType.SaveProjectAs:      SaveProjectAsEvent,
    EventType.UMLDiagramModified: UMLDiagramModifiedEvent,
    EventType.SelectAllShapes:    SelectAllShapesEvent,
    EventType.DeSelectAllShapes:  DeSelectAllShapesEvent,
    EventType.CopyShapes:         CopyShapesEvent,
    EventType.PasteShapes:        PasteShapesEvent,
    EventType.Undo:               UndoEvent,
    EventType.Redo:               RedoEvent,
    EventType.CutShapes:          CutShapesEvent,
    EventType.AddOglDiagram:      AddOglDiagramEvent,
    EventType.AddPyutDiagram:     AddPyutDiagramEvent,
    EventType.RefreshFrame:       RefreshFrameEvent,
})


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
            case EventType.NewNamedProject:
                self._sendNewNamedProjectEvent(**kwargs)
            case EventType.NewDiagram:
                self._sendNewDiagramEvent(**kwargs)
            case EventType.NewProjectDiagram:
                self._sendNewProjectDiagramEvent(**kwargs)
            case EventType.InsertProject:
                self._sendInsertProjectEvent(**kwargs)
            case EventType.OpenProject:
                self._sendOpenProjectEvent(**kwargs)
            case EventType.CutShape:
                self._sendCutShapeEvent(**kwargs)
            case EventType.AddShape:
                self._sendAddShapeEvent(**kwargs)
            case EventType.SelectTool:
                self._sendSelectToolEvent(**kwargs)
            case EventType.SetToolAction:
                self._sendSetToolActionEvent(**kwargs)
            case EventType.MiniProjectInformation:
                self._sendMiniProjectInformationEvent(**kwargs)
            case EventType.ActiveUmlFrame:
                self._sendGetActiveUmlFrameEvent(**kwargs)
            case EventType.ActiveProjectInformation:
                self._sendActiveProjectInformationEvent(**kwargs)
            case EventType.EditClass:
                self._sendEditClassEvent(**kwargs)
            case EventType.EditNote:
                self._sendEditNoteEvent(**kwargs)
            case EventType.EditText:
                self._sendEditTextEvent(**kwargs)
            case EventType.EditActor:
                self._sendEditActorEvent(**kwargs)
            case EventType.EditUseCase:
                self._sendEditUseCaseEvent(**kwargs)
            case EventType.EditInterface:
                self._sendEditInterfaceEvent(**kwargs)

            case EventType.FrameInformation:
                self._sendFrameInformationEvent(**kwargs)
            case EventType.SelectedOglObjects:
                self._sendSelectedOglObjectsEvent(**kwargs)
            case EventType.UpdateRecentProjects:
                self._sendUpdateRecentProjectEvent(**kwargs)

            case EventType.UpdateEditMenu:
                self._sendUpdateEditMenuEvent(**kwargs)
            case EventType.AssociateEditMenu:
                self._sendAssociateEditMenuEvent(**kwargs)

            case EventType.RequestCurrentProject:
                self._sendRequestCurrentProjectEvent(**kwargs)
            case EventType.ClassNameChanged:
                self._sendClassNameChangedEvent(**kwargs)

            case EventType.OverrideProgramExitPosition:
                self._sendOverrideProgramExitPositionEvent(**kwargs)

            case EventType.OverrideProgramExitSize:
                self._sendOverrideProgramExitSizeEvent(**kwargs)

            case EventType.GetLollipopInterfaces:
                self._sendGetLollipopInterfacesEvent(**kwargs)
            case EventType.NewProject | EventType.DeleteDiagram | EventType.CloseProject | EventType.SaveProject | EventType.SaveProjectAs | \
                    EventType.UMLDiagramModified | EventType.SelectAllShapes | EventType.DeSelectAllShapes | \
                    EventType.CopyShapes | EventType.PasteShapes | EventType.Undo | EventType.Redo | EventType.CutShapes | \
                    EventType.AddOglDiagram | EventType.AddPyutDiagram | EventType.RefreshFrame:
                self._simpleSendEvent(eventType=eventType)
            case _:
                assert False, f'Unknown event type: `{eventType}`'

    def _simpleSendEvent(self, eventType: EventType):

        try:
            eventClazz = SimpleEvents[eventType]
            event = eventClazz()
            PostEvent(dest=self._listeningWindow, event=event)
        except KeyError:
            self.logger.error(f'Unhandled event type: {eventType.value}')

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

    def _sendNewNamedProjectEvent(self, **kwargs):
        projectFilename: str                     = kwargs[NEW_PROJECT_FROM_FILENAME_PARAMETER]
        callback:        NewNamedProjectCallback = kwargs[CALLBACK_PARAMETER]
        eventToPost:     NewNamedProjectEvent    = NewNamedProjectEvent(projectFilename=projectFilename, callback=callback)

        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendNewProjectDiagramEvent(self, **kwargs):
        info: NewProjectDiagramInformation = kwargs[NEW_PROJECT_DIAGRAM_INFORMATION_PARAMETER]
        eventToPost: NewProjectDiagramEvent = NewProjectDiagramEvent(newProjectDiagramInformation=info)

        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendNewDiagramEvent(self, **kwargs):

        diagramType: DiagramType = kwargs[DIAGRAM_TYPE_PARAMETER]
        eventToPost: NewDiagramEvent = NewDiagramEvent(diagramType=diagramType)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendCutShapeEvent(self, **kwargs):
        shapeToCut: OglObject = kwargs[SHAPE_TO_CUT_PARAMETER]
        eventToPost: CutShapeEvent = CutShapeEvent(shapeToCut=shapeToCut)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendAddShapeEvent(self, **kwargs):
        shapeToAdd: OglObject = kwargs[SHAPE_TO_ADD_PARAMETER]
        eventToPost: AddShapeEvent = AddShapeEvent(shapeToAdd=shapeToAdd)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendSelectToolEvent(self, **kwargs):

        toolId: int = kwargs[TOOL_ID_PARAMETER]
        eventToPost: SelectToolEvent = SelectToolEvent(toolId=toolId)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendSetToolActionEvent(self, **kwargs):
        action: int = kwargs[ACTION_PARAMETER]
        eventToPost: SetToolActionEvent = SetToolActionEvent(action=action)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendMiniProjectInformationEvent(self, **kwargs):

        cb:          MiniProjectInformationCallback = kwargs[CALLBACK_PARAMETER]
        eventToPost: MiniProjectInformationEvent = MiniProjectInformationEvent(callback=cb)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendGetActiveUmlFrameEvent(self, **kwargs):

        cb:          ActiveUmlFrameCallback = kwargs[CALLBACK_PARAMETER]
        eventToPost: ActiveUmlFrameEvent = ActiveUmlFrameEvent(callback=cb)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendActiveProjectInformationEvent(self, **kwargs):

        cb:          ActiveUmlFrameCallback         = kwargs[CALLBACK_PARAMETER]
        eventToPost: ActiveProjectInformationEvent = ActiveProjectInformationEvent(callback=cb)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendEditClassEvent(self, **kwargs):
        pyutClass:   PyutClass      = kwargs[PYUT_CLASS_PARAMETER]
        eventToPost: EditClassEvent = EditClassEvent(pyutClass=pyutClass)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendEditNoteEvent(self, **kwargs):
        pyutNote:    PyutNote      = kwargs[PYUT_NOTE_PARAMETER]
        eventToPost: EditNoteEvent = EditNoteEvent(pyutNote=pyutNote)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendEditTextEvent(self, **kwargs):
        pyutText:    PyutText      = kwargs[PYUT_TEXT_PARAMETER]
        eventToPost: EditTextEvent = EditTextEvent(pyutText=pyutText)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendEditActorEvent(self, **kwargs):
        pyutActor: PyutActor       = kwargs[PYUT_ACTOR_PARAMETER]
        eventToPost: EditActorEvent = EditActorEvent(pyutActor=pyutActor)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendEditUseCaseEvent(self, **kwargs):
        pyutUseCase: PyutUseCase     = kwargs[PYUT_USE_CASE_PARAMETER]
        eventToPost: EditUseCaseEvent = EditUseCaseEvent(pyutUseCase=pyutUseCase)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendEditInterfaceEvent(self, **kwargs):

        oglInterface2: OglInterface2      = kwargs[OGL_INTERFACE2_PARAMETER]
        implementor:   OglClass           = kwargs[IMPLEMENTOR_PARAMETER]
        eventToPost:   EditInterfaceEvent = EditInterfaceEvent(oglInterface2=oglInterface2, implementor=implementor)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendFrameInformationEvent(self, **kwargs):

        cb: FrameInformationCallback = kwargs[CALLBACK_PARAMETER]
        eventToPost: FrameInformationEvent = FrameInformationEvent(callback=cb)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendSelectedOglObjectsEvent(self, **kwargs):

        cb: FrameInformationCallback = kwargs[CALLBACK_PARAMETER]
        eventToPost: SelectedOglObjectsEvent = SelectedOglObjectsEvent(callback=cb)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendUpdateRecentProjectEvent(self, **kwargs):
        projectFilename: str = kwargs[PROJECT_FILENAME_PARAMETER]
        eventToPost: UpdateRecentProjectsEvent = UpdateRecentProjectsEvent(projectFilename=projectFilename)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendUpdateEditMenuEvent(self, **kwargs):

        from wx import CommandProcessor

        commandProcessor: CommandProcessor    = kwargs[COMMAND_PROCESSOR_PARAMETER]
        eventToPost:      UpdateEditMenuEvent = UpdateEditMenuEvent(commandProcessor=commandProcessor)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendAssociateEditMenuEvent(self, **kwargs):

        from wx import CommandProcessor

        commandProcessor: CommandProcessor       = kwargs[COMMAND_PROCESSOR_PARAMETER]
        eventToPost:      AssociateEditMenuEvent = AssociateEditMenuEvent(commandProcessor=commandProcessor)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendClassNameChangedEvent(self, **kwargs):
        oldClassName: str = kwargs[OLD_CLASS_NAME_PARAMETER]
        newClassName: str = kwargs[NEW_CLASS_NAME_PARAMETER]
        eventToPost: ClassNameChangedEvent = ClassNameChangedEvent(oldClassName=oldClassName, newClassName=newClassName)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendGetLollipopInterfacesEvent(self, **kwargs):

        cb: GetLollipopInterfacesCallback = kwargs[CALLBACK_PARAMETER]

        event: GetLollipopInterfacesEvent = GetLollipopInterfacesEvent(callback=cb)
        PostEvent(dest=self._listeningWindow, event=event)

    def _sendRequestCurrentProjectEvent(self, **kwargs):
        callback:    CurrentProjectCallback     = kwargs[CALLBACK_PARAMETER]
        eventToPost: RequestCurrentProjectEvent = RequestCurrentProjectEvent(callback=callback)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendOverrideProgramExitPositionEvent(self, **kwargs):
        value:       bool = kwargs[OVERRIDE_PARAMETER]
        eventToPost: OverrideProgramExitPositionEvent = OverrideProgramExitPositionEvent(override=value)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendOverrideProgramExitSizeEvent(self, **kwargs):
        value:       bool = kwargs[OVERRIDE_PARAMETER]
        eventToPost: OverrideProgramExitSizeEvent = OverrideProgramExitSizeEvent(override=value)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

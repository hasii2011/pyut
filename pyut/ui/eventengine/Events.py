
from wx.lib.newevent import NewEvent

#
# The constructor returns a tuple; The first is the event,  The second is the binder
#
NewProjectEvent,               EVENT_NEW_PROJECT                = NewEvent()
NewNamedProjectEvent,          EVENT_NEW_NAMED_PROJECT          = NewEvent()
NewDiagramEvent,               EVENT_NEW_DIAGRAM                = NewEvent()
NewProjectDiagramEvent,        EVENT_NEW_PROJECT_DIAGRAM        = NewEvent()
DeleteDiagramEvent,            EVENT_DELETE_DIAGRAM             = NewEvent()
OpenProjectEvent,              EVENT_OPEN_PROJECT               = NewEvent()
InsertProjectEvent,            EVENT_INSERT_PROJECT             = NewEvent()
SaveProjectEvent,              EVENT_SAVE_PROJECT               = NewEvent()
SaveProjectAsEvent,            EVENT_SAVE_PROJECT_AS            = NewEvent()
CloseProjectEvent,             EVENT_CLOSE_PROJECT              = NewEvent()
UpdateTreeItemNameEvent,       EVENT_UPDATE_TREE_ITEM_NAME      = NewEvent()
UpdateApplicationTitleEvent,   EVENT_UPDATE_APPLICATION_TITLE   = NewEvent()
UpdateApplicationStatusEvent,  EVENT_UPDATE_APPLICATION_STATUS  = NewEvent()
UMLDiagramModifiedEvent,       EVENT_UML_DIAGRAM_MODIFIED       = NewEvent()
UpdateRecentProjectsEvent,     EVENT_UPDATE_RECENT_PROJECTS     = NewEvent()
SelectAllShapesEvent,          EVENT_SELECT_ALL_SHAPES          = NewEvent()
DeSelectAllShapesEvent,        EVENT_DESELECT_ALL_SHAPES        = NewEvent()
AddShapeEvent,                 EVENT_ADD_SHAPE                  = NewEvent()
CopyShapesEvent,               EVENT_COPY_SHAPES                = NewEvent()
PasteShapesEvent,              EVENT_PASTE_SHAPES               = NewEvent()
CutShapesEvent,                EVENT_CUT_SHAPES                 = NewEvent()
UndoEvent,                     EVENT_UNDO                       = NewEvent()
RedoEvent,                     EVENT_REDO                       = NewEvent()
CutShapeEvent,                 EVENT_CUT_SHAPE                  = NewEvent()          # TODO:  I do not think this is used anymore
EditClassEvent,                EVENT_EDIT_CLASS,                = NewEvent()
EditNoteEvent,                 EVENT_EDIT_NOTE                  = NewEvent()
EditTextEvent,                 EVENT_EDIT_TEXT                  = NewEvent()
EditActorEvent,                EVENT_EDIT_ACTOR                 = NewEvent()
EditUseCaseEvent,              EVENT_EDIT_USE_CASE              = NewEvent()
EditInterfaceEvent,            EVENT_EDIT_INTERFACE             = NewEvent()
AddPyutDiagramEvent,           EVENT_ADD_PYUT_DIAGRAM           = NewEvent()
AddOglDiagramEvent,            EVENT_ADD_OGL_DIAGRAM            = NewEvent()
SelectToolEvent,               EVENT_SELECT_TOOL                = NewEvent()
SetToolActionEvent,            EVENT_SET_TOOL_ACTION            = NewEvent()
MiniProjectInformationEvent,   EVENT_MINI_PROJECT_INFORMATION   = NewEvent()
ActiveUmlFrameEvent,           EVENT_ACTIVE_UML_FRAME           = NewEvent()
ActiveProjectInformationEvent, EVENT_ACTIVE_PROJECT_INFORMATION = NewEvent()
GetLollipopInterfacesEvent,    EVENT_GET_LOLLIPOP_INTERFACES    = NewEvent()
DarkModeChangedEvent,          EVENT_DARK_MODE_CHANGED          = NewEvent()

OverrideProgramExitSizeEvent,     EVENT_OVERRIDE_PROGRAM_EXIT_SIZE     = NewEvent()
OverrideProgramExitPositionEvent, EVENT_OVERRIDE_PROGRAM_EXIT_POSITION = NewEvent()

# The following specifically for the plugin adapter
FrameInformationEvent,         EVENT_FRAME_INFORMATION       = NewEvent()
FrameSizeEvent,                EVENT_FRAME_SIZE              = NewEvent()
SelectedOglObjectsEvent,       EVENT_SELECTED_OGL_OBJECTS    = NewEvent()      # Pyut will also use this eventHandler
RefreshFrameEvent,             EVENT_REFRESH_FRAME           = NewEvent()
UpdateEditMenuEvent,           EVENT_UPDATE_EDIT_MENU        = NewEvent()
AssociateEditMenuEvent,        EVENT_ASSOCIATE_EDIT_MENU     = NewEvent()
ClassNameChangedEvent,         EVENT_CLASS_NAME_CHANGED      = NewEvent()
RequestCurrentProjectEvent,    EVENT_REQUEST_CURRENT_PROJECT = NewEvent()
DeleteLinkEvent,               EVENT_DELETE_LINK             = NewEvent()
CreateLinkEvent,               EVENT_CREATE_LINK             = NewEvent()

ShowOrthogonalRoutingPointsEvent, EVENT_SHOW_ORTHOGONAL_ROUTING_POINTS = NewEvent()
ShowRulersEvent,                  EVENT_SHOW_RULERS                    = NewEvent()
ShowRouteGridEvent,               EVENT_SHOW_ROUTE_GRID                = NewEvent()

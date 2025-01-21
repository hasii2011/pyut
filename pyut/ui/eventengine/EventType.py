
from enum import Enum

from pyut.ui.eventengine.Events import EVENT_ACTIVE_PROJECT_INFORMATION
from pyut.ui.eventengine.Events import EVENT_ACTIVE_UML_FRAME
from pyut.ui.eventengine.Events import EVENT_ADD_OGL_DIAGRAM
from pyut.ui.eventengine.Events import EVENT_ADD_PYUT_DIAGRAM
from pyut.ui.eventengine.Events import EVENT_ADD_SHAPE
from pyut.ui.eventengine.Events import EVENT_ASSOCIATE_EDIT_MENU
from pyut.ui.eventengine.Events import EVENT_CLASS_NAME_CHANGED
from pyut.ui.eventengine.Events import EVENT_CLOSE_PROJECT
from pyut.ui.eventengine.Events import EVENT_COPY_SHAPES
from pyut.ui.eventengine.Events import EVENT_CREATE_LINK
from pyut.ui.eventengine.Events import EVENT_CUT_SHAPE
from pyut.ui.eventengine.Events import EVENT_CUT_SHAPES
from pyut.ui.eventengine.Events import EVENT_DARK_MODE_CHANGED
from pyut.ui.eventengine.Events import EVENT_DELETE_DIAGRAM
from pyut.ui.eventengine.Events import EVENT_DELETE_LINK
from pyut.ui.eventengine.Events import EVENT_DESELECT_ALL_SHAPES
from pyut.ui.eventengine.Events import EVENT_EDIT_ACTOR
from pyut.ui.eventengine.Events import EVENT_EDIT_CLASS
from pyut.ui.eventengine.Events import EVENT_EDIT_INTERFACE
from pyut.ui.eventengine.Events import EVENT_EDIT_NOTE
from pyut.ui.eventengine.Events import EVENT_EDIT_TEXT
from pyut.ui.eventengine.Events import EVENT_EDIT_USE_CASE
from pyut.ui.eventengine.Events import EVENT_FRAME_INFORMATION
from pyut.ui.eventengine.Events import EVENT_FRAME_SIZE
from pyut.ui.eventengine.Events import EVENT_GET_LOLLIPOP_INTERFACES
from pyut.ui.eventengine.Events import EVENT_INSERT_PROJECT
from pyut.ui.eventengine.Events import EVENT_MINI_PROJECT_INFORMATION
from pyut.ui.eventengine.Events import EVENT_NEW_DIAGRAM
from pyut.ui.eventengine.Events import EVENT_NEW_NAMED_PROJECT
from pyut.ui.eventengine.Events import EVENT_NEW_PROJECT
from pyut.ui.eventengine.Events import EVENT_NEW_PROJECT_DIAGRAM
from pyut.ui.eventengine.Events import EVENT_OPEN_PROJECT
from pyut.ui.eventengine.Events import EVENT_OVERRIDE_PROGRAM_EXIT_POSITION
from pyut.ui.eventengine.Events import EVENT_OVERRIDE_PROGRAM_EXIT_SIZE
from pyut.ui.eventengine.Events import EVENT_PASTE_SHAPES
from pyut.ui.eventengine.Events import EVENT_REDO
from pyut.ui.eventengine.Events import EVENT_REFRESH_FRAME
from pyut.ui.eventengine.Events import EVENT_REQUEST_CURRENT_PROJECT
from pyut.ui.eventengine.Events import EVENT_SAVE_PROJECT
from pyut.ui.eventengine.Events import EVENT_SAVE_PROJECT_AS
from pyut.ui.eventengine.Events import EVENT_SELECTED_OGL_OBJECTS
from pyut.ui.eventengine.Events import EVENT_SELECT_ALL_SHAPES
from pyut.ui.eventengine.Events import EVENT_SELECT_TOOL
from pyut.ui.eventengine.Events import EVENT_SET_TOOL_ACTION
from pyut.ui.eventengine.Events import EVENT_UML_DIAGRAM_MODIFIED
from pyut.ui.eventengine.Events import EVENT_UNDO
from pyut.ui.eventengine.Events import EVENT_UPDATE_APPLICATION_STATUS
from pyut.ui.eventengine.Events import EVENT_UPDATE_APPLICATION_TITLE
from pyut.ui.eventengine.Events import EVENT_UPDATE_EDIT_MENU
from pyut.ui.eventengine.Events import EVENT_UPDATE_RECENT_PROJECTS
from pyut.ui.eventengine.Events import EVENT_UPDATE_TREE_ITEM_NAME


class EventType(Enum):
    """
    The value for a specific EventType is going to be the ID of
    its associated PyEventBinder.

    UpdateApplicationTitleEvent
        Updates the application title
        parameters:
            newFilename: str
            currentFrameZoomFactor : float
            projectModified : bool

    UpdateApplicationStatusEvent
        Updates the application status bar
        parameters:
            applicationStatusMsg:  The new message to display

    RemoveDocumentEvent
        Removes the currently selected document

    NewNamedProjectEvent
        Creates a new project in the project manager and the appropriate UI elements
        parameter:
            projectFilename:  The fully qualified filename
            callback:         The callback to return the IPyutProject object

    InsertProjectEvent
        parameter:
            projectFilename:  The fully qualified filename

    NewDiagramEvent
        Creates a new diagram on the current project
        parameter:
            diagramType:   A value from the DiagramType enumeration

    NewProjectDiagramEvent
        Creates a new diagram for the given project;  Includes the UI and model artifacts
        parameters:
            NewProjectDiagramInformation

    CutShapeEvent
        Cuts only the specified shape
        parameter:
            shapeToCut

    EditClassEvent
        Invokes the Edit Class dialog
        parameter:
            pyutClass

    EditNoteEvent
        Invokes the Edit Note dialog
        parameter:
            pyutNote

    EditTextEvent
        Invokes the Edit Text dialog
        parameter:
            pyutText

    EditActorEvent
        Invokes a general Edit dialog for the name
        parameter:
            pyutActor

    AddShapeEvent
        Adds the specified shape on the UI
        parameter:
            oglObject      The Ogl document to place on the UML UmlFrame

    SelectToolEvent
        Use to select tools in the toolbar as a visual-aid to the end-user/developer
        parameter:
            toolId - The tool id;  The value generated by wx.NewIdRef

    SetToolActionEvent
        Used to set the appropriate tool action for the ActionHandler.
        Parameter
            action The action identifier from Actions

    MiniProjectInformationEvent:
        Used to get some project data;
        parameters
            callback - Callback that is invoked with a parameter of type MiniProjectInformation

    ActiveUmlFrameEvent
        Used to retrieve the currently active frame
        parameters:
            callback - Callback this is invoked with a parameter of type UmlDiagramsFrame

    ActiveProjectInformationEvent
        Used to get information on the active project so that the UML Object edit dialogs
        can do their job
        parameters:
            callback - Callback that is invoked with a parameter of type ActiveProjectInformation

    FrameInformationEvent
        Use by the plugin adaptor to provide low level to plugins that need item
        parameters:
            callback - Callback this is invoked with a parameter of type FrameInformation

    UpdateEditMenuEvent
        Used to update the Edit menu Undo/redo menu items.  This involves using the
        command processor associated with each Uml Frame
        parameters:
            commandProcessor - The command processor associated with the currently visible UML Frame

    AssociateEditMenuEvent:
        Used on the initial creation of a Unified Modeling Language (UML) frame to associate it with the Edit Menu
        parameters:
            commandProcessor - The command processor associated with the currently visible UML Frame

    ClassNameChangedEvent:
        Used if a dialog or some code changes a class name.  We have to update the model and the
        model
        parameters:
            oldClassName - the old class name
            newClassName - the new class name

    Events with no parameters get stuffed into the enumeration as instances, so they can be used
    event engine simple send method;  To simplify enumeration creation I create instances for all
    event types
    """

    NewProject                  = EVENT_NEW_PROJECT.typeId
    NewNamedProject             = EVENT_NEW_NAMED_PROJECT.typeId
    NewDiagram                  = EVENT_NEW_DIAGRAM.typeId
    NewProjectDiagram           = EVENT_NEW_PROJECT_DIAGRAM.typeId
    DeleteDiagram               = EVENT_DELETE_DIAGRAM.typeId
    OpenProject                 = EVENT_OPEN_PROJECT.typeId
    InsertProject               = EVENT_INSERT_PROJECT.typeId
    SaveProject                 = EVENT_SAVE_PROJECT.typeId
    SaveProjectAs               = EVENT_SAVE_PROJECT_AS.typeId
    CloseProject                = EVENT_CLOSE_PROJECT.typeId
    UpdateTreeItemName          = EVENT_UPDATE_TREE_ITEM_NAME.typeId
    UpdateApplicationTitle      = EVENT_UPDATE_APPLICATION_TITLE.typeId
    UpdateApplicationStatus     = EVENT_UPDATE_APPLICATION_STATUS.typeId
    UpdateRecentProjects        = EVENT_UPDATE_RECENT_PROJECTS.typeId
    UMLDiagramModified          = EVENT_UML_DIAGRAM_MODIFIED.typeId
    SelectAllShapes             = EVENT_SELECT_ALL_SHAPES.typeId
    DeSelectAllShapes           = EVENT_DESELECT_ALL_SHAPES.typeId
    AddShape                    = EVENT_ADD_SHAPE.typeId
    CopyShapes                  = EVENT_COPY_SHAPES.typeId
    PasteShapes                 = EVENT_PASTE_SHAPES.typeId
    CutShapes                   = EVENT_CUT_SHAPES.typeId
    Undo                        = EVENT_UNDO.typeId
    Redo                        = EVENT_REDO.typeId
    CutShape                    = EVENT_CUT_SHAPE.typeId         # TODO:  I do not think this is used anymore
    AddPyutDiagram              = EVENT_ADD_PYUT_DIAGRAM.typeId
    AddOglDiagram               = EVENT_ADD_OGL_DIAGRAM.typeId
    SelectTool                  = EVENT_SELECT_TOOL.typeId
    SetToolAction               = EVENT_SET_TOOL_ACTION.typeId
    MiniProjectInformation      = EVENT_MINI_PROJECT_INFORMATION.typeId
    ActiveUmlFrame              = EVENT_ACTIVE_UML_FRAME.typeId
    ActiveProjectInformation    = EVENT_ACTIVE_PROJECT_INFORMATION.typeId
    GetLollipopInterfaces       = EVENT_GET_LOLLIPOP_INTERFACES.typeId
    EditClass                   = EVENT_EDIT_CLASS.typeId
    EditNote                    = EVENT_EDIT_NOTE.typeId
    EditText                    = EVENT_EDIT_TEXT.typeId
    EditActor                   = EVENT_EDIT_ACTOR.typeId
    EditUseCase                 = EVENT_EDIT_USE_CASE.typeId
    EditInterface               = EVENT_EDIT_INTERFACE.typeId
    FrameInformation            = EVENT_FRAME_INFORMATION.typeId
    FrameSize                   = EVENT_FRAME_SIZE.typeId
    SelectedOglObjects          = EVENT_SELECTED_OGL_OBJECTS.typeId
    RefreshFrame                = EVENT_REFRESH_FRAME.typeId
    UpdateEditMenu              = EVENT_UPDATE_EDIT_MENU.typeId
    AssociateEditMenu           = EVENT_ASSOCIATE_EDIT_MENU.typeId
    ClassNameChanged            = EVENT_CLASS_NAME_CHANGED.typeId
    RequestCurrentProject       = EVENT_REQUEST_CURRENT_PROJECT.typeId
    DeleteLink                  = EVENT_DELETE_LINK.typeId
    CreateLink                  = EVENT_CREATE_LINK.typeId
    DarkModeChanged             = EVENT_DARK_MODE_CHANGED.typeId

    OverrideProgramExitSize     = EVENT_OVERRIDE_PROGRAM_EXIT_SIZE.typeId
    OverrideProgramExitPosition = EVENT_OVERRIDE_PROGRAM_EXIT_POSITION.typeId

    NOT_SET = -6666


from enum import Enum

from wx import CommandEvent
from wx import PyEventBinder

from wx.lib.newevent import NewEvent

#
# Constructor return Tuple; First is the event,  The second is the binder
#
NewProjectEvent,              EVENT_NEW_PROJECT               = NewEvent()
NewDiagramEvent,              EVENT_NEW_DIAGRAM               = NewEvent()
DeleteDiagramEvent,           EVENT_DELETE_DIAGRAM            = NewEvent()
OpenProjectEvent,             EVENT_OPEN_PROJECT              = NewEvent()
InsertProjectEvent,           EVENT_INSERT_PROJECT            = NewEvent()
SaveProjectEvent,             EVENT_SAVE_PROJECT              = NewEvent()
SaveProjectAsEvent,           EVENT_SAVE_PROJECT_AS           = NewEvent()
CloseProjectEvent,            EVENT_CLOSE_PROJECT             = NewEvent()
UpdateTreeItemNameEvent,      EVENT_UPDATE_TREE_ITEM_NAME     = NewEvent()
UpdateApplicationTitleEvent,  EVENT_UPDATE_APPLICATION_TITLE  = NewEvent()
UpdateApplicationStatusEvent, EVENT_UPDATE_APPLICATION_STATUS = NewEvent()

UMLDiagramModifiedEvent, EVENT_UML_DIAGRAM_MODIFIED    = NewEvent()

UpdateRecentProjectsEvent,    EVENT_UPDATE_RECENT_PROJECTS    = NewEvent()

SelectAllShapesEvent, EVENT_SELECT_ALL_SHAPES = NewEvent()
CopyShapesEvent,      EVENT_COPY_SHAPES       = NewEvent()
PasteShapesEvent,     EVENT_PASTE_SHAPES      = NewEvent()
CutShapesEvent,       EVENT_CUT_SHAPES        = NewEvent()
UndoEvent,            EVENT_UNDO              = NewEvent()
RedoEvent,            EVENT_REDO              = NewEvent()

AddPyutDiagramEvent, EVENT_ADD_PYUT_DIAGRAM = NewEvent()
AddOglDiagramEvent,  EVENT_ADD_OGL_DIAGRAM  = NewEvent()


class EventType(str, Enum):
    """
    UpdateApplicationTitleEvent
        Updates the application title
        parameters:
            newFilename: str
            currentFrameZoomFactor : float
            projectModified : bool

    RemoveDocumentEvent
        Removes the currently selected document

    InsertProjectEvent
        parameter:
            projectFilename:  Fully qualified name

    NewDiagramEvent
        Creates a new diagram on the current project
        parameter:
            diagramType:   A value from the DiagramType enumeration

    Events with no parameters get stuffed into the enumeration as instances, so they can be used
    event engine simple send method;  To simplify enumeration creation I create instances for all
    event types
    """

    commandEvent:  CommandEvent
    pyEventBinder: PyEventBinder

    def __new__(cls, title: str, commandEvent: CommandEvent, binder: PyEventBinder) -> 'EventType':
        obj = str.__new__(cls, title)
        obj._value_ = title

        obj.commandEvent  = commandEvent
        obj.pyEventBinder = binder
        return obj

    NewProject              = ('NewProject',              NewProjectEvent(),              EVENT_NEW_PROJECT)
    NewDiagram              = ('NewDiagram',              NewDiagramEvent(),              EVENT_NEW_DIAGRAM)
    DeleteDiagram           = ('DeleteDiagram',           DeleteDiagramEvent(),           EVENT_DELETE_DIAGRAM)
    OpenProject             = ('OpenProject',             OpenProjectEvent(),             EVENT_OPEN_PROJECT)
    InsertProject           = ('InsertProject',           InsertProjectEvent(),           EVENT_INSERT_PROJECT)
    SaveProject             = ('SaveProject',             SaveProjectEvent(),             EVENT_SAVE_PROJECT)
    SaveProjectAs           = ('SaveProjectAs',           SaveProjectAsEvent(),           EVENT_SAVE_PROJECT_AS)
    CloseProject            = ('CloseProject',            CloseProjectEvent(),            EVENT_CLOSE_PROJECT)
    UpdateTreeItemName      = ('UpdateTreeItemName',      UpdateTreeItemNameEvent(),      EVENT_UPDATE_TREE_ITEM_NAME)
    UpdateApplicationTitle  = ('UpdateApplicationTitle',  UpdateApplicationTitleEvent(),  EVENT_UPDATE_APPLICATION_TITLE)
    UpdateApplicationStatus = ('UpdateApplicationStatus', UpdateApplicationStatusEvent(), EVENT_UPDATE_APPLICATION_STATUS)

    UpdateRecentProjects    = ('UpdateRecentProjects', UpdateRecentProjectsEvent(), EVENT_UPDATE_RECENT_PROJECTS)

    UMLDiagramModified      = ('UMLDiagramModified',   UMLDiagramModifiedEvent(),   EVENT_UML_DIAGRAM_MODIFIED)

    SelectAllShapes = ('SelectAllShapes', SelectAllShapesEvent(), EVENT_SELECT_ALL_SHAPES)
    CopyShapes      = ('CopyShapes',      CopyShapesEvent(),      EVENT_COPY_SHAPES)
    PasteShapes     = ('PasteShapes',     PasteShapesEvent(),     EVENT_PASTE_SHAPES)
    CutShapes       = ('CutShapes',       CutShapesEvent(),       EVENT_CUT_SHAPES)
    Undo            = ('Undo',            UndoEvent(),            EVENT_UNDO)
    Redo            = ('Redo',            RedoEvent(),            EVENT_REDO)

    AddPyutDiagram = ('AddPyutDiagram', AddPyutDiagramEvent(), EVENT_ADD_PYUT_DIAGRAM)
    AddOglDiagram  = ('AddOglDiagram',  AddOglDiagramEvent(),  EVENT_ADD_OGL_DIAGRAM)

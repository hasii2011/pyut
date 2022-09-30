
from enum import Enum

from wx import CommandEvent
from wx import PyEventBinder

from wx.lib.newevent import NewEvent

#
# Constructor return Tuple; First is the event,  The second is the binder
#
NewProjectEvent,              EVENT_NEW_PROJECT               = NewEvent()
NewDocumentEvent,             EVENT_NEW_DOCUMENT              = NewEvent()
RemoveDocumentEvent,          EVENT_REMOVE_DOCUMENT           = NewEvent()
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

    """

    commandEvent:  CommandEvent
    pyEventBinder: PyEventBinder

    def __new__(cls, title: str, commandEvent: CommandEvent, binder: PyEventBinder) -> 'EventType':
        obj = str.__new__(cls, title)
        obj._value_ = title

        obj.commandEvent  = commandEvent
        obj.pyEventBinder = binder
        return obj

    NewProject              = ('NewProject',              NewProjectEvent,              EVENT_NEW_PROJECT)
    NewDocument             = ('NewDocument',             NewDocumentEvent,             EVENT_NEW_DOCUMENT)
    RemoveDocument          = ('RemoveDocument',          RemoveDocumentEvent,          EVENT_REMOVE_DOCUMENT)
    OpenProject             = ('OpenProject',             OpenProjectEvent,             EVENT_OPEN_PROJECT)
    InsertProject           = ('InsertProject',           InsertProjectEvent,           EVENT_INSERT_PROJECT)
    SaveProject             = ('SaveProject',             SaveProjectEvent,             EVENT_SAVE_PROJECT)
    SaveProjectAs           = ('SaveProjectAs',           SaveProjectAsEvent,           EVENT_SAVE_PROJECT_AS)
    CloseProject            = ('CloseProject',            CloseProjectEvent,            EVENT_CLOSE_PROJECT)
    UpdateTreeItemName      = ('UpdateTreeItemName',      UpdateTreeItemNameEvent,      EVENT_UPDATE_TREE_ITEM_NAME)
    UpdateApplicationTitle  = ('UpdateApplicationTitle',  UpdateApplicationTitleEvent,  EVENT_UPDATE_APPLICATION_TITLE)
    UpdateApplicationStatus = ('UpdateApplicationStatus', UpdateApplicationStatusEvent, EVENT_UPDATE_APPLICATION_STATUS)

    UpdateRecentProjects    = ('UpdateRecentProjects', UpdateRecentProjectsEvent, EVENT_UPDATE_RECENT_PROJECTS)

    UMLDiagramModified      = ('UMLDiagramModified',   UMLDiagramModifiedEvent,   EVENT_UML_DIAGRAM_MODIFIED)

    SelectAllShapes = ('SelectAllShapes', SelectAllShapesEvent, EVENT_SELECT_ALL_SHAPES)
    CopyShapes      = ('CopyShapes',      CopyShapesEvent,      EVENT_COPY_SHAPES)
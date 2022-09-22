
from enum import Enum

from wx import CommandEvent
from wx import PyEventBinder

from wx.lib.newevent import NewEvent

#
# Constructor return Tuple; First is the event,  The second is the binder
#
NewProjectEvent,             EVENT_NEW_PROJECT              = NewEvent()
NewDocumentEvent,            EVENT_NEW_DOCUMENT             = NewEvent()
LoadProjectEvent,            EVENT_LOAD_PROJECT             = NewEvent()
UpdateTreeItemNameEvent,     EVENT_UPDATE_TREE_ITEM_NAME    = NewEvent()
UpdateApplicationTitleEvent, EVENT_UPDATE_APPLICATION_TITLE = NewEvent()


class EventType(str, Enum):
    """
    UpdateApplicationTitleEvent
        parameters:
            newFilename: str
            currentFrameZoomFactor : float
            projectModified : bool
    """

    commandEvent:  CommandEvent
    pyEventBinder: PyEventBinder

    def __new__(cls, title: str, commandEvent: CommandEvent, binder: PyEventBinder) -> 'EventType':
        obj = str.__new__(cls, title)
        obj._value_ = title

        obj.commandEvent  = commandEvent
        obj.pyEventBinder = binder
        return obj

    NewProject             = ('NewProject',             NewProjectEvent,             EVENT_NEW_PROJECT)
    NewDocument            = ('NewDocument',            NewDocumentEvent,            EVENT_NEW_DOCUMENT)
    LoadProject            = ('LoadProjectEvent',       LoadProjectEvent,            EVENT_LOAD_PROJECT)
    UpdateTreeItemName     = ('UpdateTreeItemName',     UpdateTreeItemNameEvent,     EVENT_UPDATE_TREE_ITEM_NAME)
    UpdateApplicationTitle = ('UpdateApplicationTitle', UpdateApplicationTitleEvent, EVENT_UPDATE_APPLICATION_TITLE)


from wx.lib.newevent import NewEvent

#
# Constructor return Tuple; First is the event,  The second is the binder
#
NewProjectEvent,         EVENT_NEW_PROJECT           = NewEvent()
LoadProjectEvent,        EVENT_LOAD_PROJECT          = NewEvent()
UpdateTreeItemNameEvent, EVENT_UPDATE_TREE_ITEM_NAME = NewEvent()

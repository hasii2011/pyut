
from wx.lib.newevent import NewEvent

ShapeSelectedEvent,   EVT_SHAPE_SELECTED   = NewEvent()
CutOglClassEvent,     EVT_CUT_OGL_CLASS    = NewEvent()
ProjectModifiedEvent, EVT_PROJECT_MODIFIED = NewEvent()

RequestLollipopLocationEvent, EVT_REQUEST_LOLLIPOP_LOCATION = NewEvent()
CreateLollipopInterfaceEvent, EVT_CREATE_LOLLIPOP_INTERFACE = NewEvent()

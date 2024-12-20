

from dataclasses import dataclass
from dataclasses import field

from pyut.ui.eventengine.inspector.EventSender import EventSendersMap
from pyut.ui.eventengine.inspector.EventSender import createEventSendersFactory

from pyut.ui.eventengine.inspector.RegisteredListener import RegisteredListenerMap
from pyut.ui.eventengine.inspector.RegisteredListener import createRegisteredListenersMapFactory


@dataclass
class EventEngineDiagnostics:
    registeredListenersMap: RegisteredListenerMap = field(default_factory=createRegisteredListenersMapFactory)
    eventSendersMap:        EventSendersMap       = field(default_factory=createEventSendersFactory)

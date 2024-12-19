
from typing import Dict
from typing import List
from typing import NewType

from dataclasses import dataclass

from pyut.ui.eventengine.EventType import EventType

RegisteredBy = NewType('RegisteredBy', str)
EventHandler = NewType('EventHandler', str)


@dataclass
class RegisteredListener:
    """
    This data class necessary since we do not have access to the wxPython event table
    """
    eventType:    EventType    = EventType.NOT_SET
    eventHandler: EventHandler = EventHandler('')


RegisteredListeners   = NewType('RegisteredListeners',   List[RegisteredListener])
RegisteredListenerMap = NewType('RegisteredListenerMap', Dict[RegisteredBy, RegisteredListeners])


def createRegisteredListenersMapFactory() -> RegisteredListenerMap:
    return RegisteredListenerMap({})

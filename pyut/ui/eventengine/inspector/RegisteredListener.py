from dataclasses import field
from typing import Dict
from typing import List
from typing import NewType

from dataclasses import dataclass

from pyut.ui.eventengine.EventType import EventType

EventSender = NewType('EventSender', str)
CallCount   = NewType('CallCount',   Dict[EventSender, int])


def createCallCountFactor() -> CallCount:
    return CallCount({})


@dataclass
class RegisteredListener:
    """
    This data class necessary since we do not have access to the wxPython

    """
    eventType:    EventType = EventType.NOT_SET
    registeredBy: str       = ''
    eventHandler:     str       = ''
    callCount:    CallCount = field(default_factory=createCallCountFactor)


RegisteredListeners = NewType('RegisteredListeners', List[RegisteredListener])

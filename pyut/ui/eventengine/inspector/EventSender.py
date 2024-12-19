
from typing import Dict
from typing import List
from typing import NewType

from dataclasses import dataclass

from pyut.ui.eventengine.EventType import EventType

SenderName = NewType('SenderName', str)


@dataclass
class EventSender:
    senderName: SenderName = SenderName('')
    callCount:  int        = 0


EventSenders    = NewType('EventSenders',    List[EventSender])
EventSendersMap = NewType('EventSendersMap', Dict[EventType, EventSenders])


def createEventSendersFactory() -> EventSendersMap:
    return EventSendersMap({})

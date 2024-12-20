
from logging import Logger
from logging import getLogger
from typing import Callable
from typing import cast

from wx import PyEventBinder

from pyut.ui.eventengine.EventType import EventType

from pyut.ui.eventengine.inspector.EventEngineDiagnostics import EventEngineDiagnostics
from pyut.ui.eventengine.inspector.EventSender import EventSender
from pyut.ui.eventengine.inspector.EventSender import EventSenders
from pyut.ui.eventengine.inspector.EventSender import EventSendersMap
from pyut.ui.eventengine.inspector.EventSender import SenderName
from pyut.ui.eventengine.inspector.Inspector import Inspector
from pyut.ui.eventengine.inspector.RegisteredListener import EventHandler
from pyut.ui.eventengine.inspector.RegisteredListener import RegisteredBy
from pyut.ui.eventengine.inspector.RegisteredListener import RegisteredListener
from pyut.ui.eventengine.inspector.RegisteredListener import RegisteredListenerMap
from pyut.ui.eventengine.inspector.RegisteredListener import RegisteredListeners

INSPECTOR_SKIP_DEPTH: int = 3


class EventEngineDebugger:
    """
    Isolate this code outside the event engine
    """
    def __init__(self):
        self._logger: Logger = getLogger(__name__)

        self._eventEngineDiagnostics: EventEngineDiagnostics = EventEngineDiagnostics()

    @property
    def eventEngineDiagnostics(self) -> EventEngineDiagnostics:
        return self._eventEngineDiagnostics

    def makeListenerEntry(self, callback: Callable, pyEventBinder: PyEventBinder):
        """

        Args:
            callback:
            pyEventBinder:

        """
        from pyut.ui.eventengine.inspector.Inspector import Inspector

        cbStr:  str = callback.__qualname__
        typeId: int = pyEventBinder.typeId
        self._logger.debug(f'{cbStr=} {typeId=}')
        eventType: EventType = EventType(typeId)

        registeredListener: RegisteredListener = RegisteredListener()
        registeredListener.eventHandler = EventHandler(cbStr)
        registeredListener.eventType    = eventType

        # 1 for us, 1 for the caller of this method, 1 for the caller
        registeredBy: RegisteredBy = RegisteredBy(Inspector.getCallerName(skip=INSPECTOR_SKIP_DEPTH))

        registeredListenerMap: RegisteredListenerMap = self._eventEngineDiagnostics.registeredListenersMap

        self._logger.debug(f'{registeredBy=}')

        if registeredBy in registeredListenerMap:
            registeredListeners: RegisteredListeners = registeredListenerMap[registeredBy]
        else:
            registeredListeners = RegisteredListeners([])

        registeredListeners.append(registeredListener)
        registeredListenerMap[registeredBy] = registeredListeners

        self._eventEngineDiagnostics.registeredListenersMap = registeredListenerMap

        # self._logger.debug(f'{self._eventEngineDiagnostics}')

    def updateListenerStatistics(self, eventType: EventType):

        senderName: SenderName = SenderName(Inspector.getCallerName(skip=INSPECTOR_SKIP_DEPTH))

        eventSendersMap: EventSendersMap = self._eventEngineDiagnostics.eventSendersMap

        # find the senders of a specific event
        if eventType in eventSendersMap:
            eventSenders:  EventSenders = eventSendersMap[eventType]
        else:
            eventSenders = EventSenders([])

        foundSender: EventSender = cast(EventSender, None)

        for sender in eventSenders:
            eventSender: EventSender = cast(EventSender, sender)
            if eventSender.senderName == senderName:
                foundSender = eventSender
                break

        if foundSender is None:
            newSender: EventSender = EventSender(senderName=senderName, callCount=1)
            eventSendersMap[eventType] = EventSenders([newSender])
        else:
            foundSender.callCount += 1

        self._logger.debug(f'{eventSendersMap=}')

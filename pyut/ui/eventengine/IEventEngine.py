
from typing import Callable

from abc import ABC
from abc import abstractmethod

from wx import PyEventBinder

from pyut.ui.eventengine.EventType import EventType
from pyut.ui.eventengine.inspector.EventEngineDiagnostics import EventEngineDiagnostics


class IEventEngine(ABC):
    """
    Implement an interface using standard Python library.  I found zope too abstract
    and python interface could not handle subclasses
    """
    @abstractmethod
    def registerListener(self, pyEventBinder: PyEventBinder, callback: Callable):
        pass

    @abstractmethod
    def sendEvent(self, eventType: EventType, **kwargs):
        pass

    @property
    @abstractmethod
    def eventEngineDiagnostics(self) -> EventEngineDiagnostics:
        pass

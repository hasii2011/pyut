from typing import Callable

from wx import Point
from wx import PyEventBinder

from org.pyut.miniogl.Shape import Shape

from abc import ABC
from abc import abstractmethod


class IEventEngine(ABC):
    """
    Implement an interface using standard Python library.  I found zope to abstract
    and python interface could not handle subclasses
    """
    @abstractmethod
    def registerListener(self, event: PyEventBinder, callback: Callable):
        pass

    @abstractmethod
    def sendSelectedShapeEvent(self, shape: Shape, position: Point):
        pass

    @abstractmethod
    def sendCutShapeEvent(self, shapeToCut: Shape):
        pass

    @abstractmethod
    def sendRequestLollipopLocationEvent(self, requestShape: Shape):
        pass

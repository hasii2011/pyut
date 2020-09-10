
from typing import Dict
from typing import Any
from typing import Union

from org.pyut.general.Singleton import Singleton


class IDFactory(Singleton):
    """
    Type hinting results in self-documenting code. I really prefer and evangelize it.

    A user-defined class or class object is an instance of the object named `type`, which is itself a `class`. Classes
    are created from `type`, or in other words:

    >   A class is an instance of the class `type`.  In Python 3 there is no difference between `classes` and `types`
    """
    nextID: int = 1

    def init(self):
        """
        The singleton initialization method
        """
        self._classCache: Dict[type, int] = {}

    def getID(self, cls: Union[Any, type]):
        if cls in self._classCache:
            return self._classCache[cls]
        else:
            clsId = IDFactory.nextID
            self._classCache[cls] = clsId
            IDFactory.nextID += 1
            return clsId

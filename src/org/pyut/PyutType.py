
from FlyweightString import FlyweightString


class PyutType:
    """
    Type of a field.
    """
    def __init__(self, value=''):
        self._value = value

    def __str__(self) -> str:
        """
        String representation.
        """
        return self._value

    def __repr__(self) -> str:
        return self.__str__()

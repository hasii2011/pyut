
class PyutType:
    """
    This class defines a field type or a method return type
    """
    def __init__(self, value=''):
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, theNewValue: str):
        raise NotImplementedError('PyutType is read-only once constructed')

    def __str__(self) -> str:
        """
        String representation.
        """
        return self._value

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, PyutType):
            if self._value == other._value:
                return True
            else:
                return False
        else:
            return False


class PyutType:
    """
    Type of a field or the return type for a method
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

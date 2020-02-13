
class PyutType:
    """
    Type of a field.
    """
    def __init__(self, value=''):
        self._value = value

    def getValue(self) -> str:
        return self._value

    def setValue(self, theNewValue: str):
        raise NotImplementedError('PyutType is read-only once constructed')

    value = property(getValue, setValue)

    def __str__(self) -> str:
        """
        String representation.
        """
        return self._value

    def __repr__(self) -> str:
        return self.__str__()


from FlyweightString import FlyweightString


class PyutType(FlyweightString):
    """
    Type of a field.
    See `FlyweightString.py` for an explanation of the Flyweight pattern.
    A pyut type is an immutable string, like "int", "float"...
    """
    def init(self, value=''):
        super().init(name=value)
        self._value = value

    def __str__(self):
        """
        String representation.

        @return type : string
        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        # return self.getName()
        return self._value

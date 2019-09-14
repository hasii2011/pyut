
from FlyweightString import *


def getPyutType(name):
    """
    Factory method to return a new or existing PyutType for the given name.

    @deprecated use `PyutType` constructor directly.
    @param String name : name of the type
    @return PyutType : a PyutType object for the given type name
    @author Laurent Burgbacher <lb@alawa.ch>
    """
    return PyutType(name)


class PyutType(FlyweightString):
    def __init__(self, value):
        self._value = value

    """
    Type of a field.
    See `FlyweightString.py` for an explanation of the Flyweight pattern.
    A pyut type is an immutable string, like "int", "float"...

    :author: Laurent Burgbacher
    :contact: <lb@alawa.ch>
    :version: $Revision: 1.4 $
    """
    def __str__(self):
        """
        String representation.

        @return type : string
        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        # return self.getName()
        return self._value


def main():
    a = PyutType("salut")
    b = PyutType("salut")
    c = PyutType("autre")
    d = PyutType("autre")
    #print repr(a), a
    #print repr(b), b
    #print repr(c), c
    #print repr(d), d
    del a
    del b
    a = PyutType("salut")
    b = PyutType("toto")

    #print repr(a), a
    #print repr(b), b
    #print repr(c), c
    #print repr(d), d

    del b

    keys = a.getAllFlies()

    assert 'autre' in keys
    assert 'salut' in keys
    print("FlyweightString working")


if __name__ == "__main__": main()

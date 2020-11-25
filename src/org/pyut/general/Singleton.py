from types import MethodType


class Singleton(object):
    """
    Base class for singleton classes.

    Any class derived from this one is a singleton. You can call its
    constructor multiple times, you'll get only one instance.

    Note that `__init__` must not be defined. Use `init` instead.
    This is because `__init__` will always be called, thus reinitializing the
    state of your singleton each time you try to instantiate it.
    On the contrary, `init` will be called just one time.

    To be sure that the `__init__` method won't be inadvertently defined,
    the singleton will check for it at first instantiation and raise an
    `AssertionError` if it finds it.

    Example::

        # This class is OK
        class A(Singleton):
            def init(self, theNewValue):
                self.theNewValue = theNewValue

        # This class will raise AssertionError at first instantiation, because
        # of the __init__ method.
        class B(Singleton):
            def __init__(self, theNewValue):
                self.theNewValue = theNewValue
    """
    def __new__(cls, *args, **kwds):
        """
        New operator of a singleton class.
        Will return the only instance, or create it if needed.

        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        instance = cls.__dict__.get("__instance__")
        if instance is None:
            instance = object.__new__(cls)
            assert type(instance.__init__) != MethodType, f"Error, your singleton class {cls} cannot contain a __init__ method."
            try:
                instance.init(*args, **kwds)
            except Exception as e:
                raise e
            cls.__instance__ = instance
        return instance

    def init(self, *args, **kwds):
        """
        Constructor of a singleton class.

        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        pass


from weakref import WeakValueDictionary


class FlyweightString:
    """
    This class instantiates flyweight objects.

    Basically, when you have to manage a lot of identical objects, you can make
    them immutable, keep them in a pool, and have only one instance of each
    possible kind. Then, when you try to instantiate an object whose state
    already exist, you get it from the pool. This is called a Flyweight.
    See Design Patterns for more information.

    Like for the singleton (see `singleton.py`), you can't use the standard
    `__init__` method.

    To be sure that the `__init__` method won't be inadvertently defined,
    the singleton will check for it at first instantiation and raise an
    `AssertionError` if it finds it.

    Examples of `FlyweightString` in Pyut are `PyutType` (there will probably
    be a lot of `int` `PyutType` objects...), `PyutStereotype`,
    `PyutModifier`, `PyutVisibility`

    :author: Laurent Burgbacher
    :contact: <lb@alawa.ch>
    :version: $Revision: 1.3 $
    """
    __instances = WeakValueDictionary()

    def __new__(cls, name=""):
        ref = None  # we need a ref if we must create the object
        if name not in cls.__instances.keys():
            # ref = object.__new__(cls, name)
            ref = object.__new__(cls)
            # assert type(ref.__init__) != MethodType, f"Error, your flyweight class {cls} cannot contain a __init__ "  "method."
            try:
                ref.init(name)
            except Exception as e:
                raise e
            ref.init(name)
            cls.__instances[name] = ref

        return cls.__instances[name]

    def init(self, name=""):
        """

        Args:
            name: String for the type

        """
        self.__name = name

    def getName(self):
        """
        Get method, used to know the name.

        @return string name
        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        return self.__name

    def getAllFlies(self):
        """
        Return a list of names of the objects existing at this time.

        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        keys = []
        for k, v in list(FlyweightString.__instances.items()):
            keys.append(k)
        return keys

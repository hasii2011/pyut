#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.3 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2001-11-14"

#from PyutUnmutableObject import *
import weakref
from types import MethodType

class FlyweightString(object):
    """
    This class instanciates flyweight objects.

    Basically, when you have to manage a lot of identical objects, you can make
    them unmutable, keep them in a pool, and have only one instance of each
    possible kind. Then, when you try to instantiate an object whose state
    already exist, you get it from the pool. This is called a Flyweight.
    See Design Patterns for more information.

    Like for the singleton (see `singleton.py`), you can't use the standard
    `__init__` method.

    To be sure that the `__init__` method won't be inadvertantly defined,
    the singleton will check for it at first instanciation and raise an
    `AssertionError` if it finds it.

    Examples of `FlyweightString` in Pyut are `PyutType` (there will probably
    be a lot of `int` `PyutType` objects...), `PyutStereotype`,
    `PyutModifier`, `PyutVisibility`

    :author: Laurent Burgbacher
    :contact: <lb@alawa.ch>
    :version: $Revision: 1.3 $
    """
    __instances = weakref.WeakValueDictionary()
    def __new__(cls, name=""):
        ref = None # we need a ref if we must create the object
        if name not in cls.__instances.keys():
            ref = object.__new__(cls, name)
            assert type(ref.__init__) != MethodType, \
                "Error, your flyweight class %s cannot contain a __init__ " \
                "method." % cls
            try:
                ref.init(name)
            except:
                raise
            ref.init(name)
            cls.__instances[name] = ref

        return cls.__instances[name]

    #>------------------------------------------------------------------------

    def init(self, name=""):
        """
        Constructor.

        @param String for the type
        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        self.__name = name
        #PyutUnmutableObject.__init__(self, name)

    #>------------------------------------------------------------------------

    def getName(self):
        """
        Get method, used to know the name.

        @return string name
        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        return self.__name

    #>------------------------------------------------------------------------

    def getAllFlies(self):
        """
        Return a list of names of the objects existing at this time.

        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        return FlyweightString.__instances.keys()

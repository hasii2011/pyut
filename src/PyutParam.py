#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.4 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2001-11-21"

from PyutObject      import *
from PyutType        import *
from types           import *

class PyutParam(PyutObject):
    """
    Parameter.
    @version $Revision: 1.4 $
    """

    def __init__(self, name="", type="", defaultValue=None):
        """
        Constructor with name and type.

        @param string name : init name with the name
        @param PyutType type : the param type
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        try:
            #import pychecker.checker
            #PyutObject.__init__(PyutObject(self), name)
            PyutObject.__init__(self, name)
        except:
            import sys, traceback
            print sys.exc_info()[0]
            print sys.exc_info()[1]
            for el in traceback.extract_tb(sys.exc_info()[2]):
                print str(el)
            print "==========================================="

            
            
        self._type = getPyutType(type)
        self._defaultValue = defaultValue

    #>------------------------------------------------------------------------

    def __str__(self):
        """
        Get method, used to know the name.

        @return string param
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        @modified L. Burgbacher <lb@alawa.ch>
            don't put the : if there's no type defined
        """
        s = self.getName()

        if str(self._type) != "":
            s += " : " + str(self._type)

        if self._defaultValue is not None:
            s += " = " + self._defaultValue

        return s

    #>------------------------------------------------------------------------

    def getType(self):
        """
        Get method, used to know the type.

        @return PyutType type
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        return self._type

    #>------------------------------------------------------------------------

    def setType(self, theType):
        """
        Set method, used to know initialize type.

        @param PyutType type
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        if type(theType) == StringType or type(theType) == UnicodeType:
            theType = getPyutType(theType)
        self._type = theType

    #>------------------------------------------------------------------------

    def getDefaultValue(self):
        """
        Get method, used to know the defaultValue.

        @return string defaultValue
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        return self._defaultValue

    #>------------------------------------------------------------------------

    def setDefaultValue(self, defaultValue):
        """
        Set method, used to know initialize defaultValue.

        @param string defaultValue
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        self._defaultValue = defaultValue

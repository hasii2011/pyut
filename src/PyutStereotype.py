#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.4 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2001-11-14"

from FlyweightString import *

def getPyutStereotype(name):
    """
    Factory method to return a new or existing PyutStereotype for the given 
    name.

    @param String name : name of the stereotype
    @return PyutType : a PyutStereotype object for the given type name
    @author Laurent Burgbacher <lb@alawa.ch>
    """
    return PyutStereotype(name)


class PyutStereotype:#(FlyweightString):
    """
    Stereotype for a class, a link

    @version $Revision: 1.4 $
    """
    def __str__(self):
        """
        String representation.

        @return type : string
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        return "<< %s >>" % (self.getName())

    #>------------------------------------------------------------------------

    def getStereotype(self):
        """
        Get method, used to know the stereotype.

        @return string name
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        return self.getName()

    #>------------------------------------------------------------------------

    def __init__(self, name=""):
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


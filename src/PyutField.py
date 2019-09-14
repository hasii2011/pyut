#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.3 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2001-11-21"

from PyutParam import PyutParam
from PyutVisibility import * 
from types import *

class PyutField(PyutParam):
    """
    Field of a class.

    A PyutField represents a UML field in a Class of Pyut program
        - father (`PyutParam`)
        - field  visibility 

    Example::
        myField = PyutField("aField", "integer", "55")

    :version: $Revision: 1.3 $
    :author:  Deve Roux 
    :contact: droux@eivd.ch 
    """

    def __init__(self, name="", type="", defaultValue=None, visibility="-"):
        """
        Constructor.

        @param string name : init name with the name
        @param string type : the param type
        @defaultValue string 
        @visibility   string : "+", "-", "#"
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        PyutParam.__init__(self, name, type, defaultValue)
        self._visibility = getPyutVisibility(visibility)

    #>------------------------------------------------------------------------

    def __str__(self):
        """
        Get method, used to know the name and visibility.

        @return string field 
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        return str(self._visibility) + PyutParam.__str__(self)

    #>------------------------------------------------------------------------

    def getVisibility(self):
        """
        Get Visibility, used to know the visibility ("+", "-", "#").

        @return PyutVisibility
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        return self._visibility

    #>------------------------------------------------------------------------

    def setVisibility(self, visibility):
        """
        Set method, used to change the visibility.

        @param string visibility
        @param PyutVisibility visibility
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        if type(visibility) == StringType or type(visibility) == UnicodeType:
            visibility = getPyutVisibility(visibility)
        self._visibility = visibility

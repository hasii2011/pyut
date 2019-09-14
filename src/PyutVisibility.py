#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.5 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2001-11-21"

from FlyweightString import *

def getPyutVisibility(name):
    """
    Factory method to return a new or existing PyutVisibility for the given
    name.

    @param String name : name of the visibility (normaly "-", "#", "+")
    @return PyutVisibility : a PyutVisibility object for the given type name
    @author Laurent Burgbacher <lb@alawa.ch>
    """
    if name=="public": name="+"
    if name=="Public": name="+"
    if name=="PUBLIC": name="+"
    if name=="private": name="-"
    if name=="Private": name="-"
    if name=="PRIVATE": name="-"
    if name=="protected": name="#"
    if name=="Protected": name="#"
    if name=="PROTECTED": name="#"
    return PyutVisibility(name)



class PyutVisibility:#(FlyweightString):

    def __init__(self, value):
        self._value = value

    """
    Visibility of a field or method.
    Use one of ("-", "#", "+").

    :author: Laurent Burgbacher
    :contact: <lb@alawa.ch>
    :version: $Revision: 1.5 $
    """
    def __str__(self):
        """
        Get method, used to know the name.

        @return string field 
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        #return self.getName()
        return self._value

    #>------------------------------------------------------------------------

    def getVisibility(self):
        """
        Get Visibility, used to know the visibility ("+", "-", "#").

        @return string type
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        #return self.getName()
        return self._value

    #>------------------------------------------------------------------------

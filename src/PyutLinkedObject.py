#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.6 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2001-12-05"

from PyutObject      import PyutObject
#from wxPython.wx     import True, False
#from types           import *

class PyutLinkedObject(PyutObject):
    """
    An object which can be connected to other one.
    This class provides all support for link management in data layer. All
    classes that may be interconnected (classes for examples) should inherate
    this class to have all links support.

    :version: $Revision: 1.6 $
    :author: Philippe Waelti
    :contact: pwaelti@eivd.ch
    """


    def __init__(self, name=""):
        """
        Constructor.

        @param string name : object name
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        PyutObject.__init__(self, name)

        

        self._links = []
        self._fathers = []
        self._filename = ""


    #>------------------------------------------------------------------------

    def getNextSafeID(self):
        """
        Get the next safe id

        @author C.Dutoit
        """
        # Verify that next id is not already used
        while self.isIDUsed(PyutLinkedObject.nextId):
            PyutLinkedObject.nextId+=1

    #>------------------------------------------------------------------------

    def __getstate__(self):
        """
        For deepcopy operations, tells which fields to avoid copying.
        Deepcopy must not copy the links to other classes, or it would result
        in copying all the diagram.

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        dict = self.__dict__.copy()
        dict["_links"] = []
        return dict

    #>------------------------------------------------------------------------

    def getLinks(self):
        """
        Return a list of the links.
        This is not a copy, but the original one. Any change made to it is
        directly made on the class.

        @since 1.1
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        return self._links

    #>------------------------------------------------------------------------

    def setLinks(self, links):
        """
        Replace the actual links by those given in the list.
        The methods passed are not copied, but used directly.

        @since 1.1
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        self._links = links

    #>------------------------------------------------------------------------

    def addLink(self, link):
        """
        Add the given link to the links

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        self._links.append(link)

    #>------------------------------------------------------------------------

    def getFathers(self):
        """
        Return a list of the fathers. 
        This is not a copy, but the original one. Any change made to it is
        directly made on the class.

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        return self._fathers

    #>------------------------------------------------------------------------

    def setFathers(self, fathers):
        """
        Replace the actual fathers by those given in the list.
        The methods passed are not copied, but used directly.

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        self._fathers = fathers

    #>------------------------------------------------------------------------

    def addFather(self, father):
        """
        Add a father in a fathers list

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        return self._fathers.append(father)

    #>------------------------------------------------------------------------

    def setFilename(self, filename):
        """
        Set the associated filename.
        This is used by the reverse engineering plugins.

        @param String filename
        @since 1.0
        """
        self._filename = filename

    #>------------------------------------------------------------------------

    def getFilename(self):
        """
        Get the associated filename.
        "" is returned if there's no filename.

        @return String
        @since 1.0
        """
        return self._filename

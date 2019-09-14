#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.7 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2001-12-05"

from PyutLinkedObject import *
from types            import *
from PyutStereotype   import *
#import wx

class PyutClass(PyutLinkedObject):
    """
    A standard class representation.

    A PyutClass represents a UML class in Pyut. It manages its:
        - object data fields (`PyutField`)
        - methods (`PyutMethod`)
        - fathers (`PyutClass`)(classes from which this one inherits)
        - stereotype (`PyutStereotype`)
        - a description (`string`)

    Example::
        myClass = PyutClass("Foo") # this will create a `Foo` class
        myClass.setDescription("Example class")
        fields = myClass.getFields() # this is the original fields []
        fields.append(PyutField("bar", "int"))

    :version: $Revision: 1.7 $
    :author: Laurent Burgbacher
    :contact: lb@alawa.ch
    """

    def __init__(self, name=""):
        """
        Constructor.

        @param string name : class name
        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        PyutLinkedObject.__init__(self, name)
        self._fields = []
        self._methods = []
        self._description = ""
        self._stereotype = None

        # Display properties
        self._showStereotype = True
        self._showMethods = True
        self._showFields = True

    #>------------------------------------------------------------------------

    def __getstate__(self):
        """
        For deepcopy operations, tells which fields to avoid copying.
        Deepcopy must not copy the links to other classes, or it would result
        in copying all the diagram.

        @since 1.5
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        dict = self.__dict__.copy()
        dict["_fathers"]    = []
        return dict

    #>------------------------------------------------------------------------

    def __str__(self):
        """
        String representation.

        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        return _("Class : %s") % (self.getName())

    #>------------------------------------------------------------------------

    def setDescription(self, description):
        """
        Description field.
        This description may be inserted just after the class declaration when
        using python code generation, for example.

        @param String description : description string
        @since 1.15
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        self._description = description

    #>------------------------------------------------------------------------

    def getDescription(self):
        """
        Returns the description field.
        This description may be inserted just after the class declaration when
        using python code generation, for example.

        @return String : Description string
        @since 1.15
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        return self._description

    #>------------------------------------------------------------------------

    def getFields(self):
        """
        Return a list of the fields. 
        This is not a copy, but the original one. Any change made to it is
        directly made on the class.

        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        return self._fields

    #>------------------------------------------------------------------------

    def setFields(self, fields):
        """
        Replace the actual fields by those given in the list.
        The methods passed are not copied, but used directly.

        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        self._fields = fields

    #>------------------------------------------------------------------------

    def addField(self, field):
        """
        Add a field
        @author C.Dutoit
        """
        self._fields.append(field)

    #>------------------------------------------------------------------------

    def getMethods(self):
        """
        Return a list of the methods. 
        This is not a copy, but the original one. Any change made to it is
        directly made on the interface.

        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        return self._methods

    #>------------------------------------------------------------------------

    def setMethods(self, methods):
        """
        Replace the actual methods by those given in the list.
        The methods passed are not copied, but used directly.

        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        self._methods = methods

    #>------------------------------------------------------------------------

    def getStereotype(self):
        """
        Return the stereotype used, or None if there's no stereotype.

        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        return self._stereotype

    #>------------------------------------------------------------------------

    def setStereotype(self, stereotype):
        """
        Replace the actual stereotype by the one given.

        @param String or Unicode or PyutStereotype stereotype
        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        if type(stereotype) == StringType or type(stereotype) == UnicodeType:
            stereotype = getPyutStereotype(stereotype)
        self._stereotype = stereotype


    #>------------------------------------------------------------------------
    
    def getShowStereotype(self):
        """
        Return True if we must display the stereotype

        @return boolean indicating if we must display the stereotype
        @since 1.1.1.2
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        return self._showStereotype

    #>------------------------------------------------------------------------
    
    def setShowStereotype(self, value):
        """
        Define the showStereotype property

        @param value : boolean indicating if we must display the stereotype
        @since 1.1.1.2
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._showStereotype = value

    #>------------------------------------------------------------------------
    
    def getShowMethods(self):
        """
        Return True if we must display the methods

        @return boolean indicating if we must display the methods
        @since 1.1.1.2
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        return self._showMethods

    #>------------------------------------------------------------------------
    
    def setShowMethods(self, value):
        """
        Define the showMethods property

        @param value : boolean indicating if we must display the methods
        @since 1.1.1.2
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._showMethods = value

    #>------------------------------------------------------------------------
    
    def getShowFields(self):
        """
        Return True if we must display the fields

        @return boolean indicating if we must display the fields
        @since 1.1.1.2
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        return self._showFields

    #>------------------------------------------------------------------------
    
    def setShowFields(self, value):
        """
        Define the showFields property

        @param value : boolean indicating if we must display the fields
        @since 1.1.1.2
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._showFields = value


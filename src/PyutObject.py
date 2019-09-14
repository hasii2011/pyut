#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.7 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2001-11-21"

#from wxPython.wx import True, False

class PyutObject(object):
    """
    Base Object of PyutData.
    @version $Revision: 1.7 $
    """

    nextId = 0


    def __init__(self, name=""):
        """
        Constructor.

        @param string name : init name with the name
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        object.__init__(self)
        self._name = name

        # Setting an arbitrary ID, for identical name purpose
        self.getNextSafeID()
        self._id = PyutObject.nextId
        PyutObject.nextId += 1


    #>------------------------------------------------------------------------

    def getNextSafeID(self):
        """
        Get the next safe id

        @author C.Dutoit
        """
        # Verify that next id is not already used
        while self.isIDUsed(PyutObject.nextId):
            PyutObject.nextId+=1




    #>------------------------------------------------------------------------

    def isIDUsed(self, id):
        """
        Verify if an ID is already used

        @author C.Dutoit
        """
        # Verify that next id is not already used
        import mediator
        ctrl = mediator.getMediator()
        for obj in [el for el in ctrl.getUmlObjects() 
                       if isinstance(el, PyutObject)]:
            if obj.getId() == id:
                return True
        return False

    #>------------------------------------------------------------------------

    def getName(self):
        """
        Get method, used to know the name.

        @return string name
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        try:
            return self._name
        except:
            return ""

    #>------------------------------------------------------------------------

    def setName(self, name):
        """
        Set method, used to know initialize name.

        @param string name
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        self._name = name

    #>------------------------------------------------------------------------

    def setId(self, id):
        """
        Setting ID.

        @param int id : ID
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        self._id = id


    #>------------------------------------------------------------------------

    def getId(self):
        """
        Get object ID.

        @return int : ID
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        return self._id

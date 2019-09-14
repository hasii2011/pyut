#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.5 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2001-12-05"

from PyutObject      import PyutObject
from types           import *

class PyutLink(PyutObject):
    """
    A standard link between Class or Note.

    A PyutLink represents a UML link between Class in Pyut.

    Example::
        myLink  = PyutLink("linkName", 0, "0", "*")

    :version: $Revision: 1.5 $
    :author: Deve Roux
    :contact: droux@eivd.ch
    """

    def __init__(self, name="", linkType=0, cardSrc="", cardDest="",
                 bidir=0, source=None, destination=None):
        """
        Constructor.

        @param string name     : for the link name
        @param int    type     : type of link
        @param string  cardSrc : cardinality of source of link
        @param string  cardDest: cardinality of destination of link
        @param boolean bidir   : design if link is bidirational or not
        @param obj source      : source of the link
        @param obj destination : where goes the link
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        @modified Laurent Burgbacher <lb@alawa.ch>
            added source field
        """
        PyutObject.__init__(self, name)
        self._type    = linkType
        self._cardSrc = cardSrc
        self._cardDes = cardDest
        self._bidir   = bidir
        self._src     = source
        self._dest    = destination
        

    #>------------------------------------------------------------------------

    def __str__(self):
        """
        String representation.

        @return : string representing link
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        return _("(%s) links from %s to %s") % \
                (self.getName(), self._src, self._dest)


    #>------------------------------------------------------------------------

    def getSrcCard(self):
        """
        Return a string representing cardinality source. 

        @return string source cardinality
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        return self._cardSrc

    #>------------------------------------------------------------------------

    def setSrcCard(self, cardSrc):
        """
        Updating source cardinality.

        @param  string cardSrc
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        self._cardSrc = cardSrc
    
    #>------------------------------------------------------------------------

    def getDestCard(self):
        """
        Return a string representing cardinality destination. 

        @return string destination cardinality
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        return self._cardDes
    
    #>------------------------------------------------------------------------

    def setDestCard(self, cardDest):
        """
        Updating destination cardinality.

        @param string cardDest
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        self._cardDes = cardDest
    
    #>------------------------------------------------------------------------

    def getSource(self):
        """
        Return the source object of the link

        @return object Class or Note
        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        return self._src
    
    #>------------------------------------------------------------------------
    
    def setSource(self, source):
        """
        Set the source object of this link.

        @param PyutClass or PyutNote source
        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        self._src = source
   
    #>------------------------------------------------------------------------

    def getDestination(self):
        """
        Return an object destination who is linked to this link. 

        @return object Class or Note
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        return self._dest
    
    #>------------------------------------------------------------------------
    
    def setDestination(self, destination):
        """
        Updating destination.

        @param PyutClass or PyutNote destination
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        self._dest = destination
   
    #>------------------------------------------------------------------------

    def getBidir(self):
        """
        To know if the link is bidirectional.

        @return boolean
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        return self._bidir
    
    #>------------------------------------------------------------------------
    
    def setBidir(self, bidirectional):
        """
        Updating bidirectional.

        @param boolean bidirectional
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        self._bidir = bidirectional 

    #>------------------------------------------------------------------------

    def setType(self, theType):
        """
        Updating type of link.

        @param int type : Type of the link
        @since 1.2
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        if type(theType) == StringType or type(theType) == UnicodeType:
            try:
                theType = int(theType)
            except:
                theType = 0
        self._type = theType

    #>------------------------------------------------------------------------

    def getType(self):
        """
        To get the link type.

        @return int : The type of the link
        @since 1.2
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        return self._type




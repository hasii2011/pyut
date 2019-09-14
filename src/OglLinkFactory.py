#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.5 $"
__author__  = "EI5, eivd, Group Burgbacher - Waelti"
__date__    = "2001-12-12"

from __future__     import nested_scopes
from OglAggregation import *
from OglComposition import *
from OglInheritance import *
from OglInterface   import *
from OglNoteLink    import *
from OglSDMessage   import *

from singleton      import *
from PyutConsts     import *

def getOglLinkFactory():
    """
    Function to get the unique OglLinkFactory instance (singleton).

    @since 1.0
    @author P. Waelti <pwaelti@eivd.ch>
    """
    return OglLinkFactory()



def getLinkType(link):
    """
    Added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (20.11.2005)
    @return type (integer) of the link as defined in PyutConsts.py
    """
    if isinstance(link, OglAggregation):
        return OGL_AGGREGATION
    elif isinstance(link, OglComposition):
        return OGL_COMPOSITION
    elif isinstance(link, OglInheritance):
        return OGL_INHERITANCE
    elif isinstance(link, OglAssociation):
        return OGL_ASSOCIATION
    elif isinstance(link, OglInterface):
        return OGL_INTERFACE
    elif isinstance(link, OglNoteLink):
        return OGL_NOTELINK


class OglLinkFactory(Singleton):
    """
    This class is a factory to produce `OglLink` objects.
    It works under the Factory Design Pattern model. Ask a kind of link
    to this object and it will return you what you was asking for.

    :version: $Revision: 1.5 $
    :author: Philippe Waelti
    :contact: pwaelti@eivd.ch
    """
    def getOglLink(self, srcShape, pyutLink, destShape, linkType, 
                   srcPos=None, dstPos=None):
        """
        Used to get a OglLink of the given linkType.

        @param OglObject srcShape : Source shape
        @param PyutLink pyutLink : Conceptual links associated with the
                                   graphical links.
        @param OglObject destShape : Destination shape
        @param int linkType : The linkType of the link (OGL_INHERITANCE, ...)
        @param tuple srcPos, dstPos : position on both src and dst objects

        @return OglLink : The link you asked

        @author Philippe Waelti
        @modified C.Dutoit 25112002 : added OGL_SD_MESSAGE
        """
        if linkType == OGL_AGGREGATION:
            return OglAggregation(srcShape, pyutLink, destShape)

        elif linkType == OGL_COMPOSITION:
            return OglComposition(srcShape, pyutLink, destShape)

        elif linkType == OGL_INHERITANCE:
            return OglInheritance(srcShape, pyutLink, destShape)

        elif linkType == OGL_ASSOCIATION:
            return OglAssociation(srcShape, pyutLink, destShape)

        elif linkType == OGL_INTERFACE:
            return OglInterface(srcShape, pyutLink, destShape)

        elif linkType == OGL_NOTELINK:
            return OglNoteLink(srcShape, pyutLink, destShape)
        else:
            print "Unknown linkType of OglLink into factory :", repr(linkType)
            return None



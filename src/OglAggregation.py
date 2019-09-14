#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.6 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2001-11-14"

#from wxPython.wx    import *
#from wxPython.ogl   import *
#import wx
from OglAssociation import *

#>------------------------------------------------------------------------

class OglAggregation(OglAssociation):
    """
    Graphical link representation of aggregation, (empty diamond, arrow).
    To get a new link, you should use the `OglLinkFatory` and specify
    the kind of link you want, OGL_AGGREGATION for an instance of this class.

    :version: $Revision: 1.6 $
    :author: Philippe Waelti
    :contact: pwaelti@eivd.ch
    """

    def __init__(self, srcShape, pyutLink, dstShape):
        """
        Constructor.

        @param OglClass srcShape : Source shape
        @param PyutLink pyutLink : Conceptual links associated with the
                                   graphical links.
        @param OglClass destShape : Destination shape

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """

        # Init
        OglAssociation.__init__(self, srcShape, pyutLink, dstShape)

        # Adding arrows
        self.SetDrawArrow(True)


    #>------------------------------------------------------------------------

    def Draw(self, dc):#, withChildren):
        """
        Called for contents drawing of links.

        @param wxDC dc : Device context
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        # Call father
        OglAssociation.Draw(self, dc)#, withChildren)

        # Draw losange
        self.drawLosange(dc, 0)

    #>------------------------------------------------------------------------

    def cleanUp(self):
        """
        Clean up object references before quitting.

        @since 1.4
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        OglAssociation.cleanUp(self)
        self.ClearArrowsAtPosition() # remove all arrows

    #>------------------------------------------------------------------------

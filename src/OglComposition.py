#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.6 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2001-11-14"

#from wxPython.wx     import *
#from wxPython.ogl    import *
from OglAssociation  import *

#>------------------------------------------------------------------------

class OglComposition(OglAssociation):
    """
    Graphical link representation of composition, (plain diamond, arrow).
    To get a new link, you should use the `OglLinkFatory` and specify
    the kind of link you want, OGL_COMPOSITION for an instance of this class.

    :version: $Revision: 1.6 $
    :author: Philippe Waelti
    :contact: pwaelti@eivd.ch
    """

    def __init__(self, srcShape, pyutLink, dstShape):
        """
        Constructor.

        @param OglObject srcShape : Source shape
        @param PyutLinkedObject pyutLink : Conceptual links associated with the
                                           graphical links.
        @param OglObject destShape : Destination shape
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """

        # Init
        OglAssociation.__init__(self, srcShape, pyutLink, dstShape)

        # Add arrows
        #self.AddArrow(ARROW_FILLED_CIRCLE, ARROW_POSITION_START)
        #self.AddArrow(ARROW_ARROW, ARROW_POSITION_END)
        #modified by C.Dutoit : losange done in OglAssociation
        #self.AddArrow(ARROW_ARROW, ARROW_POSITION_END)
        self.SetDrawArrow(True)

        #self.startArrow = OglDiamondArrow()
        #self.endArrow = OglOpenArrow()

    #>------------------------------------------------------------------------

    #def OnDrawContents(self, dc):
    def Draw(self, dc):#, withChildren=False):
        """
        Called for contents drawing of links.

        @param wxDC dc : Device context
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        # Call father
        #OglAssociation.OnDrawContents(self, dc)
        OglAssociation.Draw(self, dc)#, withChildren)

        #self.startArrow.drawArrow(dc)
        #self.endArrow.drawArrow(dc)


        # Draw losange
        self.drawLosange(dc, 1)

    #>------------------------------------------------------------------------

    def cleanUp(self):
        """
        Clean up object references before quitting.

        @since 1.5
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        OglAssociation.cleanUp(self)
        self.ClearArrowsAtPosition() # remove all arrows

    #>------------------------------------------------------------------------

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.4 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2001-11-14"

from __future__ import nested_scopes
#from wxPython.wx import *
#from wxPython.ogl import *
from PyutLink import PyutLink
from OglClass import *
from OglLink import *
from DlgRemoveLink import *
import wx


#>------------------------------------------------------------------------

class OglInheritance(OglLink):
    """
    Graphical OGL representation of an inheritance link.
    This class provide the methods for drawing an inheritance link between
    two classes of an UML diagram. Add labels to an OglLink.

    @version $Revision: 1.4 $
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
        OglLink.__init__(self, srcShape, pyutLink, dstShape)

        # Arrow must be white inside
        self.SetBrush(wx.WHITE_BRUSH)

        # Add arrow
        #self.AddArrow(ARROW_ARROW, ARROW_POSITION_END, 15.0)
        self.SetDrawArrow(True)

    #>------------------------------------------------------------------------

    def cleanUp(self):
        """
        Clean up object references before quitting.

        @since 1.4
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        OglLink.cleanUp(self)
        self.ClearArrowsAtPosition() # remove all arrows

    #>------------------------------------------------------------------------

    def OnLeftClick(self, x, y, keys, attachment):
        """
        Event handler for left mouse click.
        This event handler call the link dialog to edit link properties.

        @param int x : X position
        @param int y : Y position
        @param int keys : ...
        @param int attachments : ...
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """

        # get the shape
        shape = self.GetShape()
        # the canvas wich contain the shape
        #canvas = shape.GetCanvas()

        # Open dialog to edit link
        dlg = DlgRemoveLink()
        rep = dlg.ShowModal()
        dlg.Destroy()
        if rep == wx.ID_YES: # destroy link
            Mediator().removeLink(self)
        self._diagram.Refresh()



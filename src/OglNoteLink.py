#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.8 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2001-11-14"

#from wxPython.wx import *
#from wxPython.ogl import *
from PyutLink import PyutLink
from OglNote import *
from OglLink import *
from DlgRemoveLink import *
import wx



#>------------------------------------------------------------------------

class OglNoteLink(OglLink):
    """
    A note like link, with dashed line and no arrows.
    To get a new link, you should use the `OglLinkFactory` and specify
    the kind of link you want, OGL_NOTELINK for an instance of this class.

    :version: $Revision: 1.8 $
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
        OglLink.__init__(self, srcShape, pyutLink, dstShape)
        self.SetDrawArrow(False)

        # Pen
        #self.SetPen(wx.BLACK_DASHED_PEN)
        self.SetPen(wx.Pen("BLACK", 1 , wx.LONG_DASH))

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

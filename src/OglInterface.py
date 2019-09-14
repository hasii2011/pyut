#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.9 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2001-11-14"

from __future__ import nested_scopes
#from wxPython.wx import *
#from wxPython.ogl import *
from PyutLink import PyutLink
from OglClass import *
from OglLink import *
from DlgRemoveLink import *

# Kind of labels
[CENTER] = range(1)

#>------------------------------------------------------------------------

class OglInterface(OglLink):
    """
    Graphical OGL representation of an interface link.
    This class provide the methods for drawing an interface link between
    two classes of an UML diagram. Add labels to an OglLink.

    @version $Revision: 1.9 $
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

        # Pen
        #self.SetPen(wx.BLACK_DASHED_PEN)
        self.SetPen(wx.Pen("BLACK", 1 , wx.LONG_DASH))

        # Arrow must be white inside
        self.SetBrush(wx.WHITE_BRUSH)

        # Add labels
        self._labels = {}

        # Initialize labels objects
        self._labels[CENTER] = self.AddText(0, 0, "")
        self.updateLabels()

        # Add arrow
        #self.AddArrow(ARROW_ARROW, ARROW_POSITION_END, 15.0)
        self.SetDrawArrow(True)


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

    #>------------------------------------------------------------------------

    def updateLabels(self):
        """
        Update the labels according to the link.

        @since 1.14
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        def prepareLabel(textShape, text):
            """
            Update a label.

            @author Laurent Burgbacher <lb@alawa.ch>
            """
            # If label should be drawn
            if text.strip() != "":
                textShape.SetText(text)
                #textShape.Show(True)
                textShape.SetVisible(True)
            else:
                #textShape.Show(False)
                textShape.SetVisible(False)

        # Prepares labels
        prepareLabel(self._labels[CENTER], self._link.getName())

    #>------------------------------------------------------------------------

    def getLabels(self):
        """
        Get the labels.

        @return TextShape []
        @since 1.0
        """
        return self._labels

    #>------------------------------------------------------------------------

    def Draw(self, dc):#, withChildren=False):
        """
        Called for contents drawing of links.

        @param wx.DC dc : Device context
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        self.updateLabels()
        OglLink.Draw(self, dc)#, withChildren)


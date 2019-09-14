#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.11 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2001-11-14"

from __future__   import division
#from wxPython.wx  import *
#from wxPython.ogl import *
import wx
from PyutLink     import PyutLink
from OglLink      import *
from DlgEditLink  import *
from math import pi, atan, cos, sin

# Kind of labels
[CENTER, SRC_CARD, DEST_CARD] = range(3)

#>------------------------------------------------------------------------

class OglAssociation(OglLink):
    """
    Graphical link representation of association, (simple line, no arrow).
    To get a new link, you should use the `OglLinkFatory` and specify
    the kind of link you want, OGL_ASSOCIATION for an instance of this class.

    :version: $Revision: 1.11 $
    :author: Philippe Waelti
    :contact: pwaelti@eivd.ch
    """

    def __init__(self, srcShape, pyutLink, dstShape):
        """
        Constructor.

        @param OglObject srcShape : Source shape
        @param PyutLink pyutLink : Conceptual links associated with the
                                   graphical links.
        @param OglObject destShape : Destination shape
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        # Init
        OglLink.__init__(self, srcShape, pyutLink, dstShape)

        # Add labels
        self._labels = {}

        # Define position
        from math import sqrt
        srcX, srcY = srcShape.GetPosition()
        dstX, dstY = dstShape.GetPosition()
        dy = dstY - srcY
        dx = dstX - srcX
        l  = sqrt(dx*dx + dy*dy)
        if l==0: l=0.01
        cenLblX = -dy*5/l
        cenLblY =  dx*5/l
        srcLblX =  20*dx/l #- dy*5/l
        srcLblY =  20*dy/l #+ dx*5/l
        dstLblX = -20*dx/l #+ dy*5/l
        dstLblY = -20*dy/l #- dy*5/l


        # Initialize labels objects
        self._labels[CENTER] = self.AddText(cenLblX, cenLblY, "")
        self._labels[SRC_CARD] = self._src.AddText(srcLblX, srcLblY, "")
        self._labels[DEST_CARD] = self._dst.AddText(dstLblX, dstLblY, "")
        self.updateLabels()
        self.SetDrawArrow(False)

        # Test
        #self.AddShape(self._labels[SRC_CARD])
        #self.AddShape(self._labels[DEST_CARD])

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
        prepareLabel(self._labels[SRC_CARD], self._link.getSrcCard())
        prepareLabel(self._labels[DEST_CARD], self._link.getDestCard())

    #>------------------------------------------------------------------------

    def getLabels(self):
        """
        Get the labels.

        @return TextShape []
        @since 1.0
        """
        return self._labels

    #>------------------------------------------------------------------------

    def Draw(self, dc):#, withChildren = False):
        """
        Called for contents drawing of links.

        @param wxDC dc : Device context
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        self.updateLabels()
        OglLink.Draw(self, dc)#, withChildren)

    #>------------------------------------------------------------------------

    def drawLosange(self, dc, filled=False):
        """
        Draw an arrow at the begining of the line.

        @param wxDC dc
        @param bool filled : True if the losange must be filled, False otherwise
        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        pi_6 = pi/6
        points = []
        line = self.GetSegments()
        x1, y1 = line[1]
        x2, y2 = line[0]
        a = x2 - x1
        b = y2 - y1
        if abs(a) < 0.01: # vertical segment
            if b > 0:
                alpha = -pi/2
            else:
                alpha = pi/2
        else:
            if a==0:
                if b>0:
                    alpha = pi/2
                else:
                    alpha = 3*pi/2
            else:
                alpha = atan(b/a)
        if a > 0:
            alpha += pi
        alpha1 = alpha + pi_6
        alpha2 = alpha - pi_6
        size = 8
        points.append((x2 + size * cos(alpha1), y2 + size * sin(alpha1)))
        points.append((x2, y2))
        points.append((x2 + size * cos(alpha2), y2 + size * sin(alpha2)))
        points.append((x2 + 2*size * cos(alpha),  y2 + 2*size * sin(alpha)))
        dc.SetPen(wx.BLACK_PEN)
        if (filled):
            dc.SetBrush(wx.BLACK_BRUSH)
        else:
            dc.SetBrush(wx.WHITE_BRUSH)
        dc.DrawPolygon(points)
        dc.SetBrush(wx.WHITE_BRUSH)

    #>------------------------------------------------------------------------

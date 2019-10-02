#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.16 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2001-11-14"

#from wxPython.wx  import *
from PyutConsts   import *
from Mediator     import *
from MiniOgl      import *
from OglLink      import *
DEBUG=False
#TODO : Find a way to report moves from AnchorPoints to PyutSDMessage
#

# Kind of labels
[CENTER, SRC_CARD, DEST_CARD] = range(3)

#>------------------------------------------------------------------------

class OglSDMessage(LineShape, ShapeEventHandler):
    """
    class for graphical message

    :version: $Revision: 1.16 $
    :author: C.Dutoit
    """

    def __init__(self, srcShape, pyutObject, dstShape):
        """
        Constructor.

        @param OglObject srcShape : Source shape
        @param OglObject destShape : Destination shape

        @author : Added srcPos and dstPos
        """
        # Init
        self._pyutObject = pyutObject
        #print srcShape.getLifeLineShape().GetPosition()
        srcY = pyutObject.getSrcY() - srcShape.getLifeLineShape().GetPosition()[1]
        dstY = pyutObject.getDstY() - dstShape.getLifeLineShape().GetPosition()[1]
        #print "OglSDMessage - adding shape at 0-", srcY, "; 0-", dstY
        src = srcShape.getLifeLineShape().AddAnchor(0, srcY)
        dst = dstShape.getLifeLineShape().AddAnchor(0, dstY)
        #print "OglSDMessage - anchors = ", src.GetPosition(), dst.GetPosition()
        src.SetStayOnBorder(False)
        dst.SetStayOnBorder(False)
        src.SetStayInside(True)
        dst.SetStayInside(True)
        src.SetVisible(True)
        dst.SetVisible(True)
        src.SetDraggable(True)
        dst.SetDraggable(True)
        self._srcShape = srcShape
        self._dstShape = dstShape
        self._srcAnchor = src
        self._dstAnchor = dst
        LineShape.__init__(self, src, dst)

        # Pen
        self.SetPen(wx.BLACK_PEN)

        # Add labels
        self._labels = {}

        # Initialize labels objects
        self._labels[CENTER] = self.AddText(0, 0, "")
        self.updateLabels()

        # Add arrow
        self.SetDrawArrow(True)


    #>------------------------------------------------------------------------

    def updatePositions(self):
        """
        Define the positions on lifeline (y)
        @author C.Dutoit
        """
        #print "OglMessage - updatePositions"
        src = self.GetSource()
        dst = self.GetDestination()
        srcY = self._pyutObject.getSrcY() + src.GetParent().GetSegments()[0][1]
        dstY = self._pyutObject.getDstY() + dst.GetParent().GetSegments()[0][1]
        srcX = 0
        dstX = 0
        #src.SetDraggable(True)
        #dst.SetDraggable(True)
        src.SetPosition(srcX, srcY)
        dst.SetPosition(dstX, dstY)
        #src.SetDraggable(False)
        #dst.SetDraggable(False)
        #print "OglMessage - updatePositions2 ", srcX, srcY, dstX, dstY

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
        prepareLabel(self._labels[CENTER], self._pyutObject.getMessage())

    #>------------------------------------------------------------------------

    def getPyutObject(self):
        """
        Return my pyut object
        @author C.Dutoit
        """
        return self._pyutObject

    #>------------------------------------------------------------------------

    def getLabels(self):
        """
        Get the labels.

        @return TextShape []
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
        #print "OglSDMEssage.Draw"
        self.updateLabels()
        #self.updatePositions()

        #Set position
        #src = self.GetSource()
        #dst = self.GetDestination()
        #srcY = self._pyutObject.getSrcY()
        #dstY = self._pyutObject.getDstY()
        #src.SetPosition(src.GetPosition()[0], srcY)
        #dst.SetPosition(dst.GetPosition()[0], dstY)

        #OglLink.Draw(self, dc)
        if DEBUG:
            print("Draw")
            print(self.GetSource().GetPosition())
            print(self.GetDestination().GetPosition())
        LineShape.Draw(self, dc, withChildren)

    #>------------------------------------------------------------------

    def OnLeftDClick(self, event):
        """
        Callback for left double clicks.
        @author C.Dutoit
        """
        dlg = wx.TextEntryDialog(None, _("Message"), _("Enter message"),
                self._pyutObject.getMessage(), wx.OK | wx.CANCEL | wx.CENTRE)
        if dlg.ShowModal() == wx.ID_OK:
            self._pyutObject.setMessage(dlg.GetValue())
        dlg.Destroy()

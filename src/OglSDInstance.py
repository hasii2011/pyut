#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.13 $"
__author__ = "C.Dutoit"
__date__ = "2002-11-22"

#from wxPython.wx  import *
from PyutLink     import PyutLink
from PyutConsts   import *
from mediator     import *
from MiniOgl      import *
from OglObject    import *
from PyutSDInstance import *


# Constants
DEFAULT_X = 0
DEFAULT_Y = 0
DEFAULT_WIDTH = 100
DEFAULT_HEIGHT = 400

##############################################################################

class OglInstanceName(TextShape, ShapeEventHandler):
    """
    TextShape that support text editing
    @author C.Dutoit
    """

    #>------------------------------------------------------------------

    def __init__(self, pyutObject, x, y, text, parent=None):
        """
        @author C.Dutoit
        """
        self._pyutObject = pyutObject
        TextShape.__init__(self, x, y, text, parent)




    #>------------------------------------------------------------------

    def OnLeftDClick(self, event):
        """
        Callback for left double clicks.
        @author C.Dutoit
        """
        dlg = wx.TextEntryDialog(None, _("Message"), _("Enter message"),
              self._pyutObject.getInstanceName(), wx.OK | wx.CANCEL | wx.CENTRE)
        if dlg.ShowModal() == wx.ID_OK:
            self._pyutObject.setInstanceName(dlg.GetValue())
        dlg.Destroy()






##############################################################################

class OglSDInstance(OglObject):
    """
    Class Diagram Instance
    This class is an OGL object for class diagram instance (vertical line, ..)
    This class implements the following functions : 
        - ...

    Instanciated by UmlClassDiagramFrame

    :version: $Revision: 1.13 $
    :author: C.Dutoit   
    :contact: dutoitc@hotmail.com
    """

    #>------------------------------------------------------------------------
    
    def __init__(self, pyutObject, parentFrame):
        """
        Constructor.
        @author C.Dutoit
        """
        # Init datas
        self._parentFrame = parentFrame
        self._instanceYPosition = 50       # Start of instances position

        # Get diagram
        diagram = self._parentFrame.GetDiagram()

        # Init this class
        OglObject.__init__(self, pyutObject, DEFAULT_WIDTH, DEFAULT_HEIGHT)
        diagram.AddShape(self)
        self.SetDraggable(True)
        self.SetVisible(True)
        self.SetPen(wx.Pen(wx.Colour(200, 200, 255), 1, wx.LONG_DASH))
        self.SetPosition(self.GetPosition()[0], self._instanceYPosition)

        # Init lineShape
        (srcX, srcY, dstX, dstY) = (DEFAULT_WIDTH/2, 0, 
                                    DEFAULT_WIDTH/2, DEFAULT_HEIGHT)
        #self._lifeLineX = srcX
        (src, dst) = (AnchorPoint(srcX, srcY, self), AnchorPoint(dstX, dstY, self))
        for el in [src, dst]:
            el.SetVisible(False)
            el.SetDraggable(False)
        self._lineShape = LineShape(src, dst)
        self.AppendChild(self._lineShape)
        self._lineShape.SetParent(self)
        self._lineShape.SetDrawArrow(False)
        self._lineShape.SetDraggable(True)
        self._lineShape.SetPen(wx.BLACK_DASHED_PEN)
        self._lineShape.SetVisible(True)
        diagram.AddShape(self._lineShape)
        
        # Instance box
        self._instanceBox = RectangleShape(0, 0, 100, 50)
        self.AppendChild(self._instanceBox)
        self._instanceBox.SetDraggable(False)
        self._instanceBox.Resize = self.OnInstanceBoxResize
        self._instanceBox.SetResizable(True)
        self._instanceBox.SetParent(self)
        diagram.AddShape(self._instanceBox)

        # Text of the instance box
        text = self._pyutObject.getInstanceName()
        self._instanceBoxText = OglInstanceName(pyutObject, 0, 20, text, self._instanceBox)
        self.AppendChild(self._instanceBoxText)
        diagram.AddShape(self._instanceBoxText)
        #TODO : set instance box size to the size of the text
        #       by invoking self._instanceBoxText.setSize()



    #>------------------------------------------------------------------------

    def getLifeLineShape(self):
        """
        return the lifeline object
        @author C.Dutoit
        Used by OGLSDMessage to use it as parent
        """
        return self._lineShape


    ##>------------------------------------------------------------------------

    #def getLifeLineX(self):
    #    """
    #    return the lifeline X position

    #    @return int : the position in X of the lifeline
    #    @author C.Dutoit
    #    """
    #    return self._lifeLineX

    #>------------------------------------------------------------------------
    def OnInstanceBoxResize(self, sizer, width, height):
        """
        Resize the instance box, so all instance

        @param double x, y : position of the sizer
        """
        RectangleShape.Resize(self._instanceBox, sizer, width, height)
        size = self._instanceBox.GetSize()
        self.SetSize(size[0], self.GetSize()[1])


    #>------------------------------------------------------------------------
    def Resize(self, sizer, width, height):
        """
        Resize the rectangle according to the new position of the sizer.

        @param double x, y : position of the sizer
        """
        OglObject.Resize(self, sizer, width, height)

    #>------------------------------------------------------------------------
    def SetSize(self, width, height):
        """
        """
        OglObject.SetSize(self, width, height)
        # Set lifeline
        #self._lifeLineX = width/2
        (myX, myY) = self.GetPosition()
        (myX, myY) = self.GetPosition()
        (w, h) = self.GetSize()
        lineDst = self._lineShape.GetDestination()
        lineSrc = self._lineShape.GetSource()
        lineSrc.SetDraggable(True)
        lineDst.SetDraggable(True)
        lineSrc.SetPosition(w/2 + myX, 0 + myY)
        lineDst.SetPosition(w/2 + myX, height + myY)
        lineSrc.SetDraggable(False)
        lineDst.SetDraggable(False)

        # Update all links positions
        for link in self._oglLinks:
            try:
                link.updatePositions()
            except:
                pass

        # Set TextBox
        RectangleShape.SetSize(self._instanceBox, 
                               width, self._instanceBox.GetSize()[1])

    
    #>------------------------------------------------------------------------

    def SetPosition(self, x, y):
        """ 
        Debug
        @author C.Dutoit
        """
        y = self._instanceYPosition
        OglObject.SetPosition(self, x, y)

    
    #>------------------------------------------------------------------------

    def Draw(self, dc):#, withChildren=False):
        """
        Draw overload; update labels
        @author C.Dutoit
        """
        # Update labels
        self._instanceBoxText.SetText(self._pyutObject.getInstanceName())

        # Call parent's Draw method
        if self.IsSelected():
            self.SetVisible(True)
            self.SetPen(wx.Pen(wx.Colour(200, 200, 255), 1, wx.LONG_DASH))

        # Draw
        OglObject.Draw(self, dc)#, withChildren)


    #>------------------------------------------------------------------

    #def addLink(self, link):
        #"""
        #Add a link to an ogl object.
#
        #@param OglLink link : the link to add
        #@author Philippe Waelti
        #@modified C.Dutoit 20021125 : Added as error, since it's not used here
        #"""
        #raise _("Not valid in this case")

    #>------------------------------------------------------------------

    #def getLinks(self):
        #"""
        #Return the links.
#
        #@return OglLink[] : Links connected to object
        #@author Philippe Waelti
        #@modified C.Dutoit 20021125 : Added as error, since it's not used here
        #"""
        #raise _("Not valid in this case")



    #>------------------------------------------------------------------

    def OnLeftUp(self, event):
        """
        Callback for left clicks.

        @since 1.0
        """
        self.SetPosition(self.GetPosition()[0], self._instanceYPosition)

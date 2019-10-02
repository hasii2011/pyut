#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.4 $"
__author__  = "EI5, eivd, Group Burgbacher - Waelti"
__date__    = "2001-12-12"

#from wxPython.wx  import *
from MiniOgl      import *
from Mediator     import *
from OglLink      import *
from PyutConsts   import *

DEFAULT_FONT_SIZE = 10

#----------------------------------------------------------------------

class OglCDObject(ShapeEventHandler):
    """
    This is the base class for new CD OGL objects.
    Every new CD OGL class must inherate this class and redefines methods if
    necessary.

    This is to be the most compatible with old OglObject class.


    :version: $Revision: 1.4 $
    :author: C.Dutoit
    """

    #>------------------------------------------------------------------

    def __init__(self, pyutObject):
        """
        Constructor.

        @param PyutObject pyutObject : Associated PyutObject
        @since 1.0
        @author C.Dutoit
        """
        # Associated PyutObject
        self._pyutObject = pyutObject

        # Default font
        self._defaultFont = wx.Font(DEFAULT_FONT_SIZE, wx.SWISS, \
                wx.NORMAL, wx.NORMAL)


    #>------------------------------------------------------------------

    def setPyutObject(self, pyutObject):
        """
        Set the associated pyut object.

        @param PyutObject pyutObject : Associated PyutObject
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        self._pyutObject = pyutObject

    #>------------------------------------------------------------------

    def getPyutObject(self):
        """
        Return the associated pyut object.

        @return PyutObject : Associated PyutObject
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        return self._pyutObject


    #>------------------------------------------------------------------

    def OnLeftDown(self, event):
        """
        Handle event on left click.
        @author C.Dutoit
        """
        # Get mediator and signal selection
        med = getMediator()
        if med.actionWaiting():
            med.shapeSelected(self, event.GetPositionTuple())
            return EVENT_PROCESSED
        return SKIP_EVENT

    #>------------------------------------------------------------------------

    def autoResize(self):
        """
        Find the right size to see all the content, and resize self.

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        pass

    #>------------------------------------------------------------------

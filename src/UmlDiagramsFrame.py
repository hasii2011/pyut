#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
__version__ = "$Revision: 1.6 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2002-03-13"
__PyUtVersion__ = "1.0"

#from wx.Python.ogl    import *
#from wx.Python.wx.     import *
#from wx.Python.html   import *
import wx
from UmlFrame        import *
from pyutUtils       import *
from PyutPrintout    import *
from PluginManager   import *
from copy            import deepcopy
from mediator        import Mediator


# wx.OGLInitialize()

# ...
# wx.InitAllImageHandlers()

class UmlDiagramsFrame(UmlFrame):
    """
    ClassFrame : class diagram frame.

    This class is a frame where we can draw Class diagrams.
    It can load and save class diagrams datas.
    It is used by UmlClassDiagramsFrame

    :author: C.Dutoit
    :contact: dutoitc@hotmail.com
    :version: $Revision: 1.6 $
    """
    #>------------------------------------------------------------------------

    def __init__(self, parent):
        """
        Constructor.

        @param wx.Window parent : parent window
        @param int ID : wx. ID of this frame
        @param String title : Title to display
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        import os
        UmlFrame.__init__(self, parent, -1)

    #>-----------------------------------------------------------------------

    def OnClose(self, force=False):
        """
        Closing handler (must be called explicitly).
        Save files and ask for confirmation.

        @return True if the close succeeded
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self.cleanUp()
        #wx.OGLCleanUp()
        self.Destroy()
        return True


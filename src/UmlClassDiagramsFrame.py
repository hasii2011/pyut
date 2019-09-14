#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__version__ = "$Revision: 1.8 $"
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
from UmlDiagramsFrame import *
import mediator

class UmlClassDiagramsFrame(UmlDiagramsFrame):
    """
    UmlClassDiagramsFrame : a UML class diagram frame.

    This class is the instance of one UML class diagram structure.
    It derives its functionalities from UmlDiagramsFrame, but
    as he know the structure of a class diagram, 
    he can load class diagram datas.

    Used by FilesHandling.

    :author: C.Dutoit
    :contact: dutoitc@hotmail.com
    :version: $Revision: 1.8 $
    """

    #>------------------------------------------------------------------------

    def __init__(self, parent):
        """
        Constructor.

        @param wx.Window parent : parent window
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        import os
        #print ">>>UmlClassDiagramsFrame-1"
        UmlDiagramsFrame.__init__(self, parent)
        #print "---UmlClassDiagramsFrame-2"
        self.newDiagram()
        #print "---UmlClassDiagramsFrame-3"
        #self._

    ##>-----------------------------------------------------------------------
    #def displayDiagramProperties(self):
    #    """
    #    Display class diagram properties
    #    @author C.Dutoit
    #    """
    #    from DlgClassDiagramProperties import DlgClassDiagramProperties
    #    dlg = DlgClassDiagramProperties(self, -1, self._ctrl)
    #    dlg.ShowModal()
    #    dlg.Destroy()
    #    self._ctrl.getUmlFrame().Refresh()

    #>-----------------------------------------------------------------------

    #def OnOpen(self, filename):
        #"""
        #Open datas from a file
#
        #@return True if the file has been loaded, False in others cases
        #@since 1.0
        #@author C.Dutoit <dutoitc@hotmail.com>
        #"""
        ##Init loading
        #self.newDiagram()
#
        ##Return with success
        #wx.EndBusyCursor()
        #return True
        
    #>-----------------------------------------------------------------------

    #def onClose(self, force=False):
        #"""
        #Closing handler (must be called explicitly). 
        #Save files and ask for confirmation.
#
        #@return True if the close succeeded
        #@since 1.0
        #@author C.Dutoit <dutoitc@hotmail.com>
        #"""
        #self.cleanUp()
        ##wx.OGLCleanUp()
        #self.Destroy(-1)
        #return True


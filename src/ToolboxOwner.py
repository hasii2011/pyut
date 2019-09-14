#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Goal : be a toolbox owner

__version__ = "$Revision: 1.4 $"
__author__ = "C.Dutoit"
__date__ = "2002-05-25"
#from wxPython.wx import *
from Toolbox import Toolbox
#import wx


##############################################################################
#TODO : add observer-observable model to support dynamic plugins
class ToolboxOwner:
    """
    ToolboxOwner : a toolbox owner

    :author: C.Dutoit 
    :contact: <dutoitc@hotmail.com>
    :version: $Revision: 1.4 $
    """

    #>------------------------------------------------------------------------

    def __init__(self, parent):
        """
        Constructor.

        @param wxWindow parent : parent window
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        # Members vars
        self._toolCategories = {}
        self._parent = parent



    #>------------------------------------------------------------------------
    def displayToolbox(self, category):
        """
        display a toolbox

        @param string category : category of tools to display
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        toolbox = Toolbox(self._parent, self)
        toolbox.setCategory(category)
        #toolbox.Show(True)


    #>------------------------------------------------------------------------
    def registerTool(self, tool):
        """
        Add a tool to toolboxes

        @param Tool tool : The tool to add
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        if not self._toolCategories.has_key(tool.getInitialCategory()):
            self._toolCategories[tool.getInitialCategory()] = [tool]
        else:
            self._toolCategories[tool.getInitialCategory()].append(tool)
            


    #>------------------------------------------------------------------------
    def getCategoryTools(self, category):
        """
        Return all tools for a specified category

        @param string category : the category of tools to get
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        return self._toolCategories[category]


    #>------------------------------------------------------------------------
    def getCategories(self):
        """
        Return all categories of tools

        @return string[] of categories
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        return self._toolCategories.keys()



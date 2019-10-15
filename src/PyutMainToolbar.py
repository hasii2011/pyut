#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.5 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2001-11-14"

#from wxPython.wx import *
from UmlFrame import *
from PyutUtils import *
import os, wx
from Mediator import *

# Assign constants
[
    ID_ARROW, ID_CLASS, ID_REL_INHERITANCE, ID_REL_REALISATION,
    ID_REL_COMPOSITION, ID_REL_AGREGATION, ID_ACTOR
]=assignID(7)

ACTIONS = {
    ID_ARROW           : ACTION_SELECTOR,
    ID_CLASS           : ACTION_NEW_CLASS,
    ID_REL_INHERITANCE : ACTION_NEW_INHERIT_LINK,
    ID_REL_REALISATION : ACTION_NEW_IMPLEMENT_LINK,
    ID_REL_COMPOSITION : ACTION_NEW_COMPOSITION_LINK,
    ID_REL_AGREGATION  : ACTION_NEW_AGGREGATION_LINK,
    ID_ACTOR           : ACTION_NEW_ACTOR,
}

# todo : Tips doesn't work; how to do them ?

class PyutMainToolbar(wx.Dialog): #wxToolbar
    """
    PyutMainToolbar : Main pyut application toolbar.

    Used by AppFrame.

    :author: C.Dutoit
    :contact: <dutoitc@hotmail.com>
    :version: $Revision: 1.5 $
    """

    #>------------------------------------------------------------------------

    def __init__(self, parent, ID, title, statusbar):
        """
        Constructor.

        @parameters wxStatusBar statusbar : Statusbar where to display user tips
        @since 1.0
        @author C.Dutoit
        """
        self.__statusBar=statusbar #Application status bar for the tips
        self.__dicTips={-1:""}     #Dictionary of tips for buttons
        #Note : Modify code when wxPython support multiple toolbars
        #       for a single frame
        #wx.ToolBar.__init__(self, parent, ID,
        #                   wx.DefaultPosition, wx.DefaultSize,
                           #wx.NO_BORDER | wx.TB_FLAT | wx.TB_HORIZONTAL |
                           #wx.TB_DOCKABLE)
        #                   wx.TB_HORIZONTAL | wx.TB_DOCKABLE | wx.TB_3DBUTTONS)
        wx.Dialog.__init__(self, parent, ID, "", wx.DefaultPosition,
                          wx.Size(59, 100))

        #Create the buttons
        self.addButton(wx.Point(5,  5),  'arrow.bmp', ID_ARROW,
                       "select tool")
        self.addButton(wx.Point(27, 5),  'class.bmp', ID_CLASS,
                       "new class")
        self.addButton(wx.Point(5,  27), 'relinheritance.bmp',
                      ID_REL_INHERITANCE, "new inheritance")
        self.addButton(wx.Point(27, 27), 'relrealisation.bmp',
                      ID_REL_REALISATION, "new realisation")
        self.addButton(wx.Point(5,  49), 'relcomposition.bmp',
                      ID_REL_COMPOSITION, "new composition")
        self.addButton(wx.Point(27, 49), 'relagregation.bmp',
                      ID_REL_AGREGATION, "new agregation")
        self.addButton(wx.Point(27, 5),  'class.bmp', ID_ACTOR,
                       "new actor")

        self.Bind(EVT_BUTTON, self.OnNewAction, id=ID_ARROW)
        self.Bind(EVT_BUTTON, self.OnNewAction, id=ID_CLASS)
        self.Bind(EVT_BUTTON, self.OnNewAction, id=ID_REL_INHERINTANCE)
        self.Bind(EVT_BUTTON, self.OnNewAction, id=ID_REL_REALISATION)
        self.Bind(EVT_BUTTON, self.OnNewAction, id=ID_REL_COMPOSITION)
        self.Bind(EVT_BUTTON, self.OnNewAction, id=ID_REL_AGREGATIoN)
        self.Bind(EVT_BUTTON, self.OnNewAction, id=ID_ACTOR)
        self._ctrl = getMediator()
        self._ctrl.registerToolBar(self)

        #self.Realize()
        self.Show(True)

    #>------------------------------------------------------------------------

    def OnNewAction(self, event):
        """
        Call the mediator to specifiy the current action.

        @param wx.Event event
        @since 1.7
        @author L. Burgbacher <lb@alawa.ch>
        """
        self._ctrl.setCurrentAction(ACTIONS[event.GetId()])

    #>------------------------------------------------------------------------

    #TODO : replace when wx.Python support multiple toolbars...
    #def addButton(self, pos, filename, id=-1):
    #    bmp=wx.Bitmap('img'+os.sep+filename, wx.BITMAP_TYPE_BMP)
    #    self.AddTool(id, bmp)

    def addButton(self, pos, filename, id=-1, tips=""):
        """
        add a button to the window

        @param tuple(x,y) pos : Button position
        @param string filename: bitmap filename
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        bmp=wx.Bitmap('img'+os.sep+filename, wx.BITMAP_TYPE_BMP)
        wx.BitmapButton(self, id, bmp, pos,
                       wx.Size(bmp.GetWidth()+6, bmp.GetHeight()+6))

        #Set callback on mouse move for the tips ?
        #if tips<>"":
            ##Verify that we do have an id
            #if id==-1:
                #[id]=assignId(1)
            #EVT_MOTION(self, self.__onMouseMove(id=id))
            #self.__dicTips[id]=tips


    #>------------------------------------------------------------------------

    def __onMouseMove(self, event, id=-1):
        """
        Mouse Move=Mouse Motion : set user tips on the application statusbar

        @since 1.6
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        pass

        #self.__statusbar.SetStatusText(self.__dicTips[id])

    #>------------------------------------------------------------------------

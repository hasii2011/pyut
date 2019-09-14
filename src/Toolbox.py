#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Goal : be a toolbox for tools plugins

__version__ = "$Revision: 1.10 $"
__author__ = "C.Dutoit"
__date__ = "2002-05-25"
#from wxPython.wx import *
import wx


MARGIN = 3                  # Margin between dialog border and buttons
MARGIN_TOP = 20
BUTTON_PICTURE_SIZE = 16    # The size of a picture in one button
BUTTON_SIZE = BUTTON_PICTURE_SIZE + 3   # The size of one button


##############################################################################
# mini-clone of wxEvent to call callback
# wxWindows tell to not create wxEvent object in our applications !
class EventClone:
    def __init__(self, id):
        self._id = id
    def GetId(self):
        return self._id



##############################################################################
class Toolbox(wx.Frame):
    """
    Toolbox : a toolbox for PyUt tools plugins

    :author: C.Dutoit 
    :contact: <dutoitc@hotmail.com>
    :version: $Revision: 1.10 $
    """

    #>------------------------------------------------------------------------

    def __init__(self, parentWindow, toolboxOwner):
        """
        Constructor.

        @param 
        @param wxWindow parentWindow : parent window
        @param ToolboxOwner toolboxOwner
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        import os
        # Application initialisation
        wx.Frame.__init__(self, parentWindow, -1, "toolbox",
                         wx.DefaultPosition, wx.Size(100, 200),
                         style = 
                         wx.STATIC_BORDER | 
                         wx.SYSTEM_MENU |
                         wx.CAPTION |
                         wx.FRAME_FLOAT_ON_PARENT)

                         #style= wx.RESIZE_BORDER |
                                #wx.CAPTION |
                                #wx.RESIZE_BORDER |
                                #wx.FRAME_FLOAT_ON_PARENT 
                                #wx.FRAME_TOOL_WINDOW 
                         #       )

        # Member vars
        self._tools = []
        self._category = ""
        self._clickedButton = None
        self._parentWindow = parentWindow
        self._toolboxOwner = toolboxOwner

        # Main sizer
        #self.SetAutoLayout(True)
        #sizer = wx.BoxSizer(wx.VERTICAL)
        #sizer.Add(self._picture,                0, wx.ALL | wx.ALIGN_CENTER, 5)
        #self.SetSizer(sizer)
        #sizer.Fit(self)

        # Events
        self.Bind(wx.EVT_PAINT, self.OnRefresh)
        self.Bind(wx.EVT_CLOSE, self.evtClose)
        self.Bind(wx.EVT_LEFT_UP, self.evtLeftUp)
        self.Bind(wx.EVT_LEFT_DOWN, self.evtLeftDown)

        # Display myself
        self.Show(True)


    #>------------------------------------------------------------------------
    
    def setCategory(self, category):
        """
        Define the toolbox category

        @param string category : the new category
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._category = category
        self._tools = self._toolboxOwner.getCategoryTools(category)
        self.Refresh()

    
    #>------------------------------------------------------------------------

    def OnRefresh(self, event):
        """
        Refresh dialog box

        @since 1.1.2.4
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        # Init
        (w, h) = self.GetSizeTuple()
        nbButtonsW = (w - MARGIN*2) / BUTTON_SIZE
        dc = wx.ClientDC(self)
        oldPen = dc.GetPen()

        # Draw
        i=0
        j=0
        for tool in self._tools:
            # Calculate position
            x = MARGIN + i*BUTTON_SIZE
            y = MARGIN + j*BUTTON_SIZE + MARGIN_TOP

            # Draw
            dc.SetPen(wx.BLACK_PEN)
            dc.DrawText("[" + tool.getInitialCategory() + "]", MARGIN, MARGIN)
            dc.SetPen(wx.WHITE_PEN)
            dc.DrawLine(x, y, x+BUTTON_SIZE-1, y)
            dc.DrawLine(x, y, x, y + BUTTON_SIZE-1)
            dc.SetPen(wx.BLACK_PEN)
            dc.DrawLine(x, y+BUTTON_SIZE-1, x+BUTTON_SIZE-1, y+BUTTON_SIZE-1)
            dc.DrawLine(x + BUTTON_SIZE-1, y, x + BUTTON_SIZE-1, y + BUTTON_SIZE-1)
            dc.DrawBitmap(tool.getImg(), x+1, y+1)
            i+=1

            # Find next position
            if i>nbButtonsW-1:
                i=0
                j+=1

        # Set old pen
        dc.SetPen(oldPen)


    #>------------------------------------------------------------------------

    def _getClickedButton(self, x, y):
        """
        Return the clicked button
        @author C.Dutoit
        """
        (w, h) = self.GetSizeTuple()
        nbButtonsW = (w - MARGIN*2) / BUTTON_SIZE

        # Get position
        i=0
        j=0
        for tool in self._tools:
            # Calculate position
            bx = MARGIN + i*BUTTON_SIZE
            by = MARGIN + j*BUTTON_SIZE + MARGIN_TOP

            # Are we into the current tool ? 
            if x>bx and x<bx+BUTTON_SIZE and \
               y>by and y<by+BUTTON_SIZE:
               return (bx, by, bx+BUTTON_SIZE, by+BUTTON_SIZE, tool)

            # Find next position
            i+=1
            if i>nbButtonsW-1:
                i=0
                j+=1
        return (0, 0, 0, 0, None)
    
    #>------------------------------------------------------------------------

    def evtLeftUp(self, event):
        """
        Handle left mouse button up

        @author C.Dutoit
        """
        # Get clicked coordinates
        (x1, y1, x2, y2, tool) = self._clickedButton
        
        # Get dc
        dc = wx.ClientDC(self)
        oldPen = dc.GetPen()

        # Draw normally button
        dc.SetPen(wx.BLACK_PEN)
        dc.DrawLine(x2-1, y2-1, x2-1, y1)
        dc.DrawLine(x2-1, y2-1, x1, y2-1)
        dc.SetPen(wx.WHITE_PEN)
        dc.DrawLine(x1, y1, x2-1, y1)
        dc.DrawLine(x1, y1, x1, y2-1)

        # Set old pen
        dc.SetPen(oldPen)

        # Remove clicked button
        self._clickedButton = None

        # Execute callback
        if tool is not None:
            callback = tool.getActionCallback()
            if (callback!=None):
                callback(EventClone(tool.getWXID()))

    #>------------------------------------------------------------------------

    def evtLeftDown(self, event):
        """
        Handle left mouse button down
        @author C.Dutoit
        """
        # Get the clicked tool
        x, y = event.GetPosition()
        (x1, y1, x2, y2, tool) = self._getClickedButton(x, y)
        self._clickedButton = (x1, y1, x2, y2, tool)

        # Get dc
        dc = wx.ClientDC(self)
        oldPen = dc.GetPen()

        # Clicked illusion
        dc.SetPen(wx.GREY_PEN)
        dc.DrawLine(x2-1, y2-1, x2-1, y1)
        dc.DrawLine(x2-1, y2-1, x1, y2-1)
        dc.SetPen(wx.BLACK_PEN)
        dc.DrawLine(x1, y1, x2-1, y1)
        dc.DrawLine(x1, y1, x1, y2-1)

        # Set old pen
        dc.SetPen(oldPen)


    #>------------------------------------------------------------------------

    def evtClose(self, event):
        """
        Clean close, event handler on EVT_CLOSE

        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self.Destroy()

#!/usr/bin/env python
#
# Copyright 2002, Laurent Burgbacher, Eivd.
# Visit http://www.eivd.ch
#
# This file is part of MiniOgl.
#
# MiniOgl is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# MiniOgl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MiniOgl; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

__author__    = "Laurent Burgbacher, lb@alawa.ch, Eivd"
__copyright__ = "Copyright 2002, Laurent Burgbacher, Eivd"
__license__   = "Released under the terms of the GNU General Public Licence V2"
__date__      = "2002-10-15"
__version__   = "$Id: ShapeEventHandler.py,v 1.3 2004/06/16 19:33:18 dutoitc Exp $"


__all__ = ["ShapeEventHandler"]
DEBUG = 0


class ShapeEventHandler(object):
    """
    Let a shape receive mouse events directly.

    Exported methods:
    -----------------

    OnLeftDown(self, event)
        Callback for left clicks.
    OnLeftUp(self, event)
        Callback for left clicks.
    OnLeftDClick(self, event)
        Callback for left double clicks.
    OnMiddleDown(self, event)
        Callback for middle clicks.
    OnMiddleUp(self, event)
        Callback for middle clicks.
    OnMiddleDClick(self, event)
        Callback for middle double clicks.
    OnRightDown(self, event)
        Callback for right clicks.
    OnRightUp(self, event)
        Callback for right clicks.
    OnRightDClick(self, event)
        Callback for right double clicks.

    @author Laurent Burgbacher <lb@alawa.ch>
    """
    def OnLeftDown(self, event):
        """
        Callback for left clicks.

        @param wx.Event event
        """
        if DEBUG:
            print("Unhandled left down")
        event.Skip()

    def OnLeftUp(self, event):
        """
        Callback for left clicks.

        @param wx.Event event
        """
        if DEBUG:
            print("Unhandled left up")
        event.Skip()

    def OnLeftDClick(self, event):
        """
        Callback for left double clicks.

        @param wx.Event event
        """
        if DEBUG:
            print("Unhandled left double click")
        event.Skip()

    def OnMiddleDown(self, event):
        """
        Callback for middle clicks.

        @param wx.Event event
        """
        if DEBUG:
            print("Unhandled middle down")
        event.Skip()

    def OnMiddleUp(self, event):
        """
        Callback for middle clicks.

        @param wx.Event event
        """
        if DEBUG:
            print("Unhandled middle up")
        event.Skip()

    def OnMiddleDClick(self, event):
        """
        Callback for middle double clicks.

        @param wx.Event event
        """
        if DEBUG:
            print("Unhandled middle double click")
        event.Skip()

    def OnRightDown(self, event):
        """
        Callback for right clicks.

        @param wx.Event event
        """
        if DEBUG:
            print("Unhandled right down")
        event.Skip()

    def OnRightUp(self, event):
        """
        Callback for right clicks.

        @param wx.Event event
        """
        if DEBUG:
            print("Unhandled right up")
        event.Skip()

    def OnRightDClick(self, event):
        """
        Callback for right double clicks.

        @param wx.Event event
        """
        if DEBUG:
            print("Unhandled right double click")
        event.Skip()

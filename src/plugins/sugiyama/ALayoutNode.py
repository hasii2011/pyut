#!/usr/bin/env python
#
# Copyright 2002, Nicolas Dubois, Eivd.
# Visit http://www.eivd.ch
#
# This file is part of PyUt.
#
# PyUt is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# PyUt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyUt; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

__version__ = '$Revision: 1.4 $'
__author__ = 'Nicolas Dubois <nicdub@gmx.ch>'
__date__ = '2002-10-31'


class ALayoutNode:
    """
    ALayoutNode: Interface between OglObject/PyutObject and ALayout algorithm.
    
    Instancied by: RealSugiyamaNode.py

    :author: Nicolas Dubois
    :contact: nicdub@gmx.ch
    :version: $Revision: 1.4 $
    """

    #>------------------------------------------------------------------------
    def __init__(self, oglObject):
        """
        Constructor.

        @param OglObject oglObject: interfaced ogl object
        @author Nicolas Dubois
        """
        self._oglObject = oglObject


    #>------------------------------------------------------------------------
    def getSize(self):
        """
        Return the class size.

        @return (float, float): tuple (width, height)
        @author Nicolas Dubois
        """
        return self._oglObject.GetSize()


    #>------------------------------------------------------------------------
    def getPosition(self):
        """
        Get class position.

        @return (float, float): tuple (x, y) coordinates
        @author Nicolas Dubois
        """
        return self._oglObject.GetPosition()


    #>------------------------------------------------------------------------
    def setPosition(self, x, y):
        """
        Set the class position.

        @param float x, y: absolute coordinates
        @author Nicolas Dubois
        """
        self._oglObject.SetPosition(x, y)


    #>------------------------------------------------------------------------
    def getName(self):
        """
        Get the name of the class.

        @return String: name of the class
        @author Nicolas Dubois
        """
        return self._oglObject.getPyutObject().getName()


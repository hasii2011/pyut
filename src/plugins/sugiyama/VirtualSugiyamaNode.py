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

from plugins.sugiyama.SugiyamaNode import *

class VirtualSugiyamaNode(SugiyamaNode):
    """
    VirtualSugiyamaNode: a virtual node is a node on the Sugiyama graph which
    will not be visible on the diagram. It is used to reserve an emplacement
    for the links drawing.

    Instancied by: ../ToSugiyama.py

    :author: Nicolas Dubois
    :contact: nicdub@gmx.ch
    :version: $Revision: 1.4 $
    """


    #>------------------------------------------------------------------------
    def __init__(self):
        """
        Constructor.

        @author Nicolas Dubois
        """
        # Call mother class initialization
        SugiyamaNode.__init__(self)

        # Self fields
        self.__position = (0, 0)
        self.__size = (1, 1)


    #>------------------------------------------------------------------------
    def setSize(self, width, height):
        """
        Set the size of the node.

        @param float width, height : Size
        @author Nicolas Dubois
        """
        self.__size = (width, height)


    #>------------------------------------------------------------------------
    def getSize(self):
        """
        Get size of node.

        @return (float, float) : (width, height)
        @author Nicolas Dubois
        """
        return self.__size


    #>------------------------------------------------------------------------
    def setPosition(self, x, y):
        """
        Set node position.

        @param float x, y : position in absolute coordinate
        @author Nicolas Dubois
        """
        self.__position = (x, y)


    #>------------------------------------------------------------------------
    def getPosition(self):
        """
        Get node position.

        @return (float, float) : (x, y) in absolute coordinate
        @author Nicolas Dubois
        """
        return self.__position



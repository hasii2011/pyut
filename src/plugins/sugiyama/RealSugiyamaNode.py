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

from SugiyamaNode import *
from ALayoutNode import *

class RealSugiyamaNode(SugiyamaNode):
    """
    RealSugiyamaNode: A RealSugiyamaNode object is a node of the Sugiyama
    graph associated to an OglObject of the UML diagram, which can be a
    class or a note.

    For more information, see ../ToSugiyama.py

    Instancied by: ../ToSugiyama.py

    :author: Nicolas Dubois
    :contact: nicdub@gmx.ch
    :version: $Revision: 1.4 $
    """


    #>------------------------------------------------------------------------
    def __init__(self, oglObject):
        """
        Constructor.

        @param OglObject oglObject: class or note of the diagram
        @author Nicolas Dubois
        """
        # Call mother class initialization
        SugiyamaNode.__init__(self)
        
        # Self fields
        self.__aLayoutNode = ALayoutNode(oglObject)


    #>------------------------------------------------------------------------
    def getSize(self):
        """
        Get the size of the node.

        @return (float, float) : tuple (width, height)
        @author Nicolas Dubois
        """
        return self.__aLayoutNode.getSize()


    #>------------------------------------------------------------------------
    def setPosition(self, x, y):
        """
        Set node position.

        @param float x, y : position in absolute coordinates
        @author Nicolas Dubois
        """
        self.__aLayoutNode.setPosition(x, y)


    #>------------------------------------------------------------------------
    def getPosition(self):
        """
        Get node position.

        @return (float, float) : tuple (x, y) in absolute coordinates
        @author Nicolas Dubois
        """
        return self.__aLayoutNode.getPosition()


    #>------------------------------------------------------------------------
    def getName(self):
        """
        Get the name of the OglObject.

        @return str : name of OglObject
        @author Nicolas Dubois
        """
        return self.__aLayoutNode.getName()


    #>------------------------------------------------------------------------
    def fixAnchorPos(self):
        """
        Fix the positions of the anchor points.

        The anchor points a placed according to fathers and sons positions.
        Before calling this function, be sure you have set the index of all
        fathers and sons (see setIndex).

        @author Nicolas Dubois
        """
        # Internal comparison funtion for sorting list of fathers or sons
        # on index.
        def cmpIndex(l, r):
            return cmp(l[0].getIndex(), r[0].getIndex())
        
        
        # Get position and size of node
        (width, height) = self.getSize()
        (x, y) = self.getPosition()
        
        # Fix all sons anchors position
        
        # Sort sons list to eliminate crossing
        sons = self.getSons()
        sons.sort(cmpIndex)
        nbSons = len(sons)
        # For all sons
        for i in range(nbSons):
            (son, link) = sons[i]
            # Fix anchors coordinates
            link.setDestAnchorPos(
                x + width * (i + 1) / (nbSons + 1), y + height)
        
        # Fathers anchors position
        
        # Sort fathers list to eliminate crossing
        fathers = self.getFathers()
        fathers.sort(cmpIndex)
        nbFathers = len(fathers)
        # For all fathers
        for i in range(nbFathers):
            (father, link) = fathers[i]
            # Fix anchors coordinates
            link.setSrcAnchorPos(
                x + width * (i + 1) / (nbFathers + 1), y)



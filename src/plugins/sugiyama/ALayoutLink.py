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


class ALayoutLink:
    """
    ALayoutLink : Interface between pyut/ogl link and ALayout algorithms.
    
    ALayout algorithms can use this interface to access the links of the
    diagram. The first reason is that the interface protects the structure
    of the diagram. The second is that pyut structure and methods could
    be changed. In a such case, the only files to update is the interface, not
    your automatic layout algorithm.

    Instancied by: see in RealSugiyamaNode.py

    :author: Nicolas Dubois
    :contact: nicdub@gmx.ch
    :version: $Revision: 1.4 $
    """

    #>------------------------------------------------------------------------
    def __init__(self, oglLink):
        """
        Constructor.

        @author Nicolas Dubois
        """
        self._oglLink = oglLink
        self.__srcNode = None
        self.__dstNode = None


    #>------------------------------------------------------------------------
    def setSource(self, node):
        """
        Set the source node.

        @param InterfaceSugiyamaNode node: source node of the link
        @author Nicolas Dubois
        """
        self.__srcNode = node


    #>------------------------------------------------------------------------
    def getSource(self):
        """
        Return the source node.

        @return InterfaceSugiyamaNode: source node of the link
        @author Nicolas Dubois
        """
        return self.__srcNode


    #>------------------------------------------------------------------------
    def setDestination(self, node):
        """
        Set the destination node.

        @param InterfaceSugiyamaNode node: destination node of the link
        @author Nicolas Dubois
        """
        self.__dstNode = node


    #>------------------------------------------------------------------------
    def getDestination(self):
        """
        Return the destination node.

        @return InterfaceSugiyamaNode: destination node of the link
        @author Nicolas Dubois
        """
        return self.__dstNode


    #>------------------------------------------------------------------------
    def setSrcAnchorPos(self, x, y):
        """
        Set anchor position (absolute coordinates) on source class.
        
        @param float x, y : absolute coordinates
        @author Nicolas Dubois
        """
        self._oglLink.GetSource().SetPosition(x, y)


    #>------------------------------------------------------------------------
    def getSrcAnchorPos(self):
        """
        Get anchor position (absolute coordinates) on source class.

        @return (float, float) : tuple with (x, y) coordinates
        @author Nicolas Dubois
        """
        return self._oglLink.GetSource().GetPosition()


    #>------------------------------------------------------------------------
    def setDestAnchorPos(self, x, y):
        """
        Set anchor position (absolute coordinates) on destination class.

        @param float x, y : absolute coordinates
        @author Nicolas Dubois
        """
        self._oglLink.GetDestination().SetPosition(x, y)


    #>------------------------------------------------------------------------
    def getDestAnchorPos(self):
        """
        Return anchor position (absolute coordinates) on destination class.

        @return (float, float) : tuple with (x, y) coordinates
        @author Nicolas Dubois
        """
        return self._oglLink.GetDestination().GetPosition()


    #>------------------------------------------------------------------------
    def addControlPoint(self, control, last=None):
        """
        Add a control point. If param last given, add point right after last.

        @param ControlPoint control : control point to add
        @param ControlPoint last    : add control right after last
        @author Nicolas Dubois
        """
        self._oglLink.AddControl(control, last)


    #>------------------------------------------------------------------------
    def removeControlPoint(self, controlPoint):
        """
        Remove a control point.

        @param ControlPoint controlPoint: control point to remove
        @author Nicolas Dubois
        """
        self._oglLink.Remove(controlPoint)


    #>------------------------------------------------------------------------
    def removeAllControlPoints(self):
        """
        Remove all control points.

        @author Nicolas Dubois
        """
        self._oglLink.RemoveAllControlPoints()


    #>------------------------------------------------------------------------
    def getType(self):
        """
        Return the type of the link.

        The possible types are defined in ../../PyutConsts.py

        @return int : Link type
        @author Nicolas Dubois
        """
        return self._oglLink.getPyutObject().getType()
        



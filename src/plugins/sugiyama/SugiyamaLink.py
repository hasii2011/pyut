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

from plugins.sugiyama.ALayoutLink import *
from plugins.sugiyama.VirtualSugiyamaNode import *

# Miniogl import
from MiniOgl.ControlPoint import *


class SugiyamaLink(ALayoutLink):
    """
    SugiyamaLink: link of the Sugiyama graph.

    Instancied by: ../ToSugiyama.py

    :author: Nicolas Dubois
    :contact: nicdub@gmx.ch
    :version: $Revision: 1.4 $
    """
    def __init__(self, oglObject):
        """
        Constructor.

        @author Nicolas Dubois
        """
        # Call father's initialization
        ALayoutLink.__init__(self, oglObject)
        self.__virtualNodes = []

    def fixControlPoints(self):
        """
        Fix a graphical path with control points.

        @author Nicolas Dubois
        """
        # Clear the actual control points of the link (not the anchor points)
        self.removeAllControlPoints()

        # Current x coordinate of the link
        x = self.getSrcAnchorPos()[0]

        # For all virtual nodes, add control points to pass through
        for vnode in self.__virtualNodes:
            #~ print "Virtual node"
            (xvnode, yvnode) = vnode.getPosition()
            # If link goes to up-left
            if x > xvnode:
                # Find the first real node on the right of the virtual node
                neighbor = vnode.getRightNode()
                while isinstance(neighbor, VirtualSugiyamaNode) and \
                    neighbor is not None:

                    # Try next neighbor
                    neighbor = neighbor.getRightNode()

                # If real node found
                if neighbor is not None:
                    ctrlPoint = ControlPoint(xvnode,
                        neighbor.getPosition()[1] + neighbor.getSize()[1])
                    self.addControlPoint(ctrlPoint)

            else: # If link goes to up-right
                # Find the first real node on the left of the virtual node
                neighbor = vnode.getLeftNode()
                while isinstance(neighbor, VirtualSugiyamaNode) and \
                    neighbor is not None:

                    # Try next neighbor
                    neighbor = neighbor.getLeftNode()

                # If real node found
                if neighbor is not None:
                    ctrlPoint = ControlPoint(xvnode,
                        neighbor.getPosition()[1] + neighbor.getSize()[1])
                    self.addControlPoint(ctrlPoint)

            ctrlPoint = ControlPoint(xvnode, yvnode)#,self._oglLink)
            self.addControlPoint(ctrlPoint)

    def addVitualNode(self, node):
        """
        Add a virtual node.

        A virtual node is inserted in long links which cross a level. If the
        link crosses more than one level, insert virtual nodes, ordered
        from source to destination (son to father - bottom-up).

        @param VirtualSugiyamaNode node : virtual node
        @author Nicolas Dubois
        """
        self.__virtualNodes.append(node)

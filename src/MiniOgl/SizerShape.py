from MiniOgl.PointShape import PointShape

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
__version__   = "$Id: SizerShape.py,v 1.6 2004/12/10 23:31:59 dutoitc Exp $"



__all__ = ["SizerShape"]


class SizerShape(PointShape):
    """
    A sizer, to resize other shapes.

    Exported methods:
    -----------------

    __init__(self, x, y, parent)
        Constructor.
    SetPosition(self, x, y)
        Change the position of the shape, if it's draggable.
    SetMoving(self, state)
        Set the moving flag.

    @author Laurent Burgbacher <lb@alawa.ch>
    """
    def __init__(self, x, y, parent):
        """
        Constructor.

        @param double x, y : position of the point
        @param Shape parent : parent shape
        """
        #  print ">>>SizerShape", x, y
        PointShape.__init__(self, x, y, parent)
        self._moving = True

    def Draw(self, dc, withChildren=True):
        #  TODO : Remove this. This is for debugging purpose. CD
        PointShape.Draw(self, dc, withChildren)
        # Note : This functions seems to be needed to display anchors
        #        on rectangle when moving them, but not for lines,
        #        single anchors, ...
        pass

    def SetPosition(self, x, y):
        """
        Change the position of the shape, if it's draggable.

        @param double x, y : new position
        """
        self._parent.Resize(self, x, y)
        # the position of the sizer is not changed, because it is relative
        # to the parent

    def SetMoving(self, state):
        """
        Set the moving flag.
        If setting a sizer moving, the parent will also be set moving.

        @param
        @return
        @since 1.0
        """
        PointShape.SetMoving(self, True)
        # a sizer is always moving
        self._parent.SetMoving(state)

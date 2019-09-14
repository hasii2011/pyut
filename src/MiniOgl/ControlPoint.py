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
__version__   = "$Id: ControlPoint.py,v 1.3 2004/06/16 19:33:18 dutoitc Exp $"

from __future__                import division
#from wxPython.wx               import *
from LinePoint                 import LinePoint

__all__ = ["ControlPoint"]

class ControlPoint(LinePoint):
    """
    This is a point which guides lines.
    A control point must be linked to a line, it has no life by itself.
    If you remove the last line of a control point, the control point will
    be automatically erased.

    Exported methods:
    -----------------

    __init__(self, x, y, parent=None)
        Constructor.
    RemoveLine(self, line)
        Remove a line from the point.

    @author Laurent Burgbacher <lb@alawa.ch>
    """
    def __init__(self, x, y, parent=None):
        """
        Constructor.

        @param double x, y : position of the point
        @param Shape parent : parent shape
        """
        LinePoint.__init__(self, x, y, parent)
        self.SetVisible(False)

    #>------------------------------------------------------------------------

    def RemoveLine(self, line):
        """
        Remove a line from the point.
        If there are no more lines for this point, it is automatically
        detached.

        @param LineShape line
        """
        super(ControlPoint, self).RemoveLine(line)
        if len(self._lines) == 0:
            self.Detach()

    #>------------------------------------------------------------------------

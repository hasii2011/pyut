#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2002, Laurent Burgbacher, Eivd.
# Visit http://www.eivd.ch
#
# This file is part of Pyut.
#
# Pyut is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Pyut is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pyut; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

__author__    = "Laurent Burgbacher, lb@alawa.ch, Eivd"
__copyright__ = "Copyright 2002, Laurent Burgbacher, Eivd"
__license__   = "Released under the terms of the GNU General Public Licence V2"
__date__      = "2002-04-25"
__version__   = "$Id: PyutScripting.py,v 1.4 2006/02/04 22:01:01 dutoitc Exp $"

from __future__                 import division
#from wxPython.wx                import *

__all__ = ["PyutScripting"]

class PyutScripting(object):
    def __init__(self, mainFrame):
        self._mainFrame = mainFrame
        self._params = []

    #>------------------------------------------------------------------------

    def setParams(self, params):
        self._params = params

    #>------------------------------------------------------------------------

    def openFile(self, filename):
        self._mainFrame.loadByFilename(filename)

    #>------------------------------------------------------------------------

    def getPlugins(self):
        return self._mainFrame.plugMgr.getOutputPlugins()

    #>------------------------------------------------------------------------

    def exportToPS(self, filename):
        self._mainFrame.printDiagramToPostscript(filename)

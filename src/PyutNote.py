#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.3 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2001-11-14"

from PyutLinkedObject import *

class PyutNote(PyutLinkedObject):
    """
    Data layer representation of a UML note.
    There are currently no supplementary attributes for this class, it
    may just be linked with other objects.

    :version: $Revision: 1.3 $
    :author: Philippe Waelti
    :contact: pwaelti@eivd.ch
    """
    def __init__(self, name=""):
        """
        Constructor.
        @param String name : The note

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        PyutLinkedObject.__init__(self, name)

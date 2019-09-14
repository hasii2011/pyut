#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.3 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2002-1-9"

class AbstractClassError(Exception): pass

class Io:
    """
    Base Class to save or open file format contains diarams.

    @version $Revision: 1.3 $
    """
    def save(self, fileName, oglDiagram):
        """
        To save save diagram in file.

        @param String fileName : the file name who is saved diagram
        @param OglDiagram      : the diagram who is information

        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        raise AbstractClassError()
    #>------------------------------------------------------------------------

    def open(self, fileName, oglDiagram):
        """
        To open a file and creating diagram.

        @param String fileName : the file name who is saved diagram
        @param OglDiagram      : the diagram who is information

        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        raise AbstractClassError()

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.3 $"
__author__  = "EI5, eivd, Group Burgbacher - Waelti"
__date__    = "2001-12-12"

class LineSplitter:
    """
    This class offers a text split algorithm.
    You can give your text to the method split and this will return you
    a list of string, length of text for each string <= total width.

    Sample of use::
        text = "Hi, how are you today ?"
        splittedLines = LineSplitter().split(text, dc, 12)

    :version: $Revision: 1.3 $
    :author: Philippe Waelti
    :contact: pwaelti@eivd.ch
    """

    def split(self, text, dc, width):
        """
        Split a text in lines fitting in width pixels.

        @param String text : text to split
        @param wxDC dc
        @param int width : width for the text, in pixels
        @return String [] : a list of strings fitting in width pixels
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        lines = text.splitlines()
        newLines = []
        for line in lines:
            words = line.split()
            wline = 0
            newLine = ""
            for word in words:
                word += " "
                wword = dc.GetTextExtent(word)[0]
                if wline + wword <= width:
                    newLine += word
                    wline += wword
                else:
                    newLines.append(newLine[:-1]) # remove last space
                    newLine = word
                    wline = wword
            newLines.append(newLine[:-1])
        return newLines

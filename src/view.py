#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# MODIFICATIONS :
# C.Dutoit, 16.11.2002 : Added beautification
from zlib import *
import sys
INDENT_STR = "   "          # Standard indentation


##############################################################################
class XMLDocument:

    #>----------------------------------------------------------------------
    def __init__(self, str):
        "Constructor"
        self._str = str
        self._currentposition = 0

    #>----------------------------------------------------------------------
    def eof(self):
        "Test if we're on the end of file"
        return self._currentposition>=len(self._str)-1

    #>----------------------------------------------------------------------
    def nextTag(self):
        "Return the next tag"
        # get position
        start = self._str[self._currentposition:].find("<") + self._currentposition
        end   = self._str[start:].find(">") + self._currentposition +1
        self._currentposition = end 
        return self._str[start:end+1]



#>----------------------------------------------------------------------
def beautifyXML(str):
    "Beautify a xml document"

    # init
    document = XMLDocument(str)
    indent = -1
    ret = ""
    
    # beautify
    while not document.eof():
        tag = document.nextTag()

        if tag[1]=="?" and tag[-2]=="?":
            ret += indent * INDENT_STR + tag + "\n"
        elif tag[1]=="/":
            ret += indent * INDENT_STR + tag + "\n"
            indent-=1
        elif tag[-2]=="/":    
            ret += (indent+1) * INDENT_STR + tag + "\n"
        else:
            indent+=1
            ret += indent * INDENT_STR + tag + "\n"

    return ret



try:
    print beautifyXML(decompress(open(sys.argv[1]).read()))
except:
    print beautifyXML(open(sys.argv[1]).read())
#print decompress(open(sys.argv[1]).read())

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.8 $"
__author__  = "EI6, eivd, Group Dutoit - Roux"
__date__    = "2002-03-14"
__PyUtVersion__ = "1.0"
# local TODO :
# - do more tests
# - add shortcuts (appframe.py)

#from wxPython.wx import *
#import wx
from UmlClassDiagramsFrame import UmlClassDiagramsFrame
from UmlSequenceDiagramsFrame import UmlSequenceDiagramsFrame
from AppFrame import *
from pyutUtils import displayError
from PyutConsts import *


#>-----------------------------------------------------------------------

def shorterFilename(filename):
    """
    Return a shorter filename to display

    @param filename file name to display
    @return String better file name
    @since 1.0
    @author C.Dutoit <dutoitc@hotmail.com>
    """
    import os
    return os.path.split(filename)[1]


##############################################################################

class PyutDocument:
    """
    Document : Contain a document : frames, properties, ...

    :author: C.Dutoit 
    :contact: <dutoitc@hotmail.com>
    :version: $Revision: 1.8 $
    """

    #>------------------------------------------------------------------------

    def __init__(self, parentFrame, project, type):
        """
        Constructor.

        @param type : Type of document; one cited in PyutConsts.py
        @author C.Dutoit
        """
        self._parentFrame = None
        self._project = project
        self._treeRoot = None      # Root of the project entry in the tree
        self._treeRootParent = None# Parent of the project root entry
        self._tree     = None      # Tree i'm belonging to
        self._type     = type

        print "PyutDocument using type " , type
        if (type==CLASS_DIAGRAM):
            self._title = DiagramsLabels[type]
            self._frame = UmlClassDiagramsFrame(parentFrame)
        elif (type==SEQUENCE_DIAGRAM):
            self._title = DiagramsLabels[type]
            self._frame = UmlSequenceDiagramsFrame(parentFrame)
        elif (type==USECASE_DIAGRAM):
            self._title = DiagramsLabels[type]
            self._frame = UmlClassDiagramsFrame(parentFrame)
        else:
            displayError("Unsuported diagram type; replacing by class diagram")
            self._title = DiagramsLabels[CLASS_DIAGRAM]
            self._frame = UmlClassDiagramsFrame(parentFrame)


    #>------------------------------------------------------------------------

    def getType(self):
        """
        Return the document's type

        @author C.Dutoit
        @return String : the document's type as string
        """
        return self._type
    
    #>------------------------------------------------------------------------

    def getDiagramTitle(self):
        """
        Return the filename for captions

        @author C.Dutoit
        @return String : the caption
        """
        return self._project.getFilename() + "/" + self._title

    #>------------------------------------------------------------------------

    def getFrame(self):
        """
        Return the document's frame

        @author C.Dutoit
        @return xxxFrame this document's frame
        """
        return self._frame

    #>------------------------------------------------------------------------

    def addToTree(self, tree, root):
        self._tree = tree
        self._treeRootParent = root
        # Add the project to the project tree
        self._treeRoot = tree.AppendItem(
                         self._treeRootParent, 
                         self._title)
        #self._tree.Expand(self._treeRoot)
        self._tree.SetPyData(self._treeRoot, self._frame)

    #>------------------------------------------------------------------------
    
    def updateTreeText(self):
        """
        Update the tree text for this document

        @author C.Dutoit
        """
        self._tree.SetItemText(self._treeRoot, self._title)

    #>------------------------------------------------------------------------

    def removeFromTree(self):
        """
        Remove this document.
        """
        # Remove from tree
        self._tree.Delete(self._treeRoot)

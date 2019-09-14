#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.5 $"
__author__  = "EI5, eivd, Group Burgbacher - Waelti"
__date__    = "2002-02-22"

# Types of OGL Links
[
    OGL_ASSOCIATION,
    OGL_AGGREGATION,
    OGL_COMPOSITION,
    OGL_INHERITANCE,
    OGL_INTERFACE,
    OGL_NOTELINK,
    OGL_SD_MESSAGE,
] = range(7)

# Cardinal points, taken to correspond to the attachment points of the OglClass
NORTH = 0
EAST  = 1
SOUTH = 2
WEST  = 3


############################### Diagrams type ################################

# Types of diagrams
[
    CLASS_DIAGRAM, SEQUENCE_DIAGRAM, USECASE_DIAGRAM, UNKNOWN_DIAGRAM
] = range(4)

# Types of diagrams labels
DiagramsLabels = {
    CLASS_DIAGRAM    : _("Class Diagram"),
    SEQUENCE_DIAGRAM : _("Sequence Diagram"),
    USECASE_DIAGRAM  : _("Use-Case Diagram"),
    UNKNOWN_DIAGRAM  : _("Unknown Diagram"),
}

DiagramsStrings = {
    CLASS_DIAGRAM        : "CLASS_DIAGRAM",
    SEQUENCE_DIAGRAM     : "SEQUENCE_DIAGRAM",
    USECASE_DIAGRAM      : "USECASE_DIAGRAM",
    UNKNOWN_DIAGRAM      : "UNKNOWN_DIAGRAM",
}

def diagramTypeAsString(type):
    return DiagramsStrings[type]

def diagramTypeFromString(string):
    for key in DiagramsStrings:
        if DiagramsStrings[key]==string:
            return key
    return UNKNOWN_DIAGRAM


##############################################################################
# Default filename
DefaultFilename=_("Untitled.put")

    

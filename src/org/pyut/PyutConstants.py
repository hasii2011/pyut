
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

# Types of diagrams
[
    CLASS_DIAGRAM, SEQUENCE_DIAGRAM, USECASE_DIAGRAM, UNKNOWN_DIAGRAM
] = range(4)

# Types of diagrams labels
DiagramsLabels = {
    CLASS_DIAGRAM: "Class Diagram",
    SEQUENCE_DIAGRAM: "Sequence Diagram",
    USECASE_DIAGRAM: "Use-Case Diagram",
    UNKNOWN_DIAGRAM: "Unknown Diagram",
}

DiagramsStrings = {
    CLASS_DIAGRAM: "CLASS_DIAGRAM",
    SEQUENCE_DIAGRAM: "SEQUENCE_DIAGRAM",
    USECASE_DIAGRAM: "USECASE_DIAGRAM",
    UNKNOWN_DIAGRAM: "UNKNOWN_DIAGRAM",
}


def diagramTypeAsString(inType):
    return DiagramsStrings[inType]


def diagramTypeFromString(string):
    for key in DiagramsStrings:
        if DiagramsStrings[key] == string:
            return key
    return UNKNOWN_DIAGRAM


DefaultFilename = "Untitled.put"
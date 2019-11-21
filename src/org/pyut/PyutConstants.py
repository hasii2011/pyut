
from org.pyut.general.Globals import _

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


class PyutConstants:
    DefaultFilename = _("Untitled.put")

    @staticmethod
    def diagramTypeAsString(inType):
        return DiagramsStrings[inType]

    @staticmethod
    def diagramTypeFromString(string):
        for key in DiagramsStrings:
            if DiagramsStrings[key] == string:
                return key
        return UNKNOWN_DIAGRAM

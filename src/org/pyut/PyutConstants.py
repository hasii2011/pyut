
from org.pyut.general.Globals import _

from org.pyut.enums.DiagramType import DiagramType

# Types of diagrams labels
DiagramsLabels = {
    DiagramType.CLASS_DIAGRAM:    "Class Diagram",
    DiagramType.SEQUENCE_DIAGRAM: "Sequence Diagram",
    DiagramType.USECASE_DIAGRAM:  "Use-Case Diagram",
    DiagramType.UNKNOWN_DIAGRAM:  "Unknown Diagram",
}

DiagramsStrings = {
    DiagramType.CLASS_DIAGRAM:    "CLASS_DIAGRAM",
    DiagramType.SEQUENCE_DIAGRAM: "SEQUENCE_DIAGRAM",
    DiagramType.USECASE_DIAGRAM:  "USECASE_DIAGRAM",
    DiagramType.UNKNOWN_DIAGRAM:  "UNKNOWN_DIAGRAM",
}


class PyutConstants:

    DefaultFilename:        str = _("Untitled.put")
    THE_GREAT_MAC_PLATFORM: str = 'darwin'

    @staticmethod
    def diagramTypeAsString(inType):
        return DiagramsStrings[inType]

    @staticmethod
    def diagramTypeFromString(string):
        """
        TODO:  This code belongs in the enumeration class

        Args:
            string:   A String that can be matched to the enumeration

        Returns:

        """
        for key in DiagramsStrings:
            if DiagramsStrings[key] == string:
                return key
        return DiagramType.UNKNOWN_DIAGRAM

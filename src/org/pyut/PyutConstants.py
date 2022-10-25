
# noinspection PyProtectedMember
from org.pyut.general.Globals import _

from org.pyut.enums.DiagramType import DiagramType

# noinspection PyPackageRequirements
from deprecated import deprecated

# Types of diagrams labels
# TODO:  Make this an enumeration
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

    PYUT_EXTENSION:       str = '.put'
    XML_EXTENSION:        str = '.xml'
    DEFAULT_PROJECT_NAME: str = 'Untitled'
    DEFAULT_FILE_NAME:    str = f'{DEFAULT_PROJECT_NAME}{PYUT_EXTENSION}'

    APP_MODE:         str = 'APP_MODE'
    # noinspection SpellCheckingInspection
    PYTHON_OPTIMIZE:  str = 'PYTHONOPTIMIZE'

    THE_GREAT_MAC_PLATFORM: str = 'darwin'

    # Used to log error messages or general logging messages by using the standard
    # Python logging mechanism
    # Needs to match the name in loggingConfiguration.json
    MAIN_LOGGING_NAME:     str = "Pyut"

    # @staticmethod
    # def diagramTypeAsString(inType):
    #     return DiagramsStrings[inType]
    #
    # @staticmethod
    # @deprecated
    # def diagramTypeFromString(string):
    #     """
    #     TODO:  This code belongs in the enumeration class
    #
    #     Args:
    #         string:   A String that can be matched to the enumeration
    #
    #     Returns:
    #
    #     """
    #     for key in DiagramsStrings:
    #         if DiagramsStrings[key] == string:
    #             return key
    #     return DiagramType.UNKNOWN_DIAGRAM

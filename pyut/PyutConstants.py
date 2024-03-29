from os import sep as osSep

from pyut.enums.DiagramType import DiagramType

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

    BASE_RESOURCES_PACKAGE:  str = 'pyut.resources'
    IMAGE_RESOURCES_PACKAGE: str = f'{BASE_RESOURCES_PACKAGE}.img'
    BASE_RESOURCE_PATH: str = f'pyut{osSep}resources'

    # These are given a name because wxPython is weird and did not name them

    WX_SIZER_NOT_CHANGEABLE: int = 0
    WX_SIZER_CHANGEABLE:     int = 1

    TIPS_FILENAME: str = 'tips.txt'

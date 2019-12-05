
from enum import Enum


class ActionCallbackType(Enum):

    NEW_ACTION        = 1
    NEW_PROJECT       = 2
    NEW_CLASS_DIAGRAM = 3
    NEW_SEQUENCE_DIAGRAM = 4444
    NEW_USE_CASE_DIAGRAM = 5
    FILE_OPEN            = 6
    FILE_SAVE            = 7
    FILE_SAVE_AS         = 8
    UNDO                 = 9
    REDO                 = 10
    INSERT_PROJECT       = 11
    PROJECT_CLOSE        = 12
    REMOVE_DOCUMENT      = 13
    PRINT_SETUP          = 14
    PRINT_PREVIEW        = 15
    PRINT                = 16
    PYUT_PROPERTIES      = 17
    EXIT_PROGRAM         = 18
    PROGRAM_ABOUT        = 19
    HELP_INDEX           = 20
    HELP_VERSION         = 21
    HELP_WEB             = 22
    ADD_PYUT_HIERARCHY   = 23
    ADD_OGL_HIERARCHY    = 24
    EXPORT_BMP           = 25
    EXPORT_PNG           = 26
    EXPORT_JPG           = 27
    EXPORT_PS            = 28
    EXPORT_PDF           = 29
    EDIT_CUT             = 30
    EDIT_COPY            = 31
    EDIT_PASTE           = 32
    SELECT_ALL           = 33
    EXPORT               = 34
    IMPORT               = 35
    TOOL_PLUGIN          = 36
    TOOL_BOX_MENU        = 37

    LAST_OPENED_FILES    = 77
    CLOSE                = 666
    DEBUG                = 0xDEADBEEF

    def __str__(self):
        return str(self.name)

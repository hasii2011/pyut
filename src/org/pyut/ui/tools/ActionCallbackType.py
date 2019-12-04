
from enum import Enum


class ActionCallbackType(Enum):

    NEW_ACTION        = 1
    NEW_PROJECT       = 2
    NEW_CLASS_DIAGRAM = 3
    NEW_SEQUENCE_DIAGRAM = 4
    NEW_USE_CASE_DIAGRAM = 5
    FILE_OPEN            = 6
    FILE_SAVE            = 7
    UNDO                 = 8
    REDO                 = 9




    def __str__(self):
        return str(self.name)

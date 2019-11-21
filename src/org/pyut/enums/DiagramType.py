from enum import Enum


class DiagramType(Enum):

    CLASS_DIAGRAM    = 0
    SEQUENCE_DIAGRAM = 1
    USECASE_DIAGRAM  = 2
    UNKNOWN_DIAGRAM  = 3

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return self.__str__()

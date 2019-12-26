
from enum import Enum


class DTDElementTypes(Enum):

    EMPTY_ELEMENT         = 1
    ANY_CONTENT_ELEMENT   = 2
    PCDATA_ELEMENT        = 3
    MIN_SINGLE_OCCURRENCE = 4
    MIXED_CONTENT_ELEMENT = 5
    SEQUENCE_ELEMENT      = 6     # Sequence maybe a single element;  Zero or more is subtype 2

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f'{self.name} - {self.__str__()}'

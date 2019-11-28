
from enum import Enum


class ErrorViewTypes(Enum):

    GRAPHIC_ERROR_VIEW = 1
    TEXT_ERROR_VIEW    = 2
    RAISE_ERROR_VIEW   = 3

    def __str__(self):
        return str(self.name)

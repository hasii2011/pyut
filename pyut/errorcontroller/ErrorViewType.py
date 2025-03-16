
from enum import Enum


class ErrorViewType(Enum):

    GRAPHIC_ERROR_VIEW = 'GraphicErrorView'
    TEXT_ERROR_VIEW    = 'TextErrorView'
    RAISE_ERROR_VIEW   = 'RaiseErrorView'

    def __str__(self):
        return str(self.name)

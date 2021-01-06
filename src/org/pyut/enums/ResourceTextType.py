
from enum import Enum


class ResourceTextType(Enum):

    INTRODUCTION_TEXT_TYPE = 'Kilroy-Pyut.txt'
    HELP_TEXT_TYPE         = 'Help.txt'
    KUDOS_TEXT_TYPE        = 'Kudos.txt'
    VERSION_TEXT_TYPE      = 'version.txt'

    def __str__(self):
        return str(self.name)

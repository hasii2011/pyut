
from enum import Enum


class AttachmentPoint(Enum):
    """
    Cardinal points, taken to correspond to the attachment points of the OglClass
    """
    NORTH = 0
    EAST  = 1
    SOUTH = 2
    WEST  = 3

    def __str__(self):
        return str(self.name)

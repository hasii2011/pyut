
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

    @staticmethod
    def toEnum(strValue: str) -> 'AttachmentPoint':
        """
        Converts the input string to the attachment location
        Args:
            strValue:   A serialized string value

        Returns:  The visibility enumeration
        """
        canonicalStr: str = strValue.strip(' ')

        if canonicalStr == 'NORTH':
            return AttachmentPoint.NORTH
        elif canonicalStr == 'EAST':
            return AttachmentPoint.EAST
        elif canonicalStr == 'WEST':
            return AttachmentPoint.WEST
        elif canonicalStr == 'SOUTH':
            return AttachmentPoint.SOUTH
        else:
            print(f'Warning: did not recognize this attachment point: {canonicalStr}')
            return AttachmentPoint.NORTH

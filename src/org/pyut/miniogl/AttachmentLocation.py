
from enum import Enum


class AttachmentLocation(Enum):
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
    def toEnum(strValue: str) -> 'AttachmentLocation':
        """
        Converts the input string to the attachment location
        Args:
            strValue:   A serialized string value

        Returns:  The visibility enumeration
        """
        canonicalStr: str = strValue.strip(' ')

        if canonicalStr == 'NORTH':
            return AttachmentLocation.NORTH
        elif canonicalStr == 'EAST':
            return AttachmentLocation.EAST
        elif canonicalStr == 'WEST':
            return AttachmentLocation.WEST
        elif canonicalStr == 'SOUTH':
            return AttachmentLocation.SOUTH
        else:
            print(f'Warning: did not recognize this attachment point: {canonicalStr}')
            return AttachmentLocation.NORTH

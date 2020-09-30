from enum import Enum


class LinkType(Enum):

    """
     Types of UML Links
    """
    ASSOCIATION = 0
    AGGREGATION = 1
    COMPOSITION = 2
    INHERITANCE = 3
    INTERFACE   = 4
    NOTELINK    = 5
    SD_MESSAGE  = 6

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return self.name

    @staticmethod
    def toEnum(strValue: str) -> 'LinkType':
        """
        Converts the input string to the link type enum
        Args:
            strValue:   The serialized string representation

        Returns:  The link type enumeration
        """
        canonicalStr: str = strValue.lower().strip(' ')
        if canonicalStr == 'association':
            return LinkType.ASSOCIATION
        elif canonicalStr == 'aggregation':
            return LinkType.AGGREGATION
        elif canonicalStr == 'composition':
            return LinkType.COMPOSITION
        elif canonicalStr == 'inheritance':
            return LinkType.INHERITANCE
        elif canonicalStr == 'interface':
            return LinkType.INTERFACE
        elif canonicalStr == 'notelink':
            return LinkType.NOTELINK
        elif canonicalStr == 'sd_message':
            return LinkType.SD_MESSAGE
        else:
            print(f'Warning: did not recognize this link type: {canonicalStr}')
            return LinkType.ASSOCIATION

from enum import Enum


class PyutLinkType(Enum):

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
    def toEnum(strValue: str) -> 'PyutLinkType':
        """
        Converts the input string to the link type enum
        Args:
            strValue:   The serialized string representation

        Returns:  The link type enumeration
        """
        canonicalStr: str = strValue.lower().strip(' ')
        if canonicalStr == 'association':
            return PyutLinkType.ASSOCIATION
        elif canonicalStr == 'aggregation':
            return PyutLinkType.AGGREGATION
        elif canonicalStr == 'composition':
            return PyutLinkType.COMPOSITION
        elif canonicalStr == 'inheritance':
            return PyutLinkType.INHERITANCE
        elif canonicalStr == 'interface':
            return PyutLinkType.INTERFACE
        elif canonicalStr == 'notelink':
            return PyutLinkType.NOTELINK
        elif canonicalStr == 'sd_message':
            return PyutLinkType.SD_MESSAGE
        else:
            print(f'Warning: LinkType.toEnum - Do not recognize link type: `{canonicalStr}`')
            return PyutLinkType.ASSOCIATION

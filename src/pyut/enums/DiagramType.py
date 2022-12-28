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

    @classmethod
    def toEnum(cls, strValue: str) -> 'DiagramType':
        """
        Converts the input string to the correct diagram type
        Args:
            strValue:   A string value

        Returns:  The diagram type enumeration
        """
        canonicalStr: str = strValue.strip(' ').lower()

        if canonicalStr == 'class_diagram':
            return DiagramType.CLASS_DIAGRAM
        elif canonicalStr == 'sequence_diagram':
            return DiagramType.SEQUENCE_DIAGRAM
        elif canonicalStr == 'usecase_diagram':
            return DiagramType.USECASE_DIAGRAM
        else:
            print(f'Warning: did not recognize this diagram type: {canonicalStr}')
            return DiagramType.CLASS_DIAGRAM

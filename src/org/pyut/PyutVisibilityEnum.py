
from enum import Enum


class PyutVisibilityEnum(Enum):

    PRIVATE   = '-'
    PROTECTED = '#'
    PUBLIC    = '+'

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f'{self.name} - {self.__str__()}'

    @staticmethod
    def toEnum(strValue: str) -> 'PyutVisibilityEnum':
        """
        Converts the input string to the visibility enum
        Args:
            strValue:   A serialized string value

        Returns:  The visibility enumeration
        """
        canonicalStr: str = strValue.lower().strip(' ')
        if canonicalStr == 'public':
            return PyutVisibilityEnum.PUBLIC
        elif canonicalStr == 'private':
            return PyutVisibilityEnum.PRIVATE
        elif canonicalStr == 'protected':
            return PyutVisibilityEnum.PROTECTED
        else:
            print(f'Warning: did not recognize this visibility type: {canonicalStr}')
            return PyutVisibilityEnum.PUBLIC

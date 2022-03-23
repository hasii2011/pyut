
from typing import List

from enum import Enum
from typing import cast


class PyutVisibilityEnum(Enum):

    PRIVATE   = '-'
    PROTECTED = '#'
    PUBLIC    = '+'

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f'{self.name} - {self.__str__()}'

    @staticmethod
    def values() -> List[str]:
        retList: List[str] = []
        for valEnum in PyutVisibilityEnum:
            val:    PyutVisibilityEnum = cast(PyutVisibilityEnum, valEnum)
            retList.append(val.__str__())
        return retList

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
        elif canonicalStr == '+':
            return PyutVisibilityEnum.PUBLIC
        elif canonicalStr == '-':
            return PyutVisibilityEnum.PRIVATE
        elif canonicalStr == '#':
            return PyutVisibilityEnum.PROTECTED
        else:
            assert False, f'Warning: PyutVisibilityEnum.toEnum - Do not recognize visibility type: `{canonicalStr}`'

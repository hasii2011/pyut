
from typing import List
from typing import cast

from enum import Enum


class PyutDisplayParameters(Enum):
    """
    Determines whether a class should display its methods parameters
    """
    DISPLAY        = 'Display'
    DO_NOT_DISPLAY = 'DoNotDisplay'
    UNSPECIFIED    = 'Unspecified'

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f'{self.name} - {self.__str__()}'

    @staticmethod
    def values() -> List[str]:
        retList: List[str] = []
        for pdp in PyutDisplayParameters:

            val:    PyutDisplayParameters = cast(PyutDisplayParameters, pdp)
            retList.append(val.__str__())
        return retList

    @staticmethod
    def toEnum(strValue: str) -> 'PyutDisplayParameters':
        """
        Converts the input string to the visibility enum
        Args:
            strValue:   A serialized string value

        Returns:  The visibility enumeration
        """
        canonicalStr: str = strValue.lower().strip(' ')
        if canonicalStr == 'display':
            return PyutDisplayParameters.DISPLAY
        elif canonicalStr == 'donotdisplay':
            return PyutDisplayParameters.DO_NOT_DISPLAY
        elif canonicalStr == 'unspecified':
            return PyutDisplayParameters.UNSPECIFIED
        else:
            print(f'Warning: did not recognize this parameter visibility type: {canonicalStr}')
            return PyutDisplayParameters.UNSPECIFIED

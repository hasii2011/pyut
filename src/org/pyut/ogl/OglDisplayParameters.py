
from typing import List
from typing import cast

from enum import Enum


class OglDisplayParameters(Enum):
    """
    Determines whether a class should display its' methods parameters
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
        for val in OglDisplayParameters:
            val:    OglDisplayParameters = cast(OglDisplayParameters, val)
            retList.append(val.__str__())
        return retList

    @staticmethod
    def toEnum(strValue: str) -> 'OglDisplayParameters':
        """
        Converts the input string to the visibility enum
        Args:
            strValue:   A serialized string value

        Returns:  The visibility enumeration
        """
        canonicalStr: str = strValue.lower().strip(' ')
        if canonicalStr == 'display':
            return OglDisplayParameters.DISPLAY
        elif canonicalStr == 'donotdisplay':
            return OglDisplayParameters.DO_NOT_DISPLAY
        elif canonicalStr == 'unspecified':
            return OglDisplayParameters.UNSPECIFIED
        else:
            print(f'Warning: did not recognize this parameter visibility type: {canonicalStr}')
            return OglDisplayParameters.UNSPECIFIED

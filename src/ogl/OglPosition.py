
from dataclasses import dataclass
from typing import Tuple


@dataclass
class OglPosition:

    x: int = 0
    y: int = 0

    @classmethod
    def tupleToOglPosition(cls, position: Tuple[int, int]) -> 'OglPosition':
        """
        tuple[0] is the abscissa
        tuple[1] is the ordinate

        Args:
            position:  A position in Tuple format,

        Returns:  An OglPosition object
        """

        return OglPosition(x=position[0], y=position[1])
        return OglPosition(x=position[0], y=position[1])

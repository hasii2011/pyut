from dataclasses import dataclass
from typing import List


@dataclass
class Dimensions:

    width:  int = 0
    height: int = 0

    @classmethod
    def deSerialize(cls, value: str) -> 'Dimensions':

        dimensions: Dimensions = Dimensions()

        widthHeight: List[str] = value.split(sep=',')

        assert len(widthHeight) == 2, 'Incorrectly formatted dimensions'

        try:
            dimensions.width  = int(widthHeight[0])
            dimensions.height = int(widthHeight[1])
        except ValueError as ve:
            print(f'Warning: Dimensions.deSerialize - {ve}')
            dimensions.width  = 0
            dimensions.height = 0

        return dimensions

    def __str__(self):
        return f'{self.width},{self.height}'

    def __repr__(self):
        return self.__str__()

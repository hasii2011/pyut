
from typing import List

from dataclasses import dataclass


@dataclass
class Position:

    x: int = 0
    y: int = 0

    @classmethod
    def deSerialize(cls, value: str) -> 'Position':

        position: Position = Position()

        xy: List[str] = value.split(sep=',')

        assert len(xy) == 2, 'Incorrectly formatted position'

        try:
            position.x = int(xy[0])
            position.y = int(xy[1])
        except ValueError as ve:
            print(f'Dimensions - {ve}.')
            position.x = 0
            position.y = 0

        return position

    def __str__(self):
        return f'{self.x},{self.y}'

    def __repr__(self):
        return self.__str__()

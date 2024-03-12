
from enum import Enum


class ToolBarIconSize(Enum):

    SIZE_32 = '32'
    SIZE_16 = '16'

    @classmethod
    def deSerialize(cls, value: str) -> 'ToolBarIconSize':

        toolBarIconSize: ToolBarIconSize = ToolBarIconSize.SIZE_32
        if value == '16':
            toolBarIconSize = ToolBarIconSize.SIZE_16

        return toolBarIconSize

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.__str__()

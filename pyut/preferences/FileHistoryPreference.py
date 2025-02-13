
from enum import Enum

from wx import FH_PATH_SHOW_ALWAYS
from wx import FH_PATH_SHOW_IF_DIFFERENT
from wx import FH_PATH_SHOW_NEVER


class FileHistoryPreference(Enum):
    """
    Implemented so we can present easy to read values to developer
    """
    SHOW_IF_DIFFERENT = 'If Different'
    SHOW_NEVER        = 'Never'
    SHOW_ALWAYS       = 'Always'

    @classmethod
    def toWxMenuPathStyle(cls, value: 'FileHistoryPreference') -> int | None:

        match value:
            case FileHistoryPreference.SHOW_IF_DIFFERENT:
                pathStyle: int = FH_PATH_SHOW_IF_DIFFERENT
            case FileHistoryPreference.SHOW_NEVER:
                pathStyle = FH_PATH_SHOW_NEVER
            case FileHistoryPreference.SHOW_ALWAYS:
                pathStyle = FH_PATH_SHOW_ALWAYS
            case _:
                eMsg: str = f'Unknown enumeration value {value}'
                print(eMsg)
                assert False, eMsg

        return pathStyle

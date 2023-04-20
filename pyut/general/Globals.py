
from os import sep as osSep

PYUT_PROJECT_SUFFIX:     str = '.put'
BASE_RESOURCES_PACKAGE:  str = 'pyut.resources'
IMAGE_RESOURCES_PACKAGE: str = f'{BASE_RESOURCES_PACKAGE}.img'

BASE_RESOURCE_PATH: str = f'pyut{osSep}resources'

# These are given a name because wxPython is weird and did not name them
WX_SIZER_NOT_CHANGEABLE: int = 0
WX_SIZER_CHANGEABLE:     int = 1


def _(x): return x  # Set lang function emulation


def cmp(left, right):
    """
        Python 2 standin

    Args:
        left:
        right:

    Returns:
        -1 if left < right

        0 if left = right

        1 if left > right
    """
    return (left > right) - (left < right)


def secureBool(x):
    try:
        if x is not None:
            if x in [True, "True", "true", 1, "1"]:
                return True
    except (ValueError, Exception) as e:
        print(f'secure_bool error: {e}')
    return False


def secureStr(x):
    if x is None:
        return ""
    else:
        return x

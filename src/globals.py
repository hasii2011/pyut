
from sys import exc_info
from traceback import extract_tb

IMG_PKG = "img"


def _(x): return x  # Set lang function emulation


def cmp(left, right):
    """
        Python 2 standing

    Args:
        left:
        right:

    Returns:

    """
    return (left > right) - (left < right)


def composeErrorMessageFromStack() -> str:
    """
    Does this belong in the error manager?

    Returns:

    """

    errMsg = f'The following error occured : {str(exc_info()[1])}'
    errMsg += f'\n\n---------------------------\n'
    if exc_info()[0] is not None:
        errMsg += f'Error : {exc_info()[0]}\n'
    if exc_info()[1] is not None:
        errMsg += f'Msg   : {exc_info()[1]}\n'
    if exc_info()[2] is not None:
        errMsg += 'Trace :\n'
        for el in extract_tb(exc_info()[2]):
            errMsg = errMsg + f'{str(el)}\n'

    return errMsg

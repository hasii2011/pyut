
IMG_PKG = "img"


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

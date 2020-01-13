
IMG_PKG = "org.pyut.resources.img"


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

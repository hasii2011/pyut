
def _(x): return x  # Set lang function emulation


"""
    Stolen from https://github.com/stefanholek/apply
"""


def apply(callback, args=None, kwargs=None):
    """
    This belongs in hasiihelper

    Stolen from:  https://github.com/stefanholek/apply

    Call a callable object with positional arguments taken from the
    tuple args, and keyword arguments taken from the optional dictionary
    kwargs; return its results.
    """
    if args is None:
        args = ()
    if kwargs is None:
        kwargs = {}
    return callback(*args, **kwargs)


def cmp(left, right):
    """
        Python 2 stand in

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

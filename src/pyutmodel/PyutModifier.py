
# noinspection PyPackageRequirements
from deprecated import deprecated


class PyutModifier:
    """
    Modifier for a method or param.
    These are words like:

    * "abstract"
    * "virtual"
    *"const"...

    """
    def __init__(self, modifierTypeName: str = ""):
        """

        Args:
            modifierTypeName:   for the type
        """
        self.__name: str = modifierTypeName

    @property
    def name(self) -> str:
        return self.__name

    @deprecated('Use read only property')
    def getName(self) -> str:
        """

        Returns:  The modifier name

        """
        return self.__name

    def __str__(self) -> str:
        """
        Returns:
            String representation.
        """
        return self.getName()

    def __repr__(self) -> str:
        return self.__str__()



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
        self.__name = modifierTypeName

    def getName(self) -> str:
        """

        Returns:
             name
        """
        """
        Get method, used to know the name.

        @return 
        """
        return self.__name

    def __str__(self):
        """
        Returns:
            String representation.
        """
        return self.getName()

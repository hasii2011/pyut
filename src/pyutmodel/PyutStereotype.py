

class PyutStereotype:

    def __init__(self, name=""):
        """
        Stereotype for a class or a link

        Args:
            name: for the type
        """
        self._name: str = name

    @property
    def name(self) -> str:
        return self._name

    def __str__(self):
        return f"<< {self._name} >>"


# noinspection PyPackageRequirements
from deprecated import deprecated


@deprecated('Just instantiate a new class')
def getPyutStereotype(name):
    """
    Factory method to return a new or existing PyutStereotype for the given
    name.

    @param String name : name of the stereotype
    @return PyutType : a PyutStereotype object for the given type name
    @author Laurent Burgbacher <lb@alawa.ch>
    """
    return PyutStereotype(name)


class PyutStereotype:

    def __init__(self, name=""):
        """
        Stereotype for a class, a link

        Args:
            name: for the type
        """
        self.__name: str = name

    def getStereotype(self) -> str:
        """
        Get method, used to know the stereotype.

        TODO:  This method name is confusing;  How to fix it.  -- hasii
        Fix this before externalizing data model

        Returns:  The name
        """
        return self.getName()

    def getName(self) -> str:
        """
        Get method, used to know the name.

        Returns:
                name
        """
        return self.__name

    def __str__(self):

        return f"<< {self.getName()} >>"

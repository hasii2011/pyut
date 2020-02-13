

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

        @param name for the type
        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        self.__name = name

    def getStereotype(self):
        """
        Get method, used to know the stereotype.

        @return string name
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        return self.getName()

    def getName(self):
        """
        Get method, used to know the name.

        @return string name
        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        return self.__name

    def __str__(self):

        return f"<< {self.getName()} >>"

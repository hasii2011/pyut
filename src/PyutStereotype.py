

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
        Constructor.

        @param name for the type
        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        self.__name = name

    """
    Stereotype for a class, a link

    @version $Revision: 1.4 $
    """
    def __str__(self):
        """
        String representation.

        @return type : string
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        return "<< %s >>" % (self.getName())

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



from org.pyut.PyutParam import PyutParam
from org.pyut.PyutVisibility import getPyutVisibility


class PyutField(PyutParam):
    """
    Field of a class.

    A PyutField represents a UML field in a Class of Pyut program
        - father (`PyutParam`)
        - field  visibility

    Example::
        myField = PyutField("aField", "integer", "55")

    :version: $Revision: 1.3 $
    :author:  Deve Roux
    :contact: droux@eivd.ch
    """

    def __init__(self, name: str = "", theParamType: str = "", defaultValue: str = None, visibility: str = "-"):
        """
        Constructor.

        @param string name : init name with the name
        @param string theParamType : the param type
        @defaultValue string
        @visibility   string : "+", "-", "#"
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        super().__init__(name, theParamType, defaultValue)
        self._visibility = getPyutVisibility(visibility)

    def __str__(self):
        """
        Get method, used to know the name and visibility.

        @return string field
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        return str(self._visibility) + PyutParam.__str__(self)

    def getVisibility(self):
        """
        Get Visibility, used to know the visibility ("+", "-", "#").

        @return PyutVisibility
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        return self._visibility

    def setVisibility(self, visibility):
        """
        Set method, used to change the visibility.

        @param visibility

        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        # Python 3 update
        # if type(visibility) == StringType or type(visibility) == UnicodeType:
        if type(visibility) is str:
            visibility = getPyutVisibility(visibility)
        self._visibility = visibility

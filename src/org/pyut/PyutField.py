
from org.pyut.PyutParam import PyutParam
from org.pyut.PyutVisibilityEnum import PyutVisibilityEnum


class PyutField(PyutParam):
    """
    Field of a class.

    A PyutField represents a UML field in a Class of Pyut program
        - parent (`PyutParam`)
        - field  visibility

    Example:
        myField = PyutField("aField", "integer", "55")
        or
        yourField = PyutField('anotherField', 'str', '', PyutVisibilityEnum.private)
    """

    def __init__(self, name: str = "",
                 theFieldType: str = "",
                 defaultValue: str = None,
                 visibility: PyutVisibilityEnum = PyutVisibilityEnum.PRIVATE):
        """

        Args:
            name:   The name of the field
            theFieldType: The field type
            defaultValue: Its default value if any
            visibility:  The field visibility (private, public, protected)
        """
        super().__init__(name, theFieldType, defaultValue)

        self._visibility: PyutVisibilityEnum = visibility

    def getVisibility(self) -> PyutVisibilityEnum:
        """
        Get Visibility, used to know the visibility protected, private, or public

        @return PyutVisibility
        """
        return self._visibility

    def setVisibility(self, visibility: PyutVisibilityEnum):
        """
        Set method, used to change the visibility.

        @param visibility
        """
        self._visibility = visibility

    def __str__(self):
        """
        Get method, used to know the name and visibility.

        @return string field
        """
        # return str(self._visibility) + PyutParam.__str__(self)
        return f'{self._visibility}{PyutParam.__str__(self)}'

    def __repr__(self):
        return self.__str__()

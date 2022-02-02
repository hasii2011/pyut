
# noinspection PyPackageRequirements
from deprecated import deprecated

from org.pyut.model.PyutParam import PyutParam
from org.pyut.model.PyutType import PyutType
from org.pyut.model.PyutVisibilityEnum import PyutVisibilityEnum


class PyutField(PyutParam):
    """
    A class field

    A PyutField represents a UML field
        - parent (`PyutParam`)
        - field  visibility

    Example:
        myField = PyutField("aField", "integer", "55")
        or
        yourField = PyutField('anotherField', 'str', '', PyutVisibilityEnum.Private)
    """

    def __init__(self, name: str = "", fieldType: PyutType = PyutType(''), defaultValue: str = None,
                 visibility: PyutVisibilityEnum = PyutVisibilityEnum.PRIVATE):
        """

        Args:
            name:   The name of the field
            fieldType: The field type
            defaultValue: Its default value if any
            visibility:  The field visibility (private, public, protected)
        """
        super().__init__(name, fieldType, defaultValue)

        self._visibility: PyutVisibilityEnum = visibility

    @deprecated(reason='Use the properties')
    def getVisibility(self) -> PyutVisibilityEnum:
        """

        Get Visibility, used to retrieve the visibility protected, private, or public

        @return PyutVisibility
        """
        return self._visibility

    @deprecated(reason='Use the properties')
    def setVisibility(self, visibility: PyutVisibilityEnum):
        """
        Set method, used to change the visibility.

        @param visibility
        """
        self._visibility = visibility

    @property
    def visibility(self) -> PyutVisibilityEnum:
        return self._visibility

    @visibility.setter
    def visibility(self, theNewValue: PyutVisibilityEnum):
        self._visibility = theNewValue

    def __str__(self):
        """
        Get method, used to know the name and visibility.

        @return string field
        """
        # return str(self._visibility) + PyutParam.__str__(self)
        return f'{self._visibility}{PyutParam.__str__(self)}'

    def __repr__(self):
        return self.__str__()

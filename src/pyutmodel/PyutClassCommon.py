
from typing import List

from pyutmodel.PyutField import PyutField
from pyutmodel.PyutMethod import PyutMethod


class PyutClassCommon:

    def __init__(self):

        self._description: str = ""

        self._fields:  List[PyutField]  = []
        self._methods: List[PyutMethod] = []

    def addMethod(self, newMethod: PyutMethod):
        self._methods.append(newMethod)

    @property
    def description(self) -> str:
        """
        Returns the description field.

        This description may be inserted just after the class declaration when
        using python code generation

        Returns:    Description string
        """
        return self._description

    @description.setter
    def description(self, description: str):
        """
        Description field.
        This description may be inserted just after the class declaration when
        using python code generation

        Args:
            description:    The description string

        Returns:
        """
        self._description = description

    @property
    def fields(self) -> List[PyutField]:
        """
        This is not a copy, but the original one. Any change made to it is
        directly made on the class.

        Returns:    a list of the fields.
        """
        return self._fields

    @fields.setter
    def fields(self, fields: List[PyutField]):
        """
        The fields passed are not copied, but used directly.

        Args:
            fields: Replace the actual fields by those given in the list.
        """
        self._fields = fields

    def addField(self, field):
        """
        Add a field
        @author C.Dutoit
        """
        self._fields.append(field)

    @property
    def methods(self) -> List[PyutMethod]:
        """
        This is not a copy, but the original one. Any change made to it is
        directly made on the interface.

        Returns:    a list of the methods.
        """
        return self._methods

    @methods.setter
    def methods(self, methods: List[PyutMethod]):
        """
        Replace the actual methods by those given in the list.
        The methods passed are not copied, but used directly.

        Args:
            methods: The methods
        """
        self._methods = methods

    @property
    def showMethods(self) -> bool:
        """
        `True` if we should display the methods

        Returns:  `True` if we should display the methods, else `False`
        """
        return self._showMethods

    @showMethods.setter
    def showMethods(self, value: bool):
        """
        Args:
            value:  Set to `True` to display the method, else `False`
        """
        self._showMethods = value

    @property
    def showFields(self) -> bool:
        """
        Returns:  `True` if we should display the fields, else `False`
        """
        return self._showFields

    @showFields.setter
    def showFields(self, value: bool):
        """
        Args:
            value: Indicates if we should display the fields
        """
        self._showFields = value


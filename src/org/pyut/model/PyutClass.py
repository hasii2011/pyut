
from typing import List

from org.pyut.model.PyutField import PyutField
from org.pyut.model.PyutLinkedObject import PyutLinkedObject
from org.pyut.model.PyutStereotype import getPyutStereotype


class PyutClass(PyutLinkedObject):
    """
    A standard class representation.

    A PyutClass represents a UML class in Pyut. It manages its:
        - object data fields (`PyutField`)
        - methods (`PyutMethod`)
        - fathers (`PyutClass`)(classes from which this one inherits)
        - stereotype (`PyutStereotype`)
        - a description (`string`)

    Example::
        myClass = PyutClass("Foo") # this will create a `Foo` class
        myClass.description = "Example class"

        fields = myClass.fields # this is the original fields []
        fields.append(PyutField("bar", "int"))

    """

    def __init__(self, name=""):
        """

        Args:
            name: class name
        """
        super().__init__(name)
        self._fields: List[PyutField] = []
        self._methods     = []
        self._description = ""
        self._stereotype  = None

        # Display properties
        self._showStereotype = True
        self._showMethods    = True
        self._showFields     = True

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

    def getMethods(self):
        """
        Return a list of the methods.
        This is not a copy, but the original one. Any change made to it is
        directly made on the interface.

        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        return self._methods

    def setMethods(self, methods):
        """
        Replace the actual methods by those given in the list.
        The methods passed are not copied, but used directly.

        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        self._methods = methods

    def getStereotype(self):
        """
        Return the stereotype used, or None if there's no stereotype.

        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        return self._stereotype

    def setStereotype(self, stereotype):
        """
        Replace the actual stereotype by the one given.

        @param stereotype  String or Unicode or PyutStereotype
        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        # Python 3 update
        # if type(stereotype) == StringType or type(stereotype) == UnicodeType:
        if type(stereotype) is str:
            stereotype = getPyutStereotype(stereotype)
        self._stereotype = stereotype

    def getShowStereotype(self):
        """
        Return True if we must display the stereotype

        @return boolean indicating if we must display the stereotype
        @since 1.1.1.2
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        return self._showStereotype

    def setShowStereotype(self, theNewValue: bool):
        """
        Define the showStereotype property

        @param theNewValue : boolean indicating if we must display the stereotype
        @since 1.1.1.2
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._showStereotype = theNewValue

    def getShowMethods(self):
        """
        Return True if we must display the methods

        @return boolean indicating if we must display the methods
        @since 1.1.1.2
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        return self._showMethods

    def setShowMethods(self, value):
        """
        Define the showMethods property

        @param value : boolean indicating if we must display the methods
        @since 1.1.1.2
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._showMethods = value

    def getShowFields(self):
        """
        Return True if we must display the fields

        @return boolean indicating if we must display the fields
        @since 1.1.1.2
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        return self._showFields

    def setShowFields(self, value):
        """
        Define the showFields property

        @param value : boolean indicating if we must display the fields
        @since 1.1.1.2
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._showFields = value

    def __getstate__(self):
        """
        For deepcopy operations, tells which fields to avoid copying.
        Deepcopy must not copy the links to other classes, or it would result
        in copying all the diagram.

        @since 1.5
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        aDict = self.__dict__.copy()
        aDict["_fathers"]    = []
        return aDict

    def __str__(self):
        """
        String representation.

        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        return f"Class : {self.getName()}"

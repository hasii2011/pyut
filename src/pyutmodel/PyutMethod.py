
from typing import NewType
from typing import List

from logging import Logger
from logging import getLogger

# noinspection PyPackageRequirements
from deprecated import deprecated

from pyutmodel.PyutModifier import PyutModifier
from pyutmodel.PyutParameter import PyutParameter
from pyutmodel.PyutType import PyutType
from pyutmodel.DisplayMethodParameters import DisplayMethodParameters
from pyutmodel.PyutVisibilityEnum import PyutVisibilityEnum

from pyutmodel.PyutObject import PyutObject

SourceCode     = NewType('SourceCode',     List[str])
PyutModifiers  = NewType('PyutModifiers',  List[PyutModifier])
PyutParameters = NewType('PyutParameters', List[PyutParameter])


class PyutMethod(PyutObject):
    """
    A method representation.

    A PyutMethod represents a method of a UML class in Pyut. It manages its:
    
        - visibility (`PyutVisibility`)
        - modifiers (`PyutModifier`)
        - parameters (`PyutParameter`)
        - return type (`PyutType`)
        - source code if reverse-engineered

    It has a string mode that influence the way `__str__` works. The two modes
    are:
        - `PyutGloballyDisplayParameters.WITHOUT_PARAMETERS` (default) uml string description without parameters
        - `PyutGloballyDisplayParameters.WITH_PARAMETERS`               uml string description with parameters

    You can change it with the `setStringMode` class method. This means the
    change will be done for each `PyutMethod` instance.
    """

    displayParameters: DisplayMethodParameters = DisplayMethodParameters.WITH_PARAMETERS

    def __init__(self, name="", visibility=PyutVisibilityEnum.PUBLIC, returnType: PyutType = PyutType('')):
        """

        Args:
            name:       The method name
            visibility: Its visibility public, private, protected
            returnType:  Its return value
        """
        super().__init__(name)

        self.logger: Logger = getLogger(__name__)

        self._visibility: PyutVisibilityEnum = visibility
        self._modifiers:  PyutModifiers  = PyutModifiers([])
        self._sourceCode: SourceCode     = SourceCode([])

        self._parameters:  PyutParameters = PyutParameters([])
        self._returnType: PyutType        = returnType

        self._isProperty: bool = False

    @property
    def sourceCode(self) -> SourceCode:
        return self._sourceCode

    @sourceCode.setter
    def sourceCode(self, newCode: SourceCode):
        self._sourceCode = newCode

    def getString(self) -> str:
        """
        Returns:  The method representation with parameters
        """
        return self.__stringWithParams()

    @staticmethod
    def setStringMode(mode: DisplayMethodParameters):
        """
        Set the mode for __str__.

        Args:
            mode:  The new mode
        """
        PyutMethod.displayParameters = mode

    @staticmethod
    def getStringMode() -> DisplayMethodParameters:
        """
        Returns:    The mode for __str__.
        """
        return PyutMethod.displayParameters

    @property
    def globallyDisplayParameters(self) -> DisplayMethodParameters:
        return PyutMethod.displayParameters

    @globallyDisplayParameters.setter
    def globallyDisplayParameters(self, newValue: DisplayMethodParameters):
        PyutMethod.displayParameters = newValue

    @property
    def visibility(self) -> PyutVisibilityEnum:
        return self._visibility

    @visibility.setter
    def visibility(self, theNewValue: PyutVisibilityEnum):
        self._visibility = theNewValue

    @property
    def returnType(self) -> PyutType:
        return self._returnType

    @returnType.setter
    def returnType(self, theNewValue: PyutType):
        self._returnType = theNewValue

    @property
    def parameters(self) -> PyutParameters:
        return self._parameters

    @parameters.setter
    def parameters(self, newParams: PyutParameters):
        self._parameters = newParams

    @property
    def modifiers(self) -> PyutModifiers:
        """
        This is not a copy, but the original one. Any change made to it is
        directly made on the class.

        Returns:
            Return a list of the modifiers.
        """
        return self._modifiers

    @modifiers.setter
    def modifiers(self, newModifiers: PyutModifiers):
        self._modifiers = newModifiers

    def getVisibility(self) -> PyutVisibilityEnum:
        """
        Return the visibility of the method.

        @return PyutVisibility
        """
        return self._visibility

    @property
    def isProperty(self) -> bool:
        return self._isProperty

    @isProperty.setter
    def isProperty(self, newValue: bool):
        self._isProperty = newValue

    def setVisibility(self, visibility: PyutVisibilityEnum):
        """
        Set the visibility of the method.
        """
        self._visibility = visibility

    @deprecated('Use the property')
    def getModifiers(self) -> PyutModifiers:
        """
        This is not a copy, but the original one. Any change made to it is
        directly made on the class.

        Returns:
            Return a list of the modifiers.
        """
        return self._modifiers

    @deprecated('Use the property')
    def setModifiers(self, modifiers: PyutModifiers):
        """
        Replace the actual modifiers by those given in the list.
        The methods passed are not copied, but used directly.

        Args:
            modifiers:  The replacement list
        """
        self._modifiers = modifiers

    def addModifier(self, newModifier: PyutModifier):
        """
        Adds new modifier to current list

        Args:
            newModifier:
                modifier to add to current list
        """
        self._modifiers.append(newModifier)

    @deprecated('Use parameters property')
    def getParams(self):
        """
        Return a list of the params.
        This is not a copy, but the original one. Any change made to it is
        directly made on the class.

        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        return self._parameters

    @deprecated('Use parameters property')
    def setParams(self, params):
        """
        Replace the actual params by those given in the list.
        The methods passed are not copied, but used directly.

        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        self._parameters = params

    def addParameter(self, parameter: PyutParameter):
        """
        Add a parameter.

        Args:
            parameter: parameter to add
        """
        self._parameters.append(parameter)

    @deprecated('Use returnType property')
    def getReturns(self) -> PyutType:
        """
        Return the return type.

        Returns:
            The method return type
        """
        return self._returnType

    @deprecated('Use returnType property')
    def setReturns(self, returnType: PyutType):
        """
        Set the return type of the method.

        Args:
            returnType:  A string but preferably a PyutType

        """
        pyutType: PyutType = returnType
        if type(returnType) is str:
            pyutType = PyutType(returnType)
            self.logger.warning(f'Setting return type as string is deprecated.  use PyutType')

        self._returnType = pyutType

    def methodWithParameters(self) -> str:
        return self.__stringWithParams()

    def methodWithoutParameters(self) -> str:
        return self.__stringWithoutParams()

    def __stringWithoutParams(self):
        """

        Returns:   String representation without params.
        """
        string = f'{self._visibility}{self._name}()'
        # add the parameters
        if str(self._returnType) != "":
            string = f'{string}: {self._returnType}'
        return string

    def __stringWithParams(self):
        """

        Returns: The string representation with parameters
        """
        string = f'{self._visibility}{self._name}('
        # add the params
        if not self._parameters:
            string = f'{string}  '  # to compensate the removing [:-2]
        for param in self._parameters:
            string = f'{string}{param}, '

        string = string[:-2] + ")"      # remove the last "," and add a )
        if self._returnType != "":
            string = f'{string}: {self._returnType}'

        return string

    def __str__(self) -> str:
        """
        Returns:    The configured representation
        """
        if PyutMethod.displayParameters == DisplayMethodParameters.WITH_PARAMETERS:
            return self.__stringWithParams()
        else:
            return self.__stringWithoutParams()

    def __repr__(self) -> str:
        internalRepresentation: str = (
            f'{self.__str__()} '
            f'{self.modifiers} '
            f'{self.sourceCode}'
        )
        return internalRepresentation

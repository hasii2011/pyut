
from typing import cast
from typing import List

from logging import Logger
from logging import getLogger

from org.pyut.preferences.PyutPreferences import PyutPreferences

from org.pyut.model.PyutModifier import PyutModifier
from org.pyut.model.PyutParam import PyutParam
from org.pyut.model.PyutType import PyutType
from org.pyut.model.PyutGloballyDisplayParameters import PyutGloballyDisplayParameters
from org.pyut.model.PyutVisibilityEnum import PyutVisibilityEnum

from org.pyut.model.PyutObject import PyutObject


class PyutMethod(PyutObject):

    DEFAULT_METHOD_NAME: str = 'method'

    PyutModifiers  = List[PyutModifier]
    SourceCodeType = List[str]
    PyutParameters = List[PyutParam]

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

    # define class flag to avoid PyCharm warning in get/set string mode
    __selectedStringMode = None

    def __init__(self, name="", visibility=PyutVisibilityEnum.PUBLIC, returns: PyutType = PyutType('')):
        """

        Args:
            name:       The method name
            visibility: Its visibility public, private, protected
            returns:  Its return value
        """
        super().__init__(name)

        self.logger: Logger = getLogger(__name__)

        self._visibility: PyutVisibilityEnum = visibility
        self._modifiers:  PyutMethod.PyutModifiers  = cast(PyutMethod.PyutModifiers, [])
        self._sourceCode: PyutMethod.SourceCodeType = cast(PyutMethod.SourceCodeType, [])

        self._params:  PyutMethod.PyutParameters = []
        self._returns: PyutType                  = returns

        prefs = PyutPreferences()
        if prefs.showParameters is True:
            PyutMethod.setStringMode(PyutGloballyDisplayParameters.WITH_PARAMETERS)
        else:
            PyutMethod.setStringMode(PyutGloballyDisplayParameters.WITHOUT_PARAMETERS)

    @property
    def sourceCode(self) -> SourceCodeType:
        return self._sourceCode

    @sourceCode.setter
    def sourceCode(self, newCode: SourceCodeType):
        self._sourceCode = newCode

    def getString(self) -> str:
        """
        Returns:  The method representation with parameters
        """
        return self.__stringWithParams()

    @classmethod
    def setStringMode(cls, mode: PyutGloballyDisplayParameters):
        """
        Set the mode for __str__.
        """
        if mode == PyutGloballyDisplayParameters.WITH_PARAMETERS:
            cls.__selectedStringMode = cls.__stringWithParams
        elif mode == PyutGloballyDisplayParameters.WITHOUT_PARAMETERS:
            cls.__selectedStringMode = cls.__stringWithoutParams

    @classmethod
    def getStringMode(cls) -> PyutGloballyDisplayParameters:
        """
        Get the mode for __str__.
        """
        if cls.__selectedStringMode is cls.__stringWithParams:
            return PyutGloballyDisplayParameters.WITH_PARAMETERS
        else:
            return PyutGloballyDisplayParameters.WITHOUT_PARAMETERS

    @property
    def visibility(self) -> PyutVisibilityEnum:
        return self._visibility

    @visibility.setter
    def visibility(self, theNewValue: PyutVisibilityEnum):
        self._visibility = theNewValue

    @property
    def returnType(self) -> PyutType:
        return self._returns

    @returnType.setter
    def returnType(self, theNewValue: PyutType):
        self._returns = theNewValue

    @property
    def parameters(self) -> PyutParameters:
        return self._params

    @parameters.setter
    def parameters(self, newParams: PyutParameters):
        self._params = newParams

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

    def setVisibility(self, visibility: PyutVisibilityEnum):
        """
        Set the visibility of the method.
        """
        self._visibility = visibility

    def getModifiers(self) -> PyutModifiers:
        """
        This is not a copy, but the original one. Any change made to it is
        directly made on the class.

        Returns:
            Return a list of the modifiers.
        """
        return self._modifiers

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

    def getParams(self):
        """
        Return a list of the params.
        This is not a copy, but the original one. Any change made to it is
        directly made on the class.

        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        return self._params

    def addParam(self, param):
        """
        Add a param.

        @param PyutParam param : param to add
        @since 1.6
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        self._params.append(param)

    def setParams(self, params):
        """
        Replace the actual params by those given in the list.
        The methods passed are not copied, but used directly.

        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        self._params = params

    def getReturns(self) -> PyutType:
        """
        Return the return type.

        Returns:
            The method return type
        """
        return self._returns

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

        self._returns = pyutType

    def __stringWithoutParams(self):
        """
        String representation without params.

        @since 1.7
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        string = str(self._visibility) + self._name + "()"
        # add the params
        if str(self._returns) != "":
            string += ": " + str(self._returns)
        return string

    def __stringWithParams(self):
        """
        String representation with params.

        @since 1.7
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        string = str(self._visibility) + self._name + "("
        # add the params
        # if self._params == []:
        if not self._params:
            string += "  "  # to compensate the removing [:-2]
        for param in self._params:
            string += str(param) + ", "
        string = string[:-2] + ")"      # remove the last "," and add a )
        if str(self._returns) != "":
            string += ": " + str(self._returns)
        return string

    def __str__(self):
        """
        String representation.
        Select the wanted representation with setStringMode().

        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        try:
            return self.__selectedStringMode()
        except (ValueError, Exception) as e:
            self.logger.error(f'{e}')
            return ""

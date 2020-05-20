
from logging import Logger
from logging import getLogger

from sys import exc_info
from traceback import extract_tb

from org.pyut.model.PyutObject import PyutObject
from org.pyut.model.PyutType import PyutType


class PyutParam(PyutObject):

    DEFAULT_PARAMETER_NAME: str = 'param'

    def __init__(self, name: str = DEFAULT_PARAMETER_NAME, theParameterType: PyutType = PyutType(""), defaultValue=None):
        """

        Args:
            name: init name with the name
            theParameterType: the param type

        """
        super().__init__(name)

        self.logger: Logger = getLogger(__name__)

        self._type: PyutType = theParameterType
        self._defaultValue = defaultValue

    def getType(self) -> PyutType:
        """
        Get method, used to know the type.

        @return PyutType type
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        return self._type

    def setType(self, theParameterType: PyutType):
        """
        Set parameter type

        Args:
            theParameterType:
        """

        if type(theParameterType) is str:
            self.logger.warning(f'Setting return type as string is deprecated.  use PyutType')
            theParameterType = PyutType(theParameterType)

        self.logger.debug(f'theParameterType: `{theParameterType}`')
        self._type = theParameterType

    def getDefaultValue(self) -> str:
        """
        Get method, used to know the defaultValue.

        @return string defaultValue
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        return self._defaultValue

    def setDefaultValue(self, defaultValue: str):
        """
        Set method, used to know initialize defaultValue.

        @param  defaultValue
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        self._defaultValue = defaultValue

    def __str__(self) -> str:
        """

        Returns:  String version of a PyutParm
        """
        s = self.getName()

        if str(self._type) != "":
            s += ": " + str(self._type)

        if self._defaultValue is not None:
            s += " = " + self._defaultValue

        return s

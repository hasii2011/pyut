
from typing import Any

# noinspection PyPackageRequirements
from deprecated import deprecated

from logging import Logger
from logging import getLogger

from org.pyut.model.PyutObject import PyutObject
from org.pyut.model.PyutType import PyutType


class PyutParam(PyutObject):

    DEFAULT_PARAMETER_NAME: str = 'param'

    def __init__(self, name: str = DEFAULT_PARAMETER_NAME, theParameterType: PyutType = PyutType(""), defaultValue: Any = None):
        """

        Args:
            name: init name with the name
            theParameterType: the param type

        """
        super().__init__(name)

        self.logger: Logger = getLogger(__name__)

        self._type:         PyutType = theParameterType
        self._defaultValue: Any      = defaultValue

    @deprecated(reason='Use the properties')
    def getType(self) -> PyutType:
        return self._type

    @deprecated(reason='Use the properties')
    def setType(self, theType: PyutType):
        """
        Set parameter type

        Args:
            theType:
        """
        if type(theType) is str:
            self.logger.warning(f'Setting return type as string is deprecated.  use PyutType')
            theType = PyutType(theType)

        self.logger.debug(f'theType: `{theType}`')
        self._type = theType

    @deprecated(reason='Use the properties')
    def getDefaultValue(self) -> Any:
        """
        """
        return self._defaultValue

    @deprecated(reason='Use the properties')
    def setDefaultValue(self, defaultValue: Any):
        self._defaultValue = defaultValue

    @property
    def type(self) -> PyutType:
        return self._type

    @type.setter
    def type(self, theType: PyutType):
        if type(theType) is str:
            self.logger.warning(f'Setting return type as string is deprecated.  use PyutType')
            theType = PyutType(theType)

        self.logger.debug(f'theType: `{theType}`')
        self._type = theType

    @property
    def defaultValue(self) -> Any:
        return self._defaultValue

    @defaultValue.setter
    def defaultValue(self, theNewValue: Any):
        self._defaultValue = theNewValue

    def __str__(self) -> str:
        """

        Returns:  String version of a PyutParm
        """
        s = self.getName()

        if str(self._type) != "":
            s = f'{s}: {self._type}'

        if self._defaultValue is not None:
            s = f'{s} = {self._defaultValue}'

        return s


from logging import Logger
from logging import getLogger

from sys import exc_info
from traceback import extract_tb

from org.pyut.PyutObject import PyutObject
from org.pyut.PyutType import PyutType


class PyutParam(PyutObject):

    def __init__(self, name: str = "", theParameterType: str = "", defaultValue=None):
        """

        Args:
            name: init name with the name

            theParameterType: the param type

            defaultValue:
        """
        self.logger: Logger = getLogger(__name__)
        try:
            super().__init__(name)
        except (ValueError, Exception) as e:

            self.logger.error(f'{e}')
            self.logger.error((exc_info()[0]))
            self.logger.error((exc_info()[1]))
            for el in extract_tb(exc_info()[2]):
                self.logger.error((str(el)))
            self.logger.error("===========================================")

        self._type = PyutType(theParameterType)
        self._defaultValue = defaultValue

    def getType(self) -> PyutType:
        """
        Get method, used to know the type.

        @return PyutType type
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        return self._type

    def setType(self, theParameterType):
        """
        Set method, used to know initial type.

        @param theParameterType
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        # Python 3 update
        # if type(theParameterType) == StringType or type(theParameterType) == UnicodeType:
        if type(theParameterType) is str:
            theParameterType = PyutType(theParameterType)
        self.logger.error(f'theParameterType: `{theParameterType}`')
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
        Get method, used to know the name.

        @return string param
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        @modified L. Burgbacher <lb@alawa.ch>
            don't put the : if there's no type defined
        """
        s = self.getName()

        if str(self._type) != "":
            s += " : " + str(self._type)

        if self._defaultValue is not None:
            s += " = " + self._defaultValue

        return s


from logging import Logger
from logging import getLogger

from org.pyut.model.PyutClass import PyutClass
from org.pyut.model.PyutClassCommon import PyutClassCommon
from org.pyut.model.PyutObject import PyutObject


class PyutInterface(PyutClassCommon, PyutObject):

    def __init__(self, name=""):
        """

        Args:
            name:  The object name
        """
        PyutObject.__init__(self, name)
        PyutClassCommon.__init__(self)

        self.logger: Logger = getLogger(__name__)

        self._implementingClass: PyutClass

    @property
    def implementor(self) -> PyutClass:
        """

        Returns: Return the PyutClass that implements this interface
        """
        return self._implementingClass

    @implementor.setter
    def implementor(self, implementingClass: PyutClass):
        """
        Args:
            implementingClass:  The implementor
        """
        self._implementingClass = implementingClass

    def __repr__(self):

        methodsStr = ''
        for method in self._methods:
            methodsStr = f'{methodsStr} {method} '

        return f'PyutInterface- - {self._name} {methodsStr}'

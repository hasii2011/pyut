
from logging import Logger
from logging import getLogger

from pyutmodel.ModelTypes import ClassName
from pyutmodel.ModelTypes import Implementors
from pyutmodel.PyutClassCommon import PyutClassCommon
from pyutmodel.PyutObject import PyutObject


class PyutInterface(PyutClassCommon, PyutObject):

    def __init__(self, name: str = ''):
        """

        Args:
            name:  The interface name
        """
        interfaceName: str = name

        PyutObject.__init__(self, name=interfaceName)
        PyutClassCommon.__init__(self)

        self.logger: Logger = getLogger(__name__)

        self._implementors: Implementors = Implementors([])

    @property
    def implementors(self) -> Implementors:
        return self._implementors

    @implementors.setter
    def implementors(self, newImplementors: Implementors):
        self._implementors = newImplementors

    def addImplementor(self, newClassName: ClassName):
        self._implementors.append(newClassName)

    def __repr__(self):

        methodsStr = ''
        for method in self._methods:
            methodsStr = f'{methodsStr} {method} '

        return f'PyutInterface- - {self._name} {methodsStr}'


from typing import List


from logging import Logger
from logging import getLogger

from org.pyut.model.PyutClassCommon import PyutClassCommon
from org.pyut.model.PyutObject import PyutObject


class PyutInterface(PyutClassCommon, PyutObject):

    ClassName    = str
    Implementors = List[ClassName]

    DEFAULT_INTERFACE_NAME: str = 'IClassInterface'

    def __init__(self, name: str = DEFAULT_INTERFACE_NAME):
        """

        Args:
            name:  The object name
        """
        PyutObject.__init__(self, name)
        PyutClassCommon.__init__(self)

        self.logger: Logger = getLogger(__name__)

        self._implementors: PyutInterface.Implementors = []

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


from logging import Logger
from logging import getLogger

from org.pyut.model.ModelTypes import ClassName
from org.pyut.model.ModelTypes import Implementors
from org.pyut.model.PyutClassCommon import PyutClassCommon
from org.pyut.model.PyutObject import PyutObject

from org.pyut.preferences.PyutPreferences import PyutPreferences


class PyutInterface(PyutClassCommon, PyutObject):

    def __init__(self, name: str = ''):
        """

        Args:
            name:  The interface name
        """
        interfaceName: str = name
        if name is None or name == '':
            interfaceName = PyutPreferences().interfaceName

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


from logging import Logger
from logging import getLogger

from org.pyut.model.PyutClassCommon import PyutClassCommon
from org.pyut.model.PyutObject import PyutObject


class PyutInterface(PyutClassCommon, PyutObject):

    DEFAULT_INTERFACE_NAME: str = 'IClassInterface'

    def __init__(self, name: str = DEFAULT_INTERFACE_NAME):
        """

        Args:
            name:  The object name
        """
        PyutObject.__init__(self, name)
        PyutClassCommon.__init__(self)

        self.logger: Logger = getLogger(__name__)

    def __repr__(self):

        methodsStr = ''
        for method in self._methods:
            methodsStr = f'{methodsStr} {method} '

        return f'PyutInterface- - {self._name} {methodsStr}'


from logging import Logger
from logging import getLogger

# noinspection PyPackageRequirements
from deprecated import deprecated

from enum import Enum

from pyutmodel.PyutObject import PyutObject


class PyutSDInstanceType(Enum):
    INSTANCE_TYPE_ACTOR = 'Actor'
    INSTANCE_TYPE_CLASS = 'Class'


class PyutSDInstance(PyutObject):
    """
    Data model representation of a UML Collaboration instance (C.Diagram).
    """
    def __init__(self):
        """
        Constructor.
        """
        super().__init__()
        self.logger:                 Logger = getLogger(__name__)
        self._instanceName:          str    = "Unnamed instance"
        self._lifeLineLength:        int    = 200

        self._instanceGraphicalType: PyutSDInstanceType    = PyutSDInstanceType.INSTANCE_TYPE_CLASS

    @deprecated('Use the instanceName property')
    def getInstanceName(self):
        """
        Return instance name
        """
        return self._instanceName

    @deprecated('Use the instanceName property')
    def setInstanceName(self, value):
        """
        Set this instance name

        Args:
            value:  The new instance name value
        """
        self._instanceName = value

    @deprecated('Use the instanceLifeLineLength property')
    def getInstanceLifeLineLength(self):
        """
        Return instance lifeline length
        """
        return self._lifeLineLength

    @deprecated('Use the instanceLifeLineLength property')
    def setInstanceLifeLineLength(self, value):
        """
        Set this instance lifeline length

        Args:
            value:  the new instance value
        """
        self._lifeLineLength = value

    @property
    def instanceName(self) -> str:
        """
        Return instance name
        """
        return self._instanceName

    @instanceName.setter
    def instanceName(self, value: str):
        """
        Set this instance name

        Args:
            value:  The new instance name value
        """
        self._instanceName = value

    @property
    def instanceLifeLineLength(self) -> int:
        """
        Return instance lifeline length
        """
        return self._lifeLineLength

    @instanceLifeLineLength.setter
    def instanceLifeLineLength(self, value: int):
        """
        Set this instance lifeline length

        Args:
            value:  the new instance value
        """
        self._lifeLineLength = value

    @property
    def instanceGraphicalType(self) -> PyutSDInstanceType:
        """
        Return instance graphical type

        Returns: The instance graphical type
        """
        return self._instanceGraphicalType

    @instanceGraphicalType.setter
    def instanceGraphicalType(self, value: PyutSDInstanceType):
        """
        Set this instance graphical type

        Args:
            value: The new value
        """
        self._instanceGraphicalType = value

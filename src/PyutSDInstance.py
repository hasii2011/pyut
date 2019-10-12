

from pyutUtils import *
from org.pyut.PyutObject import *


[INSTANCE_TYPE_ACTOR, INSTANCE_TYPE_CLASS] = assignID(2)

# List of possible instance type
INSTANCE_TYPES = [INSTANCE_TYPE_ACTOR, INSTANCE_TYPE_CLASS]
DEBUG = False


class PyutSDInstance(PyutObject):
    """
    Data layer representation of a UML Collaboration instance (C.Diagram).

    :version: $Revision: 1.10 $
    :author: C.Dutoit
    :contact: dutoitc@hotmail.com
    """
    def __init__(self):
        """
        Constructor.

        @author C.Dutoit
        """
        super().__init__()
        self._instanceName = "Unnamed instance"
        self._instanceGraphicalType = INSTANCE_TYPE_CLASS
        self._lifeLineLength = 200

    def getInstanceName(self):
        """
        Return instance name

        @author C.Dutoit
        """
        return self._instanceName

    def setInstanceName(self, value):
        """
        Set this instance name

        @param String value : the new instance value
        @author C.Dutoit
        """
        self._instanceName = value

    def getInstanceGraphicalType(self):
        """
        Return instance graphical type

        @author C.Dutoit
        """
        return self._instanceGraphicalType

    def setInstanceGraphicalType(self, value):
        """
        Set this instance graphical type

        @param String value : the new instance graphical type
        @author C.Dutoit
        """
        self._instanceGraphicalType = value

    def getInstanceLifeLineLength(self):
        """
        Return instance lifeline length

        @author C.Dutoit
        """
        return self._lifeLineLength

    def setInstanceLifeLineLength(self, value):
        """
        Set this instance lifeline length

        @param String value : the new instance value
        @author C.Dutoit
        """
        self._lifeLineLength = value

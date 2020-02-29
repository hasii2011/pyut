

class PyutObject:
    """
    PyutData  base object
    """

    nextId: int = 0

    def __init__(self, name=""):
        """
        Constructor.

        @param string name : init name with the name
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        self._name = name

        # Setting an arbitrary ID, for identical name purpose
        self.getNextSafeID()
        self._id = PyutObject.nextId
        PyutObject.nextId += 1

    def getNextSafeID(self):
        """
        Get the next safe id
        Verify that next id is not already used
        @author C.Dutoit
        """
        while self.isIDUsed(PyutObject.nextId):
            PyutObject.nextId += 1

    def isIDUsed(self, idToCheck):
        """
        Verify if an ID is already used

        @author C.Dutoit
        """
        from org.pyut.general import Mediator
        ctrl = Mediator.getMediator()
        for obj in [el for el in ctrl.getUmlObjects() if isinstance(el, PyutObject)]:
            if obj.getId() == idToCheck:
                return True
        return False

    def getName(self) -> str:
        """

        Returns:
            Return the object name
        """
        try:
            return self._name
        except (ValueError, Exception) as e:
            # print(f'PyutObject warning: {e}')
            return ""

    def setName(self, theName: str):
        """
        Set method, used to know initialize name.

        @param theName
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        self._name = theName

    def setId(self, theId: int):
        """
        Setting ID.

        @param theId : ID
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        self._id = theId

    def getId(self):
        """
        Get object ID.

        @return int : ID
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        return self._id
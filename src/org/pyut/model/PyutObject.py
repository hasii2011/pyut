

class PyutObject:
    BASE_OBJECT_NAME: str = 'PyutObject_'
    """
    Pyut model  base object
    """
    nextId: int = 0

    def __init__(self, name=""):
        """

        Args:
            name:   The initial object name
        """
        # Setting an arbitrary ID, for identity purposes
        self.computeNextSafeID()

        self._id: int = PyutObject.nextId
        if len(name) == 0:
            self._name = f'{PyutObject.BASE_OBJECT_NAME}{self._id:05}'
        else:
            self._name = name

        PyutObject.nextId += 1

    def computeNextSafeID(self):
        """
        Compute the next safe id
        Verify that next id is not in use
        """
        while self.isIDUsed(PyutObject.nextId):
            PyutObject.nextId += 1

    def isIDUsed(self, idToCheck) -> bool:
        """
        Determine if an ID is in use

        Args:
            idToCheck:

        Returns:
            `True` if `idToCheck` is in use, else `False`
        """
        from org.pyut.general import Mediator
        ctrl = Mediator.getMediator()
        #
        # TODO:  This seems compute heavy;  I wonder if we should have a lookup map
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
            print(f'PyutObject warning: {e}')
            return ""

    def setName(self, theName: str):
        """
        Set method, used to know initialize name.

        Args:
            theName:
        """
        self._name = theName

    def setId(self, theId: int):
        """

        Args:
            theId:  the id (doh!)
        """
        self._id = theId

    def getId(self) -> int:
        """
        Get object ID.

        Returns:
            The object ID
        """
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, theNewName: str):
        self._name = theNewName

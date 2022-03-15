
# noinspection PyPackageRequirements
from deprecated import deprecated


class PyutObject:

    """
    Pyut model  base object
    """
    nextId: int = 0

    def __init__(self, name: str = ""):
        """
        Args:
            name:   The initial object name
        """
        self._fileName: str = ""
        self._id:       int = PyutObject.nextId
        self._name:     str = name

        PyutObject.nextId += 1

    @deprecated('Use the property "name"')
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

    @deprecated('Use the property "name"')
    def setName(self, theName: str):
        """
        Set method, used to know initialize name.

        Args:
            theName:
        """
        self._name = theName

    @deprecated('Use the id property')
    def setId(self, theId: int):
        """

        Args:
            theId:  the id (doh!)
        """
        self._id = theId

    @deprecated('Use the id property')
    def getId(self) -> int:
        """
        Get object ID.

        Returns:
            The object ID
        """
        return self._id

    @deprecated('Use the fileName property')
    def setFilename(self, fileName: str):
        """
        Set the associated filename.
        This is used by the reverse engineering plugins.

        Args:
            fileName:  the file name
        """
        self._fileName = fileName

    @deprecated('Use the fileName property')
    def getFilename(self) -> str:
        """
        Get the associated fileName.

        Returns: An empty is returned if there is no fileName.
        """
        return self._fileName

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, theNewName: str):
        self._name = theNewName

    @property
    def id(self) -> int:
        """
        Returns: The object ID.
        """
        return self._id

    @id.setter
    def id(self, newValue: int):
        """
        Returns: Sets object ID.
        """
        self._id = newValue

    @property
    def fileName(self) -> str:
        return self._fileName

    @fileName.setter
    def fileName(self, theNewName: str):
        self._fileName = theNewName

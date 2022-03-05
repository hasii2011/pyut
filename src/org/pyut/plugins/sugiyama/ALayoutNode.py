

class ALayoutNode:
    """
    ALayoutNode: Interface between OglObject/PyutObject and ALayout algorithm.
    """
    def __init__(self, oglObject):
        """

        Args:
            oglObject: interfaced ogl object
        """
        self._oglObject = oglObject

    def getSize(self):
        """
        Return the class size.

        Returns: (int, int): tuple (width, height)
        """
        return self._oglObject.GetSize()

    def getPosition(self):
        """
        Get class position.

        Returns: (int, int): tuple (x, y) coordinates
        """
        return self._oglObject.GetPosition()

    def setPosition(self, x: int, y: int):
        """
        Set the class position.

        Args:
            x: absolute coordinates
            y: absolute coordinates
        """
        self._oglObject.SetPosition(x, y)

    def getName(self) -> str:
        """
        Get the name of the class.

        Returns: name of the class
        """
        return self._oglObject.pyutObject.name

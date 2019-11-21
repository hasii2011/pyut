

class ALayoutNode:
    """
    ALayoutNode: Interface between OglObject/PyutObject and ALayout algorithm.
    """
    def __init__(self, oglObject):
        """
        Constructor.

        @param OglObject oglObject: interfaced ogl object
        @author Nicolas Dubois
        """
        self._oglObject = oglObject

    def getSize(self):
        """
        Return the class size.

        @return (float, float): tuple (width, height)
        @author Nicolas Dubois
        """
        return self._oglObject.GetSize()

    def getPosition(self):
        """
        Get class position.

        @return (float, float): tuple (x, y) coordinates
        @author Nicolas Dubois
        """
        return self._oglObject.GetPosition()

    def setPosition(self, x: float, y: float):
        """
        Set the class position.

        @param  x: absolute coordinates
        @param  y : absolute coordinates
        """
        self._oglObject.SetPosition(x, y)

    def getName(self):
        """
        Get the name of the class.

        @return String: name of the class
        @author Nicolas Dubois
        """
        return self._oglObject.getPyutObject().getName()

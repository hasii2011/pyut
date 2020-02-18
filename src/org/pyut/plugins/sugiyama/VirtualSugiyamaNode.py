
from org.pyut.plugins.sugiyama.SugiyamaNode import SugiyamaNode


class VirtualSugiyamaNode(SugiyamaNode):
    """
    VirtualSugiyamaNode: a virtual node is a node on the Sugiyama graph which
    will not be visible on the diagram.  It is used to reserve space
    for the links drawing.
    """
    def __init__(self):
        """
        Constructor.

        @author Nicolas Dubois
        """
        # Call parent class initialization
        super().__init__()

        # Self fields
        self.__position = (0, 0)
        self.__size = (1, 1)

    def setSize(self, width: float, height: float):
        """
        Set the size of the node.

        Args:
            width: Size
            height: Size
        """
        self.__size = (width, height)

    def getSize(self):
        """
        Get size of node.

        @return (float, float) : (width, height)
        @author Nicolas Dubois
        """
        return self.__size

    def setPosition(self, x, y):
        """
        Set node position.

        Args:
            x: position in absolute coordinate
            y: position in absolute coordinate
        """
        self.__position = (x, y)

    def getPosition(self):
        """
        Get node position.

        @return (float, float) : (x, y) in absolute coordinate
        @author Nicolas Dubois
        """
        return self.__position

    def __repr__(self):
        return f'VirtualSugiyamaNode level: {self.getLevel()}'

from typing import Tuple

from org.pyut.plugins.sugiyama.SugiyamaNode import SugiyamaNode


class VirtualSugiyamaNode(SugiyamaNode):
    """
    VirtualSugiyamaNode: a virtual node is a node on the Sugiyama graph which
    will not be visible on the diagram.  It is used to reserve space
    for the links drawing.
    """
    def __init__(self):
        super().__init__()

        self.__position: Tuple[int, int] = (0, 0)
        self.__size:     Tuple[int, int] = (1, 1)

    def setSize(self, width: int, height: int):
        """
        Set the size of the node.

        Args:
            width: Size
            height: Size
        """
        self.__size = (width, height)

    def getSize(self) -> Tuple[int, int]:
        """
        Get size of node.

        Returns: A tuple (int, int) : (width, height)

        """
        return self.__size

    def setPosition(self, x: int, y: int):
        """
        Set node position.

        Args:
            x: position in absolute coordinates
            y: position in absolute coordinates
        """
        self.__position = (x, y)

    def getPosition(self) -> Tuple[int, int]:
        """
        Get node position.

        Returns:    (int, int) : (x, y) in absolute coordinate
        """
        return self.__position

    def __repr__(self):
        return f'VirtualSugiyamaNode level: {self.getLevel()}'

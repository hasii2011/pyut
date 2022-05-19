
from typing import Tuple

from miniogl.ShapeModel import ShapeModel


class RectangleShapeModel(ShapeModel):
    """
    This class is the model of a RectangleShape ('view' in an MVC pattern).
    """
    def __init__(self, viewShape=None):
        """
        Used when the model is created first without any view.
        We have to use AddShape() and UpdateModel from the shape before
        we can use the model.

        Set the coordinates to 0 and a empty list of associated shapes (views)
        """
        super().__init__(viewShape)

        self._width:  int = 0
        self._height: int = 0

    def GetSize(self) -> Tuple[int, int]:
        """

        Returns:
            the size of the model
        """
        return self._width, self._height

    def SetSize(self, width: int, height: int):
        """
        Set the size of the model

        Args:
            width:      width of the model
            height:     height of the model
        """
        self._width = width
        self._height = height

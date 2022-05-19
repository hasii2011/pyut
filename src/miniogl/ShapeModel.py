
from typing import Tuple


class ShapeModel:
    """
    This class is the model of a shape ('view' in a MVC pattern).
    """

    def __init__(self, viewShape=None):
        """
        A model can have many views on different diagram frames

        Args:
            viewShape:  Shape (view) that represents this model
        """
        self._views = []

        if viewShape is not None:
            self._views.append(viewShape)

        self._x: int = 0
        self._y: int = 0

    def GetPosition(self) -> Tuple[int, int]:
        """

        Returns:
            the position of the model
        """
        return self._x, self._y

    def SetPosition(self, x: int, y: int):
        """

        Args:
            x:  abscissa of the model.
            y:  ordinate of the model.

        """
        self._x = x
        self._y = y

    def AddShape(self, viewShape):
        """
        Add the specified Shape (view) to the model
        Args:
            viewShape:
                Shape (view) to add to the model
        """
        self._views.append(viewShape)

    def removeShape(self, viewShape):
        """
        Remove the specified Shape (view) from the model. An exception is
        thrown when the specified Shape doesn't exist.
        Args:
            viewShape:
                Shape (view) to remove from the model
        """
        self._views.remove(viewShape)

    def GetAllViews(self):
        """

        Returns:
            all the shapes (views) attached to this model
        """
        return self._views

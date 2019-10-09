
from MiniOgl.ShapeModel import ShapeModel


class RectangleShapeModel(ShapeModel):
    """
    @author P. Dabrowski <przemek.dabrowski@destroy-display.com> (12.11.2005)
    This class is the model of a RectangleShape ('view' in a
    MVC pattern).
    """

    def __init__(self, viewShape=None):
        """
        Used when the model is created first without any view.
        We have to use AddShape() and UpdateModel from the shape before
        we can use the model.
        """

        # set the coords to 0 and a empty list of associated shapes (views)
        ShapeModel.__init__(self, viewShape)

        # width and height of the model
        self._width = 0.0
        self._height = 0.0

    def GetSize(self):
        """
        @return the size of the model
        """

        return self._width, self._height

    def SetSize(self, width, height):
        """
        Set the size of the model

        @param width          : width of the model
        @param height         : height of the model
        """

        self._width = width
        self._height = height

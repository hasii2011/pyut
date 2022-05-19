
from miniogl.RectangleShapeModel import RectangleShapeModel


class TextShapeModel(RectangleShapeModel):
    """
    This class is the model of a TextShape ('view' in an MVC pattern).
    """
    def __init__(self, viewShape=None):
        """
        Used when the model is created first without any view.
        We have to use AddShape() and UpdateModel from the shape before
        we can use the model.
        """
        super().__init__(viewShape=viewShape)

        self._fontSize = 0

    def GetFontSize(self):
        return self._fontSize

    def SetFontSize(self, fontSize):
        self._fontSize = fontSize

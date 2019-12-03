from org.pyut.MiniOgl.RectangleShapeModel import RectangleShapeModel


class TextShapeModel(RectangleShapeModel):
    """
    @author P. Dabrowski <przemek.dabrowski@destroy-display.com> (12.11.2005)
    This class is the model of a TextShape ('view' in a
    MVC pattern).
    """
    def __init__(self):
        """
        Constructor.
        Used when the model is created first without any view.
        We have to use AddShape() and UpdateModel from the shape before
        we can use the model.
        """

        # set the coords and size to 0 and a empty list of associated
        # shapes (views)
        super().__init__()

        self._fontSize = 0

    def __init__(self, viewShape):
        """
        Constructor.
        Used when the Shape (view) is created first.
        Before we can use it, we have to do a UpdateModel from the shape.
        """

        # set the coords and size to 0 and add the specified shape to the list.
        super().__init__(viewShape)

        # init the font of the shape
        self._fontSize = 0

    def GetFontSize(self):
        return self._fontSize

    def SetFontSize(self, fontSize):
        self._fontSize = fontSize



from logging import Logger
from logging import getLogger

from wx import BLACK
from wx import WHITE
from wx import PENSTYLE_SOLID

from wx import Font
from wx import Colour

from wx import DC
from wx import MemoryDC

from miniogl.Shape import Shape
from miniogl.RectangleShape import RectangleShape
from miniogl.TextShapeModel import TextShapeModel


class TextShape(RectangleShape):

    clsLogger: Logger = getLogger(__name__)
    """
    A text shape that can be attached to another shape standalone).
    """
    def __init__(self, x: int, y: int, text: str, parent=None, font: Font = None):
        """

        Args:
            x:          x position of the point
            y:          y position of the point
            text:       the text that the shape displays
            parent:     parent shape
            font:       Font to use
        """
        self._text:  str    = ''

        super().__init__(x, y, 0, 0, parent)

        self._color: Colour = BLACK
        self.SetText(text)

        self._drawFrame: bool = False
        self._resizable: bool = False
        self._textBack:  Colour = WHITE    # text background colour

        self._model: TextShapeModel = TextShapeModel(self)
        self._font:  Font = font

    def Attach(self, diagram):
        """
        Do not use this method, use Diagram.AddShape instead !!!
        Attach the shape to a diagram.
        When you create a new shape, you must attach it to a diagram before
        you can see it. This method is used internally by Diagram.AddShape.

        Args:
            diagram
        """
        # RectangleShape.Attach(self, diagram)
        super().Attach(diagram)
        self._textBack = self._diagram.GetPanel().GetBackgroundColour()

    def GetText(self) -> str:
        """
        Returns:  The text that the text shape displays
        """
        return self._text

    def SetText(self, text: str):
        """
        Set the text that the shape displays

        Args:
              text
        """
        self._text = text
        self._width, self._height = MemoryDC().GetTextExtent(text)

    def SetTextBackground(self, color: Colour):
        """
        Set the text background color.

        Args:
             color
        """
        self._textBack = color

    def GetTextBackground(self) -> Colour:
        """
        Get the text background color.

        Returns:
             the text background color
        """
        return self._textBack

    def Draw(self, dc: DC, withChildren: bool = True):
        """
        Draw the text on the dc.

        Args:
            dc
            withChildren
        """
        if self._visible:
            RectangleShape.Draw(self, dc, False)
            dc.SetTextForeground(self._color)
            dc.SetBackgroundMode(PENSTYLE_SOLID)
            dc.SetTextBackground(self._textBack)
            x, y = self.GetPosition()

            # to draw the text shape with its own font size
            saveFont: Font = dc.GetFont()
            if self.GetFont() is not None:
                dc.SetFont(self.GetFont())

            dc.DrawText(self._text, x, y)
            dc.SetFont(saveFont)

            if withChildren:
                self.DrawChildren(dc)

    def DrawBorder(self, dc: DC):
        """
        Draw the border of the shape, for fast rendering.

        Args:
            dc
        """
        if self._selected:
            RectangleShape.DrawBorder(self, dc)
        else:
            Shape.DrawBorder(self, dc)

    def GetColor(self) -> Colour:
        """
        Return the text color

        Returns wx.Colour
        """
        return self._color

    def SetColor(self, color: Colour):
        """
        Set the color of the text.

        Args:
             color
        """
        self._color = color

    def UpdateFromModel(self):
        """
        Updates the shape position and size from the model in light of a
        change of state of the diagram frame.  Here it is only for the zoom
        """

        # change the position and size of the shape from the model
        # RectangleShape.UpdateFromModel(self)
        super().UpdateFromModel()
        # get the diagram frame ratio between the shape and the model
        ratio = self.GetDiagram().GetPanel().GetCurrentZoom()

        fontSize = round(self.GetModel().GetFontSize() * ratio)
        TextShape.clsLogger.debug(f'UpdateFromModel - ratio: {ratio}')

        # set the new font size
        if self._font is not None:
            self._font.SetPointSize(fontSize)

    def UpdateModel(self):
        """
        Updates the model when the shape (view) is displaced or resized.
        """
        # change the coordinates and size of model
        # RectangleShape.UpdateModel(self)
        super().UpdateModel()

        # get the ratio between the model and the shape (view) from
        # the diagram frame where the shape is displayed.
        ratio = self.GetDiagram().GetPanel().GetCurrentZoom()

        # TextShape.clsLogger.debug(f'UpdateModel - ratio: {ratio}')
        if self.GetFont() is not None:
            fontSize = self.GetFont().GetPointSize() // ratio
            self.GetModel().SetFontSize(fontSize)

    def GetFont(self) -> Font:
        """

        Returns:  The font used by the text shape

        """
        return self._font

    def __repr__(self):
        x, y = self.GetPosition()
        return f'TextShape[{self._text=} position: ({x},{y}])'

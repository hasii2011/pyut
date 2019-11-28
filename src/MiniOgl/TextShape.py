
import wx

from MiniOgl.RectangleShape import RectangleShape
from MiniOgl.Shape import Shape


class TextShape(RectangleShape):
    """
    A text shape that can be attached to another shape (or be standalone).

    @author Laurent Burgbacher <lb@alawa.ch>
    """
    def __init__(self, x, y, text, parent=None):
        """
        Constructor.

        @param double x, y : position of the point
        @param string text : the text of the shape
        @param Shape parent : parent shape
        """
        RectangleShape.__init__(self, x, y, 0, 0, parent)
        self._text = None
        self._color = wx.BLACK
        self.SetText(text)
        self._drawFrame = False
        self._resizable = False
        self._textBack = wx.WHITE    # text background colour

    def Attach(self, diagram):
        """
        Don't use this method, use Diagram.AddShape instead !!!
        Attach the shape to a diagram.
        When you create a new shape, you must attach it to a diagram before
        you can see it. This method is used internally by Diagram.AddShape.

        @param  diagram
        """
        RectangleShape.Attach(self, diagram)
        self._textBack = self._diagram.GetPanel().GetBackgroundColour()

    def GetText(self):
        """
        Get the text of the shape.

        @return string
        """
        return self._text

    def SetText(self, text: str):
        """
        Set the text of the shape.

        @param  text
        """
        self._text = text
        self._width, self._height = wx.MemoryDC().GetTextExtent(text)

    def SetTextBackground(self, colour):
        """
        Set the text background color.

        @param colour
        """
        self._textBack = colour

    def GetTextBackground(self):
        """
        Get the text background color.

        @return wx.Colour
        """
        return self._textBack

    def Draw(self, dc, withChildren=True):
        """
        Draw the text on the dc.

        @param dc
        @param withChildren
        """
        if self._visible:
            RectangleShape.Draw(self, dc, False)
            dc.SetTextForeground(self._color)
            dc.SetBackgroundMode(wx.PENSTYLE_SOLID)
            dc.SetTextBackground(self._textBack)
            x, y = self.GetPosition()
            dc.DrawText(self._text, x, y)
            if withChildren:
                self.DrawChildren(dc)

    def DrawBorder(self, dc):
        """
        Draw the border of the shape, for fast rendering.

        @param  dc
        """
        if self._selected:
            RectangleShape.DrawBorder(self, dc)
        else:
            Shape.DrawBorder(self, dc)

    def GetColor(self):
        """
        Get the color of the text.

        @return wx.Colour
        """
        return self._color

    def SetColor(self, color):
        """
        Set the color of the text.

        @param color
        """
        self._color = color

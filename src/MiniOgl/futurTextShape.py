##########################################################
# Added by P. Dabrowski (21.11.2005)
# This is the future TextShape that should replace the
# actual when pyut will be refactorised (oglClass, ogl...)
# When it is the case just rename this file as TextShape
# and remove the ancient version
##########################################################

import wx

from MiniOgl.Shape import Shape
from MiniOgl.RectangleShape import RectangleShape
from MiniOgl.TextShapeModel import TextShapeModel


class TextShape(RectangleShape):
    """
    A text shape that can be attached to another shape (or be standalone).


    @author Laurent Burgbacher <lb@alawa.ch>
    """
    def __init__(self, x, y, text, parent=None, font=None):
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
        # added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (16.11.2005)
        self._model = TextShapeModel(self)
        self._font = font

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

    def SetTextBackground(self, colour: wx.Colour):
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

    def Draw(self, dc: wx.DC, withChildren: bool = True):
        """
        Draw the text on the dc.

        @param dc
        @param withChildren
        """
        if self._visible:
            RectangleShape.Draw(self, dc, False)
            dc.SetTextForeground(self._color)
            dc.SetBackgroundMode(wx.SOLID)
            dc.SetTextBackground(self._textBack)
            x, y = self.GetPosition()

            # added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (16.11.2005)
            # to draw the textshape with its own font size
            dcFont = dc.GetFont()
            if self.GetFont() is not None:
                dc.SetFont(self.GetFont())

            dc.DrawText(self._text, x, y)
            dc.SetFont(dcFont)

            if withChildren:
                self.DrawChildren(dc)

    def DrawBorder(self, dc: wx.DC):
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

    def SetColor(self, color: wx.Colour):
        """
        Set the color of the text.

        @param color
        """
        self._color = color

    def UpdateFromModel(self):
        """
        Added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (12.11.2005)

        Updates the shape position and size from the model in the light of a
        change of state of the diagram frame (here it's only for the zoom)
        """

        # change the position and size of the shape from the model
        RectangleShape.UpdateFromModel(self)

        # get the diagram frame ratio between the shape and the model
        ratio = self.GetDiagram().GetPanel().GetCurrentZoom()

        fontSize = self.GetModel().GetFontSize() * ratio

        # set the new font size
        if self._font is not None:
            self._font.SetPointSize(fontSize)

    def UpdateModel(self):
        """
        Added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (12.11.2005)

        Updates the model when the shape (view) is deplaced or resized.
        """
        # change the coords and size of model
        RectangleShape.UpdateModel(self)

        # get the ratio between the model and the shape (view) from
        # the diagram frame where the shape is displayed.
        ratio = self.GetDiagram().GetPanel().GetCurrentZoom()

        if self.GetFont() is not None:
            fontSize = self.GetFont().GetPointSize() / ratio
            self.GetModel().SetFontSize(fontSize)

    def GetFont(self):
        return self._font

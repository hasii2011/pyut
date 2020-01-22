from logging import Logger
from logging import getLogger

from wx import BLACK_DASHED_PEN
from wx import Colour
from wx import PENSTYLE_LONG_DASH
from wx import Pen

from org.pyut.MiniOgl.AnchorPoint import AnchorPoint
from org.pyut.MiniOgl.LineShape import LineShape
from org.pyut.MiniOgl.RectangleShape import RectangleShape

from org.pyut.ogl.OglObject import OglObject

from org.pyut.ogl.sd.OglInstanceName import OglInstanceName


class OglSDInstance(OglObject):

    DEFAULT_X:      int = 0
    DEFAULT_Y:      int = 0
    DEFAULT_WIDTH:  int = 100
    DEFAULT_HEIGHT: int = 400

    """
    Sequence Diagram Instance
    This class is an OGL object for class diagram instance (vertical line, ..)
    """
    def __init__(self, pyutObject, parentFrame):

        self._parentFrame = parentFrame
        self._instanceYPosition = 50       # Start of instances position

        diagram = self._parentFrame.GetDiagram()

        super().__init__(pyutObject, OglSDInstance.DEFAULT_WIDTH, OglSDInstance.DEFAULT_HEIGHT)

        self.logger: Logger = getLogger(__name__)
        diagram.AddShape(self)
        self.SetDraggable(True)
        self.SetVisible(True)

        self.SetPen(Pen(Colour(200, 200, 255), 1, PENSTYLE_LONG_DASH))
        self.SetPosition(self.GetPosition()[0], self._instanceYPosition)

        dstAnchorPoint, srcAnchorPoint = self._createAnchorPoints()

        self._lifeLineShape: LineShape = self._createLifeLineShape(src=srcAnchorPoint, dst=dstAnchorPoint)
        diagram.AddShape(self._lifeLineShape)

        # Instance box
        self._instanceBox: RectangleShape = RectangleShape(0, 0, 100, 50)

        self.AppendChild(self._instanceBox)
        self._instanceBox.SetDraggable(False)
        self._instanceBox.Resize = self.OnInstanceBoxResize
        self._instanceBox.SetResizable(True)
        self._instanceBox.SetParent(self)
        diagram.AddShape(self._instanceBox)

        # Text of the instance box
        text = self._pyutObject.getInstanceName()
        self._instanceBoxText = OglInstanceName(pyutObject, 20.0, 20.0, text, self._instanceBox)
        self.AppendChild(self._instanceBoxText)
        diagram.AddShape(self._instanceBoxText)
        # TODO : set instance box size to the size of the text
        #       by invoking self._instanceBoxText.SetSize()

    def getLifeLineShape(self):
        """
        Used by OGLSDMessage to use it as parent

        Returns: the lifeline object

        """
        return self._lifeLineShape

    def OnInstanceBoxResize(self, sizer, width, height):
        """
        Resize the instance box, so all instance
        """
        RectangleShape.Resize(self._instanceBox, sizer, width, height)
        size = self._instanceBox.GetSize()
        self.SetSize(size[0], self.GetSize()[1])

    def Resize(self, sizer, width, height):
        """
        Resize the rectangle according to the new position of the sizer.

        """
        OglObject.Resize(self, sizer, width, height)

    def SetSize(self, width, height):
        """
        """
        OglObject.SetSize(self, width, height)
        # Set lifeline
        # self._lifeLineX = width/2
        #  (myX, myY) = self.GetPosition()
        (myX, myY) = self.GetPosition()
        (w, h) = self.GetSize()
        lineDst = self._lifeLineShape.GetDestination()
        lineSrc = self._lifeLineShape.GetSource()
        lineSrc.SetDraggable(True)
        lineDst.SetDraggable(True)
        lineSrc.SetPosition(w/2 + myX, 0 + myY)
        lineDst.SetPosition(w/2 + myX, height + myY)
        lineSrc.SetDraggable(False)
        lineDst.SetDraggable(False)

        # Update all links positions
        for link in self._oglLinks:
            try:
                link.updatePositions()
            except (ValueError, Exception) as e:
                self.logger.error(f'Link update position error: {e}')

        # Set TextBox
        RectangleShape.SetSize(self._instanceBox, width, self._instanceBox.GetSize()[1])

    def SetPosition(self, x, y):
        """
        Debug
        @author C.Dutoit
        """
        y = self._instanceYPosition
        OglObject.SetPosition(self, x, y)

    def Draw(self, dc, withChildren=False):
        """
        Draw overload; update labels
        """
        # Update labels
        self._instanceBoxText.SetText(self._pyutObject.getInstanceName())

        # Call parent's Draw method
        if self.IsSelected():
            self.SetVisible(True)
            self.SetPen(Pen(Colour(200, 200, 255), 1, PENSTYLE_LONG_DASH))

        # Draw
        OglObject.Draw(self, dc)

    def OnLeftUp(self, event):
        """
        """
        self.SetPosition(self.GetPosition()[0], self._instanceYPosition)

    def _createAnchorPoints(self):

        srcX = OglSDInstance.DEFAULT_WIDTH / 2
        srcY = 0
        dstX = OglSDInstance.DEFAULT_WIDTH / 2
        dstY = OglSDInstance.DEFAULT_HEIGHT
        srcAnchorPoint: AnchorPoint = AnchorPoint(srcX, srcY, self)
        dstAnchorPoint: AnchorPoint = AnchorPoint(dstX, dstY, self)

        for el in [srcAnchorPoint, dstAnchorPoint]:
            el.SetVisible(False)
            el.SetDraggable(False)

        return dstAnchorPoint, srcAnchorPoint

    def _createLifeLineShape(self, src: AnchorPoint, dst: AnchorPoint) -> LineShape:

        lifeLineShape: LineShape = LineShape(src, dst)

        self.AppendChild(lifeLineShape)
        lifeLineShape.SetParent(self)
        lifeLineShape.SetDrawArrow(False)
        lifeLineShape.SetDraggable(True)
        lifeLineShape.SetPen(BLACK_DASHED_PEN)
        lifeLineShape.SetVisible(True)

        return lifeLineShape


from typing import cast

from logging import Logger
from logging import getLogger

from wx import BLACK_DASHED_PEN
from wx import PENSTYLE_LONG_DASH

from wx import Colour
from wx import Pen

from miniogl.AnchorPoint import AnchorPoint
from miniogl.Diagram import Diagram
from miniogl.LineShape import LineShape
from miniogl.RectangleShape import RectangleShape

from ogl.OglObject import OglObject

from ogl.sd.OglInstanceName import OglInstanceName


class OglSDInstance(OglObject):
    """
    Class Diagram Instance
    This class is an OGL object for class diagram instance (vertical line)

    Instantiated by UmlClassDiagramFrame
    """
    DEFAULT_WIDTH: int = 100
    DEFAULT_HEIGHT: int = 400

    def __init__(self, pyutObject, parentFrame):
        """
        """
        self._parentFrame = parentFrame
        self._instanceYPosition: int = 50       # Start of instances position

        self.logger: Logger = getLogger(__name__)

        diagram: Diagram = self._parentFrame.GetDiagram()

        # OglObject.__init__(self, pyutObject, DEFAULT_WIDTH, DEFAULT_HEIGHT)
        super().__init__(pyutObject, OglSDInstance.DEFAULT_WIDTH, OglSDInstance.DEFAULT_HEIGHT)

        diagram.AddShape(self)
        self.SetDraggable(True)
        self.SetVisible(True)
        self.SetPen(Pen(Colour(200, 200, 255), 1, PENSTYLE_LONG_DASH))
        self.SetPosition(self.GetPosition()[0], self._instanceYPosition)

        # Init lineShape
        (srcX, srcY, dstX, dstY) = (OglSDInstance.DEFAULT_WIDTH // 2, 0,
                                    OglSDInstance.DEFAULT_WIDTH // 2, OglSDInstance.DEFAULT_HEIGHT
                                    )

        (src, dst) = (AnchorPoint(srcX, srcY, self), AnchorPoint(dstX, dstY, self))
        for el in [src, dst]:
            el.SetVisible(False)
            el.SetDraggable(False)
        self._lifeLineShape: LineShape = LineShape(src, dst)
        self.AppendChild(self._lifeLineShape)
        self._lifeLineShape.SetParent(self)
        self._lifeLineShape.SetDrawArrow(False)
        self._lifeLineShape.SetDraggable(True)
        self._lifeLineShape.SetPen(BLACK_DASHED_PEN)
        self._lifeLineShape.SetVisible(True)
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
        text = self._pyutObject.instanceName
        self._instanceBoxText: OglInstanceName = OglInstanceName(pyutObject, 0, 20, text, self._instanceBox)
        self.AppendChild(self._instanceBoxText)
        diagram.AddShape(self._instanceBoxText)
        # TODO : set instance box size to the size of the text by invoking self._instanceBoxText.setSize()

    def getLifeLineShape(self):
        """
        Used by OGLSDMessage to use it as parent

        Returns: The lifeline object
        """
        return self._lifeLineShape

    def OnInstanceBoxResize(self, sizer, width: int, height: int):
        """
        Resize the instance box, so all instance

        Args:
            sizer:
            width:
            height:

        """
        """

        @param double x, y : position of the sizer
        """
        RectangleShape.Resize(self._instanceBox, sizer, width, height)
        size = self._instanceBox.GetSize()
        self.SetSize(size[0], self.GetSize()[1])

    def Resize(self, sizer, width: int, height: int):
        """
        Resize the rectangle according to the new position of the sizer.

        Args:
            sizer:
            width:
            height:
        """
        OglObject.Resize(self, sizer, width, height)

    def SetSize(self, width: int, height: int):
        """
        """
        OglObject.SetSize(self, width, height)
        # Set lifeline
        (myX, myY) = self.GetPosition()
        (w, h) = self.GetSize()
        lineDst = self._lifeLineShape.GetDestination()
        lineSrc = self._lifeLineShape.GetSource()
        lineSrc.SetDraggable(True)
        lineDst.SetDraggable(True)
        lineSrc.SetPosition(w // 2 + myX, 0 + myY)
        lineDst.SetPosition(w // 2 + myX, height + myY)
        lineSrc.SetDraggable(False)
        lineDst.SetDraggable(False)

        from ogl.sd.OglSDMessage import OglSDMessage
        # Update all OglSDMessage positions
        for link in self._oglLinks:
            try:
                oglSDMessage: OglSDMessage = cast(OglSDMessage, link)
                oglSDMessage.updatePositions()
            except (ValueError, Exception) as e:
                self.logger.error(f'Link update position error: {e}')
        # Set TextBox
        RectangleShape.SetSize(self._instanceBox, width, self._instanceBox.GetSize()[1])

    def SetPosition(self, x: int, y: int):
        """ 
        Debug
        """
        y = self._instanceYPosition
        OglObject.SetPosition(self, x, y)

    def Draw(self, dc, withChildren=False):
        """
        Draw overload; update labels
        """
        # Update labels
        self._instanceBoxText.SetText(self._pyutObject.instanceName)

        # Call parent's Draw method
        if self.IsSelected():
            self.SetVisible(True)
            self.SetPen(Pen(Colour(200, 200, 255), 1, PENSTYLE_LONG_DASH))

        # Draw
        # OglObject.Draw(self, dc, withChildren)
        super().Draw(dc=dc, withChildren=withChildren)

    def OnLeftUp(self, event):
        """
        Callback for left clicks.
        """
        self.SetPosition(self.GetPosition()[0], self._instanceYPosition)

    def __str__(self) -> str:
        instanceName: str = self._pyutObject.instanceName
        return f'OglSDInstance[{self._id=} {instanceName=}]'

    def __repr__(self) -> str:
        return self.__str__()

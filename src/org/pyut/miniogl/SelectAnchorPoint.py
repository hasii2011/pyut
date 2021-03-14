

from wx import BLACK_PEN
from wx import RED_PEN

from wx import Pen
from wx import MouseEvent

from org.pyut.miniogl.Shape import Shape
from org.pyut.miniogl.AnchorPoint import AnchorPoint
from org.pyut.miniogl.ShapeEventHandler import ShapeEventHandler

from org.pyut.enums.AttachmentPoint import AttachmentPoint


class SelectAnchorPoint(AnchorPoint, ShapeEventHandler):

    """
    This is a point attached to a shape to indicate where to click;  Presumably, to indicate where
    to attach something

    """
    def __init__(self, x: int, y: int, attachmentPoint: AttachmentPoint, parent: Shape = None):
        """

        Args:
            x: x position of the point
            y: y position of the point
            parent:
        """
        super().__init__(x, y, parent)

        self._attachmentPoint: AttachmentPoint = attachmentPoint
        self._pen:             Pen             = RED_PEN
        self.SetDraggable(True)     # So it sticks on OglClass resize

    @property
    def attachmentPoint(self) -> AttachmentPoint:
        return self._attachmentPoint

    @attachmentPoint.setter
    def attachmentPoint(self, newValue: AttachmentPoint):
        self._attachmentPoint = newValue

    def setYouAreTheSelectedAnchor(self):
        self._pen = BLACK_PEN

    def Draw(self, dc, withChildren=True):

        dc.SetPen(self._pen)
        super().Draw(dc, withChildren)

    def OnLeftDown(self, event: MouseEvent):
        """
        Callback for left clicks.

        Args:
            event: The mouse event
        """

        from org.pyut.ui.Mediator import Mediator   # avoid circular import

        print(f'SelectAnchorPoint: {self._attachmentPoint}')

        mediator: Mediator = Mediator()
        mediator.createLollipopInterface(implementor=self.GetParent(), attachmentAnchor=self)

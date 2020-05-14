
from wx import MouseEvent
from wx import RED_PEN

from org.pyut.MiniOgl.AnchorPoint import AnchorPoint
from org.pyut.MiniOgl.Shape import Shape
from org.pyut.MiniOgl.ShapeEventHandler import ShapeEventHandler
from org.pyut.enums.PyutAttachmentPoint import PyutAttachmentPoint


class SelectAnchorPoint(AnchorPoint, ShapeEventHandler):

    """
    This is a point attached to a shape to indicate where to click;  Presumably, to indicate where
    to attach something

    """
    def __init__(self, x: float, y: float, attachmentPoint: PyutAttachmentPoint, parent: Shape = None):
        """

        Args:
            x: x position of the point
            y: y position of the point
            parent:
        """
        super().__init__(x, y, parent)
        self._attachmentPoint: PyutAttachmentPoint = attachmentPoint

    @property
    def attachmentPoint(self) -> PyutAttachmentPoint:
        return self._attachmentPoint

    @attachmentPoint.setter
    def attachmentPoint(self, newValue: PyutAttachmentPoint):
        self._attachmentPoint = newValue

    def Draw(self, dc, withChildren=True):

        dc.SetPen(RED_PEN)
        super().Draw(dc, withChildren)

    def OnLeftDown(self, event: MouseEvent):
        """
        Callback for left clicks.

        Args:
            event: The mouse event
        """
        print(f'SelectAnchorPoint left down')
        event.Skip()

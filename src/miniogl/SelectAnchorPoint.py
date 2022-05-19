
from logging import Logger
from logging import getLogger

from wx import BLACK_PEN
from wx import RED_PEN

from wx import Pen
from wx import MouseEvent

from miniogl.Shape import Shape
from miniogl.AnchorPoint import AnchorPoint
from miniogl.ShapeEventHandler import ShapeEventHandler

from miniogl.AttachmentLocation import AttachmentLocation


class SelectAnchorPoint(AnchorPoint, ShapeEventHandler):

    """
    This is a point attached to a shape to indicate where to click;  Presumably, to indicate where
    to attach something

    """
    def __init__(self, x: int, y: int, attachmentPoint: AttachmentLocation, parent: Shape = None):
        """

        Args:
            x: x position of the point
            y: y position of the point
            parent:
        """
        super().__init__(x, y, parent)

        self.logger: Logger = getLogger(__name__)
        self._attachmentPoint: AttachmentLocation = attachmentPoint
        self._pen:             Pen                = RED_PEN
        self.SetDraggable(True)     # So it sticks on OglClass resize;  But now the user can move it !!

    @property
    def attachmentPoint(self) -> AttachmentLocation:
        return self._attachmentPoint

    @attachmentPoint.setter
    def attachmentPoint(self, newValue: AttachmentLocation):
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
        self.logger.debug(f'SelectAnchorPoint.OnLeftDown:  {self._parent=} {event.GetPosition()=}')
        self._parent.handleSelectAnchorPointSelection(event)      # bad form;  but anything to get rid of mediator

    def __str__(self) -> str:
        x, y = self.GetPosition()
        draggable: bool = self._draggable
        return f'SelectAnchorPoint[({x},{y}) - {draggable=}]'

    def __repr__(self):
        return self.__str__()

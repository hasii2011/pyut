
from typing import Union

from logging import Logger
from logging import getLogger

from wx import Brush
from wx import Pen
from wx import Window

from miniogl.DiagramFrame import DiagramFrame
from miniogl.SelectAnchorPoint import SelectAnchorPoint

from ogl.OglInterface2 import OglInterface2
from ogl.OglAssociationLabel import OglAssociationLabel
from ogl.OglObject import OglObject
from ogl.OglLink import OglLink

from pyut.preferences.PyutPreferences import PyutPreferences


class UmlFrameShapeHandler(DiagramFrame):

    def __init__(self, parent: Window):
        """

        Args:
            parent:  The window where we put the UML Diagram Frames
        """

        super().__init__(parent)

        self.logger:       Logger = getLogger(__name__)
        self._preferences: PyutPreferences = PyutPreferences()

    def addShape(self, shape: Union[OglObject, OglInterface2, SelectAnchorPoint, OglLink, OglAssociationLabel],
                 x: int, y: int, pen: Pen = None, brush: Brush = None, withModelUpdate: bool = True):
        """
        Add a shape to the UmlFrame.

        Args:
            shape: the shape to add
            x: coord of the center of the shape
            y: coord of the center of the shape
            pen: pen to use
            brush:  brush to use
            withModelUpdate: if true the model of the shape will update from the shape (view) when added to the diagram.
        """
        shape.draggable = True
        shape.SetPosition(x, y)
        if pen is not None:
            shape.SetPen(pen)
        if brush is not None:
            shape.SetBrush(brush)
        self._diagram.AddShape(shape, withModelUpdate)

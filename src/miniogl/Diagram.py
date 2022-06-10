
from logging import Logger
from logging import getLogger

from miniogl.Shape import Shape
from miniogl.SizerShape import SizerShape


class Diagram:

    clsLogger: Logger = getLogger(__name__)
    """
    A diagram contains shapes and is responsible to manage them.
    It can be saved to a file, and loaded back. It knows every shapes that
    can be clicked (selected, moved...).
    """
    def __init__(self, panel):
        """
        Constructor.

        @param  panel : the panel on which to draw
        """
        self._panel = panel
        self._shapes = []        # all selectable shapes
        self._parentShapes = []  # all first level shapes

    def AddShape(self, shape, withModelUpdate: bool = True):
        """
        Add a shape to the diagram.
        This is the correct way to do it. Don't use Shape.Attach(diagram)!

        Args:
            shape:  the shape to add
            withModelUpdate:
        """
        if shape not in self._shapes:
            self._shapes.append(shape)
        if shape not in self._parentShapes and shape.GetParent() is None:
            self._parentShapes.append(shape)

        self.clsLogger.debug(f'.AddShape before shape.Attach()=> {shape} withModelUpdate {withModelUpdate}')
        shape.Attach(self)

        # makes the shape's model (MVC pattern) have the right values depending on
        # the diagram frame state.
        if withModelUpdate:
            shape.UpdateModel()

    def DeleteAllShapes(self):
        """
        Delete all shapes in the diagram.
        """
        while self._shapes:
            self._shapes[0].Detach()
        self._shapes = []
        self._parentShapes = []

    def RemoveShape(self, shape: SizerShape):
        """
        Remove a shape from the diagram. Use Shape.Detach() instead!
        This also works, but it not the better way.

        @param  shape
        """
        if shape in self._shapes:
            self._shapes.remove(shape)
        if shape in self._parentShapes:
            self._parentShapes.remove(shape)

    def GetShapes(self):
        """
        Return a list of the shapes in the diagram.
        It is a copy of the original. You cannot detach or add shapes to the
        diagram this way.

        @return Shape []
        """
        return self._shapes[:]

    def GetParentShapes(self):
        """
        Return a list of the parent shapes in the diagram.
        It is a copy of the original. You cannot detach or add shapes to the
        diagram this way.

        @return Shape []
        """
        return self._parentShapes[:]

    def GetPanel(self):
        """
        Return the panel associated with this diagram.

        @return DiagramFrame
        """
        return self._panel

    def MoveToFront(self, shape: Shape):
        """
        Move the given shape to the end of the display list => last drawn.

        Args:
            shape: The shape to move
        """
        shapes = [shape] + shape.GetAllChildren()
        for s in shapes:
            self._shapes.remove(s)
        self._shapes = self._shapes + shapes

    def MoveToBack(self, shape: Shape):
        """
        Move the given shape to the start of the display list => first drawn.

        Args:
            shape: The shape to move
        """
        shapes = [shape] + shape.GetAllChildren()
        for s in shapes:
            self._shapes.remove(s)
        self._shapes = shapes + self._shapes

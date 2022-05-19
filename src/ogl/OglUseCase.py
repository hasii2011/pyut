
from wx import DC

from ogl.OglObject import OglObject
from pyutmodel.PyutUseCase import PyutUseCase
from ogl.OglUtils import OglUtils


class OglUseCase(OglObject):
    """
    OGL object that represent a UML use case in use case diagrams.
    This class defines OGL objects that represents a use case for Use
    Cases diagram. You can just instantiate an OGLUseCase and add it to
    the diagram, links, resizing, ... are managed by parent class
    `OglObject`.

    For more instructions about how to create an OGL object, please refer
    to the `OglObject` class.
    """
    def __init__(self, pyutUseCase=None, w: int = 100, h: int = 60):
        """

        Args:
            pyutUseCase:
            w: Width of the shape
            h: Height of the shape
        """
        # Init associated PyutObject
        if pyutUseCase is None:
            pyutObject = PyutUseCase()
        else:
            pyutObject = pyutUseCase

        super().__init__(pyutObject, w, h)

        # Should not draw border
        self._drawFrame = False

    def Draw(self, dc: DC, withChildren=False):
        """
        Draw the actor.

        Args:
            dc:      Device context
            withChildren:
        """
        OglObject.Draw(self, dc, withChildren)
        dc.SetFont(self._defaultFont)

        # Gets the minimum bounding box for the shape
        width, height = self.GetSize()

        # Calculate the top left of the shape
        x, y = self.GetPosition()

        # Draw ellipse
        dc.DrawEllipse(x + 1, y + 1, width - 2, height - 2)

        # Draw text
        x += round(0.25 * width)
        y += round(0.25 * height)

        textWidth: int = round(0.6 * width)                 # Text area width
        space:     int = round(1.1 * dc.GetCharHeight())    # Space between lines

        # Drawing is restricted in the specified region of the device
        dc.SetClippingRegion(x, y, textWidth, round(0.6 * height))

        # Split lines
        lines = OglUtils.lineSplitter(self.pyutObject.name, dc, textWidth)

        # Draw text
        for line in lines:
            dc.DrawText(line, x, y)
            y += space

        dc.DestroyClippingRegion()

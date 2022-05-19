
from wx import DC

from ogl.OglObject import OglObject
from pyutmodel.PyutActor import PyutActor


MARGIN: int = 10


class OglActor(OglObject):
    """
    OGL object that represent a UML actor in use case diagrams.
    This class defines OGL objects that represents an actor for Use
    Cases diagram. You can just instantiate an OGL actor and add it to
    the diagram, links, resizing, ... are managed by parent class
    `OglObject`.

    For more instructions about how to create an OGL object, please refer
    to the `OglObject` class.

    :version: $Revision: 1.9 $
    :author: Philippe Waelti
    :contact: pwaelti@eivd.ch
    """
    def __init__(self, pyutActor=None, w: int = 80, h: int = 100):
        """

        Args:
            pyutActor:

            w:  width of shape
            h:  height of shape
        """

        # Init associated PyutObject
        if pyutActor is None:
            pyutObject = PyutActor()
        else:
            pyutObject = pyutActor

        super().__init__(pyutObject, w, h)
        self._drawFrame = False

    def Draw(self, dc: DC, withChildren: bool = False):
        """
        Draw an actor

        Args:
            dc:     The device context to draw on
            withChildren:   Draw the children or not

        """
        OglObject.Draw(self, dc)
        # Get current font
        dc.SetFont(self._defaultFont)

        # Gets the minimum bounding box for the shape
        width, height = self.GetSize()

        # Calculate the top center of the shape
        x, y = self.GetPosition()

        # drawing is restricted in the specified region of the device
        dc.SetClippingRegion(x, y, width, height)

        # Our sweet actor size
        actorWidth  = width
        actorHeight = int(0.8 * (height - 2.0 * MARGIN))  # 80 % of total height
        sizer = min(actorHeight, actorWidth)

        # Draw our actor head
        centerX = x + width  // 2
        centerY = y + height // 2

        x = int(centerX - 0.2 * sizer)
        y += MARGIN
        percentageSizer: int = int(0.4 * sizer)
        # dc.DrawEllipse(x, y, 0.4 * sizer, 0.4 * sizer)
        dc.DrawEllipse(x, y, percentageSizer, percentageSizer)

        # Draw body and arms
        x = centerX
        y += round(0.4 * sizer)
        # dc.DrawLine(x, y, x, y + 0.3 * actorHeight)
        # dc.DrawLine(x - 0.25 * actorWidth, y + 0.15 * actorHeight,
        #             x + 0.25 * actorWidth, y + 0.15 * actorHeight)
        dc.DrawLine(x, y, x, y + round(0.3 * actorHeight))
        dc.DrawLine(round(x - 0.25 * actorWidth), round(y + 0.15 * actorHeight),
                    round(x + 0.25 * actorWidth), round(y + 0.15 * actorHeight))

        # And the feet
        # y += round(0.3 * actorHeight)
        # dc.DrawLine(x, y, x - 0.25 * actorWidth, y + 0.3 * actorHeight)
        # dc.DrawLine(x, y, x + 0.25 * actorWidth, y + 0.3 * actorHeight)

        actorFeetPercentage: int = round(0.3 * actorHeight)
        y += round(actorFeetPercentage)
        # dc.DrawLine(x, y, x - 0.25 * actorWidth, y + actorFeetPercentage)
        # dc.DrawLine(x, y, x + 0.25 * actorWidth, y + actorFeetPercentage)
        dc.DrawLine(x, y, x - round(0.25 * actorWidth), y + actorFeetPercentage)
        dc.DrawLine(x, y, x + round(0.25 * actorWidth), y + actorFeetPercentage)

        # Draw our buddy name
        textWidth, textHeight = dc.GetTextExtent(self.pyutObject.name)

        # y = centerY + 0.5 * height - MARGIN - 0.1 * actorHeight
        y = round(centerY + 0.5 * height - MARGIN - 0.1 * actorHeight)

        # dc.DrawText(self.getPyutObject().getName(), x - 0.5 * textWidth, y)
        dc.DrawText(self.pyutObject.name, round(x - 0.5 * textWidth), y)
        dc.DestroyClippingRegion()

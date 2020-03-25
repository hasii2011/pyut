from logging import Logger
from logging import getLogger

from wx import WHITE_BRUSH

from org.pyut.MiniOgl.Shape import Shape

from org.pyut.model.PyutLink import PyutLink

from org.pyut.ogl.OglClass import OglClass
from org.pyut.ogl.OglLink import OglLink


class OglInheritance(OglLink):
    """
    Graphical OGL representation of an inheritance link.
    This class provide the methods for drawing an inheritance link between
    two classes of an UML diagram. Add labels to an OglLink.
    """
    def __init__(self, srcShape: OglClass, pyutLink: PyutLink, dstShape: OglClass):
        """

        Args:
            srcShape: Source shape
            pyutLink: Conceptual links associated with the graphical links.
            dstShape: Destination shape
        """
        super().__init__(srcShape, pyutLink, dstShape)

        self.logger: Logger = getLogger(__name__)
        # Arrow must be white inside
        self.SetBrush(WHITE_BRUSH)
        self.SetDrawArrow(True)

    def __repr__(self):
        srcShape:  Shape = self.getSourceShape()
        destShape: Shape = self.getDestinationShape()
        sourceId:  int   = srcShape.GetID()
        destId:    int   = destShape.GetID()
        return f'OglInheritance - from: id: {sourceId} {self.getSourceShape()}  to: id: {destId} {self.getDestinationShape()}'

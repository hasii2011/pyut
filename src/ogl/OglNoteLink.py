
from wx import PENSTYLE_LONG_DASH

from wx import Pen

from miniogl.Shape import Shape

from pyutmodel.PyutLink import PyutLink
from ogl.OglLink import OglLink
from ogl.OglObject import OglObject


class OglNoteLink(OglLink):
    """
    A note like link, with dashed line and no arrows.
    To get a new link, you should use the `OglLinkFactory` and specify
    the kind of link you want, OGL_NOTELINK for an instance of this class.

    """

    def __init__(self, srcShape: OglObject, pyutLink: PyutLink, dstShape: OglObject):
        """

        Args:
            srcShape:  Source shape
            pyutLink:  Conceptual links associated with the graphical links.
            dstShape: Destination shape
        """
        super().__init__(srcShape, pyutLink, dstShape)
        self.SetDrawArrow(False)
        self.SetPen(Pen("BLACK", 1, PENSTYLE_LONG_DASH))

    def __repr__(self):

        srcShape:  Shape = self.getSourceShape()
        destShape: Shape = self.getDestinationShape()
        sourceId:  int   = srcShape.GetID()
        destId:    int   = destShape.GetID()
        return f'OglNoteLink - from: id: {sourceId} {self.getSourceShape()}  to: id: {destId} {self.getDestinationShape()}'

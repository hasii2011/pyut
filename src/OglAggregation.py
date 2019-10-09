
from logging import Logger
from logging import getLogger

from wx import DC

from OglAssociation import OglAssociation


class OglAggregation(OglAssociation):
    """
    Graphical link representation of aggregation, (empty diamond, arrow).
    To get a new link, you should use the `OglLinkFatory` and specify
    the kind of link you want, OGL_AGGREGATION for an instance of this class.

    :version: $Revision: 1.6 $
    :author: Philippe Waelti
    :contact: pwaelti@eivd.ch
    """

    def __init__(self, srcShape, pyutLink, dstShape):
        """
        Constructor.

        @param OglClass srcShape : Source shape
        @param PyutLink pyutLink : Conceptual links associated with the
                                   graphical links.
        @param OglClass dstShape : Destination shape

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        super().__init__(srcShape, pyutLink, dstShape)

        self.logger: Logger = getLogger(__name__)
        self.SetDrawArrow(True)

    def Draw(self, dc: DC, withChildren: bool = False):
        """
        Called for contents drawing of links.

        @param  dc : Device context
        @param withChildren

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        super().Draw(dc, withChildren)

        # Draw losange
        self.drawLosange(dc, False)

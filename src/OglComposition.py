

from OglAssociation import OglAssociation


class OglComposition(OglAssociation):
    """
    Graphical link representation of composition, (plain diamond, arrow).
    To get a new link, you should use the `OglLinkFatory` and specify
    the kind of link you want, OGL_COMPOSITION for an instance of this class.

    :version: $Revision: 1.6 $
    :author: Philippe Waelti
    :contact: pwaelti@eivd.ch
    """

    def __init__(self, srcShape, pyutLink, dstShape):
        """
        Constructor.

        @param OglObject srcShape : Source shape
        @param PyutLinkedObject pyutLink : Conceptual links associated with the graphical links.
        @param OglObject dstShape : Destination shape
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """

        super().__init__(srcShape, pyutLink, dstShape)
        self.SetDrawArrow(True)

    def Draw(self, dc):
        """
        Called for contents drawing of links.

        @param wxDC dc : Device context
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        OglAssociation.Draw(self, dc)
        self.drawLosange(dc, True)

    def cleanUp(self):
        """
        Clean up object references before quitting.

        @since 1.5
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        OglAssociation.cleanUp(self)
        self.ClearArrowsAtPosition()

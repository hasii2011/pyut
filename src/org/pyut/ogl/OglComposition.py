
from wx import DC

from org.pyut.ogl.OglClass import OglClass
from org.pyut.PyutLink import PyutLink

from org.pyut.ogl.OglAssociation import OglAssociation


class OglComposition(OglAssociation):
    """
    Graphical link representation of composition, (plain diamond, arrow).
    To get a new link, you should use the `OglLinkFatory` and specify
    the kind of link you want, OGL_COMPOSITION for an instance of this class.

    :version: $Revision: 1.6 $
    :author: Philippe Waelti
    :contact: pwaelti@eivd.ch
    """

    def __init__(self, srcShape: OglClass, pyutLink: PyutLink, dstShape: OglClass):
        """
        Constructor.

        @param  srcShape : Source shape
        @param  pyutLink : Conceptual links associated with the graphical links
        @param  dstShape : Destination shape
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """

        super().__init__(srcShape, pyutLink, dstShape)
        self.SetDrawArrow(True)

    def Draw(self, dc: DC, withChildren: bool = False):
        """

        Args:
            dc:     Device Context
            withChildren:   Draw the children or not
        """
        OglAssociation.Draw(self, dc)
        self.drawLosange(dc, True)

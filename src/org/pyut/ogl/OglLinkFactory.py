
from logging import Logger
from logging import getLogger

from org.pyut.ogl.OglAssociation import OglAssociation
from org.pyut.ogl.OglAggregation import OglAggregation
from org.pyut.ogl.OglComposition import OglComposition
from org.pyut.ogl.OglInheritance import OglInheritance
from org.pyut.ogl.OglInterface import OglInterface
from org.pyut.ogl.OglNoteLink import OglNoteLink

from org.pyut.enums.LinkType import LinkType

from org.pyut.general.Singleton import Singleton
from org.pyut.ogl.sd.OglSDMessage import OglSDMessage


def getOglLinkFactory():
    """
    Function to get the unique OglLinkFactory instance (singleton).

    @since 1.0
    @author P. Waelti <pwaelti@eivd.ch>
    """
    return OglLinkFactory()


def getLinkType(link: OglAssociation) -> LinkType:
    """

    Args:
        link:   The enumeration OglLinkType

    Returns:  The OglLinkType

    """

    if isinstance(link, OglAggregation):
        return LinkType.AGGREGATION
    elif isinstance(link, OglComposition):
        return LinkType.COMPOSITION
    elif isinstance(link, OglInheritance):
        return LinkType.INHERITANCE
    elif isinstance(link, OglAssociation):
        return LinkType.ASSOCIATION
    elif isinstance(link, OglInterface):
        return LinkType.INTERFACE
    elif isinstance(link, OglNoteLink):
        return LinkType.NOTELINK


class OglLinkFactory(Singleton):
    """
    This class is a factory to produce `OglLink` objects.
    It works under the Factory Design Pattern model. Ask for a link
    from this object and it will return you what you was asking for.
    """
    def init(self, *args, **kwds):
        self.logger: Logger = getLogger(__name__)

    # noinspection PyUnusedLocal
    def getOglLink(self, srcShape, pyutLink, destShape, linkType: LinkType, srcPos=None, dstPos=None):
        """
        Used to get a OglLink of the given linkType.

        Args:
            srcShape:   Source shape
            pyutLink:   Conceptual links associated with the graphical links.
            destShape:  Destination shape
            linkType:   The linkType of the link (OGL_INHERITANCE, ...)
            srcPos:     source position
            dstPos:     destination position

        Returns:  The requested link
        """
        if linkType == LinkType.AGGREGATION:
            return OglAggregation(srcShape, pyutLink, destShape)

        elif linkType == LinkType.COMPOSITION:
            return OglComposition(srcShape, pyutLink, destShape)

        elif linkType == LinkType.INHERITANCE:
            return OglInheritance(srcShape, pyutLink, destShape)

        elif linkType == LinkType.ASSOCIATION:
            return OglAssociation(srcShape, pyutLink, destShape)

        elif linkType == LinkType.INTERFACE:
            return OglInterface(srcShape, pyutLink, destShape)

        elif linkType == LinkType.NOTELINK:
            return OglNoteLink(srcShape, pyutLink, destShape)

        elif linkType == LinkType.SD_MESSAGE:
            return OglSDMessage(srcShape=srcShape, pyutSDMessage=pyutLink, dstShape=destShape)
        else:
            self.logger.error(f"Unknown OglLinkType into factory: {linkType}")
            return None

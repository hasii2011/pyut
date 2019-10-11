
from logging import Logger
from logging import getLogger

from org.pyut.ogl.OglAssociation import OglAssociation
from OglAggregation import OglAggregation
from OglComposition import OglComposition
from OglInheritance import OglInheritance
from OglInterface import OglInterface
from org.pyut.ogl.OglNoteLink import OglNoteLink

from PyutConsts import OGL_AGGREGATION
from PyutConsts import OGL_ASSOCIATION
from PyutConsts import OGL_COMPOSITION
from PyutConsts import OGL_INHERITANCE
from PyutConsts import OGL_INTERFACE
from PyutConsts import OGL_NOTELINK

from Singleton import Singleton

# from PyutConsts import OGL_AGGREGATION


def getOglLinkFactory():
    """
    Function to get the unique OglLinkFactory instance (singleton).

    @since 1.0
    @author P. Waelti <pwaelti@eivd.ch>
    """
    return OglLinkFactory()


def getLinkType(link):
    """
    Added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (20.11.2005)
    @return type (integer) of the link as defined in PyutConsts.py
    """
    if isinstance(link, OglAggregation):
        return OGL_AGGREGATION
    elif isinstance(link, OglComposition):
        return OGL_COMPOSITION
    elif isinstance(link, OglInheritance):
        return OGL_INHERITANCE
    elif isinstance(link, OglAssociation):
        return OGL_ASSOCIATION
    elif isinstance(link, OglInterface):
        return OGL_INTERFACE
    elif isinstance(link, OglNoteLink):
        return OGL_NOTELINK


class OglLinkFactory(Singleton):
    """
    This class is a factory to produce `OglLink` objects.
    It works under the Factory Design Pattern model. Ask for a link
    from this object and it will return you what you was asking for.
    """
    def init(self, *args, **kwds):
        self.logger: Logger = getLogger(__name__)

    # noinspection PyUnusedLocal
    def getOglLink(self, srcShape, pyutLink, destShape, linkType, srcPos=None, dstPos=None):
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
        if linkType == OGL_AGGREGATION:
            return OglAggregation(srcShape, pyutLink, destShape)

        elif linkType == OGL_COMPOSITION:
            return OglComposition(srcShape, pyutLink, destShape)

        elif linkType == OGL_INHERITANCE:
            return OglInheritance(srcShape, pyutLink, destShape)

        elif linkType == OGL_ASSOCIATION:
            return OglAssociation(srcShape, pyutLink, destShape)

        elif linkType == OGL_INTERFACE:
            return OglInterface(srcShape, pyutLink, destShape)

        elif linkType == OGL_NOTELINK:
            return OglNoteLink(srcShape, pyutLink, destShape)
        else:
            self.logger.error(f"Unknown linkType of OglLink into factory: {repr(linkType)}")
            return None

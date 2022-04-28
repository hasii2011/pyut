
from logging import Logger
from logging import getLogger

from org.pyut.ogl.OglAssociation import OglAssociation
from org.pyut.ogl.OglAggregation import OglAggregation
from org.pyut.ogl.OglComposition import OglComposition
from org.pyut.ogl.OglInheritance import OglInheritance
from org.pyut.ogl.OglInterface import OglInterface
from org.pyut.ogl.OglNoteLink import OglNoteLink

from org.pyut.model.PyutLinkType import PyutLinkType

from org.pyut.general.Singleton import Singleton
from org.pyut.ogl.sd.OglSDMessage import OglSDMessage


def getOglLinkFactory():
    """
    Function to get the unique OglLinkFactory instance (singleton).
    """
    return OglLinkFactory()


def getLinkType(link: OglAssociation) -> PyutLinkType:
    """

    Args:
        link:   The enumeration OglLinkType

    Returns:  The OglLinkType

    """

    if isinstance(link, OglAggregation):
        return PyutLinkType.AGGREGATION
    elif isinstance(link, OglComposition):
        return PyutLinkType.COMPOSITION
    elif isinstance(link, OglInheritance):
        return PyutLinkType.INHERITANCE
    elif isinstance(link, OglAssociation):
        return PyutLinkType.ASSOCIATION
    elif isinstance(link, OglInterface):
        return PyutLinkType.INTERFACE
    elif isinstance(link, OglNoteLink):
        return PyutLinkType.NOTELINK


class OglLinkFactory(Singleton):
    """
    This class is a factory to produce `OglLink` objects.
    It works under the Factory Design Pattern model. Ask for a link
    from this object, and it will return you what you was asking for.
    """
    def init(self, *args, **kwargs):
        self.logger: Logger = getLogger(__name__)

    # noinspection PyUnusedLocal
    def getOglLink(self, srcShape, pyutLink, destShape, linkType: PyutLinkType, srcPos=None, dstPos=None):
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
        if linkType == PyutLinkType.AGGREGATION:
            return OglAggregation(srcShape, pyutLink, destShape)

        elif linkType == PyutLinkType.COMPOSITION:
            return OglComposition(srcShape, pyutLink, destShape)

        elif linkType == PyutLinkType.INHERITANCE:
            return OglInheritance(srcShape, pyutLink, destShape)

        elif linkType == PyutLinkType.ASSOCIATION:
            return OglAssociation(srcShape, pyutLink, destShape)

        elif linkType == PyutLinkType.INTERFACE:
            return OglInterface(srcShape, pyutLink, destShape)

        elif linkType == PyutLinkType.NOTELINK:
            return OglNoteLink(srcShape, pyutLink, destShape)

        elif linkType == PyutLinkType.SD_MESSAGE:
            return OglSDMessage(srcShape=srcShape, pyutSDMessage=pyutLink, dstShape=destShape)
        else:
            self.logger.error(f"Unknown OglLinkType: {linkType}")
            return None

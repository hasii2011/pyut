from org.pyut.PyutLink import PyutLink
from org.pyut.enums.OglLinkType import OglLinkType
from org.pyut.ogl.OglClass import OglClass
from org.pyut.ogl.OglLinkFactory import getOglLinkFactory
from org.pyut.ui.UmlDiagramsFrame import UmlDiagramsFrame


class UmlClassDiagramsFrame(UmlDiagramsFrame):
    """
    UmlClassDiagramsFrame : a UML class diagram frame.

    This class is the instance of one UML class diagram structure.
    It derives its functionalities from UmlDiagramsFrame, but
    as he know the structure of a class diagram,
    he can load class diagram datas.

    Used by FilesHandling.

    :author: C.Dutoit
    :contact: dutoitc@hotmail.com
    :version: $Revision: 1.8 $
    """
    def __init__(self, parent):
        """
        Constructor.

        @param wx.Window parent : parent window
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        super().__init__(parent)
        self.newDiagram()

    def createLink(self, src: OglClass, dst: OglClass, linkType: OglLinkType = OglLinkType.OGL_AGGREGATION):
        """
        An API that is primarily used the Plugins

        Args:
            src:        The source OglClass
            dst:        The destination OglClass
            linkType:   The type of link
        """
        pyutLink = PyutLink("", linkType=linkType, source=src.getPyutObject(), destination=dst.getPyutObject())

        oglLinkFactory = getOglLinkFactory()
        oglLink = oglLinkFactory.getOglLink(src, pyutLink, dst, linkType)

        src.addLink(oglLink)
        dst.addLink(oglLink)

        src.getPyutObject().addLink(pyutLink)

        return oglLink

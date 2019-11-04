

from UmlDiagramsFrame import UmlDiagramsFrame

from org.pyut.PyutSDInstance import PyutSDInstance
from org.pyut.PyutSDMessage import PyutSDMessage

from OglSDInstance import OglSDInstance
from OglSDMessage import OglSDMessage

from PyutConsts import OGL_SD_MESSAGE


class UmlSequenceDiagramsFrame(UmlDiagramsFrame):
    """
    UmlSequenceDiagramsFrame : a UML sequence diagram frame.

    This class is the instance of one UML sequence diagram structure.
    It derives its functionalities from UmlDiagramsFrame, but
    as he know the structure of a sequence diagram,
    he can load sequence diagram datas.

    Used by FilesHandling.

    :Note on datas:
        - cdInstances is a set of class diagram instances,
          composed by label and lifeline


    :author: C.Dutoit
    :contact: dutoitc@hotmail.com
    :version: $Revision: 1.11 $
    """
    def __init__(self, parent):
        """
        Constructor.

        @param wx.Window parent : parent window
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        UmlDiagramsFrame.__init__(self, parent)
        self.newDiagram()
        self._cdInstances = []

    # noinspection PyUnusedLocal
    def createNewSDInstance(self, x, y):
        """
        Create a new class diagram instance

        @author C.Dutoit
        """
        # Create and add instance
        pyutSDInstance = PyutSDInstance()
        oglSDInstance  = OglSDInstance(pyutSDInstance, self)
        self.addShape(oglSDInstance, x, oglSDInstance.GetPosition()[1])

        return pyutSDInstance

    # noinspection PyUnusedLocal
    def createNewLink(self, src, dst, linkType=OGL_SD_MESSAGE, srcPos=None, dstPos=None):
        """
        Add a link between src and dst.

        @param OglSDInstance src  : source of the link
        @param OglSDInstance dst  : destination of the link
        @param int linkType : type of the link
        @param srcPos : position on source
        @param dstPos : position on  destination

        @return OglLink : the link created
        @author L. Burgbacher
        @modified C.Dutoit 20021125 : added srcPos and dstPos to be compatible  with Sequence diagram
        """

        srcTime = src.ConvertCoordToRelative(0, srcPos[1])[1]
        dstTime = dst.ConvertCoordToRelative(0, dstPos[1])[1]
        # srcTime=srcPos[1] - src.GetPosition()[1]
        # dstTime=dstPos[1] - dst.GetPosition()[1]
        # print "CreateNewLink - ", srcTime, dstTime print ", src/dst=", src, dst
        pyutLink = PyutSDMessage("msg test", src.getPyutObject(), srcTime, dst.getPyutObject(), dstTime)

        # Call the factory to create OGL Link
        oglLink = OglSDMessage(src, pyutLink, dst)
        pyutLink.setOglObject(oglLink)

        src.addLink(oglLink)                # add it to the source OglShape
        dst.addLink(oglLink)                # add it to the destination OglShape
        self._diagram.AddShape(oglLink)     # add it to the diagram

        self.Refresh()

        return oglLink

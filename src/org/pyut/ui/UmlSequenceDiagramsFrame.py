
from org.pyut.ui.UmlDiagramsFrame import UmlDiagramsFrame

from org.pyut.PyutSDInstance import PyutSDInstance
from org.pyut.PyutSDMessage import PyutSDMessage

from org.pyut.ogl.sd.OglSDInstance import OglSDInstance
from org.pyut.ogl.sd.OglSDMessage import OglSDMessage


class UmlSequenceDiagramsFrame(UmlDiagramsFrame):
    """
    UmlSequenceDiagramsFrame : a UML sequence diagram frame.

    This class is the instance of one UML sequence diagram structure.
    It derives its functionality from UmlDiagramsFrame, but
    it knows the structure of a sequence diagram,
    It can load sequence diagram data

    :Note on data
        - sdInstances is a set of class diagram instances,
          composed by label and lifeline
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
        Create a new sequence diagram instance
        """
        # Create and add instance
        pyutSDInstance = PyutSDInstance()
        oglSDInstance  = OglSDInstance(pyutSDInstance, self)
        self.addShape(oglSDInstance, x, oglSDInstance.GetPosition()[1])

        return pyutSDInstance

    def createNewLink(self, src, dst, srcPos=None, dstPos=None):
        """
        Adds an OglSDMessage link between src and dst.

        Args:
            src:    source of the link
            dst:    destination of the link
            srcPos: position on source
            dstPos: position on  destination

        Returns: the created OglSDMessage link
        """
        srcTime = src.ConvertCoordToRelative(0, srcPos[1])[1]
        dstTime = dst.ConvertCoordToRelative(0, dstPos[1])[1]
        pyutLink = PyutSDMessage("msg test", src.getPyutObject(), srcTime, dst.getPyutObject(), dstTime)

        oglLink = OglSDMessage(src, pyutLink, dst)
        pyutLink.setOglObject(oglLink)

        src.addLink(oglLink)
        dst.addLink(oglLink)
        self._diagram.AddShape(oglLink)

        self.Refresh()

        return oglLink

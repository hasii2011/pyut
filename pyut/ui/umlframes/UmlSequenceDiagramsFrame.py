
from logging import Logger
from logging import getLogger

from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

from pyutmodelv2.PyutSDInstance import PyutSDInstance
from pyutmodelv2.PyutSDMessage import PyutSDMessage

from ogl.sd.OglSDInstance import OglSDInstance
from ogl.sd.OglSDMessage import OglSDMessage

from pyut.ui.eventengine.IEventEngine import IEventEngine


class UmlSequenceDiagramsFrame(UmlDiagramsFrame):
    """
    UmlSequenceDiagramsFrame : a UML sequence diagram frame.

    This class is the instance of one UML sequence diagram structure.
    It derives its functionality from UmlDiagramsFrame, but
    it knows the structure of a sequence diagram,
    It can load sequence diagram data

    Note on data
        - sdInstances is a set of class diagram instances,
          composed by label and lifeline
    """
    cdfDebugId: int = 0x00FFF   # UML Sequence Diagrams Frame Debug ID

    def __init__(self, parent, eventEngine: IEventEngine | None = None):
        """

        Args:
            parent:  The parent window
            eventEngine: Pyut event engine
        """
        super().__init__(parent, eventEngine=eventEngine)   # type: ignore

        self._seqLogger: Logger = getLogger(__name__)
        self._cdfDebugId: int = UmlSequenceDiagramsFrame.cdfDebugId

        UmlSequenceDiagramsFrame.cdfDebugId += 1

        self.newDiagram()
        self._cdInstances = []  # type: ignore

    # noinspection PyUnusedLocal
    def createNewSDInstance(self, x, y) -> OglSDInstance:
        """
        Create a new sequence diagram instance
        """
        # Create and add instance
        pyutSDInstance: PyutSDInstance = PyutSDInstance()
        oglSDInstance:  OglSDInstance  = OglSDInstance(pyutSDInstance=pyutSDInstance)
        self.addShape(oglSDInstance, x, oglSDInstance.GetPosition()[1])

        self._seqLogger.info(f'Created {oglSDInstance}')
        return oglSDInstance

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
        # pyutLink.setOglObject(oglLink)

        src.addLink(oglLink)
        dst.addLink(oglLink)
        self._diagram.AddShape(oglLink)

        self.Refresh()

        self._seqLogger.info(f'Created {oglLink}')

        return oglLink

    def __repr__(self) -> str:

        debugId: str = f'0x{self._cdfDebugId:06X}'
        return f'UmlSequenceDiagramsFrame:[{debugId=}]'

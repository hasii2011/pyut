
from typing import TYPE_CHECKING
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from miniogl.AnchorPoint import AnchorPoint
from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutLink import PyutLink
from pyutmodel.PyutLinkType import PyutLinkType
from pyutmodel.PyutSDMessage import PyutSDMessage

from ogl.OglClass import OglClass
from ogl.OglLink import OglLink
from ogl.OglLinkFactory import getOglLinkFactory

from ogl.sd.OglSDInstance import OglSDInstance
from ogl.sd.OglSDMessage import OglSDMessage

from wx import Command
from wx import Point

from pyut.uiv2.eventengine.Events import EventType
from pyut.uiv2.eventengine.IEventEngine import IEventEngine

if TYPE_CHECKING:
    from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame


class CommandCreateOglLink(Command):

    NO_NAME_MESSAGE: str = "testMessage()"

    def __init__(self, eventEngine: IEventEngine,
                 src, dst,
                 linkType: PyutLinkType = PyutLinkType.INHERITANCE,
                 srcPos: Point = None,
                 dstPos: Point = None):

        super().__init__(canUndo=True, name='CreateOglLink')

        self.logger:       Logger       = getLogger(__name__)
        self._eventEngine: IEventEngine = eventEngine

        if src is None or dst is None:
            self._link = None
        else:
            self._link = self._createLink(src, dst, linkType, srcPos, dstPos)

    def GetName(self) -> str:
        return 'CreateOglLink'

    def CanUndo(self):
        return True

    def Do(self) -> bool:

        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._cbGetActiveUmlFrameForAdd)
        return True

    def Undo(self) -> bool:
        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._cbGetActiveUmlFrameForUndo)
        return True

    def _cbGetActiveUmlFrameForUndo(self, frame: 'UmlDiagramsFrame'):

        umlFrame: UmlDiagramsFrame = frame

        self._link.Detach()
        umlFrame.Refresh()

    def _cbGetActiveUmlFrameForAdd(self, frame: 'UmlDiagramsFrame'):

        umlFrame: UmlDiagramsFrame = frame

        umlFrame.GetDiagram().AddShape(self._link, withModelUpdate=False)

        # get the view start and end position and assign it to the
        # model position, then the view position is updated from
        # the model -- Legacy comment.  Not sure what that means -- Humberto
        sourcePoint:      AnchorPoint = self._link.GetSource()
        destinationPoint: AnchorPoint = self._link.GetDestination()

        srcPosX, srcPosY = sourcePoint.GetPosition()
        dstPosX, dstPosY = destinationPoint.GetPosition()

        self._link.GetSource().GetModel().SetPosition(srcPosX, srcPosY)
        self._link.GetDestination().GetModel().SetPosition(dstPosX, dstPosY)
        self._link.UpdateFromModel()

        umlFrame.Refresh()

    def _createLink(self, src, dst, linkType: PyutLinkType, srcPos, dstPos) -> OglLink:

        if linkType == PyutLinkType.INHERITANCE:
            return self._createInheritanceLink(src, dst)
        elif linkType == PyutLinkType.SD_MESSAGE:
            return self._createSDMessage(src=src, dest=dst, srcPos=srcPos, destPos=dstPos)

        pyutLink: PyutLink = PyutLink("", linkType=linkType, source=src.pyutObject, destination=dst.pyutObject)

        # Call the factory to create OGL Link
        oglLinkFactory = getOglLinkFactory()

        oglLink: OglLink = oglLinkFactory.getOglLink(srcShape=src, pyutLink=pyutLink, destShape=dst, linkType=linkType)

        src.addLink(oglLink)  # add it to the source Ogl Linkable Object
        dst.addLink(oglLink)  # add it to the destination Linkable Object

        src.pyutObject.addLink(pyutLink)   # add it to the source PyutClass

        return oglLink

    def _createInheritanceLink(self, child: OglClass, parent: OglClass) -> OglLink:
        """
        Add a parent link between the child and parent objects.

        Args:
            child:  Child PyutClass
            parent: Parent PyutClass

        Returns:
            The inheritance OglLink
        """
        sourceClass:      PyutClass = cast(PyutClass, child.pyutObject)
        destinationClass: PyutClass = cast(PyutClass, parent.pyutObject)
        pyutLink:         PyutLink = PyutLink("", linkType=PyutLinkType.INHERITANCE, source=sourceClass, destination=destinationClass)
        oglLink:          OglLink = getOglLinkFactory().getOglLink(child, pyutLink, parent, PyutLinkType.INHERITANCE)

        child.addLink(oglLink)
        parent.addLink(oglLink)

        # add it to the PyutClass
        # child.getPyutObject().addParent(parent.getPyutObject())
        childPyutClass:  PyutClass = cast(PyutClass, child.pyutObject)
        parentPyutClass: PyutClass = cast(PyutClass, parent.pyutObject)

        childPyutClass.addParent(parentPyutClass)

        return oglLink

    def _createSDMessage(self, src: OglSDInstance, dest: OglSDInstance, srcPos: Point, destPos: Point) -> OglSDMessage:

        srcRelativeCoordinates:  Tuple[int, int] = src.ConvertCoordToRelative(0, srcPos[1])
        destRelativeCoordinates: Tuple[int, int] = dest.ConvertCoordToRelative(0, destPos[1])

        srcY  = srcRelativeCoordinates[1]
        destY = destRelativeCoordinates[1]

        pyutSDMessage = PyutSDMessage(CommandCreateOglLink.NO_NAME_MESSAGE, src.pyutObject, srcY, dest.pyutObject, destY)

        oglLinkFactory = getOglLinkFactory()
        oglSdMessage: OglSDMessage = oglLinkFactory.getOglLink(srcShape=src, pyutLink=pyutSDMessage, destShape=dest,
                                                               linkType=PyutLinkType.SD_MESSAGE, srcPos=srcPos, dstPos=destPos)

        return oglSdMessage

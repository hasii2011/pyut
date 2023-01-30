
from typing import TYPE_CHECKING
from typing import Tuple
from typing import cast

from wx import Command
from wx import Point

from miniogl.AnchorPoint import AnchorPoint

from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutLink import PyutLink
from pyutmodel.PyutLinkType import PyutLinkType
from pyutmodel.PyutSDMessage import PyutSDMessage

from ogl.OglClass import OglClass
from ogl.OglLink import OglLink

from ogl.sd.OglSDInstance import OglSDInstance
from ogl.sd.OglSDMessage import OglSDMessage

from ogl.OglLinkFactory import getOglLinkFactory

from pyut.ui.wxcommands.Types import DoableObjectType

from pyut.uiv2.eventengine.IEventEngine import IEventEngine

if TYPE_CHECKING:
    from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame


class BaseWxLinkCommand(Command):

    NO_NAME_MESSAGE: str = "testMessage()"

    def __init__(self, partialName: str, linkType: PyutLinkType, eventEngine: IEventEngine):

        self._name: str = f'{partialName} {self._toCommandName(linkType=linkType)}'

        super().__init__(canUndo=True, name=self._name)

        self._eventEngine: IEventEngine = eventEngine

        self._srcOglObject: DoableObjectType = cast(DoableObjectType, None)
        self._dstOglObject: DoableObjectType = cast(DoableObjectType, None)

        self._linkType: PyutLinkType = linkType

        self._srcPoint: Point = cast(Point, None)
        self._dstPoint: Point = cast(Point, None)

        self._link: OglLink      = cast(OglLink, None)

    def GetName(self) -> str:
        return self._name

    def CanUndo(self):
        return True

    def _cbDoDeleteLink(self, frame: 'UmlDiagramsFrame'):
        """
        Dual purpose depending on the context
        From CommandCreateOglLink.Undo or from CommandDeleteOglLink.Do

        Args:
            frame:  Currently, active frame
        """

        umlFrame: UmlDiagramsFrame = frame

        self._link.Detach()
        umlFrame.Refresh()

    def _cbPlaceLink(self, frame: 'UmlDiagramsFrame'):
        """
        Assumes that self._link was created prior to invoking this method
        Dual purpose depending on context
        From CommandCreateOglLink.Do and from CommandDeleteOglLink.Undo
        Args:
            frame: Currently active frame
        """

        umlFrame: UmlDiagramsFrame = frame

        umlFrame.diagram.AddShape(self._link, withModelUpdate=False)

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

    def _createLink(self, src, dst, linkType: PyutLinkType, srcPos: Point, dstPos: Point) -> OglLink:
        """
        Creates a specific OglLink instance depending on the link type
        Args:
            src:        The source object
            dst:        The destination object
            linkType:
            srcPos:     The source position
            dstPos:     The destination position

        Returns:
        """

        if linkType == PyutLinkType.INHERITANCE:
            return self._createInheritanceLink(src, dst)
        elif linkType == PyutLinkType.SD_MESSAGE:
            return self._createSDMessage(src=src, dest=dst, srcPos=srcPos, destPos=dstPos)

        pyutLink: PyutLink = PyutLink("", linkType=linkType, source=src.pyutObject, destination=dst.pyutObject)
        pyutLink.name = f'{linkType.name.capitalize()}-{pyutLink.id}'

        # Call the factory to create OGL Link
        oglLinkFactory = getOglLinkFactory()

        oglLink: OglLink = oglLinkFactory.getOglLink(srcShape=src, pyutLink=pyutLink, destShape=dst, linkType=linkType)

        src.addLink(oglLink)  # add it to the source Ogl Linkable Object
        dst.addLink(oglLink)  # add it to the destination Linkable Object

        src.pyutObject.addLink(pyutLink)   # add it to the source PyutClass

        self._name = self._toCommandName(linkType)
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
        childPyutClass:  PyutClass = cast(PyutClass, child.pyutObject)
        parentPyutClass: PyutClass = cast(PyutClass, parent.pyutObject)

        childPyutClass.addParent(parentPyutClass)

        return oglLink

    def _createSDMessage(self, src: OglSDInstance, dest: OglSDInstance, srcPos: Point, destPos: Point) -> OglSDMessage:

        srcRelativeCoordinates:  Tuple[int, int] = src.ConvertCoordToRelative(0, srcPos[1])
        destRelativeCoordinates: Tuple[int, int] = dest.ConvertCoordToRelative(0, destPos[1])

        srcY  = srcRelativeCoordinates[1]
        destY = destRelativeCoordinates[1]

        pyutSDMessage = PyutSDMessage(BaseWxLinkCommand.NO_NAME_MESSAGE, src.pyutObject, srcY, dest.pyutObject, destY)

        oglLinkFactory = getOglLinkFactory()
        oglSdMessage: OglSDMessage = oglLinkFactory.getOglLink(srcShape=src, pyutLink=pyutSDMessage, destShape=dest, linkType=PyutLinkType.SD_MESSAGE)

        return oglSdMessage

    def _toCommandName(self, linkType: PyutLinkType) -> str:
        return f'{linkType.name.capitalize()} Link'


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
from ogl.OglAssociation import OglAssociation

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

        link: OglLink = self._link

        if isinstance(link, OglAssociation):
            oglAssociation: OglAssociation = cast(OglAssociation, link)
            if oglAssociation.centerLabel is not None:
                oglAssociation.centerLabel.Detach()
            if oglAssociation.sourceCardinality is not None:
                oglAssociation.sourceCardinality.Detach()
            if oglAssociation.destinationCardinality is not None:
                oglAssociation.destinationCardinality.Detach()

        link.Detach()
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
        #
        # TODO: Is this a hack?  I think it is
        #
        if isinstance(self._link, OglAssociation):
            oglAssociation: OglAssociation = cast(OglAssociation, self._link)
            oglAssociation.createDefaultAssociationLabels()

            umlFrame.diagram.AddShape(shape=oglAssociation.centerLabel)
            umlFrame.diagram.AddShape(shape=oglAssociation.sourceCardinality)
            umlFrame.diagram.AddShape(shape=oglAssociation.destinationCardinality)

        # get the view start and end position and assign it to the
        # model position, then the view position is updated from
        # the model -- Legacy comment.  Not sure what that means -- Humberto
        sourcePoint:      AnchorPoint = self._link.sourceAnchor
        destinationPoint: AnchorPoint = self._link.destinationAnchor

        srcPosX, srcPosY = sourcePoint.GetPosition()
        dstPosX, dstPosY = destinationPoint.GetPosition()

        self._link.sourceAnchor.GetModel().SetPosition(srcPosX, srcPosY)
        self._link.destinationAnchor.GetModel().SetPosition(dstPosX, dstPosY)
        self._link.UpdateFromModel()

        umlFrame.Refresh()

    def _createLink(self) -> OglLink:
        """

        Returns:  A specific OglLink instance depending on the link type
        """
        # src, dst, linkType: PyutLinkType, srcPos: Point, dstPos: Point
        # self._srcOglObject, self._dstOglObject, self._linkType, self._srcPoint, self._dstPoint
        linkType: PyutLinkType     = self._linkType
        src:      DoableObjectType = self._srcOglObject
        dst:      DoableObjectType = self._dstOglObject
        srcPos:   Point            = self._srcPoint
        dstPos:   Point            = self._dstPoint

        srcClass: OglClass = cast(OglClass, src)
        dstClass: OglClass = cast(OglClass, dst)

        if linkType == PyutLinkType.INHERITANCE:
            return self._createInheritanceLink(srcClass, dstClass)
        elif linkType == PyutLinkType.SD_MESSAGE:
            srcSdInstance: OglSDInstance = cast(OglSDInstance, src)
            dstSdInstance: OglSDInstance = cast(OglSDInstance, dst)
            return self._createSDMessage(src=srcSdInstance, dest=dstSdInstance, srcPos=srcPos, destPos=dstPos)

        pyutLink: PyutLink = PyutLink("", linkType=linkType, source=srcClass.pyutObject, destination=dstClass.pyutObject)

        pyutLink.name = f'{linkType.name.capitalize()}-{pyutLink.id}'
        # pyutLink.destinationCardinality = ''
        # pyutLink.sourceCardinality      = ''

        # Call the factory to create OGL Link
        oglLinkFactory = getOglLinkFactory()

        oglLink: OglLink = oglLinkFactory.getOglLink(srcShape=src, pyutLink=pyutLink, destShape=dst, linkType=linkType)

        srcClass.addLink(oglLink)  # add it to the source Ogl Linkable Object
        dstClass.addLink(oglLink)  # add it to the destination Linkable Object

        srcClass.pyutObject.addLink(pyutLink)   # add it to the source PyutClass

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
        # Because I do not like the generated name
        if linkType == PyutLinkType.SD_MESSAGE:
            return f'SDMessage Link'
        else:
            return f'{linkType.name.capitalize()} Link'

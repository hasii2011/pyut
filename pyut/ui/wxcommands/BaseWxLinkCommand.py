
from typing import TYPE_CHECKING
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from wx import Command
from wx import Point

from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.PyutLink import PyutLink
from pyutmodelv2.PyutSDMessage import PyutSDMessage

from pyutmodelv2.enumerations.PyutLinkType import PyutLinkType

from miniogl.AnchorPoint import AnchorPoint
from miniogl.LineShape import ControlPoints
from miniogl.ControlPoint import ControlPoint
from miniogl.models.ShapeModel import ShapeModel

from ogl.OglClass import OglClass
from ogl.OglLink import OglLink
from ogl.OglActor import OglActor
from ogl.OglAssociation import OglAssociation

from ogl.sd.OglSDInstance import OglSDInstance
from ogl.sd.OglSDMessage import OglSDMessage

from ogl.OglLinkFactory import getOglLinkFactory

from pyut.ui.wxcommands.Types import DoableObjectType

from pyut.ui.eventengine.IEventEngine import IEventEngine

if TYPE_CHECKING:
    from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame


class BaseWxLinkCommand(Command):

    NO_NAME_MESSAGE: str = "testMessage()"

    def __init__(self, partialName: str, linkType: PyutLinkType, eventEngine: IEventEngine):

        self._name: str = f'{partialName} {self._toCommandName(linkType=linkType)}'

        super().__init__(canUndo=True, name=self._name)

        self._linkLogger:     Logger         = getLogger(__name__)
        self._eventEngine:    IEventEngine   = eventEngine

        self._srcOglObject: DoableObjectType = cast(DoableObjectType, None)
        self._dstOglObject: DoableObjectType = cast(DoableObjectType, None)

        self._linkType: PyutLinkType = linkType

        self._srcPoint: Point = cast(Point, None)
        self._dstPoint: Point = cast(Point, None)

        self._link:          OglLink       = cast(OglLink, None)
        self._pyutLink:      PyutLink      = cast(PyutLink, None)    # for undo of delete
        self._controlPoints: ControlPoints = ControlPoints([])       # for undo of delete or create link from plugin manager
        self._spline:        bool          = False

    def _controlPointsSetter(self, newValues: ControlPoints):
        self._controlPoints = newValues

    # noinspection PyTypeChecker
    controlPoints = property(fget=None, fset=_controlPointsSetter)

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
        self._linkLogger.info(f'{link.__repr__()} deleted')
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

        if isinstance(self._link, OglAssociation):
            oglAssociation: OglAssociation = cast(OglAssociation, self._link)

            umlFrame.diagram.AddShape(shape=oglAssociation.centerLabel)
            umlFrame.diagram.AddShape(shape=oglAssociation.sourceCardinality)
            umlFrame.diagram.AddShape(shape=oglAssociation.destinationCardinality)

        # get the view start and end position and assign it to the
        # model position, then the view position is updated from
        # the model: Legacy comment.  Not sure what that means: Humberto
        sourcePoint:      AnchorPoint = self._link.sourceAnchor
        destinationPoint: AnchorPoint = self._link.destinationAnchor

        srcPosX, srcPosY = sourcePoint.GetPosition()
        dstPosX, dstPosY = destinationPoint.GetPosition()

        self._link.sourceAnchor.model.SetPosition(srcPosX, srcPosY)
        self._link.destinationAnchor.model.SetPosition(dstPosX, dstPosY)
        self._link.UpdateFromModel()

        umlFrame.Refresh()

        self._linkLogger.info(f'Create: {self._link}')

    def _createLink(self) -> OglLink:
        """

        Returns:  A specific OglLink instance depending on the link type
        """
        linkType: PyutLinkType = self._linkType
        srcPos:   Point        = self._srcPoint
        dstPos:   Point        = self._dstPoint

        if linkType == PyutLinkType.INHERITANCE:
            srcClass: OglClass = cast(OglClass, self._srcOglObject)
            dstClass: OglClass = cast(OglClass, self._dstOglObject)
            oglLink: OglLink = self._createInheritanceLink(srcClass, dstClass)
        elif linkType == PyutLinkType.SD_MESSAGE:
            srcSdInstance: OglSDInstance = cast(OglSDInstance, self._srcOglObject)
            dstSdInstance: OglSDInstance = cast(OglSDInstance, self._dstOglObject)
            oglLink = self._createSDMessage(src=srcSdInstance, dest=dstSdInstance, srcPos=srcPos, destPos=dstPos)
        elif isinstance(self._srcOglObject, OglActor) and isinstance(self._dstOglObject, OglSDInstance):
            # Special case for sequence diagram
            oglActor:   OglActor      = cast(OglActor, self._srcOglObject)
            sdInstance: OglSDInstance = cast(OglSDInstance, self._dstOglObject)
            pyutLink:   PyutLink      = PyutLink(name="", linkType=linkType, source=oglActor.pyutObject, destination=sdInstance.pyutSDInstance)

            oglLinkFactory = getOglLinkFactory()

            oglLink = oglLinkFactory.getOglLink(srcShape=oglActor, pyutLink=pyutLink, destShape=sdInstance, linkType=linkType)

        else:
            oglLink = self._createAssociationLink()

        oglLink.spline = self._spline

        return oglLink

    def _createAssociationLink(self) -> OglLink:

        srcClass: OglClass = cast(OglClass, self._srcOglObject)
        dstClass: OglClass = cast(OglClass, self._dstOglObject)

        linkType: PyutLinkType = self._linkType

        # If none, we are creating from scratch
        if self._pyutLink is None:
            pyutLink: PyutLink = PyutLink(name="", linkType=linkType, source=srcClass.pyutObject, destination=dstClass.pyutObject)
            # TODO: This will not be needed when Ogl supports this as a preference
            if linkType == PyutLinkType.INTERFACE:
                pyutLink.name = 'implements'
            else:
                pyutLink.name = f'{linkType.name.capitalize()}-{pyutLink.id}'
        else:
            # If we have a value, we are undoing a delete action
            pyutLink = self._pyutLink

        # Call the factory to create OGL Link

        oglLinkFactory = getOglLinkFactory()
        oglLink: OglLink = oglLinkFactory.getOglLink(srcShape=srcClass, pyutLink=pyutLink, destShape=dstClass, linkType=linkType)
        self._placeAnchorsInCorrectPosition(oglLink=oglLink)
        self._createNeededControlPoints(oglLink=oglLink)

        srcClass.addLink(oglLink)  # add it to the source Ogl Linkable Object
        dstClass.addLink(oglLink)  # add it to the destination Ogl Linkable Object
        srcClass.pyutObject.addLink(pyutLink)  # add it to the source PyutClass

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
        pyutLink:         PyutLink  = PyutLink("", linkType=PyutLinkType.INHERITANCE, source=sourceClass, destination=destinationClass)
        oglLink:          OglLink   = getOglLinkFactory().getOglLink(child, pyutLink, parent, PyutLinkType.INHERITANCE)

        child.addLink(oglLink)
        parent.addLink(oglLink)

        self._placeAnchorsInCorrectPosition(oglLink=oglLink)
        self._createNeededControlPoints(oglLink=oglLink)
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

        if isinstance(src, OglActor):
            pyutSDMessage: PyutSDMessage = PyutSDMessage(BaseWxLinkCommand.NO_NAME_MESSAGE, src.pyutObject, srcY, dest.pyutSDInstance, destY)
        else:
            pyutSDMessage = PyutSDMessage(BaseWxLinkCommand.NO_NAME_MESSAGE, src.pyutSDInstance, srcY, dest.pyutSDInstance, destY)

        oglLinkFactory = getOglLinkFactory()
        oglSdMessage: OglSDMessage = oglLinkFactory.getOglLink(srcShape=src, pyutLink=pyutSDMessage, destShape=dest, linkType=PyutLinkType.SD_MESSAGE)

        return oglSdMessage

    def _placeAnchorsInCorrectPosition(self, oglLink: OglLink):

        srcAnchor: AnchorPoint = oglLink.sourceAnchor
        dstAnchor: AnchorPoint = oglLink.destinationAnchor

        srcX, srcY = self._srcPoint.Get()
        dstX, dstY = self._dstPoint.Get()

        srcAnchor.SetPosition(x=srcX, y=srcY)
        dstAnchor.SetPosition(x=dstX, y=dstY)

        srcModel: ShapeModel = srcAnchor.model
        dstModel: ShapeModel = dstAnchor.model

        srcModel.SetPosition(x=srcX, y=srcY)
        dstModel.SetPosition(x=dstY, y=dstY)

    def _createNeededControlPoints(self, oglLink: OglLink):

        parent:   OglClass = oglLink.sourceAnchor.parent
        selfLink: bool     = parent is oglLink.destinationAnchor.parent

        for cp in self._controlPoints:
            controlPoint: ControlPoint = cast(ControlPoint, cp)
            oglLink.AddControl(control=controlPoint, after=None)
            if selfLink:
                x, y = controlPoint.GetPosition()
                controlPoint.parent = parent
                controlPoint.SetPosition(x, y)

    def _toCommandName(self, linkType: PyutLinkType) -> str:
        # Because I do not like the generated name
        if linkType == PyutLinkType.SD_MESSAGE:
            return f'SDMessage Link'
        else:
            return f'{linkType.name.capitalize()} Link'

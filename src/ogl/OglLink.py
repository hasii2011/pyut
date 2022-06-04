
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from math import sqrt

# noinspection PyPackageRequirements
from deprecated import deprecated

from wx import BLACK_PEN
from wx import EVT_MENU

from wx import CommandEvent
from wx import Menu
from wx import MenuItem
from wx import MouseEvent


from miniogl.AnchorPoint import AnchorPoint
from miniogl.ControlPoint import ControlPoint
from miniogl.LinePoint import LinePoint
from miniogl.LineShape import LineShape
from miniogl.ShapeEventHandler import ShapeEventHandler
from miniogl.AttachmentLocation import AttachmentLocation

from ogl.OglPosition import OglPosition

from pyutmodel.PyutLink import PyutLink

from ogl.IllegalOperationException import IllegalOperationException

from ogl.OglUtils import OglUtils

[
    MENU_ADD_BEND,
    MENU_REMOVE_BEND,
    MENU_TOGGLE_SPLINE,
]  = OglUtils.assignID(3)


class OglLink(LineShape, ShapeEventHandler):
    """
    Abstract class for graphical link.
    This class should be the base class for every type of link. It implements
    the following functions :
        - Link between objects position management
        - Control points (2)
        - Data layer link association
        - Source and destination objects

    You can inherit from this class to implement your favorite type of links
    like `OglAssociation`.

    There is a link factory (See `OglLinkFactory`) you can use to build
    the different type of links that exist.

    """
    clsLogger: Logger = getLogger(__name__)

    def __init__(self, srcShape, pyutLink, dstShape, srcPos=None, dstPos=None):
        """

        Args:
            srcShape:   Source shape
            pyutLink:   Conceptual links associated with the graphical links.
            dstShape:   Destination shape
            srcPos:     Position of source      Override location of input source
            dstPos:     Position of destination Override location of input destination
        """
        self._srcShape  = srcShape
        self._destShape = dstShape

        OglLink.clsLogger.debug(f'Input Override positions - srcPos: {srcPos} dstPos: {dstPos}')
        if srcPos is None and dstPos is None:
            srcX, srcY = self._srcShape.GetPosition()
            dstX, dstY = self._destShape.GetPosition()

            orient = OglLink.getOrient(srcX,  srcY, dstX, dstY)

            sw, sh = self._srcShape.GetSize()
            dw, dh = self._destShape.GetSize()
            if orient == AttachmentLocation.NORTH:
                srcX, srcY = sw//2, 0
                dstX, dstY = dw//2, dh
            elif orient == AttachmentLocation.SOUTH:
                srcX, srcY = sw//2, sh
                dstX, dstY = dw//2, 0
            elif orient == AttachmentLocation.EAST:
                srcX, srcY = sw, sh//2
                dstX, dstY = 0, dh//2
            elif orient == AttachmentLocation.WEST:
                srcX, srcY = 0, sh//2
                dstX, dstY = dw, dh//2

            # ============== Avoid over-lining; Added by C.Dutoit ================
            # lstAnchorsPoints = [anchor.GetRelativePosition() for anchor in srcShape.GetAnchors()]
            # while (srcX, srcY) in lstAnchorsPoints:
            #     OglLink.clsLogger.warning(f'Over-lining in source shape')
            #     if orient == PyutAttachmentPoint.NORTH or orient == PyutAttachmentPoint.SOUTH:
            #         srcX += 10
            #     else:
            #         srcY += 10
            #
            # lstAnchorsPoints = [anchor.GetRelativePosition() for anchor in dstShape.GetAnchors()]
            # while (dstX, dstY) in lstAnchorsPoints:
            #     from org.pyut.ogl.OglClass import OglClass
            #     dstShape: OglClass = cast(OglClass, dstShape)
            #     OglLink.clsLogger.warning(f'Over-lining in destination shape: {dstShape.getPyutObject}')
            #     if orient == PyutAttachmentPoint.NORTH or orient == PyutAttachmentPoint.SOUTH:
            #         dstX += 10
            #     else:
            #         dstY += 10

            # =========== end avoid over-lining-Added by C.Dutoit ================
        else:
            # Use provided position
            (srcX, srcY) = srcPos
            (dstX, dstY) = dstPos

        srcAnchor: AnchorPoint = self._srcShape.AddAnchor(srcX, srcY)
        dstAnchor: AnchorPoint = self._destShape.AddAnchor(dstX, dstY)
        srcAnchor.SetPosition(srcX, srcY)
        dstAnchor.SetPosition(dstX, dstY)
        srcAnchor.SetVisible(False)
        dstAnchor.SetVisible(False)
        OglLink.clsLogger.debug(f'src anchor pos: {srcAnchor.GetPosition()} dst anchor pos {dstAnchor.GetPosition()}')
        srcAnchor.SetDraggable(True)
        dstAnchor.SetDraggable(True)
        # Init
        LineShape.__init__(self, srcAnchor, dstAnchor)
        # Set up painting colors
        self.SetPen(BLACK_PEN)
        # Keep reference to the PyutLink for mouse events, in order
        # to can find back the corresponding link
        if pyutLink is not None:
            self._link = pyutLink
        else:
            self._link = PyutLink()

    @staticmethod
    def getOrient(srcX, srcY, destX, destY) -> AttachmentLocation:
        """
        Giving a source and destination, returns where the destination
        is located according to the source.

        @param int srcX  : X pos of src point
        @param int srcY  : Y pos of src point
        @param int destX : X pos of dest point
        @param int destY : Y pos of dest point
        """
        deltaX = srcX - destX
        deltaY = srcY - destY
        if deltaX > 0:  # dest is not east
            if deltaX > abs(deltaY):  # dest is west
                return AttachmentLocation.WEST
            elif deltaY > 0:
                return AttachmentLocation.NORTH
            else:
                return AttachmentLocation.SOUTH
        else:  # dest is not west
            if -deltaX > abs(deltaY):  # dest is east
                return AttachmentLocation.EAST
            elif deltaY > 0:
                return AttachmentLocation.NORTH
            else:
                return AttachmentLocation.SOUTH

    def getSourceShape(self):
        """
        Return the source shape for this link.

        @return OglObject
        @since 1.22
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        return self._srcShape

    def getDestinationShape(self):
        """
        Return the destination shape for this link.

        @return OglObject
        @since 1.22
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        return self._destShape

    @deprecated('Use pyutObject property')
    def getPyutObject(self):
        """
        Returns the associated PyutLink.

        Returns: PyutLink

        """
        return self._link

    @deprecated('Use pyutObject property')
    def setPyutObject(self, pyutLink):
        """
        Sets the associated PyutLink.

        Args:
            pyutLink: link to associate
        """
        self._link = pyutLink

    @property
    def pyutObject(self) -> PyutLink:
        return self._link

    @pyutObject.setter
    def pyutObject(self, pyutLink: PyutLink):
        self._link = pyutLink

    def getAnchors(self) -> Tuple[AnchorPoint, AnchorPoint]:
        return self._srcAnchor, self._dstAnchor

    def Detach(self):
        """
        Detach the line and all its line points, including src and dst.

        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        if self._diagram is not None and not self._protected:
            LineShape.Detach(self)
            self._srcAnchor.SetProtected(False)
            self._dstAnchor.SetProtected(False)
            self._srcAnchor.Detach()
            self._dstAnchor.Detach()
            try:
                self.getSourceShape().getLinks().remove(self)
            except ValueError:
                pass
            try:
                self.getDestinationShape().getLinks().remove(self)
            except ValueError:
                pass
            try:
                self._link.getSource().getLinks().remove(self._link)
            except ValueError:
                pass

    def optimizeLine(self):
        """
        Optimize line, so that the line length is minimized
        """
        # Get elements
        srcAnchor = self.GetSource()
        dstAnchor = self.GetDestination()

        srcX, srcY = self._srcShape.GetPosition()
        dstX, dstY = self._destShape.GetPosition()

        srcSize = self._srcShape.GetSize()
        dstSize = self._destShape.GetSize()

        OglLink.clsLogger.info(f"optimizeLine - ({srcX},{srcY}) / ({dstX},{dstY})")
        # Find new positions
        # Little tips
        optimalSrcX, optimalSrcY, optimalDstX, optimalDstY = dstX, dstY, srcX, srcY

        optimalSrcX += dstSize[0] // 2
        optimalSrcY += dstSize[1] // 2
        optimalDstX += srcSize[0] // 2
        optimalDstY += srcSize[1] // 2

        srcAnchor.SetPosition(optimalSrcX, optimalSrcY)
        dstAnchor.SetPosition(optimalDstX, optimalDstY)

    # noinspection PyUnusedLocal
    def OnRightDown(self, event: MouseEvent):
        """
        Handle right-clicks on our UML LineShape-  Override base handler;  It does nothing

        Args:
            event:
        """
        from ogl.sd.OglSDMessage import OglSDMessage

        if isinstance(self, OglSDMessage) is True:
            return
        menu: Menu = Menu()
        menu.Append(MENU_ADD_BEND,      'Add Bend',      'Add Bend at right click point')
        menu.Append(MENU_REMOVE_BEND,   'Remove Bend',   'Remove Bend closest to click point')
        menu.Append(MENU_TOGGLE_SPLINE, 'Toggle Spline', 'Best with at least one bend')

        if len(self._controls) == 0:
            bendItem: MenuItem = menu.FindItemById(MENU_REMOVE_BEND)
            bendItem.Enable(enable=False)

        x: int = event.GetX()
        y: int = event.GetY()
        clickPoint: Tuple[int, int] = (x, y)

        OglLink.clsLogger.debug(f'OglLink - {clickPoint=}')
        # I hate lambdas -- humberto
        menu.Bind(EVT_MENU, lambda evt, data=clickPoint: self._onMenuItemSelected(evt, data))

        frame = self._diagram.GetPanel()
        frame.PopupMenu(menu, x, y)

    # noinspection PyUnusedLocal
    def _onMenuItemSelected(self, event: CommandEvent, data):

        eventId: int = event.GetId()
        if eventId == MENU_ADD_BEND:
            self._addBend(data)
        elif eventId == MENU_REMOVE_BEND:
            self._removeBend(data)
        elif eventId == MENU_TOGGLE_SPLINE:
            self._toggleSpline()

    def _computeLinkLength(self, srcPosition: OglPosition, destPosition: OglPosition) -> int:
        """

        Returns:  The length of the link between the source shape and destination shape
        """
        dx, dy = self._computeDxDy(srcPosition, destPosition)
        linkLength = round(sqrt(dx*dx + dy*dy))
        if linkLength == 0:
            linkLength = 1

        return linkLength

    def _computeDxDy(self, srcPosition: OglPosition, destPosition: OglPosition) -> Tuple[int, int]:
        """

        Args:
            srcPosition:    source position
            destPosition:   destination position

        Returns:
            A tuple of deltaX and deltaY of the shape position
        """
        if self._srcShape is None or self._destShape is None:
            raise IllegalOperationException('Either the source or the destination shape is None')

        srcX: int = srcPosition.x
        srcY: int = srcPosition.y
        dstX: int = destPosition.x
        dstY: int = destPosition.y

        dx: int = dstX - srcX
        dy: int = dstY - srcY

        return dx, dy

    def _addBend(self, clickPoint: Tuple[int, int]):

        OglLink.clsLogger.debug(f'Add a bend.  {clickPoint=}')

        x = clickPoint[0]
        y = clickPoint[1]
        cp = ControlPoint(x, y)

        cp.SetVisible(True)
        #
        # Add it either before the destinationAnchor or the sourceAnchor
        #
        lp: LinePoint = self.GetSource()
        self.AddControl(control=cp, after=lp)

        frame = self._diagram.GetPanel()
        frame.GetDiagram().AddShape(cp)
        frame.Refresh()

    def _removeBend(self, clickPoint: Tuple[int, int]):

        OglLink.clsLogger.debug(f'Remove a bend.  {clickPoint=}')

        cp: ControlPoint = self._findClosestControlPoint(clickPoint=clickPoint)

        assert cp is not None, 'We should have previously verified there was at least one on the line'

        self._removeControl(control=cp)
        cp.Detach()
        cp.SetVisible(False)    # Work around still on screen but not visible and not saved

        frame = self._diagram.GetPanel()
        frame.Refresh()

    def _toggleSpline(self):

        self.SetSpline(not self.GetSpline())

        frame = self._diagram.GetPanel()
        frame.Refresh()

    def _findClosestControlPoint(self, clickPoint: Tuple[int, int]) -> ControlPoint:

        controlPoints = self.GetControlPoints()

        distance:     float        = 1000.0    # Impossibly long distance
        closestPoint: ControlPoint = cast(ControlPoint, None)
        srcPosition:  OglPosition  = OglPosition(x=clickPoint[0], y=clickPoint[1])

        for controlPoint in controlPoints:
            xy:    Tuple[int, int] = controlPoint.GetPosition()
            destX: int = xy[0]
            destY: int = xy[1]
            destPosition: OglPosition = OglPosition(x=destX, y=destY)

            dx, dy = self._computeDxDy(srcPosition, destPosition)
            currentDistance = sqrt(dx*dx + dy*dy)
            self.clsLogger.debug(f'{currentDistance=}')
            if currentDistance <= distance:
                distance = currentDistance
                closestPoint = cast(ControlPoint, controlPoint)

        return closestPoint

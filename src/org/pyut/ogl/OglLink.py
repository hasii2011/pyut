
from typing import Tuple

from logging import Logger
from logging import getLogger

from math import sqrt

from wx import BLACK_PEN

from org.pyut.MiniOgl.AnchorPoint import AnchorPoint
from org.pyut.MiniOgl.LineShape import LineShape
from org.pyut.MiniOgl.ShapeEventHandler import ShapeEventHandler

from org.pyut.model.PyutLink import PyutLink

from org.pyut.enums.AttachmentPoint import PyutAttachmentPoint
from org.pyut.ogl.IllegalOperationException import IllegalOperationException


def getOrient(srcX, srcY, destX, destY) -> PyutAttachmentPoint:
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
        if deltaX > abs(deltaY):    # dest is west
            return PyutAttachmentPoint.WEST
        elif deltaY > 0:
            return PyutAttachmentPoint.NORTH
        else:
            return PyutAttachmentPoint.SOUTH
    else:   # dest is not west
        if -deltaX > abs(deltaY):   # dest is east
            return PyutAttachmentPoint.EAST
        elif deltaY > 0:
            return PyutAttachmentPoint.NORTH
        else:
            return PyutAttachmentPoint.SOUTH


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

        self.clsLogger.debug(f'Input Override positions - srcPos: {srcPos} dstPos: {dstPos}')
        if srcPos is None and dstPos is None:
            srcX, srcY = self._srcShape.GetPosition()
            dstX, dstY = self._destShape.GetPosition()

            orient = getOrient(srcX,  srcY, dstX, dstY)

            sw, sh = self._srcShape.GetSize()
            dw, dh = self._destShape.GetSize()
            if orient == PyutAttachmentPoint.NORTH:
                srcX, srcY = sw/2, 0
                dstX, dstY = dw/2, dh
            elif orient == PyutAttachmentPoint.SOUTH:
                srcX, srcY = sw/2, sh
                dstX, dstY = dw/2, 0
            elif orient == PyutAttachmentPoint.EAST:
                srcX, srcY = sw, sh/2
                dstX, dstY = 0, dh/2
            elif orient == PyutAttachmentPoint.WEST:
                srcX, srcY = 0, sh/2
                dstX, dstY = dw, dh/2

            # ============== Avoid over-lining; Added by C.Dutoit ================
            # lstAnchorsPoints = [anchor.GetRelativePosition() for anchor in srcShape.GetAnchors()]
            # while (srcX, srcY) in lstAnchorsPoints:
            #     self.clsLogger.warning(f'Over-lining in source shape')
            #     if orient == PyutAttachmentPoint.NORTH or orient == PyutAttachmentPoint.SOUTH:
            #         srcX += 10
            #     else:
            #         srcY += 10
            #
            # lstAnchorsPoints = [anchor.GetRelativePosition() for anchor in dstShape.GetAnchors()]
            # while (dstX, dstY) in lstAnchorsPoints:
            #     from org.pyut.ogl.OglClass import OglClass
            #     dstShape: OglClass = cast(OglClass, dstShape)
            #     self.clsLogger.warning(f'Over-lining in destination shape: {dstShape.getPyutObject}')
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
        self.clsLogger.debug(f'src anchor pos: {srcAnchor.GetPosition()} dst anchor pos {dstAnchor.GetPosition()}')
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

    def getPyutObject(self):
        """
        Returns the associated PyutLink.

        Returns: PyutLink

        """
        return self._link

    def setPyutObject(self, pyutLink):
        """
        Sets the associated PyutLink.

        @param PyutLink pyutLink : link to associate
        """
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

        self.clsLogger.info(f"optimizeLine - ({srcX},{srcY}) / ({dstX},{dstY})")
        # Find new positions
        # Little tips
        optimalSrcX, optimalSrcY, optimalDstX, optimalDstY = dstX, dstY, srcX, srcY

        optimalSrcX += dstSize[0]/2
        optimalSrcY += dstSize[1]/2
        optimalDstX += srcSize[0]/2
        optimalDstY += srcSize[1]/2

        srcAnchor.SetPosition(optimalSrcX, optimalSrcY)
        dstAnchor.SetPosition(optimalDstX, optimalDstY)

    def _computeLinkLength(self, srcPosition: Tuple[float, float], destPosition: Tuple[float, float]) -> float:
        """

        Returns:  The length of the link between the source shape and destination shape
        """
        dx, dy = self._computeDxDy(srcPosition, destPosition)
        linkLength = sqrt(dx*dx + dy*dy)
        if linkLength == 0:
            linkLength = 0.01

        return linkLength

    def _computeDxDy(self, srcPosition: Tuple[float, float], destPosition: Tuple[float, float]) -> Tuple[float, float]:
        """

        Args:
            srcPosition:    Tuple x,y source position
            destPosition:   Tuple x,y destination position

        Returns:
            A tuple of deltaX and deltaY of the shape position
        """
        if self._srcShape is None or self._destShape is None:
            raise IllegalOperationException('Either the source or the destination shape is None')

        srcX, srcY = srcPosition
        dstX, dstY = destPosition

        dx = dstX - srcX
        dy = dstY - srcY

        return dx, dy


from pyutmodel.PyutLinkType import PyutLinkType


class ALayoutLink:
    """
    ALayoutLink : Interface between pyut/ogl link and ALayout algorithms.

    ALayout algorithms can use this interface to access the links of the
    diagram. The first reason is that the interface protects the structure
    of the diagram. The second is that pyut structure and methods could
    be changed. In a such case, the only files to update is the interface, not
    your automatic layout algorithm.

    """
    def __init__(self, oglLink):
        """
        Constructor.

        @author Nicolas Dubois
        """
        self._oglLink = oglLink
        self.__srcNode = None
        self.__dstNode = None

    def setSource(self, node):
        """
        Set the source node.

        @param InterfaceSugiyamaNode node: source node of the link
        @author Nicolas Dubois
        """
        self.__srcNode = node

    def getSource(self):
        """
        Return the source node.

        @return InterfaceSugiyamaNode: source node of the link
        @author Nicolas Dubois
        """
        return self.__srcNode

    def setDestination(self, node):
        """
        Set the destination node.

        @param InterfaceSugiyamaNode node: destination node of the link
        @author Nicolas Dubois
        """
        self.__dstNode = node

    def getDestination(self):
        """
        Return the destination node.

        @return InterfaceSugiyamaNode: destination node of the link
        @author Nicolas Dubois
        """
        return self.__dstNode

    def setSrcAnchorPos(self, x: int, y: int):
        """
        Set anchor position (absolute coordinates) on source class.

        Args:
            x:
            y:
        """
        self._oglLink.GetSource().SetPosition(x, y)

    def getSrcAnchorPos(self):
        """
        Get anchor position (absolute coordinates) on source class.

        Returns:    (int, int) : tuple with (x, y) coordinates
        """

        return self._oglLink.GetSource().GetPosition()

    def setDestAnchorPos(self, x: int, y: int):
        """
        Set anchor position (absolute coordinates) on destination class.

        Args:
            x:
            y:
        """
        self._oglLink.GetDestination().SetPosition(x, y)

    def getDestAnchorPos(self):
        """
        Return anchor position (absolute coordinates) on destination class.

        @return (float, float) : tuple with (x, y) coordinates
        @author Nicolas Dubois
        """
        return self._oglLink.GetDestination().GetPosition()

    def addControlPoint(self, control, last=None):
        """
        Add a control point. If param last given, add point right after last.

        @param ControlPoint control : control point to add
        @param ControlPoint last    : add control right after last
        @author Nicolas Dubois
        """
        self._oglLink.AddControl(control, last)

    def removeControlPoint(self, controlPoint):
        """
        Remove a control point.

        @param ControlPoint controlPoint: control point to remove
        @author Nicolas Dubois
        """
        self._oglLink.Remove(controlPoint)

    def removeAllControlPoints(self):
        """
        Remove all control points.

        @author Nicolas Dubois
        """
        self._oglLink.RemoveAllControlPoints()

    def getType(self) -> PyutLinkType:
        """
        Return the link type

        Returns: Link type
        """
        return self._oglLink.pyutObject.linkType

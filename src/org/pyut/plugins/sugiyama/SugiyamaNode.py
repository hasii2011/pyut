
from typing import cast
from typing import NewType
from typing import Tuple
from typing import List

from org.pyut.plugins.sugiyama.SugiyamaConstants import H_SPACE

from org.pyut.plugins.sugiyama.SugiyamaLink import SugiyamaLink

SugiyamaVertexEdge = NewType("SugiyamaVertexEdge", Tuple["SugiyamaNode", SugiyamaLink])
SugiyamaVEs        = NewType("SugiyamaVEs", List[SugiyamaVertexEdge])


class SugiyamaNode:
    """
    Real or virtual Sugiyama node interface.

    This class is an interface, you should not have an object of type
    SugiyamaNode. You have to use RealSugiyamaNode or VirtualSugiyamaNode
    objects.
    """
    def __init__(self):
        """
        """
        # Current barycenter value of the link, this value can be computed
        # on indexes or x coordinate. For more information, see function
        # getBarycenter()
        self.__barycenter: float = cast(float, None)
        self.__index = None
        """
        Index position on the level
        """
        self.__level = None
        """
        Index of level
        """
        self.__leftNode = None
        """
        Node direct on the left on the same level
        """
        self.__rightNode = None
        """
        Node direct on the right on the same level
        """
        # parents and sons
        # ================
        #
        # A child is derived from a parent. There is a hierarchical link,
        # Realization or Inheritance, from source to parent.
        # Each node can have parents and children.
        self.__parents: SugiyamaVEs = SugiyamaVEs([])
        """
        List of parents
        """
        self.__children: SugiyamaVEs = SugiyamaVEs([])
        """
        List of children : [(SugiyamaNode, SugiyamaLink), ...]
        """
        self.__links:    SugiyamaVEs = SugiyamaVEs([])
        """
        List of non-hierarchical links : [(SugiyamaNode, SugiyamaLink), ...]
        """

    def getSize(self) -> Tuple[int, int]:
        """
        Get the size of the node.

        This function should be overridden.

        Returns:    (float, float): tuple (width, height)
        """
        pass

    def setPosition(self, x, y):
        """
        Set position of node.

        This function has to be implemented.

        Args:
            x: x position in absolute coordinates
            y: y position in absolute coordinates
        """
        pass

    def getPosition(self) -> Tuple[float, float]:
        """
        Get position of node.

        This function has to be implemented.  Should be a 'pass'  But Pycharm complains
        at method self.__pushToRight()

        Returns:    (float, float): tuple (x, y) is absolute coordinates

        """
        return 0.0, 0.0

    def addParent(self, parent: "SugiyamaNode", link: SugiyamaLink):
        """
        Update parent list

        Args:
            parent:  The parent
            link:   Link between self and parent
        """
        sugiyamaData: SugiyamaVertexEdge = cast(SugiyamaVertexEdge, (parent, link))
        self.__parents.append(sugiyamaData)

    def getParents(self) -> SugiyamaVEs:
        """
        Return list of parents

        Returns:  list of parents

        """
        return self.__parents

    def addChild(self, child, link):
        """
        Add a child.

        Args:
            child:  The child
            link:   Its Link
        """
        sugiyamaData: SugiyamaVertexEdge = cast(SugiyamaVertexEdge, (child, link))
        self.__children.append(sugiyamaData)

    def getChildren(self) -> SugiyamaVEs:
        """
        Get list of children.

        Returns:  The list of children
        """
        return self.__children

    def addNonHierarchicalLink(self, node: "SugiyamaNode", link: SugiyamaLink):
        """
        Add a non-hierarchical link, ie not a parent or child relation.

        Args:
            node:   linked node
            link:   link between the two nodes
        """
        vertexEdge: SugiyamaVertexEdge = SugiyamaVertexEdge((node, link))
        self.__links.append(vertexEdge)

    def getNonHierarchicalLink(self) -> SugiyamaVEs:
        """
        Get non-hierarchical links, ie not parent or child relationship

        Returns: [(SugiyamaNode, SugiyamaLink), ...] : list of tuple

        """
        return self.__links

    def setLevel(self, level: int):
        """
        Set level index.

        Args:
            level:   level index
        """
        self.__level = level

    def getLevel(self) -> int:
        """
        Get level index.

        Returns:    level index
        """
        return self.__level

    def setIndex(self, index: int):
        """
        Set index of node in level.

        Args:
            index: index of node
        """
        self.__index = index

    def getIndex(self) -> int:
        """
        Get index of node.

        Returns:    index of node
        """
        return self.__index

    def setLeftNode(self, node: "SugiyamaNode"):
        """
        Set the left neighbor node.

        Args:
            node:   left neighbor
        """
        self.__leftNode = node

    def getLeftNode(self) -> "SugiyamaNode":
        """
        Get the left neighbor node.

        Returns:    left neighbor
        """
        return self.__leftNode

    def setRightNode(self, node: "SugiyamaNode"):
        """
        Set the right neighbor node.

        This method must be used before balancing the graph.

        Args:
            node: right neighbor
        """
        self.__rightNode = node

    def getRightNode(self) -> "SugiyamaNode":
        """
        Get the right neighbor node.

        Returns:    right neighbor
        """
        return self.__rightNode

    def getXMax(self) -> float:
        """
        Get bigger value of x coordinate according to right neighbor position.

        If there is no right neighbor, return None.

        Returns:    max x coordinate
        """
        if self.__rightNode is None:
            return cast(float, None)
        else:
            xRightNode = self.__rightNode.getPosition()[0]
            widthSelfNode = self.getSize()[0]
            return xRightNode - widthSelfNode - H_SPACE

    def __getAverageIndex(self, nodeList) -> float:
        """
        Compute the average of indices position on all the given nodes.

        Args:
            nodeList:    [SugiyamaNode, ...] : list of nodes

        Returns:  None if nodeList is empty.  float or None : Average of indexes position
        """
        if len(nodeList) == 0:
            return cast(float, None)
        else:
            summation = 0.0
            for (node, link) in nodeList:
                summation += node.getIndex()
            return float(summation) / len(nodeList)

    def fixAnchorPos(self):
        """
        Fix the positions of the anchor points.

        This function has to be overloaded.

        """
        pass

    def upBarycenterIndex(self):
        """
        Compute the up barycenter value with fathers indexes.

        For reading this value, use getBarycenter()

        """
        self.__barycenter = self.__getAverageIndex(self.__parents)

    def downBarycenterIndex(self):
        """
        Compute the down barycenter value with sons indexes.

        For reading this value, use getBarycenter()

        """
        self.__barycenter = self.__getAverageIndex(self.__children)

    def barycenterIndex(self):
        """
        Compute the average of parents down-barycenter and sons up-barycenter.

        Before calling this function, you have to call downBarycenterIndex
        on each parent and upBarycenterIndex on each child.

        For reading this value, use getBarycenter()

        @author Nicolas Dubois
        """
        nodeList = self.__parents + self.__children
        if len(nodeList) == 0:
            # ~ print self.__index, "none"
            self.__barycenter = None
        else:
            summation = 0
            for (node, link) in nodeList:
                summation += node.getBarycenter()
            # ~ print self.__index, float(sum) / len(nodeList)
            self.__barycenter = float(summation) / len(nodeList)

    def __getAverageX(self, nodeList: SugiyamaVEs) -> float:
        """
        Compute the average of x coordinates on all the given nodes.

        Args:
            nodeList:   [(SugiyamaNode, SugiyamaLink), ...] nodeList : parents or children

        Returns:    float or None : average of x coordinates
                    None if nodeList is empty.
        """
        if len(nodeList) == 0:
            return cast(float, None)
        else:
            summation: float = 0
            for (node, link) in nodeList:
                summation += node.getPosition()[0] + node.getSize()[0] / 2
            return summation / len(nodeList) - self.getSize()[0] / 2

    def upBarycenterX(self):
        """
        Compute the up barycenter value with fathers x coord.

        For reading this value, use getBarycenter()
        """
        self.__barycenter = self.__getAverageX(self.__parents)

    def downBarycenterX(self):
        """
        Compute the down barycenter value with sons x coord.

        For reading this value, use getBarycenter()
        """
        self.__barycenter = self.__getAverageX(self.__children)

    def barycenterX(self):
        """
        Compute the average of up and down barycenter on x coordinates.

        For reading this value, use getBarycenter()
        """
        parentsAndChildren: SugiyamaVEs = cast(SugiyamaVEs, self.__parents + self.__children)
        self.__barycenter = self.__getAverageX(parentsAndChildren)

    def getBarycenter(self) -> float:
        """
        Return the pre-computed barycenter value of the node.

        The barycenter value is computed when you call one of the following
        function:
            - upBarycenterIndex()
            - downBarycenterIndex()
            - upBarycenterX()
            - downBarycenterX()
        If you want to update the value, you have to recall one of the
        computing functions.

        Example:
            If you want the down barycenter computed on indexes:
            First call function downBarycenterIndex()
            and then call function getBarycenter()

        Returns:   float: barycenter value

        """
        return self.__barycenter

    def __computeWantedXPos(self):
        """
        Compute average of parents and children x coordinates.

        Returns:    tuple (float, int) : (x average, number of fathers and sons)
        """
        # Create list of parents and children
        parentsAndChildren = self.getParents() + self.getChildren()
        nbParentsAndChildren = len(parentsAndChildren)

        # If there are no parents and children
        if nbParentsAndChildren == 0:
            return None, 0

        # Compute average of parents and children x coordinates
        summation = 0
        # For all his parents and children
        for (node, link) in parentsAndChildren:
            # Get horizontal center coordinate of the node
            xCenterNode = node.getPosition()[0] + node.getSize()[0] / 2
            summation += xCenterNode

        return summation / nbParentsAndChildren - self.getSize()[0] / 2, nbParentsAndChildren

    def balance(self):
        """
        Compute a new x coordinate for balancing the hierarchical graph.

        Evaluate the best x coordinate for the node. If the best coord is on
        the right of the node, try to push the nodes on the right and then fix
        new position closer to best x coordinate.

        """
        # Get coordinate of node
        (x, y) = self.getPosition()

        # Evaluate best x coordinate of node
        (wantedXPos, nbFathersAndSons) = self.__computeWantedXPos()

        # If there are no parents nor sons
        if not wantedXPos:
            # Don't move
            return 0

        # If best x coord is righter than current x coordinate
        if wantedXPos > x:

            # If there is a right neighbor
            if self.__rightNode is not None:
                # Check max x coord according to right neighbor
                xMax = self.getXMax()

                # If right node is to close, try to push it
                if wantedXPos > xMax:
                    self.__rightNode.__pushToRight(
                        (wantedXPos - xMax) * nbFathersAndSons,
                        nbFathersAndSons)

                # Fix new position
                self.setPosition(min(wantedXPos, self.getXMax()), y)
            else:
                # There is no right node, fix position
                self.setPosition(wantedXPos, y)

        # Return true if node has been moved
        return self.getPosition()[0] - x > 3

    def __pushToRight(self, xDeltaSum: float, nbLinks: int):
        """
        Called by the left neighbor, that function tries to push the node to
        the right for the balancing. If there is not enough space, try to
        push the next node.

        xDelta is the ideal delta on x coordinate for reaching the best balance.

        xDeltaSum

        Args:
            xDeltaSum:  is xDelta multiplied by the number of parents and sons
                which are pushing to the right.

            nbLinks:   is the number of parents and sons who push from the left.
        """
        # Get current position
        (x, y) = self.getPosition()
        # Get wanted x coordinate
        (wantedXPos, nbFathersAndSons) = self.__computeWantedXPos()

        # If the node has a barycenter value (has parents or sons)
        if wantedXPos is not None:
            # Add current delta in average
            xDeltaSum += (wantedXPos - x) * nbFathersAndSons
            # Update number of fathers and sons who are pushing
            nbLinks += nbFathersAndSons
        xDelta = xDeltaSum // nbLinks

        # If the node has to be moved to the right
        if xDelta > 0:
            # If the node has a right neighbor
            if self.__rightNode is not None:
                xMax = self.getXMax()
                # If we need more place, try to push the right neighbor
                if xMax < x + xDelta:
                    self.__rightNode.__pushToRight(
                        (x + xDelta - xMax) * nbLinks, nbLinks)
                # Fix the new position
                self.setPosition(min(x + xDelta, self.getXMax()), y)
            else:
                # No right neighbor, fix the new position
                self.setPosition(x + xDelta, y)

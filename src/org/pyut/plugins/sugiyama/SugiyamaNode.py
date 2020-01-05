
from typing import cast
from typing import NewType
from typing import Tuple
from typing import List

from org.pyut.plugins.sugiyama.SugiyamaConstants import H_SPACE

from org.pyut.plugins.sugiyama.SugiyamaLink import SugiyamaLink

SugiyamaVertixEdge = NewType("SugiyamaVertixEdge", Tuple["SugiymaNode", SugiyamaLink])
SugiyamaVEs        = NewType("SugiyamaVEs",         List[SugiyamaVertixEdge])


class SugiyamaNode:
    """
    Real or virtual Sugiyama node interface.

    This class is an interface, you shouldn't have an object of type
    SugiyamaNode. You have to use RealSugiyamaNode or VirtualSugiyamaNode
    objects.
    """
    def __init__(self):
        """
        Constructor.

        @author Nicolas Dubois
        """
        # Current barycenter value of the link, this value can be computed
        # on indexes or x coordinate. For more information, see function
        # getBarycenter()
        self.__barycenter = None
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
        self.__parents: SugiyamaVEs = cast(SugiyamaVEs, [])
        """
        List of parents
        """
        self.__sons: SugiyamaVEs = cast(SugiyamaVEs, [])
        """
        List of sons : [(SugiyamaNode, SugiyamaLink), ...]
        """
        self.__links = []
        """
        List of non-hierarchical link : [(SugiyamaNode, SugiyamaLink), ...]
        """

    def getSize(self):
        """
        Get the size of the node.

        This function has to be overloaded.

        @return (float, float): tuple (width, height)
        @author Nicolas Dubois
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

    def getPosition(self):
        """
        Get position of node.

        This function has to be implemented.  Should be a 'pass'  But Pycharm complains
        at method self.__pushToRight()

        @return (float, float): tuple (x, y) is absolute coordinates
        """
        return 0.0, 0.0

    def addParent(self, parent: "SugiyamaNode", link: SugiyamaLink):
        """
        Update parent list

        Args:
            parent:  The parent
            link:   Link betweeen self and parent
        """
        sugiyamaData: SugiyamaVertixEdge = cast(SugiyamaVertixEdge, (parent, link))
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
        sugiyamaData: SugiyamaVertixEdge = cast(SugiyamaVertixEdge, (child, link))
        self.__sons.append(sugiyamaData)

    def getChildren(self) -> SugiyamaVEs:
        """
        Get list of children.

        Returns:  The list of children
        """
        return self.__sons

    def addNonHierarchicalLink(self, node, link):
        """
        Add a non hierarchical link, ie not a father nor a son relation.

        @param SugiyamaNode node : linked node
        @param SugiyamaLink link : link between the two nodes
        @author Nicolas Dubois
        """
        self.__links.append((node, link))

    def getNonHierarchicalLink(self):
        """
        Get non hierarchical links, ie not father nor son relations.

        @return [(SugiyamaNode, SugiyamaLink), ...] : list of tuple
        @author Nicolas Dubois
        """
        return self.__links

    def setLevel(self, level):
        """
        Set level index.

        @param int level : level index
        @author Nicolas Dubois
        """
        self.__level = level

    def getLevel(self):
        """
        Get level index.

        @return Int : level index
        @author Nicolas Dubois
        """
        return self.__level

    def setIndex(self, index):
        """
        Set index of node in level.

        @param int index : index of node
        @author Nicolas Dubois
        """
        self.__index = index

    def getIndex(self):
        """
        Get index of node.

        @return int : index of node
        @author Nicolas Dubois
        """
        return self.__index

    def setLeftNode(self, node):
        """
        Set the left neighbor node.

        @param SugiyamaNode node : left neighbor
        @author Nicolas Dubois
        """
        self.__leftNode = node

    def getLeftNode(self):
        """
        Get the left neighbor node.

        @return SugiyamaNode : left neighbor
        @author Nicolas Dubois
        """
        return self.__leftNode

    def setRightNode(self, node):
        """
        Set the right neighbor node.

        That function must be used before balancing the graph.

        @param SugiyamaNode node : right neighbor
        @author Nicolas Dubois
        """
        self.__rightNode = node

    def getRightNode(self):
        """
        Get the right neighbor node.

        @return SugiyamaNode : right neighbor
        @author Nicolas Dubois
        """
        return self.__rightNode

    def getXMax(self):
        """
        Get bigger value of x coordinate according to right neighbor position.

        If there is no right neighbor, return None.

        @return float : max x coordinate
        @author Nicolas Dubois
        """
        if self.__rightNode is None:
            return None
        else:
            xRightNode = self.__rightNode.getPosition()[0]
            widthSelfNode = self.getSize()[0]
            return xRightNode - widthSelfNode - H_SPACE

    def __getAverageIndex(self, nodeList):
        """
        Compute the average of indexes position on all the given nodes.

        Return None if nodeList is empty.

        @param [SugiyamaNode, ...] : list of nodes
        @return float or None : Average of indexes position
        @author Nicolas Dubois
        """
        if len(nodeList) == 0:
            return None
        else:
            summation = 0
            for (node, link) in nodeList:
                summation += node.getIndex()
            return float(summation) / len(nodeList)

    def fixAnchorPos(self):
        """
        Fix the positions of the anchor points.

        This function has to be overloaded.

        @author Nicolas Dubois
        """
        pass

    def upBarycenterIndex(self):
        """
        Compute the up barycenter value with fathers indexes.

        For reading this value, use getBarycenter()

        @author Nicolas Dubois
        """
        self.__barycenter = self.__getAverageIndex(self.__parents)

    def downBarycenterIndex(self):
        """
        Compute the down barycenter value with sons indexes.

        For reading this value, use getBarycenter()

        @author Nicolas Dubois
        """
        self.__barycenter = self.__getAverageIndex(self.__sons)

    def barycenterIndex(self):
        """
        Compute the average of parents down-barycenter and sons up-barycenter.

        Before calling this function, you have to call downBarycenterIndex
        on each fathers and upBarycenterIndex on each sons.

        For reading this value, use getBarycenter()

        @author Nicolas Dubois
        """
        nodeList = self.__parents + self.__sons
        if len(nodeList) == 0:
            # ~ print self.__index, "none"
            self.__barycenter = None
        else:
            summmation = 0
            for (node, link) in nodeList:
                summmation += node.getBarycenter()
            # ~ print self.__index, float(sum) / len(nodeList)
            self.__barycenter = float(summmation) / len(nodeList)

    def __getAverageX(self, nodeList):
        """
        Compute the average of x coords on all the given nodes.

        Return None if nodeList is empty.

        @param [(SugiyamaNode, SugiyamaLink), ...] nodeList : fathers or sons
        @return float or None : average of x coords
        @author Nicolas Dubois
        """
        if len(nodeList) == 0:
            return None
        else:
            summmation = 0
            for (node, link) in nodeList:
                summmation += node.getPosition()[0] + node.getSize()[0] / 2
            return summmation / len(nodeList) - self.getSize()[0] / 2

    def upBarycenterX(self):
        """
        Compute the up barycenter value with fathers x coord.

        For reading this value, use getBarycenter()

        @author Nicolas Dubois
        """
        self.__barycenter = self.__getAverageX(self.__parents)

    def downBarycenterX(self):
        """
        Compute the down barycenter value with sons x coord.

        For reading this value, use getBarycenter()

        @author Nicolas Dubois
        """
        self.__barycenter = self.__getAverageX(self.__sons)

    def barycenterX(self):
        """
        Compute the average of up and down barycenter on x coords.

        For reading this value, use getBarycenter()

        @author Nicolas Dubois
        """
        self.__barycenter = self.__getAverageX(self.__parents + self.__sons)

    def getBarycenter(self):
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

        @return float: barycenter value
        @author Nicolas Dubois
        """
        return self.__barycenter

    def __computeWantedXPos(self):
        """
        Compute average of fathers and sons x coordinates.

        @return tuple (float, int) : (x average, number of fathers and sons)
        @author Nicolas Dubois
        """
        # Create list of fathers and sons
        fathersAndSons = self.getParents() + self.getChildren()
        nbFathersAndSons = len(fathersAndSons)

        # If there are no fathers and sons
        if nbFathersAndSons == 0:
            return None, 0

        # Compute average of fathers and sons x coordinates
        summation = 0
        # For all his fahters and sons
        for (node, link) in fathersAndSons:
            # Get horizontal center coordinate of the node
            xCenterNode = node.getPosition()[0] + node.getSize()[0] / 2
            summation += xCenterNode

        return summation / nbFathersAndSons - self.getSize()[0] / 2, nbFathersAndSons

    def balance(self):
        """
        Compute a new x coordinate for balancing the hierarchical graph.

        Evaluate the best x coordinate for the node. If the best coord is on
        the right of the node, try to push the nodes on the right and then fix
        new position closer to best x coordinate.

        @author Nicolas Dubois
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

    def __pushToRight(self, xDeltaSum, nbLinks):
        """
        Called by the left neighbor, that function tries to push the node to
        the right for the balancing. If there is not enough space, try to
        push the next node.

        xDelta is the ideal delta on x coordinate for reaching the best balance.

        xDeltaSum is xDelta multiplied by the number of parents and sons
        which are pushing to the right.

        nbLinks is the number of parents and sons who push from the left.

        @param float xDeltaSum : see above
        @param int nbLinks : see above
        @author Nicolas Dubois
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
        xDelta = xDeltaSum / nbLinks

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

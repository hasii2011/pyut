
from org.pyut.plugins.sugiyama.ALayoutLink import ALayoutLink

# Miniogl import
from org.pyut.miniogl.ControlPoint import ControlPoint


class SugiyamaLink(ALayoutLink):
    """
    SugiyamaLink: link of the Sugiyama graph.

    Instantiated by: ../ToSugiyama.py

    :author: Nicolas Dubois
    :contact: nicdub@gmx.ch
    :version: $Revision: 1.4 $
    """
    def __init__(self, oglObject):
        """
        Constructor.

        @author Nicolas Dubois
        """
        # Call father's initialization
        ALayoutLink.__init__(self, oglObject)
        self.__virtualNodes = []

    def fixControlPoints(self):
        """
        Fix a graphical path with control points.

        @author Nicolas Dubois
        """
        # Clear the actual control points of the link (not the anchor points)
        self.removeAllControlPoints()

        # Current x coordinate of the link
        x = self.getSrcAnchorPos()[0]

        # For all virtual nodes, add control points to pass through
        for vnode in self.__virtualNodes:
            #  ~ print "Virtual node"
            (xvnode, yvnode) = vnode.getPosition()
            # If link goes to up-left
            if x > xvnode:
                # Find the first real node on the right of the virtual node
                neighbor = vnode.getRightNode()
                #
                # Don't like embedded imports, but need to avoid cyclical dependency
                from org.pyut.plugins.sugiyama.VirtualSugiyamaNode import VirtualSugiyamaNode

                while isinstance(neighbor, VirtualSugiyamaNode) and neighbor is not None:

                    # Try next neighbor
                    neighbor = neighbor.getRightNode()

                # If real node found
                if neighbor is not None:
                    ctrlPoint = ControlPoint(xvnode, neighbor.getPosition()[1] + neighbor.getSize()[1])
                    self.addControlPoint(ctrlPoint)

            else:   # If link goes to up-right
                # Don't like embedded imports, but need to avoid cyclical dependency
                from org.pyut.plugins.sugiyama.VirtualSugiyamaNode import VirtualSugiyamaNode
                # Find the first real node on the left of the virtual node
                neighbor = vnode.getLeftNode()
                while isinstance(neighbor, VirtualSugiyamaNode) and neighbor is not None:

                    # Try next neighbor
                    neighbor = neighbor.getLeftNode()

                # If real node found
                if neighbor is not None:
                    ctrlPoint = ControlPoint(xvnode, neighbor.getPosition()[1] + neighbor.getSize()[1])
                    self.addControlPoint(ctrlPoint)

            ctrlPoint = ControlPoint(xvnode, yvnode)
            self.addControlPoint(ctrlPoint)

    def addVirtualNode(self, node):
        """
        Add a virtual node.

        A virtual node is inserted in long links which cross a level. If the
        link crosses more than one level, insert virtual nodes, ordered
        from source to destination (son to father - bottom-up).

        @param VirtualSugiyamaNode node : virtual node
        @author Nicolas Dubois
        """
        self.__virtualNodes.append(node)

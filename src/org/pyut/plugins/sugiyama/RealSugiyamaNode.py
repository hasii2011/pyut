
from org.pyut.plugins.sugiyama.SugiyamaNode import SugiyamaNode
from org.pyut.plugins.sugiyama.SugiyamaNode import SugiyamaVEs

from org.pyut.plugins.sugiyama.ALayoutNode import ALayoutNode

from org.pyut.plugins.sugiyama.SugiyamGlobals import SugiyamGlobals


class RealSugiyamaNode(SugiyamaNode):
    """
    RealSugiyamaNode: A RealSugiyamaNode object is a node of the Sugiyama
    graph associated to an OglObject of the UML diagram, which can be a
    class or a note.

    For more information, see ../ToSugiyama.py

    Instantiated by: ../ToSugiyama.py

    :author: Nicolas Dubois
    :contact: nicdub@gmx.ch
    :version: $Revision: 1.4 $
    """
    def __init__(self, oglObject):
        """
        Constructor.

        @param OglObject oglObject: class or note of the diagram
        @author Nicolas Dubois
        """
        # Call mother class initialization
        SugiyamaNode.__init__(self)

        # Self fields
        self.__aLayoutNode = ALayoutNode(oglObject)

    def getSize(self):
        """
        Get the size of the node.

        @return (float, float) : tuple (width, height)
        @author Nicolas Dubois
        """
        return self.__aLayoutNode.getSize()

    def setPosition(self, xCoord, yCoord):
        """
        Set node position.

        Args:
            xCoord:  x position in absolute coordinates
            yCoord:  y position in absolute coordinates
        """
        self.__aLayoutNode.setPosition(xCoord, yCoord)

    def getPosition(self):
        """
        Get node position.

        @return (float, float) : tuple (x, y) in absolute coordinates
        @author Nicolas Dubois
        """
        return self.__aLayoutNode.getPosition()

    def getName(self):
        """
        Get the name of the OglObject.

        @return str : name of OglObject
        @author Nicolas Dubois
        """
        return self.__aLayoutNode.getName()

    def fixAnchorPos(self):
        """
        Fix the positions of the anchor points.

        The anchor points are placed according to parent and child positions.
        Before calling this method, be sure you have set the indices of all
        parent and children (see setIndex).

        """
        # Get position and size of node
        (width, height) = self.getSize()
        (x, y) = self.getPosition()

        # Fix all childrent anchors position
        # Sort child list to eliminate crossing
        children: SugiyamaVEs = self.getChildren()
        children.sort(key=SugiyamGlobals.cmpIndex)
        nChildren = len(children)
        # For all children
        for i in range(nChildren):
            (child, link) = children[i]
            # Fix anchors coordinates
            link.setDestAnchorPos(
                x + width * (i + 1) / (nChildren + 1), y + height)

        # Parent anchors position
        # Sort parents list to eliminate crossing
        parents: SugiyamaVEs = self.getParents()
        parents.sort(key=SugiyamGlobals.cmpIndex)
        nParents = len(parents)
        # For all parents
        for i in range(nParents):
            (parent, link) = parents[i]
            # Fix anchors coordinates
            link.setSrcAnchorPos(
                x + width * (i + 1) / (nParents + 1), y)


from org.pyut.plugins.sugiyama.SugiyamaNode import SugiyamaNode
from org.pyut.plugins.sugiyama import ALayoutNode

from org.pyut.plugins.sugiyama import SugiyamGlobals


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

        The anchor points a placed according to fathers and sons positions.
        Before calling this function, be sure you have set the index of all
        fathers and sons (see setIndex).

        @author Nicolas Dubois
        """
        # Get position and size of node
        (width, height) = self.getSize()
        (x, y) = self.getPosition()

        # Fix all sons anchors position
        # Sort sons list to eliminate crossing
        sons = self.getSons()
        sons.sort(key=SugiyamGlobals.cmpIndex)
        nbSons = len(sons)
        # For all sons
        for i in range(nbSons):
            (son, link) = sons[i]
            # Fix anchors coordinates
            link.setDestAnchorPos(
                x + width * (i + 1) / (nbSons + 1), y + height)
        # Fathers anchors position
        # Sort fathers list to eliminate crossing
        fathers = self.getFathers()
        fathers.sort(key=SugiyamGlobals.cmpIndex)
        nbFathers = len(fathers)
        # For all fathers
        for i in range(nbFathers):
            (father, link) = fathers[i]
            # Fix anchors coordinates
            link.setSrcAnchorPos(
                x + width * (i + 1) / (nbFathers + 1), y)

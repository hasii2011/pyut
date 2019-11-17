

from plugins.PyutToPlugin import PyutToPlugin

from plugins.sugiyama.RealSugiyamaNode import *
from plugins.sugiyama.SugiyamaLink import *
from plugins.sugiyama.sugiyamaConsts import *

from org.pyut.ogl.OglInheritance import *
from org.pyut.ogl.OglInterface import *
from org.pyut.ogl.OglObject import OglObject

from org.pyut.PyutConsts import *

from Globals import cmp

STEPBYSTEP = 0  # Do Sugiyama Step by step


def waitKey(umlFrame):
    umlFrame.Refresh()
    wx.Yield()
    input("Appuyez sur Enter pour continuer")   # Press enter to continue?


def cmpBarycenter(xNode, yNode) -> bool:
    """
    Comparison function on barycenter value
    Args:
        xNode:
        yNode:

    Returns:

    """
    return cmp(xNode.getBarycenter(), yNode.getBarycenter())


def cmpIndex(xNode, yNode) -> bool:
    """
        Comparison function on index value
    Args:
        xNode:
        yNode:

    Returns:

    """
    return cmp(xNode.getIndex(), yNode.getIndex())


class ToSugiyama(PyutToPlugin):
    """
    ToSugiyama : Automatic layout algorithm based on Sugiyama levels.

    This algorithm will change the class and links positions (not the
    structure). This plugin give good result with diagram which contains
    a lot of hierachical relation (inheritance and interface), and poor
    association relation.

    Instantiated by ../PluginManager.py

    :author: Nicolas Dubois
    :contact: nicdub@gmx.ch
    :version: $Revision: 1.8 $
    """
    def __init__(self, umlObjects, umlFrame):
        """
        Constructor.

        @param umlObjects : list of uml objects
        @param umlFrame : the umlframe of pyut
        @author Nicolas Dubois
        """
        # Call father initialisation
        super().__init__(umlObjects, umlFrame)

        # Sugiyama nodes and links
        self.__realSugiyamaNodesList = []   # List of all RealSugiyamaNode
        self.__sugiyamaLinksList = []       # List of all SugiyamaLink

        #  Hierarchy graph
        #  List of Real and Virtual Sugiyama nodes that take part in hierarchy
        self.__hierarchyGraphNodesList = []
        #  List of Sugiyama nodes that aren't in hierarchy
        self.__nonHierarchyGraphNodesList = []
        self.__nonHierarchyGraphLinksList = []

        #  All nodes of the hierarchy are assigned to a level.
        #  A level is a list of nodes (real or virtual).
        self.__levels = []  # List of levels

    def getName(self):
        """
        This method returns the name of the plugin.

        @return string
        @author Nicolas Dubois
        """
        return "Sugiyama automatic layout"

    def getAuthor(self):
        """
        This method returns the author of the plugin.

        @return string
        @author Nicolas Dubois
        """
        return "Nicolas Dubois <nicdub@gmx.ch>"

    def getVersion(self):
        """
        This method returns the version of the plugin.

        @return string
        @author Nicolas Dubois
        """
        return "1.0"

    def getMenuTitle(self):
        """
        Return a menu title string

        @return string
        @author Nicolas Dubois
        """
        # Return the menu title as it must be displayed
        return "Sugiyama ALayout"

    def __createInterfaceOglALayout(self, oglObjects):
        """
        Create the interface between oglObjects and Automatic Layout
        structure. A RealSugiyamaNode is created for each class, and a
        SugiyamaLink is created for each relation in the UML diagram.

        @param oglObjects : list of ogl objects of the diagram
        @author Nicolas Dubois
        """
        # Dictionary for oglObjects fast research
        # Key = OglObject, Value = RealSugiyamaNode
        dictOgl     = {}
        # Dictionary for RealSugiyamaNode that take part in hierarchy
        # Key = OglObject, Value = None
        dictSugiHier = {}

        # Internal function for creating a RealSugiyamaNode and add it to
        # self.__realSugiyamaNodesList and to dictOgl
        def createSugiyamaNode(theOglObject, theDictOgl):
            # Create RealSugiyamaNode only if not already done
            if theOglObject not in theDictOgl:
                node = RealSugiyamaNode(theOglObject)
                self.__realSugiyamaNodesList.append(node)
                theDictOgl[theOglObject] = node

        # Internal function for adding nodes that take part in hierarchy into
        # the __hierarchyGraphNodesList.

        def addNode2HierarchyGraph(theSugiNode, theDictSugiHier):
            if theSugiNode not in theDictSugiHier:
                theDictSugiHier[theSugiNode] = None
                self.__hierarchyGraphNodesList.append(theSugiNode)

        # For each OglObject or OglLink, create a specific interface
        for oglObject in oglObjects:

            # Class or Note :
            if isinstance(oglObject, OglObject):
                createSugiyamaNode(oglObject, dictOgl)

            # Links
            elif isinstance(oglObject, OglLink):

                # Get source and destination oglObject
                srcOglClass = oglObject.getSourceShape()
                dstOglClass = oglObject.getDestinationShape()

                # If the classes have not a RealSugiyamaNode attributed yet
                createSugiyamaNode(srcOglClass, dictOgl)
                createSugiyamaNode(dstOglClass, dictOgl)

                # Fix relations between nodes
                link = SugiyamaLink(oglObject)
                self.__sugiyamaLinksList.append(link)
                srcSugiyamaNode = dictOgl[srcOglClass]
                dstSugiyamaNode = dictOgl[dstOglClass]
                link.setSource(srcSugiyamaNode)
                link.setDestination(dstSugiyamaNode)

                # If hierarchical link
                if isinstance(oglObject, OglInheritance) or isinstance(oglObject, OglInterface):

                    srcSugiyamaNode.addFather(dstSugiyamaNode, link)
                    dstSugiyamaNode.addSon(srcSugiyamaNode, link)

                    # Add nodes in list of hierachical nodes
                    addNode2HierarchyGraph(srcSugiyamaNode, dictSugiHier)
                    addNode2HierarchyGraph(dstSugiyamaNode, dictSugiHier)

                # Non hierarchical links
                else:

                    # Add link between source and destination interface
                    srcSugiyamaNode.addNonHierarchicalLink(
                        dstSugiyamaNode, link)
                    dstSugiyamaNode.addNonHierarchicalLink(
                        srcSugiyamaNode, link)

                    # Add link into non-hierarchical links' list
                    self.__nonHierarchyGraphLinksList.append(link)

        # Create list of non hierarchical nodes

        # For each class or note
        for sugiNode in list(dictOgl.values()):
            # If not in hierarchy
            if sugiNode not in dictSugiHier:
                self.__nonHierarchyGraphNodesList.append(sugiNode)

    def __levelFind(self):
        """
        Fix the best hierarchical level for each node.

        @author Nicolas Dubois
        """
        # Simplify writing
        nodesList = self.__hierarchyGraphNodesList
        # Fix nodes indexes corresponding to matrix column and line index
        nbNodes = len(nodesList) # Number of nodes in hierarchy
        for i in range(nbNodes):
            nodesList[i].setIndex(i)

        # Initialize the boolean matrix
        #
        # Example of use:
        #
        #      |A|B|C
        #     -+-+-+-
        #     A|0|0|1 <-- that 1 means A is C's father
        #     -+-+-+-     and is on coords matrix[2][0]
        #     B|0|0|0
        #     -+-+-+-     matrix[column][line]
        #     C|0|1|0
        #
        #
        matrix = [[0 for el in range(nbNodes)] for el2 in range(nbNodes)]

        # Fill matrix
        # For each node in graph
        for node in nodesList:
            # For each father
            for (father, link) in node.getFathers():
                # Mark relation with a '1' on coords[index Son][index Father]
                matrix[node.getIndex()][father.getIndex()] = 1

        # Define levels

        # Sum each column of the matrix
        sumColumns = [None for el in range(nbNodes)]
        for i in range(nbNodes):
            sumColumns[i] = 0
            for el in matrix[i]:
                sumColumns[i] += el

        # Index of nodes that are not in any level yet
        indexNodes = list(range(nbNodes))

        # While not all nodes have an attributed level
        # while indexNodes != []:
        while indexNodes:
            level = []  # Current level
            indexNodesNotSel = indexNodes[:]
            indexNodesSel = []

            # For all nodes that haven't an attributed level
            for i in indexNodes:
                # When the sum of his matrix column is 0, that means he has no
                # parent or his parents are already in a level
                if sumColumns[i] == 0:
                    # The node is attributed on the current level
                    # Update the lists of selected nodes
                    indexNodesSel.append(i)
                    indexNodesNotSel.remove(i)

            # If no nodes is selected, there is a cycle in hierarchal links
            # if indexNodesSel == []:
            if not indexNodesSel:
                return 0

            # For all the current level's nodes
            for i in indexNodesSel:
                level.append(nodesList[i])
                # Update the sum of the columns when we remove the line of the
                # node in the matrix
                for j in indexNodesNotSel:
                    sumColumns[j] -= matrix[j][i]
            # Update the list of the nodes that haven't a level yet
            indexNodes = indexNodesNotSel[:]
            # Add the current level to the list
            self.__levels.append(level)

        # Fix nodes index and level for each nodes
        for l in range(len(self.__levels)):
            level = self.__levels[l]
            for i in range(len(level)):
                node = level[i]
                node.setIndex(i)
                node.setLevel(l)

        # No error
        return 1

    def __addNonHierarchicalNodes(self):
        """
        Add non-hierarchial nodes into levels.

        @author Nicolas Dubois
        """
        # Vocabulary:
        # Internal node: nodes present in levels
        # External node: nodes not present in levels yet

        # Dictionary internalNodes externalNodes:
        # Keys are internal respectively external nodes
        # Values :
        #   - externalNodes : # of link to internal nodes
        internalNodes = {}
        externalNodes = {}

        # Make dictionary of internal nodes
        for node in self.__hierarchyGraphNodesList:
            internalNodes[node] = None

        # Make dictionary of external nodes
        for node in self.__nonHierarchyGraphNodesList:
            # Count link to internal nodes
            count = 0
            for (dstNode, link) in node.getNonHierarchicalLink():
                if dstNode in internalNodes:
                    count += 1

            # Add node to externalNodes
            externalNodes[node] = count

        # If there is no level (no inheritance or realisation) but there are
        # nodes to put in, create new level
        if not self.__levels and externalNodes:

            # Add one level for nodes
            self.__levels.append([])

        # Function for getting node that has most connections to internal
        # nodes
        def mostConnection(externalNodes):

            maxNode = None
            maxNbLinks = -1

            for (nbLinkNode, nbLinks) in list(externalNodes.items()):
                # If current node has more connections
                if nbLinks > maxNbLinks:
                    maxNode    = nbLinkNode
                    maxNbLinks = nbLinks

            return maxNode
        # End of mostConnection

        # Function for evaluting best level and best index for an external
        # node

        def bestPos(extNode, internalNodes):
            # Returns (level, index)

            # Evaluate average of level of linked nodes
            nb = 0
            summation = 0
            nodes = []  # List of connected internal nodes

            # For all non hierarchical links
            for (dstNode, link) in extNode.getNonHierarchicalLink():
                # If node linked to internal nodes
                if dstNode in internalNodes:

                    # Add connected node to list
                    nodes.append(dstNode)

                    # Add level to sum and count number of link
                    summation += dstNode.getLevel()
                    nb += 1

            # If no link to internal nodes
            # if nodes == []:
            if not nodes:
                return None, None

            # Find closer node to average position
            avgLevel = float(summation) / nb
            levelNodes = []  # List of nodes on same level
            bestLevel = None
            # Fix best level on first node
            # if nodes != []:
            if nodes:
                bestLevel = nodes[0].getLevel()

            # For all connected internal nodes
            for connectedInternalNode in nodes:
                nodeLevel = connectedInternalNode.getLevel()

                # If current node is on bestLevel
                if nodeLevel == bestLevel:
                    levelNodes.append(connectedInternalNode)

                # Else if current node is nearer to average position or
                # is at same distance but with less nodes on level
                # TODO Refactor this test to a method
                elif abs(nodeLevel - avgLevel) < abs(bestLevel - avgLevel) or (abs(nodeLevel - avgLevel) == abs(bestLevel - avgLevel) and
                                                                               len(self.__levels[nodeLevel]) < len(self.__levels[bestLevel])):

                    # Store best level
                    bestLevel = nodeLevel

                    # Start new list of nodes on new best level
                    levelNodes = [connectedInternalNode]

            # Return average of nodes' level
            return bestLevel, levelNodes[len(levelNodes) // 2].getIndex()
        # End of bestPos

        # Function for getting level that has less nodes in.

        def getLessFilledLevel():

            lessLevel = 0  # Index of level that has less node in it
            nb = len(self.__levels[lessLevel])

            for x in range(1, len(self.__levels)):
                if len(self.__levels[x]) < nb:
                    lessLevel = x
                    nb = len(self.__levels[x])

            return lessLevel

        # Function to move a node from internal to external nodes.
        def moveExternal2Internal(node, internalNodes, externalNodes):

            # Remove node from external nodes
            del externalNodes[node]

            # Add node to internal nodes
            internalNodes[node] = None

            # For all his linked external nodes, update their counter
            extNode = None
            for (dstNode, link) in node.getNonHierarchicalLink():
                if dstNode in externalNodes:
                    externalNodes[dstNode] += 1

        # While there are nodes still not in hierarchy
        while externalNodes:
            # Get external node that has most connections to internalNodes
            extNode = mostConnection(externalNodes)
            # ~ print extNode.getName()
            # Evaluate best level and index for the node
            (level, index) = bestPos(extNode, internalNodes)

            # If node has no connection to internal node
            if level is None:
                # Find level that is less filled of nodes
                level = getLessFilledLevel()
                index = len(self.__levels[level])

            # Add node in levels
            extNode.setLevel(level)
            extNode.setIndex(index)
            self.__levels[level].insert(index, extNode)
            # Shift index attributes on right
            for i in range(index + 1, len(self.__levels[level])):
                self.__levels[level][i].setIndex(i)

            # Move node from external to internal nodes
            moveExternal2Internal(extNode, internalNodes, externalNodes)

    def __addVirtualNodes(self):
        """
        Add a vitual node by level crossed between fathers and sons that are
        separated by more than one level.

        @author Nicolas Dubois
        """

        # Internal function for updating a sons or fathers list
        def updateLink(nodesList, link, newNode):
            """
            Find the tuple (node, link2) in nodesList where link == link2 and
            replace node by newNode.
            """
            for i in range(len(nodesList)):
                (node, link2) = nodesList[i]
                if link == link2:
                    nodesList[i] = (newNode, link)
                    break

        # Add virtual nodes between a father and one of his sons
        def addVirtualNodesOnHierarchicalLink(link):

            srcNode = link.getSource()
            dstNode = link.getDestination()
            dstNodeLevel = dstNode.getLevel()

            # List of level index between dstNode and srcNode
            indexLevels = list(range(dstNodeLevel + 1, srcNode.getLevel()))

            # Continue only if there is at least one level between the two
            # nodes
            if len(indexLevels) == 0:
                return

            # For each crossed level, add a virtual node
            vnodes = [VirtualSugiyamaNode() for el in indexLevels]

            # Fix level
            for i in range(len(vnodes)):
                vnode = vnodes[i]
                vnode.setLevel(dstNodeLevel + i + 1)

            # Fix relation between virtual nodes
            for i in range(len(vnodes) - 1):
                vnodes[i].addSon(vnodes[i + 1], link)
                vnodes[i + 1].addFather(vnodes[i], link)

            # Fix relations between virtual and real nodes
            vnodes[-1].addSon(srcNode, link)
            vnodes[0].addFather(dstNode, link)

            updateLink(dstNode.getSons(), link, vnodes[0])
            updateLink(srcNode.getFathers(), link, vnodes[-1])

            # Add virtual nodes in levels
            for i in range(len(vnodes)):
                level = self.__levels[dstNodeLevel + i + 1]
                level.append(vnodes[i])
                # Fix index of the virtual node
                level[-1].setIndex(len(level) - 1)

            # Add virtual nodes in link in order bottom to top
            for i in range(len(vnodes) - 1, -1, -1):
                link.addVitualNode(vnodes[i])

        # For all links
        for link in self.__sugiyamaLinksList:
            # If hierarchical link
            if link.getType() == OGL_INHERITANCE or link.getType() == OGL_INTERFACE:

                # Add virtual nodes
                addVirtualNodesOnHierarchicalLink(link)

    def __sortLevel(self, indexLevel):
        """
        Sort nodes on a level according to precalculated barycenter value.
        Nodes that don't have a barycenter value keep their place.

        @param indexLevel : index of level in self.__levels to sort
        @author Nicolas Dubois
        """
        level = self.__levels[indexLevel]
        levelCopy = level[:]

        nbIntersect = self.__getNbIntersectAll()

        # Get list of nodes who have a barycenter value
        listIndex = []
        for i in range(len(levelCopy)):
            if levelCopy[i].getBarycenter() is not None:
                listIndex.append(i)

        # Create list of nodes to sort
        listNodes = []
        for i in listIndex:
            listNodes.append(levelCopy[i])

        # Sort list of nodes
        listNodes.sort(cmpBarycenter)

        # Put sorted list in levelCopy
        for i in range(len(listNodes)):
            levelCopy[listIndex[i]] = listNodes[i]

        # Fix indexes
        for i in range(len(levelCopy)):
            levelCopy[i].setIndex(i)

        # If there are more intersections than before, keep original order
        nbIntersect2 = self.__getNbIntersectAll()
        if nbIntersect < nbIntersect2:
            # Fix indexes
            for i in range(len(level)):
                level[i].setIndex(i)
        else:
            # Else set new order
            self.__levels[indexLevel] = levelCopy
        nbIntersect3 = self.__getNbIntersectAll()

    def __shiftSameBarycenter(self, indexLevel):
        """
        Do a left circular shifting on nodes with same barycenter on a level.

        For each group of nodes wich have the same pre-calulated value, do a
        left circular shifting of the nodes.

        @param indexLevel : index of level
        @author Nicolas Dubois
        """
        level = self.__levels[indexLevel]

        # Save current level
        levelSaved = level[:]
        # Count crossings
        nbIntersections = self.__getNbIntersectAll()

        # Shift same barycenter
        for i in range(len(level) - 1):
            if level[i].getBarycenter() is not None and level[i].getBarycenter() == level[i + 1].getBarycenter():

                level.insert(i, level.pop(i + 1))
                # Fix index
                level[i].setIndex(i)
                level[i + 1].setIndex(i + 1)

        # If new order give more intersections, return to old order
        if self.__getNbIntersectAll() > nbIntersections:
            self.__levels[indexLevel] = levelSaved
            for i in range(len(levelSaved)):
                levelSaved[i].setIndex(i)

    def __sortSameBarycenter(self, indexLevel):
        """

        @param indexLevel : index of level
        @author Nicolas Dubois
        """
        level = self.__levels[indexLevel]

        # Internal function for comparing barycenter

        # A group is a list of nodes that have the same barycenter value
        # groups is a list of all group
        # groups = [[node, node, ..], [node, ..], ..]
        groups = [[]]

        # Fix indexes
        for i in range(len(level)):
            node = level[i].setIndex(i)

        barycenter = level[0].getBarycenter()
        index = 0

        # Put all nodes in groups
        for node in level:
            if node.getBarycenter() == barycenter:
                groups[index].append(node)
            else:
                groups.append([node])
                index += 1
                barycenter = node.getBarycenter()

        # Compute new barycenter value = average of parents'down-barycenter
        # and sons'up-barycenter
        for node in level:
            node.barycenterIndex()

        # Sort each group of nodes
        for group in groups:
            group.sort(cmpBarycenter)

        # Fix new positions
        moved = 0
        index = 0
        for group in groups:
            for node in group:
                if node.getIndex() != index:
                    node.setIndex(index)
                    moved = 1
                index += 1

        # Sort level on new indexes
        level.sort(cmpIndex)

        return moved

    def __upBarycenterLevel(self, indexLevel):
        """
        Compute up barycenter (from parents) for all nodes on level.

        @param indexLevel : index of level
        @author Nicolas Dubois
        """
        level = self.__levels[indexLevel]
        for node in level:
            node.upBarycenterIndex()

    def __downBarycenterLevel(self, indexLevel):
        """
        Compute down barycenter (from sons) for all nodes on level.

        @param indexLevel : index of level
        @author Nicolas Dubois
        """
        level = self.__levels[indexLevel]
        for node in level:
            node.downBarycenterIndex()

    def __barycenterLevel(self, indexLevel):
        """
        Compute average of up and down barycenter for all nodes on level.

        @param indexLevel : index of level
        @author Nicolas Dubois
        """
        level = self.__levels[indexLevel]
        for node in level:
            node.barycenterIndex()

    def __sortNeeded(self, indexLevel):
        """
        Check if nodes have to be re-ordered.

        @param indexLevel : index of level
        @return boolean : True if nodes have to be sorted
        @author Nicolas Dubois
        """
        level = self.__levels[indexLevel]
        barycenter = level[0].getBarycenter()

        # Check nodes from left to right
        for node in level:
            # If node barycenter < his left neighbor
            if node.getBarycenter() < barycenter:
                return 1
            barycenter = node.getBarycenter()

        return 0

    def __fixXCoord(self, indexLevel):
        """
        Fix temporary x coord for each node on the level, packed on the left.

        @param indexLevel : index of level
        @author Nicolas Dubois
        """
        level = self.__levels[indexLevel]
        x = 0

        # For each node on level
        for node in level:
            # Fix x coordinate
            node.setPosition(x, 0)
            x += node.getSize()[0]

    def __initNodesIndex(self):
        """
        Initialize nodes index and level.

        @author Nicolas Dubois
        """
        # Fix nodes index for each level
        for l in range(len(self.__levels)):
            level = self.__levels[l]
            for i in range(len(level)):
                node = level[i]
                node.setIndex(i)
                node.setLevel(l)

    def __getNbIntersectAll(self):
        """
        Return number of intersections between hierarchy relations.

        @author Nicolas Dubois
        """
        count = 0
        for i in range(len(self.__levels) - 1):
            count += self.__getNbIntersect2Levels(i)

        return count

    def __getNbIntersect2Levels(self, upperLevel):
        """
        Return intersections number of hierarchical links between two levels.

        The two levels index are [upperLevel] and [upperLevel + 1].

        @param upperLevel : index of upper level
        @author Nicolas Dubois
        """
        # Get nodes from the level
        nodes = self.__levels[upperLevel]

        # Count intersect
        count = 0

        # For each node of the layer
        for indFatherL in range(len(nodes) - 1):
            # For each son of the current node
            for (sonL, link) in nodes[indFatherL].getSons():

                # Check intersect with all next parents
                indFatherR = indFatherL + 1
                while indFatherR < len(nodes):
                    for (sonR, rLink) in nodes[indFatherR].getSons():
                        # If intersect
                        if sonL.getIndex() > sonR.getIndex():
                            count += 1
                    indFatherR += 1

        return count

    def __barycenter_(self):
        """
        Find nodes index for minimizing hierarchical links crossing.

        @author Nicolas Dubois
        """

        MAX_ITER = 20       # Max number of iterations
        moved = 1           # There has been a move during a phase
        shiftOnUpward = 0   # Shift nodes only on ascending phase

        # While classes are moved and MAX_ITER not reached
        while moved and MAX_ITER:

            # Downward phase

            moved = 0
            # For each level except the first one
            for i in range(1, len(self.__levels)):

                # Memorize level state
                levelState = self.__levels[i][:]

                # Compute parents down-barycenter
                if i > 0:
                    self.__downBarycenterLevel(i - 1)
                # Compute sons up-barycenter
                if i < len(self.__levels) - 1:
                    self.__upBarycenterLevel(i + 1)

                # Compute up-barycenter on current level
                self.__upBarycenterLevel(i)
                self.__sortLevel(i)

                #
                if not shiftOnUpward and self.__getNbIntersectAll():
                    self.__shiftSameBarycenter(i)
                #
                else:
                    self.__sortSameBarycenter(i)

                # Check if order of nodes has been changed
                if levelState != self.__levels[i]:
                    moved = 1

            # Upward phase

            # For each level except last
            for i in range(len(self.__levels) - 2, -1, -1):

                # Memorize level state
                levelState = self.__levels[i][:]

                # Compute parents down-barycenter
                if i > 0:
                    self.__downBarycenterLevel(i - 1)
                # Compute sons up-barycenter
                if i < len(self.__levels) - 1:
                    self.__upBarycenterLevel(i + 1)

                # Compute up-barycenter on current level
                self.__downBarycenterLevel(i)
                #  ~ if self.__sortNeeded(i):
                    #  ~ moved = 1
                self.__sortLevel(i)
                if shiftOnUpward and self.__getNbIntersectAll():
                    self.__shiftSameBarycenter(i)
                #
                else:
                    self.__sortSameBarycenter(i)
                    #  ~ if self.__sortSameBarycenter(i):
                        #  ~ moved = 1

                # Check if order of nodes has been changed
                if levelState != self.__levels[i]:
                    moved = 1

            MAX_ITER -= 1
            shiftOnUpward = not shiftOnUpward

    def __barycenter(self):
        """
        Find nodes index for minimizing hierarchical links crossing.

        This function is not used. It was the first version, created
        according to the theoretical algorithm.
        It has been replaced by a new barycenter method.

        @author Nicolas Dubois
        """

        MAX_ITER = 20

        while self.__getNbIntersectAll() > 0 and MAX_ITER > 0:

            # Downward phase

            # For each level except first
            for i in range(1, len(self.__levels)):

                # Compute parents down-barycenter
                if i > 0:
                    self.__downBarycenterLevel(i - 1)
                # Compute sons up-barycenter
                if i < len(self.__levels) - 1:
                    self.__upBarycenterLevel(i + 1)

                # Compute up-barycenter on current level
                self.__upBarycenterLevel(i)
                self.__sortLevel(i)
                self.__shiftSameBarycenter(i)

            # Upward phase

            if self.__getNbIntersectAll() > 0:

                indexList = list(range(len(self.__levels) - 1))
                indexList.reverse()
                for i in indexList:

                    self.__downBarycenterLevel(i)
                    self.__sortLevel(i)
                    self.__shiftSameBarycenter(i)

                MAX_ITER -= 1

    def __fixPositions(self):
        """
        Compute coordinates for each nodes and links.

        @author Nicolas Dubois
        """
        self.__fixNodesNeighbors()
        self.__fixNodesPositions()
        self.__fixLinksPositions()

    def __fixNodesNeighbors(self):
        """
        For each node, fix his right neighbor.

        @author Nicolas Dubois
        """
        # For each node, fix his neighbors if he has, None else
        for level in self.__levels:
            nbNodes = len(level)

            for i in range(nbNodes - 1):
                level[i + 1].setLeftNode(level[i])
                level[i].setRightNode(level[i + 1])

            # For first and last nodes of the level
            level[0].setLeftNode(None)
            level[nbNodes - 1].setRightNode(None)

    def __fixNodesPositions(self):

        # Compute start positions packed on left
        y = UP_MARGIN
        for level in self.__levels:
            x = LEFT_MARGIN
            maxHeight = 0
            for node in level:
                (width, height) = node.getSize()
                node.setPosition(x, y)
                x += width + H_SPACE
                maxHeight = max(maxHeight, height)
            y += maxHeight + V_SPACE

        if STEPBYSTEP:
            waitKey(self._umlFrame)

        # While nodes have to be moved
        moved = 1
        while moved:
            moved = 0
            # Compute average coordinates for each node
            for level in self.__levels:
                for node in level:
                    if node.balance():
                        moved = 1
                        if STEPBYSTEP:
                            waitKey(self._umlFrame)

    def __fixNodesPositions_(self):
        """
        Compute coordinates for each nodes.

        @author Nicolas Dubois
        """
        y = UP_MARGIN
        for level in self.__levels:
            x = LEFT_MARGIN
            maxHeight = 0
            for node in level:
                (width, height) = node.getSize()
                node.setPosition(x, y)
                x += width + H_SPACE
                maxHeight = max(maxHeight, height)
            y += maxHeight + V_SPACE

        # Balance the graph with the barycenter value

        # Downward phase
        for l in range(1, len(self.__levels)):

            level = self.__levels[l]
            # Compute the barycenter on all nodes of the level before trying
            # to balance them
            for node in level:
                node.upBarycenterX()

            # Balance each node on level
            for node in level:
                node.balance()

        # Upward phase
        for l in range(len(self.__levels) - 2, -1, -1):

            level = self.__levels[l]
            # Compute the barycenter on all nodes of the level before trying
            # to balance them
            for node in level:
                node.downBarycenterX()

            # Balance each node on level
            for node in level:
                node.balance()

    def __fixLinksPositions(self):
        """
        Compute links new positions.

        @author Nicolas Dubois
        """

        # ~ def cmpSons(lSon, rSon):
            # ~ return cmp(lSon[0].getIndex(), rSon[0].getIndex())

        # For each hierarchical link, fix anchors coordinates
        for level in self.__levels:
            for node in level:
                node.fixAnchorPos()

        # For each hierarchical link, add control points to pass through
        # each virtual nodes
        for link in self.__sugiyamaLinksList:
            link.fixControlPoints()

    def doAction(self, umlObjects, selectedObjects, umlFrame):
        """
        Do the tool's action

        @param OglObject [] umlObjects : list of uml objects of the diagram
        @param OglObject [] selectedObjects : list of the selected objects
        @param UmlFrame umlFrame : the frame of the diagram
        @author Nicolas Dubois
        """
        if umlFrame is None:
            # TODO : displayError "No frame opened"
            return

        print("Begin Sugiyama algorithm")
        # Create the subgraph containing the hierarchical relations
        self.__createInterfaceOglALayout(umlObjects)

        # Compute the best level for each nodes
        if not self.__levelFind():
            print("Error: there is a cycle in hierarchial links. Sugiyama" " algorithm could not be applied")
            return

        # Add vitual nodes between fathers and sons which are separated by
        # more than one level.
        self.__addVirtualNodes()

        # Apply barycenter algorithm to the graph for minimizing crossings
        self.__barycenter()
        print("Nb of hierarchical intersections:", self.__getNbIntersectAll())

        # Add non hierarchical nodes to levels
        # ~ print self.__nonHierarchyGraphNodesList
        # ~ print self.__nonHierarchyGraphLinksList
        self.__addNonHierarchicalNodes()

        # Fix the coordinates xy of the nodes
        self.__fixPositions()

        # Redraw frame
        self._umlFrame.Refresh()

        print("End Sugiyama algorithm")

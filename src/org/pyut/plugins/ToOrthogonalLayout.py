
from typing import List

from logging import Logger
from logging import getLogger

from time import time
from typing import Tuple
from typing import cast

from pygmlparser.graphics.Point import Point
from wx import CENTRE
from wx import ICON_ERROR
from wx import MessageDialog
from wx import OK
from wx import Yield as wxYield

from pygmlparser.Graph import Graph
from pygmlparser.Node import Node

from org.pyut.MiniOgl.Shape import Shape
from org.pyut.ogl.OglLink import OglLink

from org.pyut.ogl.OglNote import OglNote

from org.pyut.plugins.PyutToPlugin import PyutToPlugin
from org.pyut.plugins.orthogonal.CartesianConverter import CartesianConverter

from org.pyut.ui.UmlFrame import UmlFrame

from org.pyut.ogl.OglClass import OglClass

from org.pyut.plugins.orthogonal.TulipMaker import TulipMaker
from org.pyut.plugins.orthogonal.TulipMaker import OglToTulipMap

from pygmlparser.Parser import Parser


class ToOrthogonalLayout(PyutToPlugin):
    """
    Layout the UML class diagram by changing the links to an orthogonal layout
    """
    def __init__(self, umlObjects: List[OglClass], umlFrame: UmlFrame):
        """

        Args:
            umlObjects:  list of ogl objects
            umlFrame:    A Pyut umlFrame
        """
        super().__init__(umlObjects, umlFrame)

        self.logger: Logger = getLogger(__name__)

    def getName(self):
        """
        Returns: the name of the plugin.
        """
        return "Orthogonal Layout"

    def getAuthor(self):
        """
        Returns:
            The author's name
        """
        return "Humberto A. Sanchez II"

    def getVersion(self):
        """
        Returns:
            The plugin version string
        """
        return "1.0"

    def getMenuTitle(self):
        """
        Returns:
            The menu title for this plugin
        """
        return "Orthogonal Layout"

    def setOptions(self):
        """
        Prepare the import.
        This can be used to ask some questions to the user.

        Returns:
            If False, the import will be cancelled.
        """
        return True

    def doAction(self, umlObjects: List[OglClass], selectedObjects: List[OglClass], umlFrame: UmlFrame):
        """
        Do the tool's action

        Args:
            umlObjects:         list of the uml objects of the diagram
            selectedObjects:    list of the selected objects
            umlFrame:           The diagram frame
        """
        if umlFrame is None:
            self.displayNoUmlFrame()
            return
        if len(umlObjects) == 0:
            self.displayNoUmlObjects()
            return

        self.logger.info(f'Begin Orthogonal algorithm')

        tulipMaker: TulipMaker = TulipMaker()

        tulipMaker.translate(umlObjects)
        success: TulipMaker.LayoutStatus = tulipMaker.layout()
        if success[0] is False:
            dlg = MessageDialog(None, success[1],  'Layout Error', OK | ICON_ERROR | CENTRE)
            dlg.ShowModal()
            dlg.Destroy()

        pathToLayout: str = tulipMaker.pathToLayout

        parser: Parser = Parser()

        parser.loadGML(path=pathToLayout)
        parser.parse()

        gmlGraph: Graph = parser.graph
        gmlNodes: Graph.Nodes = gmlGraph.graphNodes
        gmlEdges: Graph.Edges = gmlGraph.graphEdges

        self.logger.info(f'Graph Node count: {len(gmlNodes)} Edge Count: {len(gmlEdges)}')

        nodeIdMap: OglToTulipMap = tulipMaker.nodeIdMap
        edgeIdMap: OglToTulipMap = tulipMaker.edgeIdMap

        for umlObj in umlObjects:
            if isinstance(umlObj, OglClass) or isinstance(umlObj, OglNote):
                gmlNodeId: int  = nodeIdMap[umlObj.GetID()]
                gmlNode:   Node = gmlNodes[gmlNodeId]
                self._stepNodes(umlObj, gmlNode)
            self._animate(umlFrame)

        for umlLink in umlObjects:
            if isinstance(umlLink, OglLink):
                umlLink: OglLink   = cast(OglLink, umlLink)
                gmlEdgeId: int     = edgeIdMap[umlLink.GetID()]
                # gmlEdge:   Edge    = gmlEdges[gmlEdgeId]
                gmlEdge = [gEdge for gEdge in gmlEdges if gEdge.id == gmlEdgeId][0]

                line: Tuple[Point] = gmlEdge.graphics.line
                self.logger.info(f'{umlLink} has points {len(line)}')

    def _stepNodes(self, srcShape: Shape, gmlNode: Node):

        oldX, oldY = srcShape.GetPosition()
        cartesianX: int = gmlNode.graphics.x
        cartesianY: int = gmlNode.graphics.y

        newX, newY = CartesianConverter.cartesianToScreen(cartesianX, cartesianY)

        self.logger.info(f'{srcShape} - oldX,oldY = {oldX},{oldY} newX,newY = {newX},{newY}')

        srcShape.SetPosition(newX, newY)

    def _animate(self, umlFrame):
        """
        Does an animation simulation

        Args:
            umlFrame:
        """
        umlFrame.Refresh()
        self.logger.debug(f'Refreshing ...............')
        wxYield()
        t = time()
        while time() < t + 0.05:
            pass

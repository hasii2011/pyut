
from logging import Logger
from logging import getLogger
from typing import Any

from typing import List
from typing import Dict
from typing import Tuple
from typing import Union
from typing import cast

# noinspection PyPackageRequirements
from tulip import tlp           # because they named it tulip-python

from org.pyut.ogl.OglClass import OglClass
from org.pyut.ogl.OglLink import OglLink
from org.pyut.ogl.OglNote import OglNote

"""
Use Any as a substitute for tlp.Node and tlp.Edge
"""
TulipNodes = Dict[int, Any]
TulipEdges = Dict[str, Any]


class TulipMaker:

    OGL_ID: str = 'oglId'
    LayoutStatus = Tuple[bool, str]

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self._graph: tlp.Graph = tlp.newGraph()
        self._graph.setName('Translation Graph')

        self._tulipNodes: TulipNodes = {}
        self._tulipEdges: TulipEdges = {}

        self._minCoordinates: tlp.Vec3f = None
        self._maxCoordinates: tlp.Vec3f = None

        self.logger.info(f'Graph Name: {self._graph.getName()}')

    def translate(self, umlObjects: List[OglClass]):

        for umlClass in umlObjects:
            if isinstance(umlClass, OglClass) or isinstance(umlClass, OglNote):
                umlClass: OglClass = cast(OglClass, umlClass)
                tNode: tlp.Node = self._createNode(umlClass)
                self._tulipNodes[self.__getOglIdFromNode(tNode)] = tNode
        self.logger.info(f'Created {len(self._tulipNodes)} tulip nodes')

        for umlClass in umlObjects:
            if isinstance(umlClass, OglClass) or isinstance(umlClass, OglNote):
                self._createEdges(umlClass)

        self.logger.info(f'Created {len(self._tulipEdges)} tulip edges')

    def layout(self) -> LayoutStatus:

        params  = self._setupGraphParameters()

        success: TulipMaker.LayoutStatus = self._graph.applyLayoutAlgorithm('Hierarchical Tree (R-T Extended)',  params)

        if success[0] is True:
            resultLayout = self._graph.getLayoutProperty("viewLayout")
            self._minCoordinates = resultLayout.getMin()
            self._maxCoordinates = resultLayout.getMax()

            gmlPluginParams = tlp.getDefaultPluginParameters('GML Export', self._graph)
            tlp.exportGraph('GML Export', self._graph, 'translationGraph.gml', gmlPluginParams)

        return success

    def _createNode(self, umlClass: OglClass) -> Any:
        """

        Args:
            umlClass:  An OglClass

        Returns:
                a tlp.Node
        """

        graph: tlp.Graph = self._graph
        node:  tlp.Node  = graph.addNode()

        x, y = umlClass.GetPosition()
        w, h = umlClass.GetSize()

        graphViewLayout = graph.getLayoutProperty('viewLayout')
        graphViewSize   = graph.getSizeProperty('viewSize')
        graphViewShape  = graph.getIntegerProperty('viewShape')

        graphViewLayout[node] = tlp.Coord(x, y,  0)
        graphViewSize[node]   = tlp.Size(w, h, 0)
        graphViewShape[node]  = tlp.NodeShape.Square

        self.__setOglIdOnNode(node, umlClass)

        return node

    def _createEdges(self, umlClass: Union[OglClass, OglNote]):

        for link in umlClass.getLinks():
            link: OglLink = cast(OglLink, link)
            self.logger.debug(f'{umlClass} has link {link}')

            srcOglId:  int = link.getSourceShape().GetID()
            destOglId: int = link.getDestinationShape().GetID()

            sourceTulipNode = self._tulipNodes[srcOglId]
            targetTulipNode = self._tulipNodes[destOglId]

            edgeName: str = f'{srcOglId}-to-{destOglId}'
            if edgeName not in self._tulipEdges:
                tulipEdge: tlp.Edge = self._graph.addEdge(sourceTulipNode, targetTulipNode)
                edgeNameProperty = self._graph.getStringProperty('edgeName')
                edgeNameProperty.setEdgeValue(tulipEdge, edgeName)
                self._tulipEdges[edgeName] = tulipEdge

    def __setOglIdOnNode(self, node, umlClass: OglClass):

        oglId:         int                  = umlClass.GetID()
        oglIdProperty: tlp.IntegerProperty = self._graph.getIntegerProperty(TulipMaker.OGL_ID)
        oglIdProperty.setNodeValue(node, oglId)

    def __getOglIdFromNode(self, tlpNode) -> int:

        oglIdProperty: tlp.IntegerProperty = self._graph.getIntegerProperty(TulipMaker.OGL_ID)
        oglId:         int                 = oglIdProperty.getNodeValue(tlpNode)

        return oglId

    def _setupGraphParameters(self) -> Dict[str, Any]:

        params = tlp.getDefaultPluginParameters('Hierarchical Tree (R-T Extended)', self._graph)

        params['orthogonal']    = True
        params["orientation"]   = "vertical"
        params["layer spacing"] = 100.0
        params["node spacing"]  = 50.0

        return params

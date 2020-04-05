
from logging import Logger
from logging import getLogger
from typing import Any

from typing import List
from typing import Dict
from typing import Tuple
from typing import Union
from typing import cast

from os import sep as osSep

import tempfile

# noinspection PyPackageRequirements
from tulip import tlp           # because they named it tulip-python

from org.pyut.general.exceptions.UnsupportedOperation import UnsupportedOperation
from org.pyut.ogl.OglClass import OglClass
from org.pyut.ogl.OglLink import OglLink
from org.pyut.ogl.OglNote import OglNote
from org.pyut.plugins.orthogonal.OrthogonalOptions import OrthogonalOptions

"""
Use Any as a substitute for tlp.Node and tlp.Edge
"""
TulipNodes = Dict[int, Any]
TulipEdges = Dict[str, Any]

OglToTulipMap = Dict[int, int]     # OglId to Tulip Id


class TulipMaker:

    LayoutStatus = Tuple[bool, str]

    DEBUG_TEMP_FILE_LOCATION:  bool = True          # TODO: Make this a debug runtime value
    OGL_ID:                    str = 'oglId'

    TEMPORARY_GML_LAYOUT_FILENAME: str = 'translationGraph.gml'

    def __init__(self, options: OrthogonalOptions):

        self.logger: Logger = getLogger(__name__)

        self._options: OrthogonalOptions = options
        self._graph: tlp.Graph = tlp.newGraph()
        self._graph.setName('Translation Graph')

        self._tulipNodes: TulipNodes = {}
        self._tulipEdges: TulipEdges = {}

        self._nodeIdMap: OglToTulipMap = {}
        self._edgeIdMap: OglToTulipMap = {}

        self._minCoordinates: tlp.Vec3f = None
        self._maxCoordinates: tlp.Vec3f = None

        tempDir: str = tempfile.gettempdir()

        if TulipMaker.DEBUG_TEMP_FILE_LOCATION is True:
            self._pathToLayout = f'{TulipMaker.TEMPORARY_GML_LAYOUT_FILENAME}'
        else:
            self._pathToLayout = f'{tempDir}{osSep}{TulipMaker.TEMPORARY_GML_LAYOUT_FILENAME}'
        self.logger.info(f'Graph Name: {self._graph.getName()}')

    def getPathToLayout(self) -> str:
        return self._pathToLayout

    def setPathToLayout(self, theNewValue: str):
        raise UnsupportedOperation('This is a read-only property')

    def getNodeIdMap(self) -> OglToTulipMap:
        return self._nodeIdMap

    def setNodeIdMap(self, theNewValue: OglToTulipMap):
        raise UnsupportedOperation('This is a read-only property')

    def getEdgeIdMap(self) -> OglToTulipMap:
        return self._edgeIdMap

    def setEdgeIdMap(self, theNewValue: OglToTulipMap):
        self._edgeIdMap = theNewValue

    pathToLayout = property(getPathToLayout, setPathToLayout)
    nodeIdMap    = property(getNodeIdMap, setNodeIdMap)
    edgeIdMap    = property(getEdgeIdMap, setEdgeIdMap)

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
        # Normalize coordinates to screen coordinates
        bb = tlp.computeBoundingBox(self._graph)
        self._graph['viewLayout'].translate(bb[0] * -1)

        if success[0] is True:
            resultLayout = self._graph.getLayoutProperty("viewLayout")
            self._minCoordinates = resultLayout.getMin()
            self._maxCoordinates = resultLayout.getMax()

            gmlPluginParams = tlp.getDefaultPluginParameters('GML Export', self._graph)
            tlp.exportGraph('GML Export', self._graph, self._pathToLayout, gmlPluginParams)

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
        graphViewShape[node]  = tlp.NodeShape.RoundedBox

        self.__setOglIdOnNode(node, umlClass)

        self.logger.info(f'Created tulip node.id {node.id} for OglClass.id: {umlClass.GetID()}')
        # self._nodeIdMap[node.id] = umlClass.GetID()
        self._nodeIdMap[umlClass.GetID()] = node.id

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

                self._tulipEdges[edgeName]    = tulipEdge
                self._edgeIdMap[link.GetID()] = tulipEdge.id

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

        #
        # TODO Set these as plugin options
        #
        params['orthogonal']     = True
        params["orientation"]    = self._options.orientation.value
        params["layer spacing"]  = self._options.layerSpacing
        params["node spacing"]   = self._options.nodeSpacing
        params['compact layout'] = self._options.compactLayout

        return params

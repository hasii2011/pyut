
from logging import Logger
from logging import getLogger

from typing import List
from typing import cast

# noinspection PyPackageRequirements
from tulip import tlp

from org.pyut.ogl.OglClass import OglClass


class TulipMaker:

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self._graph: tlp.Graph = tlp.newGraph()
        self._graph.setName('Translation Graph')

        self._tulipNodes: List[tlp.Node] = []
        self.logger.info(f'Graph Name: {self._graph.getName()}')

    def translate(self, umlObjects: List[OglClass]):

        for umlClass in umlObjects:
            if isinstance(umlClass, OglClass):
                umlClass: OglClass = cast(OglClass, umlClass)
                tNode: tlp.Node = self._createNode(umlClass)
                self._tulipNodes.append(tNode)

        self.logger.info(f'Created {len(self._tulipNodes)} tulip nodes')

    def _createNode(self, umlClass: OglClass):

        graph: tlp.Graph = self._graph
        node:  tlp.Node  = graph.addNode()

        x, y = umlClass.GetPosition()
        w, h = umlClass.GetSize()

        graphViewLayout = graph.getLayoutProperty('viewLayout')
        graphViewSize   = graph.getSizeProperty('viewSize')
        graphViewShape  = graph.getIntegerProperty('viewShape')

        graphViewLayout[node] = tlp.Coord(x, y,  0)
        graphViewSize[node]   = tlp.Size(w, h, 0)
        graphViewShape[node] = tlp.NodeShape.Square

        oglId: int = umlClass.GetID()
        oglIdProperty = graph.getIntegerProperty('oglId')
        oglIdProperty.setNodeValue(node, oglId)

        return node

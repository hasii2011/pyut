
from typing import Set
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from miniogl.AnchorPoint import AnchorPoint
from miniogl.LinePoint import LinePoint
from miniogl.LineShape import ControlPoints

from pyutmodel.PyutObject import PyutObject

from org.pyut.ogl.OglObject import OglObject
from org.pyut.ogl.OglClass import OglClass
from org.pyut.ogl.OglLink import OglLink
from org.pyut.ogl.OglNote import OglNote

from org.pyut.general.PyutVersion import PyutVersion
from org.pyut.general.exceptions.UnsupportedOperation import UnsupportedOperation

from org.pyut.plugins.base.PluginTypes import OglClasses


class GMLExporter:

    GRAPH_TOKEN: str = 'graph'

    ID_TOKEN:    str = 'id'
    LABEL_TOKEN: str = 'label'
    NODE_TOKEN:  str = 'node'
    EDGE_TOKEN:  str = 'edge'

    SOURCE_ID_TOKEN: str = 'source'
    TARGET_ID_TOKEN: str = 'target'

    GRAPHICS_TOKEN: str = 'graphics'
    START_TOKEN:    str = '['
    END_TOKEN:      str = ']'

    QUOTE_TOKEN: str = '"'

    LINE_DEFINITION_TOKEN:  str = 'Line'
    POINT_DEFINITION_TOKEN: str = 'point'

    X_POSITION_TOKEN: str = 'x'
    Y_POSITION_TOKEN: str = 'y'
    Z_POSITION_TOKEN: str = 'z'
    WIDTH_TOKEN:      str = 'w'
    HEIGHT_TOKEN:     str = 'h'
    DEPTH_TOKEN:      str = 'd'

    singleTab: str = ''
    doubleTab: str = ''
    tripleTab: str = ''
    quadrupleTab: str = ''
    quintupleTab: str = ''

    def __init__(self):

        self.logger:   Logger = getLogger(__name__)
        self._gml:     str    = ''

        self._prettyPrint: bool = True

    def translate(self, umlObjects: OglClasses):

        if self._prettyPrint is True:
            GMLExporter.singleTab = '\t'
            GMLExporter.doubleTab = '\t\t'
            GMLExporter.tripleTab = '\t\t\t'
            GMLExporter.quadrupleTab = '\t\t\t\t'
            GMLExporter.quintupleTab = '\t\t\t\t\t'

        gml: str = self._generateGraphStart()
        gml = self._generateNodes(umlObjects, gml)
        gml = self._generateUniqueEdges(umlObjects=umlObjects, gml=gml)

        gml = self._generateGraphTermination(gml)
        self._gml = gml

    @property
    def gml(self):
        return self._gml

    @gml.setter
    def gml(self, theNewValue):
        raise UnsupportedOperation('gml is a read-only property')

    @property
    def prettyPrint(self):
        return self._prettyPrint

    @prettyPrint.setter
    def prettyPrint(self, theNewValue):
        self._prettyPrint = theNewValue

    def write(self, pathToFile: str):

        with open(pathToFile, 'w') as writer:
            writer.write(self._gml)

    def _generateNodes(self, umlObjects: OglClasses, gml: str) -> str:

        nodeGml: str = ''
        for umlClass in umlObjects:
            if isinstance(umlClass, OglClass) or isinstance(umlClass, OglNote):
                oglObject:  OglObject  = cast(OglObject, umlClass)
                pyutObject: PyutObject = oglObject.pyutObject
                nodeGml = (
                    f'{nodeGml}'
                    f'{GMLExporter.singleTab}{GMLExporter.NODE_TOKEN} {GMLExporter.START_TOKEN}\n'
                    f'{GMLExporter.doubleTab}{GMLExporter.ID_TOKEN} {oglObject.GetID()}\n'
                    f'{GMLExporter.doubleTab}{GMLExporter.LABEL_TOKEN} "{pyutObject.name}"\n'
                    f'{self._generateNodeGraphicsSection(oglObject)}'
                    f'{GMLExporter.singleTab}{GMLExporter.END_TOKEN}\n'
                )
        return f'{gml}{nodeGml}'

    def _generateNodeGraphicsSection(self, oglObject: OglObject) -> str:

        pos = oglObject.GetPosition()
        x = pos[0]
        y = pos[1]
        z = 0
        dimensions = oglObject.GetSize()
        w = dimensions[0]
        h = dimensions[1]
        d = 0
        gml = (
            f'{GMLExporter.doubleTab}{GMLExporter.GRAPHICS_TOKEN} {GMLExporter.START_TOKEN}\n'
            
            f'{GMLExporter.tripleTab}{GMLExporter.X_POSITION_TOKEN} {x}\n'
            f'{GMLExporter.tripleTab}{GMLExporter.Y_POSITION_TOKEN} {y}\n'
            f'{GMLExporter.tripleTab}{GMLExporter.Z_POSITION_TOKEN} {z}\n'
            f'{GMLExporter.tripleTab}{GMLExporter.WIDTH_TOKEN} {w}\n'
            f'{GMLExporter.tripleTab}{GMLExporter.HEIGHT_TOKEN} {h}\n'
            f'{GMLExporter.tripleTab}{GMLExporter.DEPTH_TOKEN} {d}\n'
            f'{GMLExporter.tripleTab}type "rectangle"\n'
            f'{GMLExporter.tripleTab}width 0.12\n'
            f'{GMLExporter.tripleTab}fill "#ff0000"\n'
            f'{GMLExporter.tripleTab}outline "#000000"\n'
            
            f'{GMLExporter.doubleTab}{GMLExporter.END_TOKEN}\n'
        )
        return gml

    def _generateGraphStart(self, graphName: str = 'DefaultGraphName') -> str:

        gml: str = (
            f'{GMLExporter.GRAPH_TOKEN} {GMLExporter.START_TOKEN}\n'
            f'{GMLExporter.singleTab}directed 1\n'
            f'{GMLExporter.singleTab}version  1.0\n'
            f'{GMLExporter.singleTab}label "GML for {graphName}"\n'
            f'{GMLExporter.singleTab}comment "Generated by Pyut Version {PyutVersion.getPyUtVersion()}"\n'
        )

        return gml

    def _generateGraphTermination(self, gml: str) -> str:

        gml = f'{gml}{GMLExporter.END_TOKEN}'
        return gml

    def _generateUniqueEdges(self, umlObjects: OglClasses, gml: str) -> str:

        linkSet:  Set    = set()        # Concatenated str link ids;  e.g, 1-2

        for umlClass in umlObjects:
            if isinstance(umlClass, OglClass) or isinstance(umlClass, OglNote):
                oglObject: OglObject = cast(OglObject, umlClass)
                links = oglObject.getLinks()
                self.logger.info(f'links: {links}')
                for oglLink in links:
                    srcOglId:  int = oglLink.getSourceShape().GetID()
                    destOglId: int = oglLink.getDestinationShape().GetID()
                    linkIds:   str = f'{srcOglId}-{destOglId}'
                    if linkIds not in linkSet:
                        gml = self.__generateUniqueEdge(oglLink=oglLink, gml=gml)
                        linkSet.add(linkIds)

        return gml

    def __generateUniqueEdge(self, oglLink: OglLink, gml: str) -> str:

        srcOglId:  int = oglLink.getSourceShape().GetID()
        destOglId: int = oglLink.getDestinationShape().GetID()

        gml = (
            f'{gml}'
            f'{GMLExporter.singleTab}{GMLExporter.EDGE_TOKEN} {GMLExporter.START_TOKEN}\n'
            f'{GMLExporter.doubleTab}{GMLExporter.ID_TOKEN} {oglLink.GetID()}\n'
            f'{GMLExporter.doubleTab}{GMLExporter.SOURCE_ID_TOKEN} {srcOglId}\n'
            f'{GMLExporter.doubleTab}{GMLExporter.TARGET_ID_TOKEN} {destOglId}\n'
            f'{self.__generateEdgeGraphicsSection(oglLink=oglLink)}'
            f'{GMLExporter.singleTab}{GMLExporter.END_TOKEN}\n'
        )

        return gml

    def __generateEdgeGraphicsSection(self, oglLink: OglLink) -> str:

        srcAnchor:  AnchorPoint = oglLink.sourceAnchor
        destAnchor: AnchorPoint = oglLink.destinationAnchor

        controlPoints: ControlPoints = oglLink.GetControlPoints()

        edgeGml: str = (
            f'{GMLExporter.doubleTab}{GMLExporter.GRAPHICS_TOKEN} {GMLExporter.START_TOKEN}\n'
            f'{GMLExporter.tripleTab}type "line"\n'
            f'{GMLExporter.tripleTab}arrow "last"\n'
            f'{GMLExporter.tripleTab}{GMLExporter.LINE_DEFINITION_TOKEN} {GMLExporter.START_TOKEN}\n'
            f'{self.__generatePoint(srcAnchor)}'
            f'{self.__generatePoints(controlPoints)}'
            f'{self.__generatePoint(destAnchor)}'
            f'{GMLExporter.tripleTab}{GMLExporter.END_TOKEN}\n'
            f'{GMLExporter.doubleTab}{GMLExporter.END_TOKEN}\n'
        )

        return edgeGml

    def __generatePoints(self, points: ControlPoints) -> str:

        pointsGml: str = ''
        for point in points:
            pointsGml = (
                f'{pointsGml}{self.__generatePoint(point)}'
            )

        return pointsGml

    def __generatePoint(self, linePoint: LinePoint) -> str:

        position: Tuple[int, int] = linePoint.GetPosition()

        x:        int = position[0]
        y:        int = position[1]
        z:        int = 0
        pointGml: str = (
            f'{GMLExporter.quadrupleTab}{GMLExporter.POINT_DEFINITION_TOKEN} {GMLExporter.START_TOKEN}\n'
            f'{GMLExporter.quintupleTab}{GMLExporter.X_POSITION_TOKEN} {x}\n'
            f'{GMLExporter.quintupleTab}{GMLExporter.Y_POSITION_TOKEN} {y}\n'
            f'{GMLExporter.quintupleTab}{GMLExporter.Z_POSITION_TOKEN} {z}\n'
            f'{GMLExporter.quadrupleTab}{GMLExporter.END_TOKEN}\n'
        )

        return pointGml

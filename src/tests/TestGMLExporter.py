
from logging import Logger
from logging import getLogger

from typing import List

from unittest import TestSuite
from unittest import main as unitTestMain
from unittest.mock import MagicMock

from org.pyut.MiniOgl.AnchorPoint import AnchorPoint
from org.pyut.enums.LinkType import LinkType

from org.pyut.model.PyutClass import PyutClass
from org.pyut.model.PyutLink import PyutLink

from org.pyut.ogl.OglClass import OglClass
from org.pyut.ogl.OglLink import OglLink

from tests.TestBase import TestBase

from org.pyut.plugins.gml.GMLExporter import GMLExporter
from org.pyut.plugins.gml.GMLExporter import OglClasses


class TestGMLExporter(TestBase):

    NUMBER_OF_MOCK_CLASSES:   int = 2
    MOCK_CLASS_NAME_PREFIX:   str = 'ClassName_'
    MOCK_START_ID_NUMBER:     int = 42
    MOCK_ID_NUMBER_INCREMENT: int = 5
    MOCK_INIT_WIDTH:          float = 50.0
    MOCK_INIT_HEIGHT:         float = 50.0
    MOCK_INIT_POSITION_X:     float = 100.0
    MOCK_INIT_POSITION_Y:     float = 100.0
    MOCK_X_POSITION_INCREMENT: float = 75.0
    MOCK_Y_POSITION_INCREMENT: float = 100.0
    """
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestGMLExporter.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger:   Logger      = TestGMLExporter.clsLogger
        self.exporter: GMLExporter = GMLExporter()
        self._linkIDGenerator = self._generateLinkId()

    def tearDown(self):
        pass

    def testBasicCreation(self):

        umlObjects: OglClasses = self._generateMockNodes(TestGMLExporter.NUMBER_OF_MOCK_CLASSES)

        self._addMockLinks(umlObjects)

        self.exporter.prettyPrint = True
        self.exporter.translate(umlObjects)
        gml: str = self.exporter.gml

        self.assertIsNotNone(gml, 'Generate Something!!')
        self.logger.info(f'Generated GML:\n{gml}')
        self.exporter.write(f'UnitTest.gml')

    def _generateMockNodes(self, nbrToGenerate) -> OglClasses:

        umlObjects: OglClasses = []

        initId: int                 = TestGMLExporter.MOCK_START_ID_NUMBER
        mockX: float = TestGMLExporter.MOCK_INIT_POSITION_X
        mockY: float = TestGMLExporter.MOCK_INIT_POSITION_Y
        mockWidth:  float = TestGMLExporter.MOCK_INIT_WIDTH
        mockHeight: float = TestGMLExporter.MOCK_INIT_HEIGHT

        for x in range(nbrToGenerate):
            mockPyutClass: MagicMock = MagicMock(spec=PyutClass)
            mockPyutClass.getName.return_value = f'{TestGMLExporter.MOCK_CLASS_NAME_PREFIX}{x}'

            mockOglClass: MagicMock                 = MagicMock(spec=OglClass)
            mockOglClass.GetID.return_value         = initId
            mockOglClass.GetPosition.return_value   = (mockX, mockY)
            mockOglClass.GetSize.return_value       = (mockWidth, mockHeight)
            mockOglClass.getPyutObject.return_value = mockPyutClass
            umlObjects.append(mockOglClass)

            initId += TestGMLExporter.MOCK_ID_NUMBER_INCREMENT
            mockX  += TestGMLExporter.MOCK_X_POSITION_INCREMENT
            mockY  += TestGMLExporter.MOCK_Y_POSITION_INCREMENT

        return umlObjects

    def _addMockLinks(self, oglClasses: List[MagicMock]):

        currentIdx: int = 0
        while True:

            parentClass: MagicMock = oglClasses[currentIdx]
            childClass:  MagicMock = oglClasses[currentIdx + 1]

            self.logger.info(f'parentID: {parentClass.GetID()} childID: {childClass.GetID()}')
            self.__createMockLink(parentClass, childClass)
            currentIdx += 2
            if currentIdx >= len(oglClasses):
                break

    def __createMockLink(self, src: MagicMock, dest: MagicMock) -> MagicMock:
        """
        pyutLink = PyutLink("", linkType=linkType, source=src.getPyutObject(), destination=dst.getPyutObject())

        oglLink = oglLinkFactory.getOglLink(src, pyutLink, dst, linkType)

        src.addLink(oglLink)
        dst.addLink(oglLink)

        src.getPyutObject().addLink(pyutLink)

        Args:
            src:    Mock OglClass
            dest:   Mock OglClass

        Returns:
            Mocked OglLink
        """
        oglLink:  MagicMock = MagicMock(spec=OglLink)
        linkId = next(self._linkIDGenerator)
        oglLink.GetID.return_value = linkId

        mockSourceAnchor:      MagicMock = MagicMock(spec=AnchorPoint)
        mockDestinationAnchor: MagicMock = MagicMock(spec=AnchorPoint)

        mockSourceAnchor.GetPosition.return_value = (22, 44)
        mockDestinationAnchor.GetPosition.return_value = (1024, 450)

        oglLink.sourceAnchor.return_value      = mockSourceAnchor
        oglLink.destinationAnchor.return_value = mockDestinationAnchor

        oglLink.getSourceShape.return_value      = src
        oglLink.getDestinationShape.return_value = dest
        #
        # PyutLink object simple enough so create real one
        pyutLink: PyutLink = PyutLink("", linkType=LinkType.INHERITANCE, source=src.getPyutObject(), destination=dest.getPyutObject())

        src.getLinks.return_value  = [oglLink]
        dest.getLinks.return_value = [oglLink]

        mockPyutClass = src.getPyutObject()
        mockPyutClass.getLinks.return_value = [pyutLink]

        return oglLink

    def _generateLinkId(self):
        num: int = 1024
        while True:
            yield num
            num += 1


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestGMLExporter))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

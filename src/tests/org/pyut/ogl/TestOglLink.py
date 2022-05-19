
from typing import cast
from typing import Tuple

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain
from unittest.mock import MagicMock

from tests.TestBase import TestBase

from miniogl.ControlPoint import ControlPoint
from miniogl.LineShape import ControlPoints

from org.pyut.ogl.OglPosition import OglPosition

from org.pyut.preferences.PyutPreferences import PyutPreferences

from org.pyut.ogl.OglLink import OglLink


class TestOglLink(TestBase):
    """
    """
    MOCK_SOURCE_POSITION:       OglPosition = OglPosition(x=100, y=100)
    MOCK_DESTINATION_POSITION:  OglPosition = OglPosition(x=500, y=500)

    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestOglLink.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestOglLink.clsLogger

        PyutPreferences.determinePreferencesLocation()

    def tearDown(self):
        pass

    def testExceptionRaised(self):
        """
        https://ongspxm.github.io/blog/2016/11/assertraises-testing-for-errors-in-unittest/
        """
        from org.pyut.ogl.IllegalOperationException import IllegalOperationException

        mockSourceShape:      MagicMock = self._createMockShape(OglPosition(x=100, y=100), (10, 100))
        mockDestinationShape: MagicMock = self._createMockShape(OglPosition(x=500, y=500), (10, 100))

        mockPyutLink:         MagicMock = MagicMock()

        badOglLink: OglLink = OglLink(srcShape=mockSourceShape, pyutLink=mockPyutLink, dstShape=mockDestinationShape)

        badOglLink._srcShape = None
        self.assertRaises(IllegalOperationException, lambda: self._raiseException(badOglLink))

        badOglLink._srcShape = self._createMockShape(OglPosition(x=100, y=100), (10, 100))

        badOglLink._destShape = None
        self.assertRaises(IllegalOperationException, lambda: self._raiseException(badOglLink))

    def testBasicComputeLinkLength(self):

        mockSourceShape:      MagicMock = self._createMockShape(self.MOCK_SOURCE_POSITION, (10, 100))
        mockDestinationShape: MagicMock = self._createMockShape(self.MOCK_DESTINATION_POSITION, (10, 100))

        mockPyutLink:         MagicMock = MagicMock()

        oglLink: OglLink = OglLink(srcShape=mockSourceShape, pyutLink=mockPyutLink, dstShape=mockDestinationShape)
        actualLength:   int = oglLink._computeLinkLength(self.MOCK_SOURCE_POSITION, self.MOCK_DESTINATION_POSITION)
        expectedLength: int = 566
        self.assertEqual(expectedLength, actualLength, 'Did not match')

    def testFindClosestControlPoint(self):

        mockSourceShape:      MagicMock = self._createMockShape(self.MOCK_SOURCE_POSITION, (10, 100))
        mockDestinationShape: MagicMock = self._createMockShape(self.MOCK_DESTINATION_POSITION, (10, 100))

        mockPyutLink:         MagicMock = MagicMock()

        oglLink: OglLink = OglLink(srcShape=mockSourceShape, pyutLink=mockPyutLink, dstShape=mockDestinationShape)

        pointsToAdd: ControlPoints = self._createControlPoints()

        for cp in pointsToAdd:
            oglLink.AddControl(cp)

        self.logger.debug(f'{len(oglLink._controls)=}')

        expectedControlPoint: ControlPoint = pointsToAdd[0]
        closestPoint:         ControlPoint = oglLink._findClosestControlPoint(clickPoint=(100, 151))

        self.logger.debug(f'{closestPoint=}')

        self.assertEqual(expectedControlPoint, closestPoint, 'Found incorrect control point')

    def _createMockShape(self, position: OglPosition, size: Tuple[int, int]) -> MagicMock:

        mockShape: MagicMock = MagicMock()

        mockShape.GetPosition.return_value = (position.x, position.y)
        mockShape.GetSize.return_value     = size

        return mockShape

    def _raiseException(self, badOglLink: OglLink):
        badOglLink._computeDxDy(srcPosition=self.MOCK_SOURCE_POSITION, destPosition=self.MOCK_DESTINATION_POSITION)

    def _createControlPoints(self) -> ControlPoints:
        """
        Create a list of control points between the two mock shapes

        Returns:
        """
        cp1: ControlPoint = ControlPoint(x=100, y=200)
        cp2: ControlPoint = ControlPoint(x=200, y=200)
        cp3: ControlPoint = ControlPoint(x=300, y=300)
        cp4: ControlPoint = ControlPoint(x=400, y=400)

        controlPoints: ControlPoints = cast(ControlPoints, [cp1, cp2, cp3, cp4])

        return controlPoints


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestOglLink))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

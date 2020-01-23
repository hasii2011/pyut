
from typing import Tuple

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain
from unittest.mock import MagicMock

from tests.TestBase import TestBase

from org.pyut.ogl.OglLink import OglLink


class TestOglLink(TestBase):
    """
    You need to change the name of this class to Test`xxxx`
    Where `xxxx' is the name of the class that you want to test.

    See existing tests for more information.
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestOglLink.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestOglLink.clsLogger

    def tearDown(self):
        pass

    def testExceptionRaised(self):
        """
        https://ongspxm.github.io/blog/2016/11/assertraises-testing-for-errors-in-unittest/
        """
        from org.pyut.ogl.IllegalOperationException import IllegalOperationException

        mockSourceShape:      MagicMock = self._createMockShape((100, 100), (10, 100))
        mockDestinationShape: MagicMock = self._createMockShape((500, 500), (10, 100))

        mockPyutLink:         MagicMock = MagicMock()

        badOglLink: OglLink = OglLink(srcShape=mockSourceShape, pyutLink=mockPyutLink, dstShape=mockDestinationShape)
        # cream the source shape
        badOglLink._srcShape = None
        self.assertRaises(IllegalOperationException, lambda: self._raiseException(badOglLink))

        badOglLink._srcShape = self._createMockShape((100, 100), (10, 100))
        # cream the destination shape
        badOglLink._destShape = None
        self.assertRaises(IllegalOperationException, lambda: self._raiseException(badOglLink))

    def testBasicComputeLinkLength(self):
        mockSourceShape:      MagicMock = self._createMockShape((100, 100), (10, 100))
        mockDestinationShape: MagicMock = self._createMockShape((500, 500), (10, 100))

        mockPyutLink:         MagicMock = MagicMock()

        oglLink: OglLink = OglLink(srcShape=mockSourceShape, pyutLink=mockPyutLink, dstShape=mockDestinationShape)
        actualLength:   float = oglLink._computeLinkLength()
        expectedLength: float = 565.685
        self.assertAlmostEqual(expectedLength, actualLength, places=2)

    def _createMockShape(self, position: Tuple[float, float], size: Tuple[int, int]) -> MagicMock:

        mockShape:      MagicMock = MagicMock()
        mockShape.GetPosition.return_value = position
        mockShape.GetSize.return_value     = size

        return mockShape

    def _raiseException(self, badOglLink: OglLink):
        badOglLink._computeDxDy()


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestOglLink))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

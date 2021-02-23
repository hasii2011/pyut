
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain
from unittest.mock import Mock

from org.pyut.enums.AttachmentPoint import AttachmentPoint
from org.pyut.ogl.OglPosition import OglPosition
from org.pyut.preferences.PyutPreferences import PyutPreferences

from org.pyut.persistence.converters.MiniDomToOglV10 import MiniDomToOgl

from tests.TestBase import TestBase

EAST_WIDTH:  int = 100
EAST_HEIGHT: int = 100

WEST_WIDTH:  int = 250
WEST_HEIGHT: int = 126

NORTH_WIDTH:  int = 50
NORTH_HEIGHT: int = 200

SOUTH_WIDTH:  int = 400
SOUTH_HEIGHT: int = 200


class TestMiniDomToOglV10(TestBase):
    """
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestMiniDomToOglV10.clsLogger = getLogger(__name__)
        PyutPreferences.determinePreferencesLocation()

    def setUp(self):
        self.logger:   Logger       = TestMiniDomToOglV10.clsLogger
        self._converter: MiniDomToOgl = MiniDomToOgl()

    def tearDown(self):
        pass

    def testAttachEast(self):

        mockOglClass: Mock = Mock()

        mockOglClass.GetSize.return_value = (EAST_WIDTH, EAST_HEIGHT)
        attachPosition: OglPosition = self._converter._determineAttachmentPoint(attachmentPoint=AttachmentPoint.EAST, oglClass=mockOglClass)

        self.assertIsNotNone(attachPosition)
        self.assertEqual(EAST_WIDTH,       attachPosition.x, 'Incorrect east x position')
        self.assertEqual(EAST_HEIGHT // 2, attachPosition.y, 'Incorrect easy y position')

    def testAttachWest(self):

        mockOglClass: Mock = Mock()

        mockOglClass.GetSize.return_value = (WEST_WIDTH, WEST_HEIGHT)
        attachPosition: OglPosition = self._converter._determineAttachmentPoint(attachmentPoint=AttachmentPoint.WEST, oglClass=mockOglClass)

        self.assertIsNotNone(attachPosition)
        self.assertEqual(0,                attachPosition.x, 'Incorrect west x position')
        self.assertEqual(WEST_HEIGHT // 2, attachPosition.y, 'Incorrect west y position')

    def testAttachNorth(self):

        mockOglClass: Mock = Mock()

        mockOglClass.GetSize.return_value = (NORTH_WIDTH, NORTH_HEIGHT)
        attachPosition: OglPosition = self._converter._determineAttachmentPoint(attachmentPoint=AttachmentPoint.NORTH, oglClass=mockOglClass)

        self.assertIsNotNone(attachPosition)
        self.assertEqual(NORTH_WIDTH // 2, attachPosition.x, 'Incorrect north x position')
        self.assertEqual(0,                attachPosition.y, 'Incorrect north y position')

    def testAttachSouth(self):

        mockOglClass: Mock = Mock()

        mockOglClass.GetSize.return_value = (SOUTH_WIDTH, SOUTH_HEIGHT)
        attachPosition: OglPosition = self._converter._determineAttachmentPoint(attachmentPoint=AttachmentPoint.SOUTH, oglClass=mockOglClass)

        self.assertIsNotNone(attachPosition)
        self.assertEqual(SOUTH_WIDTH // 2, attachPosition.x, 'Incorrect south x position')
        self.assertEqual(SOUTH_HEIGHT,     attachPosition.y, 'Incorrect south y position')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestMiniDomToOglV10))

    return testSuite


if __name__ == '__main__':
    unitTestMain()


from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from org.pyut.preferences.PyutPreferences import PyutPreferences
from tests.TestBase import TestBase

from org.pyut.commands.CreateOglClassCommand import CreateOglClassCommand


class TestCreateOglClassCommand(TestBase):
    """
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestCreateOglClassCommand.clsLogger = getLogger(__name__)
        PyutPreferences.determinePreferencesLocation()

    def setUp(self):
        self.logger: Logger          = TestCreateOglClassCommand.clsLogger
        self.prefs:  PyutPreferences = PyutPreferences()

    def tearDown(self):
        pass

    def testSnapCoordinatesToGrid(self):

        gridInterval: int = self.prefs.backgroundGridInterval
        x: float = 335
        y: float = 142

        snappedX, snappedY = CreateOglClassCommand.snapCoordinatesToGrid(x=x, y=y, gridInterval=gridInterval)

        expectedX: float = 325
        expectedY: float = 125

        self.assertEqual(expectedX, snappedX, 'X coordinate not correctly snapped')
        self.assertEqual(expectedY, snappedY, 'Y coordinate not correctly snapped')

    def testSnapCoordinatesToGridNoSnapping(self):
        gridInterval: int = self.prefs.backgroundGridInterval
        x: float = 300
        y: float = 200

        snappedX, snappedY = CreateOglClassCommand.snapCoordinatesToGrid(x=x, y=y, gridInterval=gridInterval)

        expectedX: float = 300
        expectedY: float = 200

        self.assertEqual(expectedX, snappedX, 'X coordinate not correctly snapped')
        self.assertEqual(expectedY, snappedY, 'Y coordinate not correctly snapped')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestCreateOglClassCommand))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

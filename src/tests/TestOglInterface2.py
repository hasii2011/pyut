
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from org.pyut.MiniOgl.SelectAnchorPoint import SelectAnchorPoint

from org.pyut.preferences.PyutPreferences import PyutPreferences

from org.pyut.enums.AttachmentPoint import AttachmentPoint

from org.pyut.model.PyutInterface import PyutInterface

from org.pyut.ogl.OglInterface2 import OglInterface2

from tests.TestBase import TestBase


class TestOglInterface2(TestBase):
    """
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestOglInterface2.clsLogger = getLogger(__name__)

        PyutPreferences.determinePreferencesLocation()

    def setUp(self):
        self.logger: Logger = TestOglInterface2.clsLogger

        self._pyutInterface:    PyutInterface     = PyutInterface()
        self._destinationAnchor: SelectAnchorPoint = SelectAnchorPoint(250, 250, AttachmentPoint.NORTH)

    def tearDown(self):
        pass

    def testEqual(self):

        oglInterface: OglInterface2 = OglInterface2(pyutInterface=self._pyutInterface,  destinationAnchor=self._destinationAnchor)
        doppleGanger: OglInterface2 = oglInterface

        self.assertEqual(oglInterface, doppleGanger, 'Magic method __equ__ does not appear to be working anymore')

    def testHash(self):

        oglInterface: OglInterface2 = OglInterface2(pyutInterface=self._pyutInterface, destinationAnchor=self._destinationAnchor)

        currentHash: int = oglInterface.__hash__()
        hashAgain:   int = oglInterface.__hash__()

        self.assertEqual(currentHash, hashAgain, '__hash__ seems to be broken')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestOglInterface2))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

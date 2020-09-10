
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from wx import App

from org.pyut.MiniOgl.SelectAnchorPoint import SelectAnchorPoint
from org.pyut.PyutPreferences import PyutPreferences

from org.pyut.enums.AttachmentPoint import AttachmentPoint
from org.pyut.model.PyutClass import PyutClass

from org.pyut.model.PyutInterface import PyutInterface
from org.pyut.ogl.OglClass import OglClass
from org.pyut.ogl.OglInterface2 import OglInterface2

from org.pyut.persistence.converters.IDFactorySingleton import IDFactory

from tests.TestBase import TestBase


class TestIDFactory(TestBase):
    """
    You need to change the name of this class to Test`xxxx`
    Where `xxxx' is the name of the class that you want to test.

    See existing tests for more information.
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestIDFactory.clsLogger = getLogger(__name__)

        PyutPreferences.determinePreferencesLocation()

    def setUp(self):
        self.logger: Logger = TestIDFactory.clsLogger

        self.app: App = App()

        self._idFactory: IDFactory = IDFactory()

        self._pyutInterface:     PyutInterface     = PyutInterface()
        self._destinationAnchor: SelectAnchorPoint = SelectAnchorPoint(250, 250, AttachmentPoint.NORTH)

        self._pyutClass: PyutClass = PyutClass(name='UnitTestClass')

    def tearDown(self):
        del self.app

    def testCacheOglInterface(self):

        oglInterface: OglInterface2 = OglInterface2(pyutInterface=self._pyutInterface,  destinationAnchor=self._destinationAnchor)
        doppleGanger: OglInterface2 = oglInterface

        initialId: int = self._idFactory.getID(oglInterface)
        nextId:    int = self._idFactory.getID(doppleGanger)

        self.assertEqual(initialId, nextId, 'Should be the same')

    def testCacheOglClass(self):

        oglClass:     OglClass = OglClass(pyutClass=self._pyutClass)
        doppleGanger: OglClass = oglClass

        initialId: int = self._idFactory.getID(oglClass)
        nextId:    int = self._idFactory.getID(doppleGanger)

        self.assertEqual(initialId, nextId, 'Should be the same')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestIDFactory))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

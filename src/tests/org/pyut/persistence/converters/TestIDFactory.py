
from typing import cast
from typing import List
from typing import Set


from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from wx import App

from org.pyut.miniogl.SelectAnchorPoint import SelectAnchorPoint
from org.pyut.miniogl.AttachmentLocation import AttachmentLocation

from org.pyut.preferences.PyutPreferences import PyutPreferences

from pyutmodel.PyutActor import PyutActor
from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutField import PyutField

from pyutmodel.PyutInterface import PyutInterface
from pyutmodel.PyutLink import PyutLink
from pyutmodel.PyutMethod import PyutMethod
from pyutmodel.PyutNote import PyutNote
from pyutmodel.PyutUseCase import PyutUseCase

from org.pyut.ogl.OglClass import OglClass
from org.pyut.ogl.OglInterface2 import OglInterface2

from org.pyut.persistence.converters.IDFactory import IDFactory

from tests.TestBase import TestBase


class TestIDFactory(TestBase):
    """
    Create App for each test that needs it.  Tried using a class instance but the
    Travis CI build complains:

        wx._core.PyNoAppError: The wx.App object must be created first!

    Although, my local OS X test works ok.   Travis CI is running the Linux variant bionic.
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        PyutPreferences.determinePreferencesLocation()
        TestBase.setUpLogging()
        TestIDFactory.clsLogger = getLogger(__name__)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.logger: Logger = TestIDFactory.clsLogger
        self.app:    App    = App()

        self._idFactory: IDFactory = IDFactory()

        self._pyutInterface:     PyutInterface     = PyutInterface()
        self._destinationAnchor: SelectAnchorPoint = SelectAnchorPoint(250, 250, AttachmentLocation.NORTH)

        self._pyutClass: PyutClass = PyutClass(name='UnitTestClass')

    def tearDown(self):
        self.app.OnExit()
        del self.app

    def testCacheOglInterface(self):

        app: App = App()

        oglInterface: OglInterface2 = OglInterface2(pyutInterface=self._pyutInterface,  destinationAnchor=self._destinationAnchor)
        doppleGanger: OglInterface2 = oglInterface

        initialId: int = self._idFactory.getID(oglInterface)
        nextId:    int = self._idFactory.getID(doppleGanger)

        self.assertEqual(initialId, nextId, 'Should be the same')

        app.OnExit()
        del app

    def testCacheOglClass(self):

        app: App = App()

        oglClass:     OglClass = OglClass(pyutClass=self._pyutClass)
        doppleGanger: OglClass = oglClass

        initialId: int = self._idFactory.getID(oglClass)
        nextId:    int = self._idFactory.getID(doppleGanger)

        self.assertEqual(initialId, nextId, 'Should be the same')

        app.OnExit()
        del app

    def testBasicIDGeneration(self):
        idFactory: IDFactory = IDFactory()

        pyutClassId: int = idFactory.getID(PyutClass)
        pyutFieldId: int = idFactory.getID(PyutField)

        self.assertNotEqual(pyutClassId, pyutFieldId, 'ID generator is failing')

    def testBasicIDCaching(self):

        idFactory: IDFactory = IDFactory()

        pyutClassId:  int = idFactory.getID(PyutClass)
        pyutClassId2: int = idFactory.getID(PyutClass)
        self.assertEqual(pyutClassId, pyutClassId2, 'ID generator is not caching')

    def testLengthierGeneration(self):

        idFactory: IDFactory = IDFactory()

        longerClassList: List[type] = [
            PyutMethod,
            PyutUseCase,
            PyutActor,
            PyutNote,
            PyutLink
        ]
        knownIds: Set[int] = set()

        for cls in longerClassList:
            clsID: int = idFactory.getID(cls)
            if clsID in knownIds:
                self.fail('')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestIDFactory))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

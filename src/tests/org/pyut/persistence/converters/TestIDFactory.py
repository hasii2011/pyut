
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

from org.pyut.model.PyutActor import PyutActor
from org.pyut.model.PyutClass import PyutClass
from org.pyut.model.PyutField import PyutField

from org.pyut.model.PyutInterface import PyutInterface
from org.pyut.model.PyutLink import PyutLink
from org.pyut.model.PyutMethod import PyutMethod
from org.pyut.model.PyutNote import PyutNote
from org.pyut.model.PyutUseCase import PyutUseCase

from org.pyut.ogl.OglClass import OglClass
from org.pyut.ogl.OglInterface2 import OglInterface2

from org.pyut.persistence.converters.IDFactory import IDFactory

from tests.TestBase import TestBase


class TestIDFactory(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)
    clsApp:    App    = None

    @classmethod
    def setUpClass(cls):
        PyutPreferences.determinePreferencesLocation()
        TestBase.setUpLogging()
        TestIDFactory.clsLogger = getLogger(__name__)
        TestIDFactory.clsApp    = App()

    @classmethod
    def tearDownClass(cls):
        cls.clsApp.OnExit()
        del cls.clsApp

    def setUp(self):
        self.logger: Logger = TestIDFactory.clsLogger

        self.app: App = TestIDFactory.clsApp

        self._idFactory: IDFactory = IDFactory()

        self._pyutInterface:     PyutInterface     = PyutInterface()
        self._destinationAnchor: SelectAnchorPoint = SelectAnchorPoint(250, 250, AttachmentLocation.NORTH)

        self._pyutClass: PyutClass = PyutClass(name='UnitTestClass')

    def tearDown(self):
        pass

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


from unittest import TestSuite
from unittest import main as unitTestMain

from unittest.mock import MagicMock
from unittest.mock import PropertyMock

from ogl.OglObject import OglObject
from pyutmodel.PyutObject import PyutObject
from wx import Notebook

from pyut.preferences.PreferencesCommon import PreferencesCommon

from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame
from pyut.ui.umlframes.UmlFrame import UmlObjects
from pyut.ui.wxcommands.BaseWxCommand import BaseWxCommand
from pyut.uiv2.eventengine.EventEngine import EventEngine

from tests.TestBase import TestBase


def idGenerator():

    num: int = 1
    while True:
        yield num
        num += 1


class Foo:
    @property
    def bar(self):
        return 'foobar'


MAX_OGL_OBJECTS: int = 2


class TestBaseWxCommand(TestBase):
    """
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        PreferencesCommon.determinePreferencesLocation()

    def setUp(self):
        super().setUp()
        self._idGenerator = idGenerator()

    def tearDown(self):
        super().tearDown()

    def testFooBar(self):

        mockedFoo: MagicMock = MagicMock(spec=Foo)

        type(mockedFoo).bar = PropertyMock(return_value='ElGatoMalo')

        print(f"This should print the mocked value: '{mockedFoo.bar}'")

    def testIsSameObjectFail(self):

        # mockNoteBook:    MagicMock = MagicMock(spec=Notebook)
        # mockEventEngine: MagicMock = MagicMock(spec=EventEngine)

        baseWxCommand:   BaseWxCommand = BaseWxCommand(canUndo=True, name='UnitTestCommand')
        objectToRemove:  MagicMock     = self._createMockOglObject()
        potentialObject: MagicMock     = self._createMockOglObject()

        same: bool = baseWxCommand._isSameObject(objectToRemove=objectToRemove, potentialObject=potentialObject)
        self.assertFalse(same, 'These are not the same')

    def testName2(self):
        """Another test"""
        pass

    def _createMockUmlFrame(self) -> MagicMock:

        mockUmlFrame: MagicMock = MagicMock(spec=UmlDiagramsFrame)

        umlObjects: UmlObjects = UmlObjects([])

        for i in range(MAX_OGL_OBJECTS):
            mockOglObject: MagicMock = self._createMockOglObject()
            umlObjects.append(mockOglObject)

        return mockUmlFrame

    def _createMockOglObject(self) -> MagicMock:
        """
        Mock Ogl Objects need mock PyutObjects
        """
        mockOglObject:  MagicMock = MagicMock(spec=OglObject)
        mockPyutObject: MagicMock = self._createMockPyutObject()

        type(mockOglObject).pyutObject = PropertyMock(return_value=mockPyutObject)

        return mockOglObject

    def _createMockPyutObject(self) -> MagicMock:

        mockPyutObject: MagicMock = MagicMock(spec=PyutObject)

        # type(mockPyutClass).name = PropertyMock(return_value=className)
        newId: int = next(self._idGenerator)
        type(mockPyutObject).id = PropertyMock(return_value=newId)

        return mockPyutObject


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestBaseWxCommand))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

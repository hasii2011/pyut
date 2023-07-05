
from unittest import TestSuite
from unittest import main as unitTestMain

from wx import CommandEvent
from wx import PyEventBinder

from pyut.uiv2.eventengine.Events import EVENT_NEW_PROJECT
from pyut.uiv2.eventengine.Events import EVENT_UPDATE_TREE_ITEM_NAME
from pyut.uiv2.eventengine.Events import NewProjectEvent
from pyut.uiv2.eventengine.Events import EventType
from pyut.uiv2.eventengine.Events import UpdateTreeItemNameEvent

from hasiihelper.UnitTestBase import UnitTestBase


class TestEventType(UnitTestBase):
    """
    """
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testNewProjectEventType(self):
        smartEnum:          EventType    = EventType.NewProject
        actualCommandEvent: CommandEvent = smartEnum.NewProject.commandEvent    # type: ignore

        self.assertTrue(isinstance(actualCommandEvent, NewProjectEvent), 'The custom enumeration is broken - Bad Event')

    def testNewProjectEventBinder(self):

        smartEnum: EventType = EventType.NewProject

        expectedBinder: PyEventBinder = EVENT_NEW_PROJECT
        actualBinder:   PyEventBinder = smartEnum.pyEventBinder

        self.assertEqual(expectedBinder, actualBinder, 'The custom enumeration is busted - Bad Binder')

    def testUpdateTreeItemNameEvent(self):
        smartEnum:          EventType    = EventType.UpdateTreeItemName
        actualCommandEvent: CommandEvent = smartEnum.UpdateTreeItemName.commandEvent    # type: ignore

        self.assertTrue(isinstance(actualCommandEvent, UpdateTreeItemNameEvent), 'The custom enumeration is broken - Bad Event')

    def testUpdateTreeItemNameEventBinder(self):

        smartEnum: EventType = EventType.UpdateTreeItemName

        expectedBinder: PyEventBinder = EVENT_UPDATE_TREE_ITEM_NAME
        actualBinder:   PyEventBinder = smartEnum.pyEventBinder

        self.assertEqual(expectedBinder, actualBinder, 'The custom enumeration is busted - Bad Binder')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestEventType))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

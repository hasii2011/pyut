
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from wx import CommandEvent
from wx import PyEventBinder

from org.pyut.uiv2.eventengine.Events import EVENT_NEW_PROJECT
from org.pyut.uiv2.eventengine.Events import EVENT_UPDATE_TREE_ITEM_NAME
from org.pyut.uiv2.eventengine.Events import NewProjectEvent
from org.pyut.uiv2.eventengine.Events import UpdateTreeItemNameEvent
from tests.TestBase import TestBase

from org.pyut.uiv2.eventengine.Events import EventType


class TestEventType(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestEventType.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestEventType.clsLogger

    def tearDown(self):
        pass

    def testNewProjectEventType(self):
        smartEnum: EventType = EventType.NewProject

        expectedCommandEvent: CommandEvent = NewProjectEvent
        actualCommandEvent:   CommandEvent = smartEnum.NewProject.commandEvent

        self.assertEqual(expectedCommandEvent, actualCommandEvent, 'The custom enumeration is broken - Bad Event')

    def testNewProjectEventBinder(self):

        smartEnum: EventType = EventType.NewProject

        expectedBinder: PyEventBinder = EVENT_NEW_PROJECT
        actualBinder:   PyEventBinder = smartEnum.pyEventBinder

        self.assertEqual(expectedBinder, actualBinder, 'The custom enumeration is busted - Bad Binder')

    def testUpdateTreeItemNameEvent(self):
        smartEnum: EventType = EventType.UpdateTreeItemName

        expectedCommandEvent: CommandEvent = UpdateTreeItemNameEvent
        actualCommandEvent:   CommandEvent = smartEnum.UpdateTreeItemName.commandEvent

        self.assertEqual(expectedCommandEvent, actualCommandEvent, 'The custom enumeration is broken - Bad Event')

    def testUpdateTreeItemNameEventBinder(self):

        smartEnum: EventType = EventType.UpdateTreeItemName

        expectedBinder: PyEventBinder = EVENT_UPDATE_TREE_ITEM_NAME
        actualBinder:   PyEventBinder = smartEnum.pyEventBinder

        self.assertEqual(expectedBinder, actualBinder, 'The custom enumeration is busted - Bad Binder')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestEventType))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
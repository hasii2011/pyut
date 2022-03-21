from typing import cast

from sys import path as sysPath

from unittest import main as unitTestMain
from unittest import TestSuite

from logging import Logger
from logging import getLogger

from tests.TestBase import TestBase

from org.pyut.PyutUtils import PyutUtils

from org.pyut.history.HistoryManager import HistoryManager

from org.pyut.history.commands.CommandGroup import CommandGroup

from tests.resources.testclass.PrintCommand import PrintCommand


class TestHistory(TestBase):
    """
    @author P. Dabrowski <przemek.dabrowski@destroy-display.com> (15.11.2005)
    This is the unit test of the HistoryManager. It was tested on 21.11.2005,
    and it works perfectly. It's also a good example to see how it works.

    Made into a real unit test; Put in Python 3 logging -- 2019 HASII

    """
    COMMAND_GROUP3_STR: str = 'cg3'
    COMMAND_GROUP2_STR: str = 'cg2'
    COMMAND_GROUP1_STR: str = 'cg1'
    COMMAND_GROUP0_STR: str = 'cg0'

    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        """"""
        TestBase.setUpLogging()
        TestHistory.clsLogger = getLogger(__name__)
        PyutUtils.setBasePath(sysPath[0])

    def setUp(self):
        """"""
        self.logger: Logger = TestHistory.clsLogger
        self.historyManager = HistoryManager(None)

    def testInitialize(self):

        expectedGroupCount: int = 0
        actualGroupCount:   int = self.historyManager.groupCount
        self.assertEqual(expectedGroupCount, actualGroupCount, 'Group count not correctly initialized')

        expectedGroupUndoIndex: int = -1
        actualGroupUndoIndex:   int = self.historyManager.groupUndoIndex
        self.assertEqual(expectedGroupUndoIndex, actualGroupUndoIndex, 'Group undo index not correctly initialized')

        expectedGroupToExecute: CommandGroup = cast(CommandGroup, None)
        actualGroupToExecute:   CommandGroup = self.historyManager.groupToExecute
        self.assertEqual(expectedGroupToExecute, actualGroupToExecute, 'Group to execute not correctly initialized')

    def testBasic(self):
        # creating the command groups
        cg0 = CommandGroup(TestHistory.COMMAND_GROUP0_STR)
        cg1 = CommandGroup(TestHistory.COMMAND_GROUP1_STR)
        cg2 = CommandGroup(TestHistory.COMMAND_GROUP2_STR)
        cg3 = CommandGroup(TestHistory.COMMAND_GROUP3_STR)
        # commands for group 0
        pc0a = PrintCommand()
        pc0b = PrintCommand()
        # commands for group 1
        pc1a = PrintCommand()
        pc1b = PrintCommand()
        # commands for group 2
        pc2a = PrintCommand()
        pc2b = PrintCommand()
        # commands for group 3
        pc3a = PrintCommand()
        pc3b = PrintCommand()

        # set the messages of the commands
        pc0a.setMessage("pc0a")
        pc0b.setMessage("pc0b")
        pc1a.setMessage("pc1a")
        pc1b.setMessage("pc1b")
        pc2a.setMessage("pc2a")
        pc2b.setMessage("pc2b")
        pc3a.setMessage("pc3a")
        pc3b.setMessage("pc3b")

        # add the commands to the groups
        cg0.addCommand(pc0a)
        cg0.addCommand(pc0b)
        cg1.addCommand(pc1a)
        cg1.addCommand(pc1b)
        cg2.addCommand(pc2a)
        cg2.addCommand(pc2b)
        cg3.addCommand(pc3a)
        cg3.addCommand(pc3b)

        # add the groups to the history
        self.historyManager.addCommandGroup(cg0)
        self.historyManager.addCommandGroup(cg1)
        self.historyManager.addCommandGroup(cg2)

        self.assertEqual(3, self.historyManager.groupCount, 'Group count mismatch')

        self._checkUndoIndex(expectedGroupUndoIndex=2)
        self.historyManager.undo()

        self._checkUndoIndex(expectedGroupUndoIndex=1)
        self.historyManager.undo()

        self.historyManager.addCommandGroup(cg3)
        self._checkUndoIndex(expectedGroupUndoIndex=1)
        self.historyManager.undo()

        self._checkUndoIndex(expectedGroupUndoIndex=0)
        self.historyManager.undo()

        self.logger.info(f'Nothing left to undo: {self.historyManager.groupUndoIndex}')

    def _checkUndoIndex(self, expectedGroupUndoIndex: int):

        actualGroupUndoIndex: int = self.historyManager.groupUndoIndex
        self.logger.info(f'Group to undo index {actualGroupUndoIndex}')
        self.assertEqual(expectedGroupUndoIndex, actualGroupUndoIndex, 'Incorrect command group index')


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestHistory))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

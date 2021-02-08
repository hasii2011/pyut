
from logging import Logger
from logging import getLogger

from os import sep as osSep
from os import getcwd as osGetCwd

from typing import List

from unittest import TestSuite
from unittest import main as unitTestMain
from unittest.mock import MagicMock

from org.pyut.PyutUtils import PyutUtils

from org.pyut.commands.Command import Command
from org.pyut.commands.DeleteOglClassCommand import DeleteOglClassCommand
from org.pyut.commands.DelOglLinkCommand import DelOglLinkCommand
from org.pyut.commands.CommandGroup import CommandGroup

from org.pyut.history.HistoryManager import HistoryManager

from tests.TestBase import TestBase
from tests.TestBase import TEST_DIRECTORY


NUMBER_OF_COMMANDS_CREATED = 2


class TestCommandGroup(TestBase):
    """
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestCommandGroup.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger:   Logger       = TestCommandGroup.clsLogger
        self._cgGroup: CommandGroup = CommandGroup(comment='This is a test group')

        PyutUtils.setBasePath(newValue=osGetCwd())
        mockFrame: MagicMock = MagicMock()
        historyMgr: HistoryManager = HistoryManager(theFrame=mockFrame)
        self._cgGroup.setHistory(history=historyMgr)

        saveFile = open(f'{TEST_DIRECTORY}{osSep}testdata{osSep}DeleteShape-Link.txt', 'r')
        self._fileContent = saveFile.read()
        saveFile.close()

    def tearDown(self):
        pass

    def testDeserialize(self):
        self.logger.debug(f'{self._fileContent}')
        self._cgGroup.deserialize(self._fileContent)

        commands: List[Command] = self._cgGroup._commands
        self.assertTrue(len(commands) == NUMBER_OF_COMMANDS_CREATED, 'Not enough commands created')
        self.logger.info(f'{commands}')

        self.assertTrue(isinstance(commands[0], DeleteOglClassCommand), 'Incorrect command created')
        self.assertTrue(isinstance(commands[1], DelOglLinkCommand),  'Incorrect command created')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestCommandGroup))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

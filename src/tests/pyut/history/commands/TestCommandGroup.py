
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from os import getcwd as osGetCwd

from unittest import TestSuite
from unittest import main as unitTestMain
from unittest.mock import MagicMock

from pkg_resources import resource_filename

from pyut.PyutUtils import PyutUtils

from pyut.history.commands.Command import Command
from pyut.history.commands.DeleteOglClassCommand import DeleteOglClassCommand
from pyut.history.commands.DelOglLinkCommand import DelOglLinkCommand
from pyut.history.commands.CommandGroup import CommandGroup

from pyut.history.HistoryManager import HistoryManager

from tests.TestBase import TestBase


NUMBER_OF_COMMANDS_CREATED = 2


class TestCommandGroup(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)
    cast(Logger, None)

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

        fqFileName: str = resource_filename(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, 'DeleteShape-Link.txt')

        saveFile = open(fqFileName)
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

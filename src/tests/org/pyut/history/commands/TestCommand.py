
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pyut.preferences.PyutPreferences import PyutPreferences

from tests.TestBase import TestBase

from org.pyut.history.commands.Command import Command
from tests.resources.testclass.UnitTestCommand import UnitTestCommand


class TestCommand(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestCommand.clsLogger = getLogger(__name__)
        PyutPreferences.determinePreferencesLocation()

    def setUp(self):
        self.logger: Logger = TestCommand.clsLogger

    def tearDown(self):
        pass

    def testBaseCommandSerialize(self):

        baseCommand:       Command = Command()

        serializedCommand: str = baseCommand.serialize()
        expectedBase:      str = '<COMMAND_MODULE=org.pyut.history.commands.Command><COMMAND_CLASS=Command>'
        self.logger.debug(f"{serializedCommand}")

        self.assertEqual(expectedBase, serializedCommand, 'Looks like Command Serialization changed')

    def testUnitTestCommandSerialize(self):

        unitTestCommand: UnitTestCommand = UnitTestCommand()

        serializedCommand: str = unitTestCommand.serialize()
        expectedBase:      str = '<COMMAND_MODULE=tests.resources.testclass.UnitTestCommand><COMMAND_CLASS=UnitTestCommand>'
        self.logger.debug(f"{serializedCommand}")

        self.assertEqual(expectedBase, serializedCommand, 'Looks like Command Serialization changed')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestCommand))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

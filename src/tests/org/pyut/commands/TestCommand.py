
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from org.pyut.preferences.PyutPreferences import PyutPreferences

from tests.TestBase import TestBase

from org.pyut.commands.Command import Command
from tests.testclass.UnitTestCommand import UnitTestCommand


class TestCommand(TestBase):
    """
    You need to change the name of this class to Test`xxxx`
    Where `xxxx' is the name of the class that you want to test.

    See existing tests for more information.
    """
    clsLogger: Logger = None

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
        expectedBase:      str = '<COMMAND_MODULE=org.pyut.commands.Command><COMMAND_CLASS=Command>'
        self.logger.warning(f"{serializedCommand}")

        self.assertEqual(expectedBase, serializedCommand, 'Looks like Command Serialization changed')

    def testUnitTestCommandSerialize(self):

        unitTestCommand: UnitTestCommand = UnitTestCommand()

        serializedCommand: str = unitTestCommand.serialize()
        expectedBase:      str = '<COMMAND_MODULE=tests.testclass.UnitTestCommand><COMMAND_CLASS=UnitTestCommand>'
        self.logger.warning(f"{serializedCommand}")

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

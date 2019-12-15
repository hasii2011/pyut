
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from org.pyut.PyutVisibilityEnum import PyutVisibilityEnum
from tests.TestBase import TestBase

from org.pyut.plugins.IoPython import IoPython

from org.pyut.PyutField import PyutField


class TestIoPython(TestBase):
    """
    You need to change the name of this class to Test`xxxx`
    Where `xxxx' is the name of the class that you want to test.

    See existing tests for more information.
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestIoPython.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestIoPython.clsLogger
        self.plugin = IoPython(oglObjects=None, umlFrame=None)

    def tearDown(self):
        pass

    def testGetPublicFieldPythonCode(self):

        s: str = self.plugin.getFieldPythonCode(PyutField("publicMethod", "", None, PyutVisibilityEnum.PUBLIC))

        unExpectedValue: int = -1
        actualValue:     int = s.find('self.publicMethod')
        self.assertNotEqual(unExpectedValue, actualValue, f'Did not code generate public method correctly: `{s}`')

    def testGetPrivateFieldPythonCode(self):

        s: str = self.plugin.getFieldPythonCode(PyutField("privateMethod", "", None, PyutVisibilityEnum.PRIVATE))

        unExpectedValue: int = -1
        actualValue:     int = s.find('self.__privateMethod')
        self.assertNotEqual(unExpectedValue, actualValue, f'Did not code generate private method correctly: `{s}`')

    def testGetProtectedFieldPythonCode(self):

        s: str = self.plugin.getFieldPythonCode(PyutField("protectedMethod", "", None, PyutVisibilityEnum.PROTECTED))

        unExpectedValue: int = -1
        actualValue:     int = s.find('self._protectedMethod')
        self.assertNotEqual(unExpectedValue, actualValue, f'Did not code generate protected method correctly: `{s}`')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestIoPython))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

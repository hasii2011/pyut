
from logging import Logger
from logging import getLogger
from unittest import TestSuite

from unittest import main as unitTestMain

from tests.TestBase import TestBase

from org.pyut.model.PyutVisibilityEnum import PyutVisibilityEnum


class TestPyutVisibilityEnum(TestBase):
    """
    You need to change the name of this class to Test`xxxx`
    Where `xxxx' is the name of the class that you want to test.

    See existing tests for more information.
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestPyutVisibilityEnum.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestPyutVisibilityEnum.clsLogger

    def tearDown(self):
        pass

    def testBasicPrivate(self):
        pve: PyutVisibilityEnum = PyutVisibilityEnum.PRIVATE
        expectedValue: str = '-'
        actualValue:   str = str(pve.value)

        self.assertEqual(expectedValue, actualValue, 'String not returning correct value')

    def testBasicPublic(self):
        pve: PyutVisibilityEnum = PyutVisibilityEnum.PUBLIC
        expectedValue: str = '+'
        actualValue:   str = str(pve.value)

        self.assertEqual(expectedValue, actualValue, 'String not returning correct value')

    def testBasicProtected(self):
        pve: PyutVisibilityEnum = PyutVisibilityEnum.PROTECTED
        expectedValue: str = '#'
        actualValue:   str = str(pve.value)

        self.assertEqual(expectedValue, actualValue, 'String not returning correct value')

    def testReprPublic(self):

        pve: PyutVisibilityEnum = PyutVisibilityEnum.PUBLIC
        expectedValue: str = 'PUBLIC - +'
        actualValue:   str = pve.__repr__()

        self.assertEqual(expectedValue, actualValue, 'repr not returning correct value')

    def testReprPrivate(self):

        pve: PyutVisibilityEnum = PyutVisibilityEnum.PRIVATE
        expectedValue: str = 'PRIVATE - -'
        actualValue:   str = pve.__repr__()

        self.assertEqual(expectedValue, actualValue, 'repr not returning correct value')

    def testReprProtected(self):

        pve: PyutVisibilityEnum = PyutVisibilityEnum.PROTECTED
        expectedValue: str = 'PROTECTED - #'
        actualValue:   str = pve.__repr__()

        self.assertEqual(expectedValue, actualValue, 'repr not returning correct value')

    def testPublicCreation(self):

        pve:           PyutVisibilityEnum = PyutVisibilityEnum('+')
        expectedValue: PyutVisibilityEnum = PyutVisibilityEnum.PUBLIC
        actualValue:   PyutVisibilityEnum = pve

        self.assertEqual(expectedValue, actualValue, 'Creation not creating correct value')

    def testPrivateCreation(self):
        pve:           PyutVisibilityEnum = PyutVisibilityEnum('-')
        expectedValue: PyutVisibilityEnum = PyutVisibilityEnum.PRIVATE
        actualValue:   PyutVisibilityEnum = pve

        self.assertEqual(expectedValue, actualValue, 'Creation not creating correct value')

    def testProtectedCreation(self):
        pve:           PyutVisibilityEnum = PyutVisibilityEnum('#')
        expectedValue: PyutVisibilityEnum = PyutVisibilityEnum.PROTECTED
        actualValue:   PyutVisibilityEnum = pve

        self.assertEqual(expectedValue, actualValue, 'Creation not creating correct value')

    def testToEnumPublic(self):

        expectedValue: PyutVisibilityEnum = PyutVisibilityEnum.PUBLIC

        self._testEnum(expectedValue, 'PUBLIC', 'All upper case public failed')
        self._testEnum(expectedValue, 'public', 'All lower case public failed')
        self._testEnum(expectedValue, 'PuBlIc', 'Mixed case public failed')
        self._testEnum(expectedValue, 'B ogus', 'Unknown public value failed')

    def testToEnumPrivate(self):

        expectedValue: PyutVisibilityEnum = PyutVisibilityEnum.PRIVATE

        self._testEnum(expectedValue, 'PRIVATE', 'All upper case private failed')
        self._testEnum(expectedValue, 'private', 'All lower case private failed')
        self._testEnum(expectedValue, 'pRiVaTe', 'Mixed case private failed')

    def testToEnumProtected(self):

        expectedValue: PyutVisibilityEnum = PyutVisibilityEnum.PROTECTED

        self._testEnum(expectedValue, 'PROTECTED', 'All upper case protected failed')
        self._testEnum(expectedValue, 'protected', 'All lower case protected failed')
        self._testEnum(expectedValue, 'PROtected', 'Mixed case protected failed')

    def _testEnum(self, expectedValue: PyutVisibilityEnum, stringToTest: str, assertMessage: str):

        actualValue:   PyutVisibilityEnum = PyutVisibilityEnum.toEnum(stringToTest)

        self.assertEqual(expectedValue, actualValue, assertMessage)


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestPyutVisibilityEnum))

    return testSuite


if __name__ == '__main__':
    unitTestMain()


from typing import cast
from typing import List

from logging import Logger
from logging import getLogger

from unittest import TestSuite

from unittest import main as unitTestMain

from tests.TestBase import TestBase

from pyutmodel.PyutVisibilityEnum import PyutVisibilityEnum


class TestPyutVisibilityEnum(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

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

    def testToEnumPrivate(self):

        expectedValue: PyutVisibilityEnum = PyutVisibilityEnum.PRIVATE

        self._testEnum(expectedValue, 'PRIVATE', 'All upper case private failed')
        self._testEnum(expectedValue, 'private', 'All lower case private failed')
        self._testEnum(expectedValue, 'pRiVaTe', 'Mixed case private failed')

    def testToEnumProtected(self):

        expectedValue: PyutVisibilityEnum = PyutVisibilityEnum.PROTECTED

        self._testEnum(expectedValue, 'PROTECTED', 'All upper case protected failed')
        self._testEnum(expectedValue, 'protected', 'All lower case protected failed')
        # noinspection spelling
        self._testEnum(expectedValue, 'PROtected', 'Mixed case protected failed')

    def testGetValues(self):

        enumValueList: List[str] = PyutVisibilityEnum.values()
        self.logger.info(f'{enumValueList}')

        self.assertIn(member=PyutVisibilityEnum.PROTECTED.value, container=enumValueList, msg='Ugh. missing value')
        self.assertIn(member=PyutVisibilityEnum.PRIVATE.value,   container=enumValueList, msg='Ugh. missing value')
        self.assertIn(member=PyutVisibilityEnum.PUBLIC.value,    container=enumValueList, msg='Ugh. missing value')

    def testToEnumPublicName(self):

        val: PyutVisibilityEnum = PyutVisibilityEnum.toEnum('public')
        self.assertEqual(PyutVisibilityEnum.PUBLIC, val, 'Public to enum name fail')

    def testToEnumPrivateName(self):

        val: PyutVisibilityEnum = PyutVisibilityEnum.toEnum('private')
        self.assertEqual(PyutVisibilityEnum.PRIVATE, val, 'Private to enum fail')

    def testToEnumProtectedName(self):

        val: PyutVisibilityEnum = PyutVisibilityEnum.toEnum('protected')
        self.assertEqual(PyutVisibilityEnum.PROTECTED, val, 'protected to enum fail')

    def testToEnumPublicValue(self):

        val: PyutVisibilityEnum = PyutVisibilityEnum.toEnum('+')
        self.assertEqual(PyutVisibilityEnum.PUBLIC, val, 'Public to enum value fail')

    def testToEnumPrivateValue(self):

        val: PyutVisibilityEnum = PyutVisibilityEnum.toEnum('-')
        self.assertEqual(PyutVisibilityEnum.PRIVATE, val, 'Private to enum value fail')

    def testToEnumProtectedValue(self):

        val: PyutVisibilityEnum = PyutVisibilityEnum.toEnum('#')
        self.assertEqual(PyutVisibilityEnum.PROTECTED, val, 'Protected to enum value fail')

    def testEnumFail(self):

        self.assertRaises(AssertionError, lambda: self._enumFail())

    def _testEnum(self, expectedValue: PyutVisibilityEnum, stringToTest: str, assertMessage: str):

        actualValue:   PyutVisibilityEnum = PyutVisibilityEnum.toEnum(stringToTest)

        self.assertEqual(expectedValue, actualValue, assertMessage)

    # noinspection PyUnusedLocal
    def _enumFail(self):
        actualValue:   PyutVisibilityEnum = PyutVisibilityEnum.toEnum('B ogus')


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestPyutVisibilityEnum))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

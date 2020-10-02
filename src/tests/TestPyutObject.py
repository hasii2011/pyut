
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from tests.TestBase import TestBase

from org.pyut.model.PyutObject import PyutObject


class TestPyutObject(TestBase):
    """

    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestPyutObject.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestPyutObject.clsLogger

    def tearDown(self):
        pass

    def testNoName(self):
        pyutObject: PyutObject = PyutObject()

        expectedSize: int = 0
        actualSize:   int = pyutObject.getName().__len__()

        self.assertEqual(expectedSize, actualSize, 'Name should be empty')

    def testNoNameValue(self):

        pyutObject: PyutObject = PyutObject()

        actualName:     str = pyutObject.getName()

        self.assertIsNotNone(actualName, 'Should have some value')

        expectedLength: int = 0
        actualLength:   int = len(actualName)

        self.assertEqual(expectedLength, actualLength, 'Should be empty')

    def testProvidedName(self):

        providedName: str = 'El Gato Malo'
        nameLength:   int = len(providedName)

        pyutObject: PyutObject = PyutObject(providedName)

        expectedLength: int = nameLength
        actualLength:   int = len(pyutObject.getName())

        self.assertEqual(expectedLength, actualLength, 'Our name appears to have NOT been used')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestPyutObject))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

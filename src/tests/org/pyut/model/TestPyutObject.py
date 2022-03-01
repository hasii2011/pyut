
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from tests.TestBase import TestBase

from org.pyut.model.PyutObject import PyutObject


class \
        TestPyutObject(TestBase):
    """

    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestPyutObject.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestPyutObject.clsLogger
        PyutObject.nextId = 0

    def tearDown(self):
        pass

    def testNoName(self):
        pyutObject: PyutObject = PyutObject()

        expectedSize: int = 0
        actualSize:   int = pyutObject.name.__len__()

        self.assertEqual(expectedSize, actualSize, 'Name should be empty')

    def testNoNameValue(self):

        pyutObject: PyutObject = PyutObject()

        actualName:     str = pyutObject.name

        self.assertIsNotNone(actualName, 'Should have some value')

        expectedLength: int = 0
        actualLength:   int = len(actualName)

        self.assertEqual(expectedLength, actualLength, 'Should be empty')

    def testProvidedName(self):

        providedName: str = 'El Gato Malo'
        nameLength:   int = len(providedName)

        pyutObject: PyutObject = PyutObject(providedName)

        expectedLength: int = nameLength
        actualLength:   int = len(pyutObject.name)

        self.assertEqual(expectedLength, actualLength, 'Our name appears to have NOT been used')

    def testInitialId(self):
        self.assertEqual(0, PyutObject.nextId, 'Not correctly initialized')

    def testHowIdsIncrement(self):

        pyutObject1: PyutObject = PyutObject(name='pyutObject1')
        self.assertEqual(1, PyutObject.nextId, f'Not correctly incremented {pyutObject1.name}')

        pyutObject2: PyutObject = PyutObject(name='pyutObject2')
        self.assertEqual(2, PyutObject.nextId, f'Not correctly incremented {pyutObject2.name}')

        pyutObject3: PyutObject = PyutObject(name='pyutObject3')
        self.assertEqual(3, PyutObject.nextId, f'Not correctly incremented {pyutObject3.name}')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestPyutObject))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

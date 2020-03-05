
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

        expectedNotSize: int = 0
        actualSize:      int = pyutObject.getName().__len__()

        self.logger.info(f'Generated PyutObject name: {pyutObject.getName()}')

        self.assertNotEqual(expectedNotSize, actualSize, 'Name should not be empty')

    def testNoNameValue(self):

        pyutObject: PyutObject = PyutObject()

        actualName:   str = pyutObject.getName()
        expectedName: str = f'{PyutObject.BASE_OBJECT_NAME}{pyutObject.nextId - 1:05}'

        self.logger.info(f'Generated PyutObject name: {pyutObject.getName()}')

        self.assertEqual(expectedName, actualName, 'Name generation algorithm changed')

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

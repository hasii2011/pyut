
from logging import Logger
from logging import getLogger

from pkg_resources import resource_filename

from unittest import TestSuite
from unittest import main as unitTestMain

from tests.TestBase import TestBase

from org.pyut.plugins.FieldExtractor import FieldExtractor


class TestFieldExtractor(TestBase):
    """
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestFieldExtractor.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestFieldExtractor.clsLogger
        self._testFileName: str = resource_filename(TestBase.RESOURCES_TEST_CLASSES_PACKAGE_NAME, 'Opie.py')

    def tearDown(self):
        pass

    def testBasicFieldFind(self):

        fe: FieldExtractor = FieldExtractor(filename=self._testFileName)

        fields = fe.getFields(className='Opie')

        expectedFieldCount: int = 3
        actualFieldCount:   int = len(fields)
        self.assertEqual(expectedFieldCount, actualFieldCount, 'Field counts do not match')
        self.logger.info(f'Found {len(fields)} fields')

        for name, init in fields.items():
            self.logger.info(f'{name} = {init}')

    def testRemoveExtraneousNameParts(self):

        fe: FieldExtractor = FieldExtractor(filename=self._testFileName)

        nameToClean: str = '.([,-*/%'
        cleanedName: str = fe._removeExtraneousNameParts(nameToClean=nameToClean)

        expectedLength: int = 0
        actualLength:   int = len(cleanedName)

        self.assertEqual(expectedLength, actualLength, 'Name was not cleaned')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestFieldExtractor))

    return testSuite


if __name__ == '__main__':
    unitTestMain()


from typing import List

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from copy import deepcopy

from tests.TestBase import TestBase

from org.pyut.model.PyutField import PyutField
from org.pyut.model.PyutVisibilityEnum import PyutVisibilityEnum


class TestPyutField(TestBase):

    clsLogger: Logger = None

    fieldNames:        List[str] = ['field1', 'field2', 'field3']
    fieldTypes:        List[str] = ['int', 'bool', 'float']
    fieldValues:       List[str] = ['22', 'False', '62.34324']
    fieldVisibilities: List[PyutVisibilityEnum] = [PyutVisibilityEnum.PRIVATE,
                                                   PyutVisibilityEnum.PUBLIC,
                                                   PyutVisibilityEnum.PROTECTED]

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestPyutField.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestPyutField.clsLogger

    def testDeepCopyList(self):

        originalFields: List[PyutField] = []
        for x in range(len(TestPyutField.fieldNames)):
            field: PyutField = PyutField(name=TestPyutField.fieldNames[x],
                                         theFieldType=TestPyutField.fieldTypes[x],
                                         defaultValue=TestPyutField.fieldValues[x],
                                         visibility=TestPyutField.fieldVisibilities[x]
                                         )
            originalFields.append(field)
        self.logger.info(f'originalFields: {originalFields}')

        doppleGangers: List[PyutField] = deepcopy(originalFields)
        self.logger.info(f'doppleGangers: {doppleGangers}')


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestPyutField))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

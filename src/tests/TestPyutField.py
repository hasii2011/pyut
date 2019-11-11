
from typing import List

from logging import Logger
from logging import getLogger

from copy import deepcopy

from unittest import main as unitTestMain

from org.pyut.PyutField import PyutField
from tests.TestBase import TestBase


class TestPyutField(TestBase):

    clsLogger: Logger = None

    fieldNames:        List[str] = ['field1', 'field2', 'field3']
    fieldTypes:        List[str] = ['int', 'bool', 'float']
    fieldValues:       List[str] = ['22', 'False', '62.34324']
    fieldVisibilities: List[str] = ['-', '+', '#']
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
                                         theParamType=TestPyutField.fieldTypes[x],
                                         defaultValue=TestPyutField.fieldValues[x],
                                         visibility=TestPyutField.fieldVisibilities[x]
                                         )
            originalFields.append(field)
        self.logger.info(f'originalFields: {originalFields}')

        doppleGangers: List[PyutField] = deepcopy(originalFields)
        self.logger.info(f'doppleGangers: {doppleGangers}')


if __name__ == '__main__':
    unitTestMain()

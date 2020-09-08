
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from org.pyut.model.PyutClass import PyutClass
from org.pyut.model.PyutField import PyutField
from org.pyut.model.PyutType import PyutType
from org.pyut.model.PyutVisibilityEnum import PyutVisibilityEnum

from org.pyut.plugins.iopythonsupport.PyutPythonVisitor import PyutPythonVisitor
from org.pyut.plugins.iopythonsupport.ReverseEngineerPython2 import ReverseEngineerPython2

from tests.TestBase import TestBase


class TestReverseEngineerPython2(TestBase):
    """
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestReverseEngineerPython2.clsLogger = getLogger(__name__)

    def setUp(self):

        self.logger:          Logger                 = TestReverseEngineerPython2.clsLogger
        self.reverseEngineer: ReverseEngineerPython2 = ReverseEngineerPython2()

    def tearDown(self):
        pass

    def testParseFieldToPyutMinimal(self):

        fieldDataMinimal: str = 'minVal=0'

        pyutField: PyutField = self.reverseEngineer._parseFieldToPyut(fieldDataMinimal)

        self.assertEqual('minVal', pyutField.name, 'No match on name')
        self.assertEqual('0', pyutField.defaultValue, 'No match on default value')

    def testParseFieldToPyutComplex(self):

        fieldDataMinimal: str       = 'minVal:int = 0'
        pyutField:        PyutField = self.reverseEngineer._parseFieldToPyut(fieldDataMinimal)

        expectedFieldVisibility: PyutVisibilityEnum = PyutVisibilityEnum.PUBLIC

        expectedFieldType: PyutType = PyutType('int')
        actualFieldType:   PyutType = pyutField.type

        self.assertEqual('minVal', pyutField.name, 'No match on name')
        self.assertEqual(expectedFieldVisibility, pyutField.visibility, 'Did not parse visibility correctly')
        self.assertEqual(expectedFieldType, actualFieldType, 'Did not parse field type correctly')
        self.assertEqual('0', pyutField.defaultValue, 'Did not parse field default value correctly')

    def testParseFieldMinimalEOLComment(self):

        fieldDataRegressionOne: str = "inc = None  # 'the first outgoing incident half-edge'"

        pyutField: PyutField = self.reverseEngineer._parseFieldToPyut(fieldDataRegressionOne)

        self.assertEqual('inc', pyutField.name, 'No match on name')
        self.assertEqual('None', pyutField.defaultValue, 'No match on default value')

    def testParseFieldToPyutComplexEOLComplex(self):

        fieldDataMinimal: str       = "minVal:int = 0   # I am end of line comment"
        pyutField:        PyutField = self.reverseEngineer._parseFieldToPyut(fieldDataMinimal)

        expectedFieldVisibility: PyutVisibilityEnum = PyutVisibilityEnum.PUBLIC

        expectedFieldType: PyutType = PyutType('int')
        actualFieldType:   PyutType = pyutField.type

        self.assertEqual('minVal', pyutField.name, 'No match on name')
        self.assertEqual(expectedFieldVisibility, pyutField.visibility, 'Did not parse visibility correctly')
        self.assertEqual(expectedFieldType, actualFieldType, 'Did not parse field type correctly')
        self.assertEqual('0', pyutField.defaultValue, 'Did not parse field default value correctly')

    def testCreateDataClassPropertiesAsFields(self):

        sampleDataClassProperties: PyutPythonVisitor.DataClassProperties = [
            ('DataTestClass', 'w="A String"'),
            ('DataTestClass', 'x:float=0.0'),
            ('DataTestClass', 'y:float=42.0'),
            ('DataTestClass', 'z:int')
        ]
        pyutClass: PyutClass = PyutClass(name='DataTestClass')

        self.reverseEngineer._createDataClassPropertiesAsFields(pyutClass=pyutClass, dataClassProperties=sampleDataClassProperties)


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestReverseEngineerPython2))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

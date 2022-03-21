
from typing import cast
from typing import Dict
from typing import List

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from unittest.mock import Mock
from unittest.mock import PropertyMock

from org.pyut.model.PyutClass import PyutClass
from org.pyut.model.PyutField import PyutField
from org.pyut.model.DisplayMethodParameters import DisplayMethodParameters
from org.pyut.model.PyutMethod import PyutMethod
from org.pyut.model.PyutParameter import PyutParameter
from org.pyut.model.PyutType import PyutType
from org.pyut.model.PyutVisibilityEnum import PyutVisibilityEnum

from org.pyut.plugins.iopythonsupport.PyutPythonVisitor import DataClassProperties
from org.pyut.plugins.iopythonsupport.PyutPythonVisitor import DataClassProperty
from org.pyut.plugins.iopythonsupport.PyutPythonVisitor import MultiParameterNames

from org.pyut.plugins.iopythonsupport.PyutPythonVisitor import PyutPythonVisitor
from org.pyut.plugins.iopythonsupport.ReverseEngineerPython2 import ReverseEngineerPython2

from tests.TestBase import TestBase


class TestReverseEngineerPython2(TestBase):
    """
    """
    PROPERTY_NAMES: List[str] = ['fontSize', 'verticalGap']

    clsLogger: Logger = cast(Logger, None)

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

        sampleDataClassProperties: DataClassProperties = [
            DataClassProperty(('DataTestClass', 'w="A String"')),
            DataClassProperty(('DataTestClass', 'x:float=0.0')),
            DataClassProperty(('DataTestClass', 'y:float=42.0')),
            DataClassProperty(('DataTestClass', 'z:int'))
        ]
        pyutClass: PyutClass = PyutClass(name='DataTestClass')

        self.reverseEngineer._createDataClassPropertiesAsFields(pyutClass=pyutClass, dataClassProperties=sampleDataClassProperties)

    def testCreatePropertiesNormal(self):

        PyutMethod.displayParameters = DisplayMethodParameters.WITH_PARAMETERS

        propName:     str       = 'fontSize'
        setterParams: List[str] = ['newSize:int']

        setter, getter = self.reverseEngineer._createProperties(propName=propName, setterParams=setterParams)
        PyutMethod.setStringMode(DisplayMethodParameters.WITH_PARAMETERS)

        self.logger.info(f'setter={setter.__str__()} getter={getter.__str__()}')

        self.assertEqual('+fontSize(newSize: int): ', setter.getString(), 'Incorrect setter generated')
        self.assertEqual('+fontSize(): int', getter.getString(), 'Incorrect getter generated')

    def testCreatePropertiesReadOnly(self):

        propName:      str = 'fontSize'
        setterParams: List[str] = []

        setter, getter = self.reverseEngineer._createProperties(propName=propName, setterParams=setterParams)
        PyutMethod.setStringMode(DisplayMethodParameters.WITH_PARAMETERS)

        self.assertIsNone(setter)
        self.assertIsNotNone(getter)

    def testGeneratePropertiesAsMethodsNormaCorrectCount(self):

        pyutClass: PyutClass = self._generateNormalMethods()

        pyutMethods:         List[PyutMethod] = pyutClass.methods
        expectedMethodCount: int = 4
        actualMethodCount:   int = len(pyutMethods)

        self.assertEqual(expectedMethodCount, actualMethodCount, 'Generated incorrect # of methods')

    def testGeneratePropertiesAsMethodsNormalDesignatedAsProperties(self):

        pyutClass: PyutClass = self._generateNormalMethods()

        pyutMethods: List[PyutMethod] = pyutClass.methods
        for pyutMethod in pyutMethods:
            self.assertTrue(pyutMethod.isProperty, 'Not correctly identified')

    def testGeneratePropertiesAsMethodsReadOnlyPropertiesCorrectCount(self):

        pyutClass: PyutClass = self._generateReadOnlyMethods()

        pyutMethods:         List[PyutMethod] = pyutClass.methods
        expectedMethodCount: int              = 3
        actualMethodCount:   int              = len(pyutMethods)

        self.assertEqual(expectedMethodCount, actualMethodCount, 'Generated incorrect # of methods')

    def testGeneratePropertiesAsMethodsReadOnlyPropertiesCorrectPyutMethods(self):

        pyutClass:   PyutClass = self._generateReadOnlyMethods()
        pyutMethods: List[PyutMethod] = pyutClass.methods

        for pyutMethod in pyutMethods:
            generatedMethodName: str = pyutMethod.name
            self.assertIn(member=generatedMethodName, container=TestReverseEngineerPython2.PROPERTY_NAMES)

    def testParametersComplexTypedAndDefaultValue(self):

        # multiParameterNames: MultiParameterNames = MultiParameterNames('param1,param2:float,param3=57.0,param4:float=42.0')
        multiParameterNames: MultiParameterNames = MultiParameterNames('param4:float=42.0')
        pyutParameters: List[PyutParameter] = self.reverseEngineer._generateParameters(multiParameterNames=multiParameterNames)
        self.logger.debug(f'{pyutParameters=}')

        pyutParameter: PyutParameter = pyutParameters[0]
        self.assertEqual('param4', pyutParameter.name, 'Name is incorrect')
        self.assertEqual(PyutType(value='float'), pyutParameter.type, 'We parsed the type incorrectly')
        self.assertEqual('42.0', pyutParameter.defaultValue, 'Did not default value correctly')

    def testGenerateParametersSimple(self):
        multiParameterNames: MultiParameterNames = MultiParameterNames('param')
        pyutParameters:      List[PyutParameter]     = self.reverseEngineer._generateParameters(multiParameterNames=multiParameterNames)

        pyutParameter: PyutParameter = pyutParameters[0]

        self.assertEqual('param', pyutParameter.name, 'Name is incorrect')
        self.assertIsNone(pyutParameter.defaultValue, 'There should be no default value')
        self.assertEqual(PyutType(''), pyutParameter.type, 'Should not have a type')

    def testGenerateParametersSimpleDefaultValue(self):
        multiParameterNames: MultiParameterNames = MultiParameterNames('param3=57.0')
        pyutParameters:      List[PyutParameter]     = self.reverseEngineer._generateParameters(multiParameterNames=multiParameterNames)

        pyutParameter: PyutParameter = pyutParameters[0]

        self.assertEqual('param3', pyutParameter.name, 'Name is incorrect')
        self.assertEqual('57.0', pyutParameter.defaultValue)
        self.assertEqual(PyutType(''), pyutParameter.type, 'Should not have a type')

    def testGenerateParametersTypedParameter(self):
        typedParameterName: MultiParameterNames = MultiParameterNames('param2:float')
        pyutParameters:      List[PyutParameter]     = self.reverseEngineer._generateParameters(multiParameterNames=typedParameterName)

        pyutParameter: PyutParameter = pyutParameters[0]
        self.assertEqual('param2', pyutParameter.name, 'Name is incorrect')

        expectedType: PyutType = PyutType(value='float')
        actualType:   PyutType = pyutParameter.type

        self.assertEqual(expectedType, actualType, 'Type not set correctly')

        self.assertIsNone(pyutParameter.defaultValue, 'There should be no default value')

    def _generateReadOnlyMethods(self):
        # Note the missing setter for fontSize
        getterProperties: Dict[str, List] = {'fontSize': [''], 'verticalGap': ['']}
        setterProperties: Dict[str, List] = {'verticalGap': ['newValue']}
        pyutClass:        PyutClass       = PyutClass(name='NormalPropertiesClass')

        self.__setMockVisitorPropertyNames()

        pyutClass = self.reverseEngineer._generatePropertiesAsMethods(pyutClass=pyutClass,
                                                                      getterProperties=getterProperties,
                                                                      setterProperties=setterProperties
                                                                      )
        return pyutClass

    def _generateNormalMethods(self):

        getterProperties: Dict[str, List] = {'fontSize': [''], 'verticalGap': ['']}
        setterProperties: Dict[str, List] = {'fontSize': ['newSize:int'], 'verticalGap': ['newValue']}

        pyutClass:   PyutClass = PyutClass(name='NormalPropertiesClass')
        self.__setMockVisitorPropertyNames()

        pyutClass = self.reverseEngineer._generatePropertiesAsMethods(pyutClass=pyutClass,
                                                                      getterProperties=getterProperties,
                                                                      setterProperties=setterProperties
                                                                      )
        return pyutClass

    def __setMockVisitorPropertyNames(self):
        mockVisitor: Mock = Mock(spec=PyutPythonVisitor)
        type(mockVisitor).propertyNames = PropertyMock(return_value=TestReverseEngineerPython2.PROPERTY_NAMES)
        self.reverseEngineer.visitor = mockVisitor


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestReverseEngineerPython2))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

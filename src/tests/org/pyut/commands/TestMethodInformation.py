
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from org.pyut.model.PyutClassCommon import PyutClassCommon
from org.pyut.model.PyutMethod import PyutMethod
from org.pyut.model.PyutModifier import PyutModifier
from org.pyut.model.PyutParam import PyutParam
from org.pyut.model.PyutType import PyutType
from org.pyut.model.PyutVisibilityEnum import PyutVisibilityEnum
from org.pyut.preferences.PyutPreferences import PyutPreferences

from tests.TestBase import TestBase

from org.pyut.commands.MethodInformation import MethodInformation


class TestMethodInformation(TestBase):
    """
    """
    clsLogger:        Logger = None
    methodParamNumber: int = 1
    methodTypeNumber: int = 1

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestMethodInformation.clsLogger = getLogger(__name__)
        PyutPreferences.determinePreferencesLocation()

    def setUp(self):
        self.logger: Logger = TestMethodInformation.clsLogger

    def tearDown(self):
        pass

    def testSerialize(self):

        pyutClassCommon: PyutClassCommon = PyutClassCommon()
        pyutClassCommon.description = 'I am a test class'

        floatMethod: PyutMethod = self._createTestMethod('floatMethod', PyutVisibilityEnum.PRIVATE,   PyutType('float'))
        finalMethod: PyutMethod = self._createTestMethod('finalMethod', PyutVisibilityEnum.PROTECTED, PyutType('int'))

        pyutModifier: PyutModifier = PyutModifier(modifierTypeName='final')
        finalMethod.addModifier(newModifier=pyutModifier)

        pyutClassCommon.methods = [floatMethod, finalMethod]
        serializedMethods: str = MethodInformation.serialize(pyutClassCommon)

        self.assertNotEqual(0, len(serializedMethods))

        self.logger.warning(f'{serializedMethods=}')

    def testDeserialize(self):
        """Another test"""
        pass

    def _createTestMethod(self, name: str, visibility: PyutVisibilityEnum, returnType: PyutType) -> PyutMethod:

        pyutMethod: PyutMethod = PyutMethod()

        pyutMethod.name       = name
        pyutMethod.visibility = visibility
        pyutMethod.returnType = returnType

        pyutParam: PyutParam = PyutParam(name=f'param{self.methodParamNumber}',
                                         theParameterType=PyutType(f'Type{self.methodTypeNumber}'),
                                         defaultValue='')

        pyutMethod.addParam(pyutParam)

        TestMethodInformation.methodParamNumber += 1
        TestMethodInformation.methodTypeNumber  += 1

        return pyutMethod


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestMethodInformation))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

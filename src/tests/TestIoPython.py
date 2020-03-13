
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from org.pyut.model.PyutType import PyutType
from tests.TestBase import TestBase

from org.pyut.model.PyutField import PyutField
from org.pyut.model.PyutMethod import PyutMethod
from org.pyut.model.PyutVisibilityEnum import PyutVisibilityEnum

from org.pyut.plugins.IoPython import IoPython
from org.pyut.plugins.iopythonsupport.PyutToPython import PyutToPython

from org.pyut.ui.UmlFrame import UmlFrame


class TestIoPython(TestBase):
    """
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestIoPython.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger   = TestIoPython.clsLogger
        self.plugin: IoPython = IoPython(oglObjects=None, umlFrame=cast(UmlFrame, None))

        self.pyutToPython: PyutToPython = PyutToPython()

    def tearDown(self):
        pass

    def testGetPublicFieldPythonCode(self):

        s: str = self.pyutToPython.generateFieldPythonCode(PyutField("publicField", "", None, PyutVisibilityEnum.PUBLIC))

        unExpectedValue: int = -1
        actualValue:     int = s.find('self.publicField')
        self.assertNotEqual(unExpectedValue, actualValue, f'Did not code generate public method correctly: `{s}`')

    def testGetPrivateFieldPythonCode(self):

        s: str = self.pyutToPython.generateFieldPythonCode(PyutField("privateField", "", None, PyutVisibilityEnum.PRIVATE))

        unExpectedValue: int = -1
        actualValue:     int = s.find('self.__privateField')
        self.assertNotEqual(unExpectedValue, actualValue, f'Did not code generate private method correctly: `{s}`')

    def testGetProtectedFieldPythonCode(self):

        s: str = self.pyutToPython.generateFieldPythonCode(PyutField("protectedField", "", None, PyutVisibilityEnum.PROTECTED))

        unExpectedValue: int = -1
        actualValue:     int = s.find('self._protectedField')
        self.assertNotEqual(unExpectedValue, actualValue, f'Did not code generate protected field correctly: `{s}`')

    def testIndent(self):

        lst1: List[str] = ['a', '   b', 'c']
        expectedIndent: List[str] = ['    a', '       b', '    c']
        actualIndent: List[str] = self.pyutToPython.indent(lst1)
        self.assertEqual(expectedIndent, actualIndent, 'Indentation failed')

    def testGetOneMethodCodePublic(self):

        pyutType: PyutType = PyutType(value='str')
        publicMethod: PyutMethod = PyutMethod(name='publicMethod', visibility=PyutVisibilityEnum.PUBLIC, returns=pyutType)

        defCode: List[str] = self.pyutToPython.generateASingleMethodsCode(publicMethod, writePass=False)
        self.logger.info(f'Generated definition: {defCode}')
        unExpectedValue: int = -1
        actualValue:     int = defCode.__contains__('def publicMethod')

        self.assertNotEqual(unExpectedValue, actualValue, f'Did not code generate public method correctly: `{defCode}`')

    def testGetOneMethodCodePrivate(self):

        pyutType: PyutType = PyutType(value='str')
        publicMethod: PyutMethod = PyutMethod(name='privateMethod', visibility=PyutVisibilityEnum.PRIVATE, returns=pyutType)

        defCode: List[str] = self.pyutToPython.generateASingleMethodsCode(publicMethod, writePass=False)
        self.logger.info(f'Generated definition: {defCode}')
        unExpectedValue: int = -1
        actualValue:     int = defCode.__contains__('def __privateMethod')

        self.assertNotEqual(unExpectedValue, actualValue, f'Did not code generate private method correctly: `{defCode}`')

    def testGetOneMethodCodeProtected(self):

        pyutType: PyutType = PyutType(value='str')
        publicMethod: PyutMethod = PyutMethod(name='protectedMethod', visibility=PyutVisibilityEnum.PROTECTED, returns=pyutType)

        defCode: List[str] = self.pyutToPython.generateASingleMethodsCode(publicMethod, writePass=False)
        self.logger.info(f'Generated definition: {defCode}')
        unExpectedValue: int = -1
        actualValue:     int = defCode.__contains__('def -protectedMethod')

        self.assertNotEqual(unExpectedValue, actualValue, f'Did not code generate protected method correctly: `{defCode}`')

#
# def testAskWhichClassesToReverse2():
#     class testClass1: pass
#     class testClass2: pass
#     class testClass3: pass
#     class testClass4: pass
#     lstClasses = [testClass1(), testClass2(), testClass3(), testClass4()]
#     ret = askWhichClassesToReverse2(lstClasses)


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestIoPython))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

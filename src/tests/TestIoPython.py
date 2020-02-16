
from typing import List

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from tests.TestBase import TestBase

from org.pyut.model.PyutField import PyutField
from org.pyut.PyutMethod import PyutMethod
from org.pyut.model.PyutVisibilityEnum import PyutVisibilityEnum

from org.pyut.plugins.IoPython import IoPython


class TestIoPython(TestBase):
    """
    You need to change the name of this class to Test`xxxx`
    Where `xxxx' is the name of the class that you want to test.

    See existing tests for more information.
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestIoPython.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestIoPython.clsLogger
        self.plugin = IoPython(oglObjects=None, umlFrame=None)

    def tearDown(self):
        pass

    def testGetPublicFieldPythonCode(self):

        s: str = self.plugin.getFieldPythonCode(PyutField("publicField", "", None, PyutVisibilityEnum.PUBLIC))

        unExpectedValue: int = -1
        actualValue:     int = s.find('self.publicField')
        self.assertNotEqual(unExpectedValue, actualValue, f'Did not code generate public method correctly: `{s}`')

    def testGetPrivateFieldPythonCode(self):

        s: str = self.plugin.getFieldPythonCode(PyutField("privateField", "", None, PyutVisibilityEnum.PRIVATE))

        unExpectedValue: int = -1
        actualValue:     int = s.find('self.__privateField')
        self.assertNotEqual(unExpectedValue, actualValue, f'Did not code generate private method correctly: `{s}`')

    def testGetProtectedFieldPythonCode(self):

        s: str = self.plugin.getFieldPythonCode(PyutField("protectedField", "", None, PyutVisibilityEnum.PROTECTED))

        unExpectedValue: int = -1
        actualValue:     int = s.find('self._protectedField')
        self.assertNotEqual(unExpectedValue, actualValue, f'Did not code generate protected field correctly: `{s}`')

    def testIndent(self):

        lst1: List[str] = ['a', '   b', 'c']
        expectedIndent: List[str] = ['    a', '       b', '    c']
        actualIndent: List[str] = self.plugin.indent(lst1)
        self.assertEqual(expectedIndent, actualIndent, 'Indentation failed')

    def testGetOneMethodCodePublic(self):

        publicMethod: PyutMethod = PyutMethod(name='publicMethod', visibility=PyutVisibilityEnum.PUBLIC, returns='str')

        defCode: List[str] = self.plugin.getOneMethodCode(publicMethod, writePass=False)
        self.logger.info(f'Generated definition: {defCode}')
        unExpectedValue: int = -1
        actualValue:     int = defCode.__contains__('def publicMethod')

        self.assertNotEqual(unExpectedValue, actualValue, f'Did not code generate public method correctly: `{defCode}`')

    def testGetOneMethodCodePrivate(self):

        publicMethod: PyutMethod = PyutMethod(name='privateMethod', visibility=PyutVisibilityEnum.PRIVATE, returns='str')

        defCode: List[str] = self.plugin.getOneMethodCode(publicMethod, writePass=False)
        self.logger.info(f'Generated definition: {defCode}')
        unExpectedValue: int = -1
        actualValue:     int = defCode.__contains__('def __privateMethod')

        self.assertNotEqual(unExpectedValue, actualValue, f'Did not code generate private method correctly: `{defCode}`')

    def testGetOneMethodCodeProtected(self):

        publicMethod: PyutMethod = PyutMethod(name='protectedeMethod', visibility=PyutVisibilityEnum.PROTECTED, returns='str')

        defCode: List[str] = self.plugin.getOneMethodCode(publicMethod, writePass=False)
        self.logger.info(f'Generated definition: {defCode}')
        unExpectedValue: int = -1
        actualValue:     int = defCode.__contains__('def -protectedeMethod')

        self.assertNotEqual(unExpectedValue, actualValue, f'Did not code generate protectec method correctly: `{defCode}`')

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

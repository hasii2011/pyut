
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from org.pyut.model.PyutGloballyDisplayParameters import PyutGloballyDisplayParameters


from org.pyut.preferences.PyutPreferences import PyutPreferences

from tests.TestBase import TestBase

from org.pyut.model.PyutMethod import PyutMethod


class TestPyutMethod(TestBase):
    """
    You need to change the name of this class to Test`xxxx`
    Where `xxxx' is the name of the class that you want to test.

    See existing tests for more information.
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestPyutMethod.clsLogger = getLogger(__name__)
        PyutPreferences.determinePreferencesLocation()

    def setUp(self):
        self.logger:      Logger     = TestPyutMethod.clsLogger
        self._pyutMethod: PyutMethod = PyutMethod()

    def tearDown(self):
        pass

    def testStringMethodWithParameters(self):

        pyutMethod: PyutMethod = self._pyutMethod

        pyutMethod.setStringMode(PyutGloballyDisplayParameters.WITH_PARAMETERS)

        self.assertEqual(PyutGloballyDisplayParameters.WITH_PARAMETERS, pyutMethod.getStringMode(), 'Did not get set correctly')

    def testStringMethodWithoutParameters(self):

        pyutMethod: PyutMethod = self._pyutMethod

        pyutMethod.setStringMode(PyutGloballyDisplayParameters.WITHOUT_PARAMETERS)

        self.assertEqual(PyutGloballyDisplayParameters.WITHOUT_PARAMETERS, pyutMethod.getStringMode(), 'Did not get set correctly')


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestPyutMethod))

    return testSuite


if __name__ == '__main__':
    unitTestMain()


from unittest import TestSuite
from unittest import main as unitTestMain

from pyut.preferences.PreferencesCommon import PreferencesCommon

from tests.TestBase import TestBase

# import the class you want to test here
# from org.pyut.template import template


class TestTemplate(TestBase):
    """
    You need to change the name of this class to Test`xxxx`
    Where `xxxx` is the name of the class that you want to test.

    See existing tests for more information.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        PreferencesCommon.determinePreferencesLocation()

    def setUp(self):
        super().setUp()
        
    def tearDown(self):
        super().tearDown()

    def testName1(self):
        pass

    def testName2(self):
        """Another test"""
        pass


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestTemplate))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

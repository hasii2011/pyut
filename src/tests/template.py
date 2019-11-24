
from logging import Logger
from logging import getLogger

from unittest import main as unitTestMain

from tests.TestBase import TestBase

# import the class you want to test here
# import ...


class Template(TestBase):
    """
    You need to change the name of this class to Test + the name of the class
    that you want to test here.
    See existing tests for more information.
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        Template.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = Template.clsLogger

    def tearDown(self):
        pass

    def testName1(self):
        """Short description (max 1 line) of the test"""
        # The test methods are names : test + name of the test
        #
        # code...
        #
        # you can use :
        #    self.failUnless(condition, errorMsg)
        # where :
        #    - `condition` returns a boolean. The test will fail if the
        #      condition is false.
        #    - `errorMsg` is an optional string which will be displayed if
        #      the test is not successful
        #
        #    self.fail(errorMsg) : to fail immediately
        pass

    def testName2(self):
        """Another test"""
        pass


if __name__ == '__main__':
    unitTestMain()

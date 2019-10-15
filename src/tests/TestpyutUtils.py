
from unittest import TestCase
from unittest import main

# from pyutUtils import assignID
import PyutUtils1

[ID_TXT_NAME, ID_TXT_STEREOTYPE] = PyutUtils1.assignID(2)


class TestpyutUtils(TestCase):
    """
    You need to change the name of this class to Test + the name of the class
    that you want to test here.
    See existing tests for more information.

    @author Laurent Burgbacher <lb@alawa.ch>
    """
    def setUp(self):
        pass

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
    main()

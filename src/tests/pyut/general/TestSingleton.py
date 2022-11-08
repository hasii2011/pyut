
from pyut.general.Singleton import Singleton


import unittest

from unittest import TestSuite


class Child(Singleton):
    """
    Test class.
    See the Singleton documentation to know why you must use `init` and not
    `__init__`.
    """
    def init(self, val):
        self.val = val


class BadChild(Singleton):
    """
    Bad test class.
    See the Singleton documentation to know why this class won't be
    instantiable at all. `__init__` is not permitted in a Singleton class.
    """
    def __init__(self, val):
        self.val = val


class TestSingleton(unittest.TestCase):
    """
    @author Laurent Burgbacher <lb@alawa.ch>
    """
    def testSingleton(self):
        """Test instances of Singleton"""
        a = Singleton()
        b = Singleton()
        self.assertTrue(a is b, "Error, two singletons are not the same.")

    def testSingletonChild(self):
        """Test instances of classes derived from Singleton"""
        a = Child(10)
        b = Child(11)
        self.assertTrue(a is b, "Error, two singletons are not the same.")

    def testBadSingletonClass(self):
        """Test bad derivations of Singleton"""
        try:
            a = BadChild(10)
        except AssertionError:
            pass  # OK
        else:
            self.fail("This should have raised an AssertionError")

    def testFailedInitialization(self):
        """Test failed initialization of a singleton"""
        try:
            a = Child()
        except TypeError:
            pass  # normal behaviour
        a = Child(10)  # good initialization
        self.assertTrue(a.val == 10, "Not correctly initialized")
        a = Child()  # now this works, because the singleton is already instantiated


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestSingleton))

    return testSuite


if __name__ == '__main__':
    unittest.main()

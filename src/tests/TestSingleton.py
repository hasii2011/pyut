#!/usr/bin/env python

__version__ = "$Revision: 1.1.1.1 $"
__author__ = "EI6, eivd, Group Dutoit - Roux"
__date__ = "2002-05-22"

import sys
if ".." not in sys.path:
    sys.path.append("..") # access to the classes to test
from singleton import Singleton
import unittest

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
    instanciable at all. `__init__` is not permitted in a Singleton class.
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
        self.failUnless(a is b, "Error, two singletons are not the same.")

    #>------------------------------------------------------------------------

    def testSingletonChild(self):
        """Test instances of classes derived from Singleton"""
        a = Child(10)
        b = Child(11)
        self.failUnless(a is b, "Error, two singletons are not the same.")

    #>------------------------------------------------------------------------

    def testBadSingletonClass(self):
        """Test bad derivations of Singleton"""
        try:
            a = BadChild(10)
        except AssertionError:
            pass # OK
        else:
            self.fail("This should have raised an AssertionError")

    #>------------------------------------------------------------------------

    def testFailedInitialization(self):
        """Test failed initialization of a singleton"""
        try:
            a = Child()
        except TypeError:
            pass # normal behaviour
        a = Child(10) # good initialization
        self.failUnless(a.val == 10, "Not correctly initialized")
        a = Child() # now this works, because the singleton is already
                    # instanciated



def suite():
    return unittest.makeSuite(TestSingleton)

def main():
    unittest.TextTestRunner().run(suite())

if __name__ == "__main__": main()

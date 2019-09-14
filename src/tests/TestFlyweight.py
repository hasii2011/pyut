#!/usr/bin/env python

__version__ = "$Revision: 1.1.1.1 $"
__author__ = "EI6, eivd, Group Dutoit - Roux"
__date__ = "2002-05-22"

import sys
if ".." not in sys.path:
    sys.path.append("..") # access to the classes to test
import unittest

from FlyweightString import FlyweightString
from PyutType import PyutType # PyutType is a FlyweightString

class TestFlyweight(unittest.TestCase):
    """
    @author Laurent Burgbacher <lb@alawa.ch>
    """
    def setUp(self):
        self.strings = [
            "salut", "hello", "ca va ?"
        ]

    #>------------------------------------------------------------------------

    def testFlyweightString(self):
        """Test whether instanciating an existing fly works correctly"""
        flies = []
        for string in self.strings:
            flies.append(FlyweightString(string))
        newFlies = []
        for string in self.strings:
            newFlies.append(FlyweightString(string))
        for oldFly, newFly in zip(flies, newFlies):
            self.failUnless(newFly is oldFly, "duplicates in flies")

        # now, try with different strings with the same values
        a = FlyweightString("salut")
        b = FlyweightString("sa" + "lut")
        self.failUnless(a is b,
            "two different objects with same values strings")

    #>------------------------------------------------------------------------

    def testPyutType(self):
        """Test PyutType class"""
        a = PyutType("salut")
        b = PyutType("s" + "alut")
        self.failUnless(a.getName() == b.getName())
        self.failUnless(a is b,
            "two different objects with same values strings")
        try:
            a.setName("Salut")
        except AttributeError:
            pass
        else:
            self.fail("PyutType should not be modifiable by setName")

    #>------------------------------------------------------------------------



def suite():
    return unittest.makeSuite(TestFlyweight)

def main():
    unittest.TextTestRunner().run(suite())

if __name__ == "__main__": main()

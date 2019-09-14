#!/usr/bin/env python

__version__ = "$Revision: 1.2 $"
__author__ = "EI6, eivd, Group Dutoit - Roux"
__date__ = "2002-05-22"

"""
Run this file to run each test found in the current directory.
@author Laurent Burgbacher <lb@alawa.ch>
"""

import sys
if ".." not in sys.path:
    sys.path.append("..") # access to the classes to test
import unittest
from glob import glob


#>--------------------------------------------------------------------------

def suite():
    """A suite composed of every suite we can find in this directory"""
    modules = glob("Test*.py")
    suite = unittest.TestSuite()
    # remove .py extension
    modules = map(lambda x: x[:-3], modules)
    modules.remove("TestAll") # remove self to avoid recursion ;-)
    for module in modules:
        m = __import__(module)
        suite.addTest(m.suite())
    return suite

#>--------------------------------------------------------------------------

def main():
    unittest.TextTestRunner().run(suite())


#>--------------------------------------------------------------------------

if __name__ == "__main__": main()

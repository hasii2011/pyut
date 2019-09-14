#!/usr/bin/env python

__version__ = "$Revision: 1.1.1.1 $"
__author__ = "EI6, eivd, Group Dutoit - Roux"
__date__ = "2002-05-22"

import sys
if ".." not in sys.path:
    sys.path.append("..") # access to the classes to test
import unittest

from PyutPreferences import PyutPreferences, PREFS_FILENAME
import os

class TestPyutPreferences(unittest.TestCase):
    """
    @author Laurent Burgbacher <lb@alawa.ch>
    """
    def emptyPrefs(self):
        """
        Empty the preferences.

        Do this by removing the prefs file and reinit the prefs
        (``prefs.init``).
        """
        if os.path.exists(PREFS_FILENAME):
            os.remove(PREFS_FILENAME)
        self.prefs.init()
        # test that it's empty
        try:
            self.failUnless(self.prefs[self.items.keys()[0]] is None)
        except:
            self.fail("Should not raise an exception")

    #>------------------------------------------------------------------------

    def setUp(self):
        """
        Remove any existing prefs file.

        Instantiate a prefs (Singleton class) and fill it.
        """
        self.items = {
            "test_int" : 12,
            "test_double" : 12.12,
            "test_string" : "salut",
            "test_tuple" : ("salut", "les", "amis"),
            "test_list" : ["comment", "allez", "vous"],
        }
        self.prefs = PyutPreferences()
        self.emptyPrefs() # empty the prefs
        # fill the prefs
        for item, value in self.items.items():
            self.prefs[item] = value

    #>------------------------------------------------------------------------

    def testValues(self):
        """
        Test that the prefs contain the good values.
        """
        for item, value in self.items.items():
            found = self.prefs[item]
            self.failUnless(found == str(value),
                "Wrong value for %s. Want %s, got %s" % (item, value, found))

    #>------------------------------------------------------------------------

    def testSpaceInName(self):
        """
        Test what happened with a space in the name of a pref.
        """
        try:
            self.prefs["salut les amis"] = 3
        except TypeError:
            pass # that's OK
        else:
            self.fail("A name without spaces has not raised an exception")

    #>------------------------------------------------------------------------

    def testLoadSave(self):
        """
        Test that load and save work correctly.
        """
        # now, prefs is already loaded, add some values that are automatically
        # saved
        self.prefs["new_pref"] = 10
        self.prefs.init() # reinit the object (that's the only way since it's
                          # a singleton
        self.failUnless(self.prefs["new_pref"] == "10", "Value doesn't exist")

    #>------------------------------------------------------------------------

    def testGetUnknowPref(self):
        """
        What happens with an unknown pref.
        """
        try:
            self.failUnless(self.prefs["unknown"] is None)
        except:
            self.fail("Should not raise an exception")

    #>------------------------------------------------------------------------

    def testGetUnknownPrefWhenEmpty(self):
        """
        What happens with an unknown section.

        All is now in `emptyPrefs`.
        """
        self.emptyPrefs()

    #>------------------------------------------------------------------------

    def testLastOpenedFiles(self):
        """
        Test the last opened files management.
        """
        files = [
            "un", "deux", "trois", "quatre", "cinq", "six"
        ]
        self.prefs.setNbLOF(len(files) - 1)
        self.prefs.init() # reload prefs
        self.failUnless(self.prefs.getNbLOF() == len(files) - 1, "wrong nbLOF")
        for file in files:
            self.prefs.addNewLastOpenedFilesEntry(file)
        self.prefs.init()
        files.reverse() # because it's a last in first out
        files.pop() # remove last one which should have been dropped
        for i in range(len(files) - 1):
            self.failUnless(self.prefs.getLastOpenedFilesList()[i] == files[i],
                "wrong file name")

    #>------------------------------------------------------------------------


def suite():
    """You need to change the name of the test class here also."""
    return unittest.makeSuite(TestPyutPreferences)

def main():
    unittest.TextTestRunner().run(suite())

if __name__ == "__main__": main()

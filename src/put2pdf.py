#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__version__ = "$Revision: 1.3 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2001-11-14"
#import pychecker.checker   #Uncomment this to test PyUt
import os, sys

exePath = None              # the pyut's path
userPath = os.getcwd()      # where the user launched pyut from


#>----------------------------------------------------------------------------
def getExePath():
    """
    Return the absolute path currently used

    @return string the path
    @since 1.5.2.19
    @author C.Dutoit
    """
    import sys, os
    print sys.argv[0]
    if sys.argv[0][0]==os.sep or sys.argv[0].find(":")>0:
        # Absolute path
        exePath = sys.argv[0]
    else:
        # Relative path
        exePath = os.getcwd() + os.sep + sys.argv[0]
    return os.path.split(exePath)[0]



#>----------------------------------------------------------------------------
def goToPyutDirectory():
    """
    Go to the pyut directory

    @since 1.5.2.19
    @author C.Dutoit
    """
    import sys, os
    # Change current directory to pyut's directory
    exePath = getCurrentAbsolutePath()
    sys.path.append(exePath)
    print "Executing PyUt from exepath ", exePath
    os.chdir(exePath)

#>----------------------------------------------------------------------------

def main(script=None):
    """
    main pyut function; create and run app

    @param string name : init name with the name
    @since 1.0
    @author C.Dutoit
    """
    import os, sys
    global exePath, userPath

    # Path
    sys.path.append(exePath)
    os.chdir(exePath)

    # Define last open directory ?
    #  - default is current directory
    #  - last opened directory for developers (pyut/src present)
    from PyutPreferences import PyutPreferences
    prefs = PyutPreferences()    # Prefs handler
    if (userPath.find('pyut/src')==-1) and (userPath.find('pyut2/src')==-1):
        # (User-mode)
        prefs["LastDirectory"] = userPath
    del prefs

    import Lang
    from PyutApp import PyutApp
    app = PyutApp(0, splash=0, show=0)

    if script is not None:
        s = script(app.frame)
        params = [
            "/home/lb/docs/pysimul/src/puts/splitters.put",
            "/home/lb/docs/pyut2/src/essai.ps"
        ]
        s.setParams(params)
        s.run()


#>----------------------------------------------------------------------------

def treatArguments():
    """
    Treat arguments, display helps, ...

    @since 1.5.2.15
    @author C.Dutoit
    @return 1 if an arguments was found and PyUt must be stopped
    """
    import sys

    # Exit if no arguments
    if len(sys.argv)<2:
        return 0

    # Treat command line arguments
    if sys.argv[1] == "--version":
        from PyutVersion import getPyUtVersion
        print "PyUt, version %s" % getPyUtVersion()
        print
        return 1
    elif sys.argv[1] == "--help":
        from PyutVersion import getPyUtVersion
        print "PyUt, version %s" % getPyUtVersion()
        print "Syntaxe : pyut.pyw [filename] [--version] [--help]" \
              "[--start_directory=xxx]"
        print
        print "i.e. :    pyut.pyw --version             display version number"
        print "          pyut.pyw --help                display this help"
        print "          pyut.pyw file1 file2           load files"
        print "          pyut.pyw --start_directory=/   start with '/' as"
        print "                                         default directory"
        print
        return 1
    for param in sys.argv[1:]:
        if param[:18] == "--start_directory=":
            import os
            print "Starting with directory ", param[18:]
            global userPath
            userPath = param[18:]
    return 0


#>------------------------------------------------------------------------
#>------------------------------------------------------------------------

# this is where you can put your script
from PyutScripting import PyutScripting
class Put2Pdf(PyutScripting):
    """
    Needs params = ["src_file_name", "dst_file_name"]
    """
    def run(self):
        src, dst = self._params
        self.openFile(src)
        self.exportToPS(dst)

#>------------------------------------------------------------------------
#>------------------------------------------------------------------------

# Program entry point
if __name__ == "__main__":
    # Get exe path
    exePath = getExePath()

    # Launch pyut
    if treatArguments()<>1:
        main(Put2Pdf)

#!/usr/bin/python
# -*- coding: utf-8 -*-
__version__ = "$Revision: 1.9 $"
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
    #TODO : fix this bug : unhandled after py2exe, on windows
    #encoding=sys.getfilesystemencoding()
    #if encoding in ["mbcs"]:
        #encoding="ISO-8859-1"
    #path = sys.path[0].decode(encoding)
    path = sys.path[0].decode(sys.getfilesystemencoding())
    return path

    #print sys.argv[0]
    #if sys.argv[0][0]==os.sep or sys.argv[0].find(":")>0:
    #    # Absolute path
    #    exePath = sys.argv[0]
    #else: 
    #    # Relative path
    #    exePath = os.getcwd() + os.sep + sys.argv[0]
    #return os.path.split(exePath)[0]
    


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

def main():
    """
    main pyut function; create and run app

    @param string name : init name with the name
    @since 1.0
    @author C.Dutoit
    """
    import os, sys
    global exePath, userPath

    # Path
    try:
        sys.path.append(exePath)
        os.chdir(exePath)
    except OSError, msg:
        print "Error while setting path: ", msg

    # Define last open directory ?
    #  - default is current directory
    #  - last opened directory for developers (pyut/src present)
    from PyutPreferences import PyutPreferences
    prefs = PyutPreferences()    # Prefs handler
    prefs["orgDirectory"] = os.getcwd()
    if (userPath.find('pyut/src')==-1) and (userPath.find('pyut2/src')==-1):
        # (User-mode)
        prefs["LastDirectory"] = userPath
    del prefs


    print """
                               ...
                              /   \\
                       °ooO  | O O |  Ooo°
=============================================================================
                       _____       _    _ _   
                      |  __ \     | |  | | |  
                      | |__) |   _| |  | | |_ 
                      |  ___/ | | | |  | | __|
                      | |   | |_| | |__| | |_ 
                      |_|    \__, |\____/ \__|
                              __/ |           
                             |___/    A little UML 1.3 editor
                      

    """
    print "Versions found : "
    import wx, sys
    print "WX     ", wx.__version__
    print "Python ", sys.version.split(" ")[0]

    print """
=============================================================================
"""


    import lang
    #print "**************"
    #print _("Untitled.put")
    from PyutApp import PyutApp
    app = PyutApp(0)
    app.MainLoop()
    app = None

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
        from pyutVersion import getPyUtVersion
        print "PyUt, version %s" % getPyUtVersion()
        print
        return 1
    elif sys.argv[1] == "--help":
        from pyutVersion import getPyUtVersion
        print "PyUt, version %s" % getPyUtVersion()
        print "Syntaxe : pyut.pyw [filename] [--version] [--help]" \
              "[--start_directory=xxx] file1 file2 ..."
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
    

# Program entry point
if __name__ == "__main__":
    # Get exe path
    exePath = getExePath()

    # Launch pyut
    if treatArguments()<>1:
        main()

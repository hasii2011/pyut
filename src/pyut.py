#!/usr/bin/python

import os

from os import chdir
from os import getcwd
from sys import path
from sys import argv

from PyutApp import PyutApp
from pyutVersion import getPyUtVersion
from PyutPreferences import PyutPreferences

exePath  = None              # the pyut's path
userPath = getcwd()      # where the user launched pyut from


def getExePath():
    """
    Return the absolute path currently used

    @return string the path
    @since 1.5.2.19
    @author C.Dutoit
    """
    # TODO : fix this bug : unhandled after py2exe, on windows
    # encoding = sys.getfilesystemencoding()
    # if encoding in ["mbcs"]:
        # encoding="ISO-8859-1"
    # path = sys.path[0].decode(encoding)
    # path = sys.path[0].decode(sys.getfilesystemencoding())
    absPath = path[0]
    return absPath


def goToPyutDirectory():
    """
    Go to the pyut directory

    @since 1.5.2.19
    @author C.Dutoit
    """
    import sys, os
    # Change current directory to pyut's directory
    # exePath = getCurrentAbsolutePath()
    exePath = os.getcwd()
    sys.path.append(exePath)
    print(f"Executing PyUt from exepath {exePath}")
    os.chdir(exePath)


def main():
    """
    main pyut function; create and run app
    """

    global exePath, userPath

    # Path
    try:
        path.append(exePath)
        chdir(exePath)
    except OSError as msg:
        print(f"Error while setting path: {msg}")

    # Define last open directory ?
    #  - default is current directory
    #  - last opened directory for developers (pyut/src present)
    prefs = PyutPreferences()    # Prefs handler
    prefs["orgDirectory"] = os.getcwd()
    if (userPath.find('pyut/src') == -1) and (userPath.find('pyut2/src') == -1):
        # (User-mode)
        prefs["LastDirectory"] = userPath
    del prefs

    print("""
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
                      

    """)
    print("Versions found : ")
    import wx, sys
    print("WX     ", wx.__version__)
    print("Python ", sys.version.split(" ")[0])

    print("""
=============================================================================
""")

    app = PyutApp(0)
    app.MainLoop()


def treatArguments():
    """
    Treat arguments, display helps, ...

    @since 1.5.2.15
    @author C.Dutoit
    @return 1 if an arguments was found and PyUt must be stopped
    """

    # Exit if no arguments
    if len(argv) < 2:
        return 0

    # Treat command line arguments
    if argv[1] == "--version":
        print(f"PyUt, version {getPyUtVersion()}")
        print()
        return 1
    elif argv[1] == "--help":
        print(f"PyUt, version {getPyUtVersion()}")
        print("Syntax : pyut.pyw [filename] [--version] [--help] [--start_directory=xxx] file1 file2 ...")
        print()
        print("i.e. :    pyut.pyw --version             display version number")
        print("          pyut.pyw --help                display this help")
        print("          pyut.pyw file1 file2           load files")
        print("          pyut.pyw --start_directory=/   start with '/' as")
        print("                                         default directory")
        print()
        return 1
    for param in argv[1:]:
        if param[:18] == "--start_directory=":
            import os
            print("Starting with directory ", param[18:])
            global userPath
            userPath = param[18:]
    return 0


# Program entry point
if __name__ == "__main__":
    # Get exe path
    exePath = getExePath()

    # Launch pyut
    if treatArguments() != 1:
        main()

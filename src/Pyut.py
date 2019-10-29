
from typing import cast

from os import chdir
from os import getcwd
from sys import path
from sys import argv

import json

from logging import Logger
from logging import getLogger

import logging.config

from org.pyut.ui.PyutApp import PyutApp
from PyutVersion import getPyUtVersion
from PyutPreferences import PyutPreferences

from Lang import importLanguage as setupPyutLanguage

JSON_LOGGING_CONFIG_FILENAME = "loggingConfiguration.json"
MADE_UP_PRETTY_MAIN_NAME     = "Pyut"

exePath  = None          # the pyut's path
userPath = getcwd()      # where the user launched pyut from
moduleLogger: Logger = cast(Logger, None)


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
    # Change current directory to pyut's directory
    # exePath = getCurrentAbsolutePath()
    execPath = getcwd()
    path.append(exePath)
    moduleLogger.info(f"Executing PyUt from exepath {execPath}")
    chdir(exePath)


def main():
    """
    main pyut function; create and run app
    """

    global exePath, userPath, moduleLogger

    # Path
    try:
        path.append(exePath)
        chdir(exePath)
    except OSError as msg:
        moduleLogger.error(f"Error while setting path: {msg}")

    # Define last open directory ?
    #  - default is current directory
    #  - last opened directory for developers (pyut/src present)
    prefs = PyutPreferences()    # Prefs handler
    prefs["orgDirectory"] = getcwd()
    if (userPath.find('pyut/src') == -1) and (userPath.find('pyut2/src') == -1):
        # (User-mode)
        prefs["LastDirectory"] = userPath
    del prefs
    # TODO: move this to an external file avoid have to account for invalid escape sequences
    print("""
                               ...
                              /   \\
                       °ooO  | O O |  Ooo°
=============================================================================
                       _____       _    _ _   
                      |  __ \\    | |  | | |  
                      | |__) |   _| |  | | |_ 
                      |  ___/ | | | |  | | __|
                      | |   | |_| | |__| | |_ 
                      |_|    \\_, |\____/ \_ |
                              __/ |           
                             |___/    A little UML 1.4 editor
                      

    """)
    print("Versions found : ")
    import wx
    import sys
    print("WX     ", wx.__version__)
    print("Python ", sys.version.split(" ")[0])

    print("""
=============================================================================
""")

    app = PyutApp(redirect=False)
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

            moduleLogger.info("Starting with directory ", param[18:])
            global userPath
            userPath = param[18:]
    return 0


# Program entry point
if __name__ == "__main__":

    with open(JSON_LOGGING_CONFIG_FILENAME, 'r') as loggingConfigurationFile:
        configurationDictionary = json.load(loggingConfigurationFile)

    logging.config.dictConfig(configurationDictionary)
    logging.logProcesses = False
    logging.logThreads   = False

    moduleLogger = getLogger(MADE_UP_PRETTY_MAIN_NAME)

    moduleLogger.info(f"Starting {MADE_UP_PRETTY_MAIN_NAME}")

    setupPyutLanguage()
    exePath = getExePath()

    # Launch pyut
    if treatArguments() != 1:
        main()

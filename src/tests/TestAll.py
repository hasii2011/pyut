
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

import logging.config

from json import load as jsonLoad

from importlib import import_module

import sys
from glob import glob

import unittest
from unittest.suite import TestSuite


if ".." not in sys.path:
    sys.path.append("..")  # access to the classes to test

moduleLogger: Logger = cast(Logger, None)
"""
Run this file to run each test found in the current directory.
@author Laurent Burgbacher <lb@alawa.ch>
"""


def suite() -> TestSuite:

    global moduleLogger

    fModules = glob("Test*.py")
    # remove .py extension
    modules = list(map(lambda x: x[:-3], fModules))
    noTests: List[str] = ['TestAll', 'TestMiniOgl', 'TestBase', 'TestTemplate', 'TestIoFile', 'TestUmlFrame']
    for doNotTest in noTests:
        modules.remove(doNotTest)

    """
    A suite composed of every suite we can find in this package
    """
    fSuite: TestSuite = unittest.TestSuite()
    for module in modules:
        try:
            m = import_module(module)
            fSuite.addTest(m.suite())
        except (ValueError, Exception) as e:
            moduleLogger.error(f'Module import problem:  {e}')
    return fSuite


def setupSystemLogging():

    with open('testLoggingConfig.json', 'r') as loggingConfigurationFile:
        configurationDictionary = jsonLoad(loggingConfigurationFile)

        logging.config.dictConfig(configurationDictionary)
        logging.logProcesses = False
        logging.logThreads   = False


def main():

    global moduleLogger

    setupSystemLogging()
    moduleLogger = getLogger('TestAll')

    testSuite: TestSuite = suite()
    unittest.TextTestRunner().run(testSuite)


if __name__ == "__main__":
    main()

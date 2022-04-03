
from typing import List

from logging import Logger
from logging import getLogger

from sys import path as sysPath
from sys import argv as sysArgv

from importlib import import_module

from os import walk as osWalk
from os import sep as osSep

from re import search as regExSearch

from unittest import TestResult
from unittest import TextTestRunner
from unittest.suite import TestSuite

from HtmlTestRunner import HTMLTestRunner


class TestAll:
    """
    The class that can run our unit tests in various formats
    """
    NOT_TESTS: List[str] = ['TestAll',
                            'org/pyut/miniogl/TestMiniOgl',
                            'TestWxOgl', 'TestBase', 'TestTemplate',
                            'org/pyut/persistence/TestIoFile',
                            'org/pyut/ui/tools/TestToolboxFrame',
                            'org/pyut/history/commands/TestCommandCommon',
                            'org/pyut/ogl/events/TestOglEventEngine',
                            'TestUmlFrame', 'org/pyut/dialogs/TestADialog', 'TestGriddedDiagramApplication']

    VERBOSITY_QUIET:   int = 0  # Print the total numbers of tests executed and the global result
    VERBOSITY_DEFAULT: int = 1  # VERBOSITY_QUIET plus a dot for every successful test or a F for every failure
    VERBOSITY_VERBOSE: int = 2  # Print help string of every test and the result
    VERBOSITY_LOUD:    int = 3  # ??

    def __init__(self):

        self._setupSystemLogging()

        self.logger: Logger = getLogger(__name__)

        self._testSuite: TestSuite = self._getTestSuite()

    def runTextTestRunner(self) -> int:

        runner: TextTestRunner = TextTestRunner(verbosity=TestAll.VERBOSITY_QUIET)
        status: TestResult     = runner.run(self._testSuite)
        print(f"THE RESULTS ARE IN:")
        print(f"run: {status.testsRun} errors: {len(status.errors)} failures: {len(status.failures)} skipped: {len(status.skipped)}")
        if len(status.failures) != 0:
            return 1
        else:
            return 0

    def runHtmlTestRunner(self) -> int:

        runner = HTMLTestRunner(report_name='PyutTestResults', combine_reports=True, add_timestamp=True)
        status = runner.run(self._testSuite)
        if len(status.failures) != 0:
            return 1
        else:
            return 0

    def _setupSystemLogging(self):
        """
        Read the unit test logging configuration file
        """
        from tests.TestBase import TestBase

        TestBase.setUpLogging()

    def _getTestSuite(self) -> TestSuite:
        """

        Returns:
            A suite of all tests in the unit test directory
        """
        modules: List[str] = self.__getTestableModuleNames()
        fSuite: TestSuite = TestSuite()
        for module in modules:
            try:
                fixedName: str = module.replace('/', '.')
                m = import_module(fixedName)
                # noinspection PyUnresolvedReferences
                fSuite.addTest(m.suite())
            except (ValueError, Exception) as e:
                self.logger.error(f'Module import problem with: {module}:  {e}')
        return fSuite

    def __getTestableModuleNames(self) -> List[str]:
        """
        Removes modules that are not unit tests

        Returns:
            A list of testable module names
        """

        allModules: List[str] = self.__getModuleNames()

        self.logger.debug(f'{allModules=}')

        for doNotTest in TestAll.NOT_TESTS:
            allModules.remove(f'tests/{doNotTest}')

        return allModules

    def __getModuleNames(self) -> List[str]:
        """
        Get all likely test modules

        Returns:
            A list of module names that we can find in this package
        """
        testFilenames: List[str] = []
        rootDir = 'tests'
        for dirName, subdirList, fileList in osWalk(rootDir):
            if '__pycache__' in dirName:
                continue
            self.logger.debug(f'directory: {dirName}')
            for fName in fileList:
                if self.__startsWith('Test', fName) is True:
                    fqFileName: str = f'{dirName}{osSep}{fName}'
                    self.logger.debug(f'{fqFileName}')
                    testFilenames.append(fqFileName)

        # remove .py extension
        modules = list(map(lambda x: x[:-3], testFilenames))

        return modules

    def __startsWith(self, pattern: str, stringToCheck: str) -> bool:

        ans: bool = False
        if pattern in stringToCheck:
            # passes first easy test
            regExp: str = f'^{pattern}'
            match = regExSearch(regExp, stringToCheck)
            if match:
                ans = True

        return ans


def main():

    if ".." not in sysPath:
        sysPath.append("..")  # access to the classes to test

    testAll: TestAll = TestAll()
    status: int = 0
    if len(sysArgv) < 2:
        status: int = testAll.runTextTestRunner()
    else:
        for param in sysArgv[1:]:
            if param[:22] == "--produce-html-results":
                print(f'Running HTML Tests')
                status: int = testAll.runHtmlTestRunner()

    return status


if __name__ == "__main__":
    cliStatus: int = main()
    exit(cliStatus)

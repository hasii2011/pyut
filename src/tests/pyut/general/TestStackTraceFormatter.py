
from typing import cast

from logging import Logger
from logging import getLogger

from traceback import StackSummary

from unittest import TestSuite
from unittest import main as unitTestMain

from tests.TestBase import TestBase

from org.pyut.general.StackTraceFormatter import StackTraceFormatter
from org.pyut.general.StackTraceFormatter import StackTraceList
from org.pyut.general.StackTraceFormatter import CodeLines
from org.pyut.general.StackTraceFormatter import CompressedLines


class TestStackTraceFormatter(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestStackTraceFormatter.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestStackTraceFormatter.clsLogger

    def tearDown(self):
        pass

    def testBasic(self):

        import traceback
        stackSummary: StackSummary = traceback.extract_stack()

        stackTraceList: StackTraceList = traceback.format_list(stackSummary)

        stackTraceFormatter: StackTraceFormatter = StackTraceFormatter(stackTraceList=stackTraceList)

        codeLines: CodeLines = stackTraceFormatter.codeLines

        expectedCodeLineCount: int = len(stackTraceList)
        actualCodeLineCount:   int = len(codeLines)

        self.assertEqual(expectedCodeLineCount, actualCodeLineCount, 'Did not process entire stack trace list')

    def testLineNumbersAreNumbers(self):

        import traceback
        stackSummary: StackSummary = traceback.extract_stack()

        stackTraceList: StackTraceList = traceback.format_list(stackSummary)

        stackTraceFormatter: StackTraceFormatter = StackTraceFormatter(stackTraceList=stackTraceList)

        codeLines: CodeLines = stackTraceFormatter.codeLines

        for codeLine in codeLines:

            try:
                # noinspection PyUnusedLocal
                lineNumber: int = int(codeLine.lineNumber)
            except ValueError as ve:
                self.fail(f'Bad line number: {codeLine.lineNumber} {ve}')

    def testRetrievedFileName(self):

        import traceback
        stackSummary: StackSummary = traceback.extract_stack()

        stackTraceList: StackTraceList = traceback.format_list(stackSummary)

        stackTraceFormatter: StackTraceFormatter = StackTraceFormatter(stackTraceList=stackTraceList)

        codeLines: CodeLines = stackTraceFormatter.codeLines

        for codeLine in codeLines:
            self.assertIsNotNone(codeLine.fileName, f'Oops, did not get a file name {codeLine.lineNumber}')
            self.logger.debug(f'{codeLine.fileName}')

    def testRetrievedMethod(self):

        import traceback
        stackSummary: StackSummary = traceback.extract_stack()

        stackTraceList: StackTraceList = traceback.format_list(stackSummary)

        stackTraceFormatter: StackTraceFormatter = StackTraceFormatter(stackTraceList=stackTraceList)

        codeLines: CodeLines = stackTraceFormatter.codeLines

        for codeLine in codeLines:
            self.assertIsNotNone(codeLine.methodName, f'Oops, did not get a file name {codeLine.lineNumber}')
            self.logger.debug(f'{codeLine.methodName}')

    def testCodeLineRepr(self):
        import traceback
        stackSummary: StackSummary = traceback.extract_stack()

        stackTraceList: StackTraceList = traceback.format_list(stackSummary)

        stackTraceFormatter: StackTraceFormatter = StackTraceFormatter(stackTraceList=stackTraceList)

        codeLines: CodeLines = stackTraceFormatter.codeLines
        for codeLine in codeLines:
            self.logger.debug(f'{codeLine}')

    def testCompressedCodeLines(self):
        import traceback
        stackSummary: StackSummary = traceback.extract_stack()

        stackTraceList: StackTraceList = traceback.format_list(stackSummary)

        stackTraceFormatter: StackTraceFormatter = StackTraceFormatter(stackTraceList=stackTraceList)

        compressedLines: CompressedLines = stackTraceFormatter.compressedCodeLines
        for cLine in compressedLines:
            self.logger.debug(cLine)

    def testDumpedStackList(self):

        import traceback
        stackSummary: StackSummary = traceback.extract_stack()

        stackTraceList: StackTraceList = traceback.format_list(stackSummary)

        stackTraceFormatter: StackTraceFormatter = StackTraceFormatter(stackTraceList=stackTraceList)

        bigString: str = stackTraceFormatter.dumpedStackList()
        self.assertIsNotNone(bigString, 'I should have something')
        self.logger.debug(f'{bigString}')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestStackTraceFormatter))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

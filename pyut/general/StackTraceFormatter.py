
from typing import List

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from os import linesep as osLineSep
from os import sep as osSep


@dataclass
class CodeLine:
    fileName:   str = ''
    lineNumber: str = ''
    methodName: str = ''
    code:       str = ''


CodeLines       = List[CodeLine]
CompressedLines = List[str]
StackTraceList  = List[str]


class StackTraceFormatter:
    """
    Get a stack trace list as follows:
        ```python
        import traceback
            trString: str = traceback.extract_stack()

            fmtString: StackTraceList = traceback.format_list(trString)
        ```
    """
    SPACE: str = ' '
    COMMA: str = ','
    METHOD_SPLITTER: str = ' in'

    FILE_NAME_RETRIEVAL_LENGTH: int = 24

    def __init__(self, stackTraceList: StackTraceList, codeFileNameLength: int = FILE_NAME_RETRIEVAL_LENGTH):

        self.logger: Logger = getLogger(__name__)

        self._stackTraceList:      StackTraceList  = stackTraceList
        self._codeLines:           CodeLines       = []
        self._compressedCodeLines: CompressedLines = []
        self._codeFileNameLength:  int             = codeFileNameLength

    @property
    def codeLines(self) -> CodeLines:
        if len(self._codeLines) == 0:
            self._parseStack()

        return self._codeLines

    @property
    def compressedCodeLines(self) -> List[str]:

        if len(self._codeLines) == 0:
            self._parseStack()
        if len(self._compressedCodeLines) == 0:
            self._compressTheStack()

        return self._compressedCodeLines

    def dumpedStackList(self) -> str:
        if len(self._codeLines) == 0:
            self._parseStack()
        if len(self._compressedCodeLines) == 0:
            self._compressTheStack()

        bigString: str = ''
        for compressedLine in self._compressedCodeLines:
            bigString = f'{bigString}{osLineSep}{compressedLine}'

        return bigString

    def _parseStack(self):

        for rawCodeLine in self._stackTraceList:
            codeLine: CodeLine = self._parseRawCodeLine(rawCodeLine)
            self._codeLines.append(codeLine)

    def _compressTheStack(self):
        """
        Assumes the stack has been parsed
        """
        for codeLine in self._codeLines:
            compressedLine = (
                f'{codeLine.fileName:24} '
                f'{codeLine.lineNumber:5}'
                f'{codeLine.methodName:16} '
                f'{codeLine.code:24}'
            )
            self._compressedCodeLines.append(compressedLine)

    def _parseRawCodeLine(self, rawCodeLine: str) -> CodeLine:

        codeLine: CodeLine  = CodeLine()
        lfParse:  List[str] = rawCodeLine.split(osLineSep)

        fileLineNumMethod: str = lfParse[0]
        sourceCode:  str = lfParse[1]

        codeLine.code       = sourceCode.strip(StackTraceFormatter.SPACE)
        codeLine.lineNumber = self._getLineNumber(fileLineNum=fileLineNumMethod)
        codeLine.methodName = self._getMethodName(fileLineNumMethod=fileLineNumMethod)
        codeLine.fileName   = self._getFileName(fileLineNum=fileLineNumMethod)

        return codeLine

    def _getLineNumber(self, fileLineNum: str) -> str:
        """

        Args:
            fileLineNum: The part of the raw code line that contains the file name and the line number

        Returns:  The text of the line number
        """
        flnParse: List[str] = fileLineNum.split(StackTraceFormatter.COMMA)

        rawLineNumberParse: str = flnParse[1]

        tmpList: List[str] = rawLineNumberParse.strip(StackTraceFormatter.SPACE).split(StackTraceFormatter.SPACE)
        lineNumber: str = tmpList[1]

        return lineNumber

    def _getMethodName(self, fileLineNumMethod: str) -> str:

        flnParse: List[str] = fileLineNumMethod.split(StackTraceFormatter.COMMA)

        rawMethodParse: str       = flnParse[2]
        methodParse:    List[str] = rawMethodParse.split(StackTraceFormatter.METHOD_SPLITTER)
        fullMethod:     str       = methodParse[1]

        return fullMethod

    def _getFileName(self, fileLineNum: str) -> str:
        """
        Does not necessarily return an entire code path;  Retrieves a default number of characters;  Can
        be controlled by the class consumer

        Args:
            fileLineNum: The part of the raw code line that contains the filename and the line number

        Returns:  The text of the filename
        """
        flnParse:         List[str] = fileLineNum.split(StackTraceFormatter.COMMA)
        rawFileNameParse: str       = flnParse[0]

        truncatedFileName: str = rawFileNameParse[-StackTraceFormatter.FILE_NAME_RETRIEVAL_LENGTH:]
        modifiedFileName:  str = self.__stripUpToFirstDirectorySeparator(longFileName=truncatedFileName)

        return modifiedFileName

    def __stripUpToFirstDirectorySeparator(self, longFileName: str):

        if longFileName.startswith(osSep):
            modifiedFileName: str = longFileName
        else:
            osSepIdx: int = longFileName.find(osSep)
            if osSepIdx == -1:
                modifiedFileName = longFileName
            else:
                modifiedFileName = longFileName[osSepIdx:]

        return modifiedFileName

    def __str__(self) -> str:
        return self.__repr_()

    def __repr_(self) -> str:

        retStr:  str = ''
        lineNum: int = 0
        for line in self._stackTraceList:
            lineNum += 1
            retStr = f'{retStr}\n{lineNum} - {line}'

        return retStr

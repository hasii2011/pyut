
from typing import List

from logging import Logger
from logging import getLogger

from antlr4 import CommonTokenStream
from antlr4 import FileStream

from org.pyut.plugins.iopythonsupport.pyantlrparser.Python3Lexer import Python3Lexer
from org.pyut.plugins.iopythonsupport.pyantlrparser.Python3Parser import Python3Parser

from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame

from org.pyut.ogl.OglClass import OglClass


class ReverseEngineerPython2:

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

    def reversePython(self, umlFrame: UmlClassDiagramsFrame, files: List[str]):
        """
        Reverse engineering

        Args:
            umlFrame:           The uml frame to display on

            files:   A list of files to parse
        """
        for fileName in files:
            self.logger.info(f'Processing file: {fileName}')

            fileStream: FileStream   = FileStream(fileName)
            lexer:      Python3Lexer = Python3Lexer(fileStream)

            stream: CommonTokenStream = CommonTokenStream(lexer)
            parser: Python3Parser     = Python3Parser(stream)

            tree: Python3Parser.File_inputContext = parser.file_input()
            if parser.getNumberOfSyntaxErrors() != 0:
                self.logger.error(f"File contains {parser.getNumberOfSyntaxErrors()} syntax errors")
                # TODO:  Put up a dialog
                continue

        objectList: List[OglClass] = []
        self._layoutUmlClasses(objectList)  # , umlFrame)

    def _layoutUmlClasses(self, objectList: List[OglClass]):    # umlFrame: UmlClassDiagramsFrame):
        """
        Organize by vertical descending sizes

        Args:
            objectList:
            # umlFrame:
        """
        # Sort by descending height
        sortedOglClasses = sorted(objectList, key=lambda oglClassToSort: oglClassToSort._height, reverse=True)

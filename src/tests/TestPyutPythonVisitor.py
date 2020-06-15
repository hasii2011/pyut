
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from antlr4 import CommonTokenStream
from antlr4 import FileStream

from org.pyut.plugins.iopythonsupport.pyantlrparser.Python3Lexer import Python3Lexer
from org.pyut.plugins.iopythonsupport.pyantlrparser.Python3Parser import Python3Parser
from tests.TestBase import TestBase

from org.pyut.plugins.iopythonsupport.PyutPythonVisitor import PyutPythonVisitor


class TestPyutPythonVisitor(TestBase):
    """

    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestPyutPythonVisitor.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestPyutPythonVisitor.clsLogger

    def tearDown(self):
        pass

    def testOnlyInitHasParameters(self):

        tree:    Python3Parser.File_inputContext = self._setupVisitor('Vertex.py')
        visitor: PyutPythonVisitor = PyutPythonVisitor()

        visitor.visit(tree)

        self.assertTrue('Vertex' in visitor.classMethods, 'Oops, I am missing my class key')

        self.assertTrue('__init__' in visitor.parameters, 'I am missing a method')
        self.assertFalse('surround_faces' in visitor.parameters, 'I am missing a method')
        self.assertFalse('surround_half_edges' in visitor.parameters, 'I am missing a method')

    def testLargeClassWithMethodsThatHaveParameters(self):

        tree:    Python3Parser.File_inputContext = self._setupVisitor('GMLExporter.py')
        visitor: PyutPythonVisitor = PyutPythonVisitor()

        visitor.visit(tree)

        self.assertTrue('GMLExporter' in visitor.classMethods, 'Oops, I am missing my class key')

        self.assertTrue('translate' in visitor.parameters, 'I am missing a method')
        self.assertTrue('prettyPrint' in visitor.parameters, 'I am missing a method')
        self.assertTrue('write' in visitor.parameters, 'I am missing a method')
        self.assertTrue('_generateNodeGraphicsSection' in visitor.parameters, 'I am missing a method')
        self.assertTrue('__generatePoint' in visitor.parameters, 'I am missing a method')

    def testRetrieveCodeFromMethods(self):

        tree:    Python3Parser.File_inputContext = self._setupVisitor('Vertex.py')
        visitor: PyutPythonVisitor = PyutPythonVisitor()

        visitor.visit(tree)

        expectedNumberOfMethodsWithCode: int = 3
        self.assertEqual(expectedNumberOfMethodsWithCode, len(visitor.methodCode), 'Not enough code')

    def testRetrieveMethods(self):

        tree:    Python3Parser.File_inputContext = self._setupVisitor('Vertex.py')
        visitor: PyutPythonVisitor = PyutPythonVisitor()

        visitor.visit(tree)

        expectedNumberOfFields: int = 3
        self.assertEqual(expectedNumberOfFields, len(visitor.fields), 'Not enough fields')

    def _setupVisitor(self, fileName: str) -> Python3Parser.File_inputContext:

        # fqFileName = resource_filename(TestBase.RESOURCES_TEST_CLASSES_PACKAGE_NAME, fileName)

        fileStream: FileStream   = FileStream(f'tests/testclass/{fileName}')
        lexer:      Python3Lexer = Python3Lexer(fileStream)

        stream: CommonTokenStream = CommonTokenStream(lexer)
        parser: Python3Parser     = Python3Parser(stream)

        tree: Python3Parser.File_inputContext = parser.file_input()
        if parser.getNumberOfSyntaxErrors() != 0:
            self.logger.error(f'File contains {parser.getNumberOfSyntaxErrors()} syntax errors')
            self.assertTrue(False, f'File contains {parser.getNumberOfSyntaxErrors()} syntax errors')

        return tree


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestPyutPythonVisitor))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

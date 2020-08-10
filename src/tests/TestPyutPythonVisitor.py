
from typing import List

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

    def testMultiClassFileWithInheritance(self):
        tree:    Python3Parser.File_inputContext = self._setupVisitor('Opie.py')
        visitor: PyutPythonVisitor = PyutPythonVisitor()

        visitor.visit(tree)

        expectedParentName: str = 'Cat'
        expectedChildName:  str = 'Opie'

        self.assertTrue(expectedParentName in visitor.parents, 'Missing parent')

        actualChildName: str = visitor.parents[expectedParentName][0]

        self.assertEqual(expectedChildName, actualChildName, 'Missing child')

    def testInheritanceMultiParentMultiChildren(self):
        tree:    Python3Parser.File_inputContext = self._setupVisitor('DeepInheritance.py')
        visitor: PyutPythonVisitor = PyutPythonVisitor()

        visitor.visit(tree)

        expectedParentName1: str = 'ParentClass1'
        expectedParentName2: str = 'ParentClass2'

        self.assertEqual(len(visitor.parents), 2, 'Incorrect parent count')
        self.assertTrue(expectedParentName1 in visitor.parents, f'Missing parent: {expectedParentName1}')
        self.assertTrue(expectedParentName2 in visitor.parents, f'Missing parent: {expectedParentName2}')

        parent1Children: List[str] = visitor.parents[expectedParentName1]

        expectedParent1Child1: str = 'ChildClass1'
        expectedParent1Child2: str = 'ChildClass2'
        self.assertTrue(expectedParent1Child1 in parent1Children, f'Missing child: {expectedParent1Child1} of parent {expectedParentName1}')
        self.assertTrue(expectedParent1Child2 in parent1Children, f'Missing child: {expectedParent1Child2} of parent {expectedParentName1}')

        parent2Children: List[str] = visitor.parents[expectedParentName2]

        expectedParent2Child3: str = 'ChildClass3'
        expectedParent2Child4: str = 'ChildClass4'
        self.assertTrue(expectedParent2Child3 in parent2Children, f'Missing child: {expectedParent2Child3} of parent {expectedParentName2}')
        self.assertTrue(expectedParent2Child4 in parent2Children, f'Missing child: {expectedParent2Child4} of parent {expectedParentName2}')

    def testDecoratedProperty(self):

        tree:    Python3Parser.File_inputContext = self._setupVisitor('ClassWithProperties.py')
        visitor: PyutPythonVisitor = PyutPythonVisitor()

        visitor.visit(tree)

        self.logger.info(f'{visitor.classMethods=}')
        self.logger.info(f'{visitor.namedProperties=}')
        self.logger.info(f'{visitor.derivedProperties=}')

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

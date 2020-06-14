from typing import Dict
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from os import sep as osSep

from antlr4 import CommonTokenStream
from antlr4 import FileStream

from org.pyut.model.PyutClass import PyutClass
from org.pyut.model.PyutMethod import PyutMethod
from org.pyut.model.PyutParam import PyutParam
from org.pyut.model.PyutType import PyutType
from org.pyut.model.PyutVisibilityEnum import PyutVisibilityEnum
from org.pyut.plugins.iopythonsupport.PyutPythonVisitor import PyutPythonVisitor
from org.pyut.plugins.iopythonsupport.pyantlrparser.Python3Lexer import Python3Lexer
from org.pyut.plugins.iopythonsupport.pyantlrparser.Python3Parser import Python3Parser

from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame

from org.pyut.ogl.OglClass import OglClass


class ReverseEngineerPython2:

    PyutClassName = str
    PyutClasses   = Dict[PyutClassName, PyutClass]
    OglClasses    = List[OglClass]

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self.visitor: PyutPythonVisitor = cast(PyutPythonVisitor, None)

        self._pyutClasses: ReverseEngineerPython2.PyutClasses = {}
        self._oglClasses:  ReverseEngineerPython2.OglClasses  = []

    def reversePython(self, umlFrame: UmlClassDiagramsFrame, directoryName: str, files: List[str]):
        """
        Reverse engineering Python files to OglClass's

        Args:
            umlFrame:       The uml frame to display on
            directoryName:  The directory name where the selected files reside
            files:          A list of files to parse
        """
        for fileName in files:

            fqFileName: str = f'{directoryName}{osSep}{fileName}'
            self.logger.info(f'Processing file: {fqFileName}')

            fileStream: FileStream   = FileStream(fqFileName)
            lexer:      Python3Lexer = Python3Lexer(fileStream)

            stream: CommonTokenStream = CommonTokenStream(lexer)
            parser: Python3Parser     = Python3Parser(stream)

            tree: Python3Parser.File_inputContext = parser.file_input()
            if parser.getNumberOfSyntaxErrors() != 0:
                self.logger.error(f"File contains {parser.getNumberOfSyntaxErrors()} syntax errors")
                # TODO:  Put up a dialog
                continue

            self.visitor = PyutPythonVisitor()

            self.visitor.visit(tree)
            self._generatePyutClasses()

        self._generateOglClasses(umlFrame)
        self._layoutUmlClasses(umlFrame)

    def _generatePyutClasses(self):

        for className in self._classNames():
            pyutClass: PyutClass = PyutClass(name=className)

            for methodName in self._methodNames(className):
                pyutMethod: PyutMethod = PyutMethod(name=methodName)
                if methodName[0:2] == "__":
                    pyutMethod.setVisibility(PyutVisibilityEnum.PRIVATE)
                elif methodName[0] == "_":
                    pyutMethod.setVisibility(PyutVisibilityEnum.PROTECTED)
                else:
                    pyutMethod.setVisibility(PyutVisibilityEnum.PUBLIC)
                pyutMethod = self._addParameters(pyutMethod)
                pyutMethod.sourceCode = self.visitor.methodCode[methodName]

                pyutClass.addMethod(pyutMethod)
            self._pyutClasses[className] = pyutClass
        self.logger.info(f'Generated {len(self._pyutClasses)} classes')

    def _addParameters(self, pyutMethod: PyutMethod) -> PyutMethod:

        methodName: str = pyutMethod.name
        if methodName in self.visitor.parameters:
            parameters: PyutPythonVisitor.Parameters = self.visitor.parameters[methodName]
            for parameter in parameters:
                self.logger.info(f'parameter: {parameter}')
                paramNameType = parameter.split(':')
                #
                # TODO: account for default values
                #
                if len(paramNameType) == 2:         # Somebody is good and did typing
                    pyutType: PyutType = PyutType(paramNameType[1])
                    pyutParam: PyutParam = PyutParam(name=paramNameType[0], theParameterType=pyutType)
                    pyutMethod.addParam(pyutParam)

        return pyutMethod

    def _generateOglClasses(self, umlFrame: UmlClassDiagramsFrame):

        for pyutClassName in self._pyutClasses:
            try:
                pyutClass: PyutClass = self._pyutClasses[pyutClassName]
                oglClass:  OglClass = OglClass(pyutClass)
                umlFrame.addShape(oglClass, 0, 0)
                oglClass.autoResize()
                self._oglClasses.append(oglClass)
            except (ValueError, Exception) as e:
                self.logger.error(f"Error while creating class {pyutClassName},  {e}")

    def _methodNames(self, className: str) -> List[str]:
        return self.visitor.classMethods[className]

    def _classNames(self) -> List[str]:
        retNames = []
        for className in self.visitor.classMethods.keys():
            retNames.append(className)

        return retNames

    def _layoutUmlClasses(self, umlFrame: UmlClassDiagramsFrame):
        """
        Organize by vertical descending sizes

        Args:
            umlFrame:
        """
        # Sort by descending height
        sortedOglClasses = sorted(self._oglClasses, key=lambda oglClassToSort: oglClassToSort._height, reverse=True)

        x: int = 20
        y: int = 20

        incY: int = 0
        for oglClass in sortedOglClasses:
            incX, sy = oglClass.GetSize()
            incX += 20
            sy += 20
            incY = max(incY, int(sy))
            # find good coordinates
            if x + incX >= umlFrame.maxWidth:
                x = 20
                y += incY
                incY = int(sy)
            oglClass.SetPosition(x, y)
            x += incX


from typing import Dict
from typing import List
from typing import NewType
from typing import Tuple
from typing import Union
from typing import cast

from logging import Logger
from logging import getLogger

from os import sep as osSep

from antlr4 import CommonTokenStream
from antlr4 import FileStream

from wx import PD_APP_MODAL
from wx import PD_ELAPSED_TIME

from wx import ProgressDialog

from org.pyut.history.commands.CommandGroup import CommandGroup
from org.pyut.history.commands.CreateOglLinkCommand import CreateOglLinkCommand

from org.pyut.history.HistoryManager import HistoryManager

from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutField import PyutField
from pyutmodel.PyutMethod import PyutMethod
from pyutmodel.PyutMethod import PyutParameters
from pyutmodel.PyutParameter import PyutParameter
from pyutmodel.PyutType import PyutType
from pyutmodel.PyutVisibilityEnum import PyutVisibilityEnum

from org.pyut.ogl.OglClass import OglClass

from org.pyut.plugins.iopythonsupport.PythonParseException import PythonParseException

from org.pyut.plugins.iopythonsupport.PyutPythonVisitor import ChildName
from org.pyut.plugins.iopythonsupport.PyutPythonVisitor import Children
from org.pyut.plugins.iopythonsupport.PyutPythonVisitor import ClassName
from org.pyut.plugins.iopythonsupport.PyutPythonVisitor import ClassNames
from org.pyut.plugins.iopythonsupport.PyutPythonVisitor import DataClassProperties
from org.pyut.plugins.iopythonsupport.PyutPythonVisitor import MethodName
from org.pyut.plugins.iopythonsupport.PyutPythonVisitor import MethodNames
from org.pyut.plugins.iopythonsupport.PyutPythonVisitor import MultiParameterNames
from org.pyut.plugins.iopythonsupport.PyutPythonVisitor import Parameters
from org.pyut.plugins.iopythonsupport.PyutPythonVisitor import ParentName
from org.pyut.plugins.iopythonsupport.PyutPythonVisitor import Parents
from org.pyut.plugins.iopythonsupport.PyutPythonVisitor import PyutPythonVisitor

from org.pyut.plugins.iopythonsupport.pyantlrparser.Python3Lexer import Python3Lexer
from org.pyut.plugins.iopythonsupport.pyantlrparser.Python3Parser import Python3Parser

from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame

PyutClassName = NewType('PyutClassName', str)
PyutClasses = NewType('PyutClasses', Dict[PyutClassName, PyutClass])
OglClasses = NewType('OglClasses', Dict[Union[PyutClassName, ParentName, ChildName, ClassName], OglClass])


class ReverseEngineerPython2:

    PYTHON_ASSIGNMENT:     str = '='
    PYTHON_TYPE_DELIMITER: str = ':'
    PYTHON_EOL_COMMENT:    str = '#'

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self.visitor: PyutPythonVisitor = cast(PyutPythonVisitor, None)

        self._pyutClasses: PyutClasses = PyutClasses({})
        self._oglClasses:  OglClasses  = OglClasses({})

    def reversePython(self, umlFrame: UmlClassDiagramsFrame, directoryName: str, files: List[str]):
        """
        Reverse engineering Python files to OglClass's

        Args:
            umlFrame:       The uml frame to display on
            directoryName:  The directory name where the selected files reside
            files:          A list of files to parse
        """
        fileCount: int = len(files)
        dlg = ProgressDialog('Parsing Files', 'Starting',  parent=umlFrame, style=PD_APP_MODAL | PD_ELAPSED_TIME)
        dlg.SetRange(fileCount)
        currentFileCount: int = 0

        onGoingParents: Parents = Parents({})
        for fileName in files:

            try:
                fqFileName: str = f'{directoryName}{osSep}{fileName}'
                self.logger.info(f'Processing file: {fqFileName}')
                dlg.Update(currentFileCount, f'Processing: {fileName}')

                fileStream: FileStream   = FileStream(fqFileName)
                lexer:      Python3Lexer = Python3Lexer(fileStream)

                stream: CommonTokenStream = CommonTokenStream(lexer)
                parser: Python3Parser     = Python3Parser(stream)

                tree: Python3Parser.File_inputContext = parser.file_input()
                if parser.getNumberOfSyntaxErrors() != 0:
                    self.logger.error(f"File {fileName} contains {parser.getNumberOfSyntaxErrors()} syntax errors")
                    # TODO:  Put up a dialog
                    continue

                self.visitor = PyutPythonVisitor()
                self.visitor.parents = onGoingParents
                self.visitor.visit(tree)
                self._generatePyutClasses()

                onGoingParents = self.visitor.parents
                currentFileCount += 1
            except (ValueError, Exception) as e:
                from org.pyut.errorcontroller.ErrorManager import ErrorManager
                eMsg: str = f'file: {fileName}\n{e} - {ErrorManager.getErrorInfo()}'
                self.logger.error(eMsg)
                dlg.Destroy()
                raise PythonParseException(eMsg)
        dlg.Destroy()
        self._generateOglClasses(umlFrame)
        self._layoutUmlClasses(umlFrame)
        self._generateInheritanceLinks(umlFrame)

    def _generatePyutClasses(self):

        for className in self._classNames():
            pyutClass: PyutClass = PyutClass(name=className)

            pyutClass = self._addFields(pyutClass)

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

            setterProperties: Parameters = self.visitor.setterProperties
            getterProperties: Parameters = self.visitor.getterProperties

            pyutClass = self._generatePropertiesAsMethods(pyutClass, getterProperties, setterProperties)

            if className in self.visitor.dataClassNames:
                self._createDataClassPropertiesAsFields(pyutClass, self.visitor.dataClassProperties)

            self._pyutClasses[className] = pyutClass
        self.logger.info(f'Generated {len(self._pyutClasses)} classes')

    def _generatePropertiesAsMethods(self, pyutClass: PyutClass, getterProperties, setterProperties) -> PyutClass:

        for propName in self.visitor.propertyNames:
            # Might be a read-only property
            try:
                setterParams: List[str] = setterProperties[propName]
            except KeyError:
                setterParams = []

            getterParams: List[str] = getterProperties[propName]
            self.logger.info(f'Processing - {propName=} {setterParams=} {getterParams=}')
            setter, getter = self._createProperties(propName=propName, setterParams=setterParams)
            if setter is not None:
                setter.isProperty = True
                pyutClass.addMethod(setter)
            getter.isProperty = True
            pyutClass.addMethod(getter)

        return pyutClass

    def _createProperties(self, propName: str, setterParams: List[str]) -> Tuple[PyutMethod, PyutMethod]:

        getter: PyutMethod = PyutMethod(name=propName, visibility=PyutVisibilityEnum.PUBLIC)
        if len(setterParams) == 0:
            setter: PyutMethod = cast(PyutMethod, None)
        else:
            setter = PyutMethod(name=propName, visibility=PyutVisibilityEnum.PUBLIC)

        if setter is not None:
            nameType: str = setterParams[0]
            potentialNameType: List[str] = nameType.split(':')

            if len(potentialNameType) == 2:

                param: PyutParameter = PyutParameter(name=potentialNameType[0], parameterType=PyutType(value=potentialNameType[1]))
                setter.addParameter(param)
                getter.returnType = PyutType(value=potentialNameType[1])
            else:
                param = PyutParameter(name=potentialNameType[0])
                setter.addParameter(param)

        return setter, getter

    def _createDataClassPropertiesAsFields(self, pyutClass: PyutClass, dataClassProperties: DataClassProperties) -> PyutClass:
        """

        Args:
            pyutClass:  The PyutClass to update
            dataClassProperties:    The dataclass properties to parse

        Returns:
            Updated PyutClass with new fields
        """
        className: str = pyutClass.name
        for dPropertyTuple in dataClassProperties:
            if dPropertyTuple[0] == className:

                pyutField: PyutField = self._parseFieldToPyut(fieldData=dPropertyTuple[1])
                pyutClass.addField(pyutField)

        return pyutClass

    def _addParameters(self, pyutMethod: PyutMethod) -> PyutMethod:

        methodName: MethodName = MethodName(pyutMethod.name)
        if methodName in self.visitor.parameters:
            multiParameterNames: MultiParameterNames = self.visitor.parameters[methodName]

            pyutParameters: PyutParameters = self._generateParameters(multiParameterNames)
            pyutMethod.parameters = pyutParameters

        return pyutMethod

    def _addFields(self, pyutClass: PyutClass) -> PyutClass:
        """
        Can look like this:

           fieldData: x:int=0
           fieldData = 0

        Args:
            pyutClass:  Where to add the fields

        Returns:  The updated input class

        """
        for fieldData in self.visitor.fields:
            self.logger.debug(f'fieldData: {fieldData}')
            pyutField: PyutField = self._parseFieldToPyut(fieldData)
            pyutClass.addField(pyutField)

        return pyutClass

    def _generateOglClasses(self, umlFrame: UmlClassDiagramsFrame):

        for pyutClassName in self._pyutClasses:
            try:
                pyutClass: PyutClass = self._pyutClasses[pyutClassName]
                oglClass:  OglClass = OglClass(pyutClass)
                umlFrame.addShape(oglClass, 0, 0)
                oglClass.autoResize()

                self._oglClasses[pyutClassName] = oglClass
            except (ValueError, Exception) as e:
                self.logger.error(f"Error while creating class {pyutClassName},  {e}")

    def _generateInheritanceLinks(self, umlFrame: UmlClassDiagramsFrame):

        parents: Parents = self.visitor.parents

        for parentName in parents.keys():
            children: Children = parents[parentName]
            for childName in children:

                try:
                    parentOglClass: OglClass = self._oglClasses[parentName]
                    childOglClass:  OglClass = self._oglClasses[childName]
                    self.__createInheritanceLink(child=childOglClass, parent=parentOglClass, umlFrame=umlFrame)
                except KeyError as ke:        # Probably there is no parent we are tracking
                    self.logger.warning(f'Apparently we are not tracking this parent:  {ke}')
                    continue

    def _methodNames(self, className: ClassName) -> MethodNames:

        methodNames: MethodNames = MethodNames([])
        try:
            methodNames = self.visitor.classMethods[className]
        except KeyError:
            self.logger.warning(f'{className} has no methods')

        return methodNames

    def _classNames(self) -> ClassNames:
        return self.visitor.classNames

    def _layoutUmlClasses(self, umlFrame: UmlClassDiagramsFrame):
        """
        Organize by vertical descending sizes

        Args:
            umlFrame:
        """
        oglClasses: List[OglClass] = list(self._oglClasses.values())
        # Sort by descending height
        # noinspection PyProtectedMember
        sortedOglClasses = sorted(oglClasses, key=lambda oglClassToSort: oglClassToSort._height, reverse=True)

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

    def _parseFieldToPyut(self, fieldData: str) -> PyutField:

        self.logger.debug(f'fieldData: {fieldData}')

        if ReverseEngineerPython2.PYTHON_TYPE_DELIMITER in fieldData and ReverseEngineerPython2.PYTHON_ASSIGNMENT in fieldData:
            pyutField: PyutField = self.__complexParseFieldToPyut(fieldData)
        else:
            pyutField = self.__simpleParseFieldToPyut(fieldData)

        return pyutField

    def _generateParameters(self, multiParameterNames: str) -> PyutParameters:
        """
        Handles the following 4 cases:
        Simple:                       param
        Typed:                        param: float
        SimpleDefaultValue:           param=0.0
        ComplexTypedAndDefaultValue: param: float = 0.0
        Args:
            multiParameterNames:

        Returns:  A list of PyutParam objects
        """
        parameterNameList: List[str] = multiParameterNames.split(',')
        pyutParams:        PyutParameters = PyutParameters([])
        for parameterStr in parameterNameList:
            if ':' in parameterStr and '=' in parameterStr:
                pyutParam: PyutParameter = self.__complexTypedAndDefaultValue(parameterStr)
            elif '=' in parameterStr:
                pyutParam = self._simpleDefaultValue(parameterStr)
            elif ':' in parameterStr:
                pyutParam = self._typedParameter(parameterStr)
            else:
                pyutParam = PyutParameter(parameterStr)
            pyutParams.append(pyutParam)

        return pyutParams

    def __complexTypedAndDefaultValue(self, complexParam: str) -> PyutParameter:

        paramNameType:  List[str] = complexParam.split(':')
        paramName:      str = paramNameType[0]
        paramTypeValue: List[str] = paramNameType[1].split('=')
        paramType:      str = paramTypeValue[0]
        paramValue:     str = paramTypeValue[1]

        pyutType: PyutType = PyutType(paramType)
        return PyutParameter(name=paramName, parameterType=pyutType, defaultValue=paramValue)

    def _simpleDefaultValue(self, simpleDefaultValueParam: str) -> PyutParameter:

        pyutParamAndValue: List[str] = simpleDefaultValueParam.split('=')
        paramName:  str = pyutParamAndValue[0]
        paramValue: str = pyutParamAndValue[1]

        pyutParam: PyutParameter = PyutParameter(name=paramName, defaultValue=paramValue)

        return pyutParam

    def _typedParameter(self, typedParam: str) -> PyutParameter:
        pyutParamAndType: List[str] = typedParam.split(':')
        paramName:        str = pyutParamAndType[0]
        paramType:        str = pyutParamAndType[1]

        pyutParam: PyutParameter = PyutParameter(name=paramName, parameterType=PyutType(value=paramType))
        return pyutParam

    def __simpleParseFieldToPyut(self, fieldData: str) -> PyutField:

        pyutField: PyutField = PyutField()

        noCommentFieldData: str = self.__stripEndOfLineComment(fieldData)
        fieldAndValue: List[str] = noCommentFieldData.split(ReverseEngineerPython2.PYTHON_ASSIGNMENT)

        if len(fieldAndValue) == 2:
            pyutField.name         = fieldAndValue[0].strip()
            pyutField.defaultValue = fieldAndValue[1].strip()
        else:   # might just be a declaration
            pyutField = self.__declarationOnlyParseToPyut(fieldData=fieldAndValue[0])
        return pyutField

    def __complexParseFieldToPyut(self, fieldData: str) -> PyutField:
        """
          Can look like this:

           fieldData: x:int=0

        Args:
            fieldData:

        Returns:
        """
        noCommentFieldData: str = self.__stripEndOfLineComment(fieldData)

        fieldAndType: List[str] = noCommentFieldData.split(ReverseEngineerPython2.PYTHON_TYPE_DELIMITER)
        fieldName:    str       = fieldAndType[0]

        vis: PyutVisibilityEnum = self.__determineFieldVisibility(fieldName)

        fieldName = self.__appropriatelyCleanupName(vis=vis, fieldName=fieldName)

        pyutField: PyutField = PyutField(name=fieldName, visibility=vis)

        if len(fieldAndType) > 1:
            typeAndDefaultValue: List[str] = fieldAndType[1].split(ReverseEngineerPython2.PYTHON_ASSIGNMENT)

            pyutType: PyutType = PyutType(value=typeAndDefaultValue[0].strip())
            pyutField.type = pyutType
            if len(typeAndDefaultValue) > 1:
                pyutField.defaultValue = typeAndDefaultValue[1].strip()

        return pyutField

    def __declarationOnlyParseToPyut(self, fieldData: str) -> PyutField:

        self.logger.info(f'{fieldData=}')
        fieldAndType: List[str] = fieldData.split(ReverseEngineerPython2.PYTHON_TYPE_DELIMITER)

        pyutField: PyutField = PyutField(name=fieldAndType[0])

        #
        # Might be something complex expression as a default value we can't handle it
        #
        if len(fieldAndType) > 1:
            pyutField.type       = PyutType(value=fieldAndType[1])
        pyutField.visibility = PyutVisibilityEnum.PUBLIC

        return pyutField

    def __determineFieldVisibility(self, name: str) -> PyutVisibilityEnum:

        vis: PyutVisibilityEnum = PyutVisibilityEnum.PUBLIC
        if len(name) > 1:
            if name[-2:] != "__":
                if name[0:2] == "__":
                    vis = PyutVisibilityEnum.PRIVATE
                elif name[0] == "_":
                    vis = PyutVisibilityEnum.PROTECTED
        return vis

    def __appropriatelyCleanupName(self, vis: PyutVisibilityEnum, fieldName: str) -> str:

        if vis == PyutVisibilityEnum.PUBLIC:
            return fieldName
        elif vis == PyutVisibilityEnum.PRIVATE:
            fieldName = fieldName[2:]
            return fieldName
        else:
            fieldName = fieldName[1:]
            return fieldName

    def __stripEndOfLineComment(self, fieldData: str) -> str:

        fieldAndComment: List[str] = fieldData.split(ReverseEngineerPython2.PYTHON_EOL_COMMENT)

        return fieldAndComment[0]

    def __createInheritanceLink(self, child: OglClass, parent: OglClass, umlFrame: UmlClassDiagramsFrame):
        """
        Add a paternity link between child and father.

        Args:
            child:  A child
            parent: The daddy!!

        Returns: an OgLink

        """
        cmdGroup: CommandGroup         = CommandGroup('Creating an inheritance link')
        # inheritance points back to parent
        cmd: CreateOglLinkCommand = CreateOglLinkCommand(src=child, dst=parent)
        cmdGroup.addCommand(cmd)

        historyManager: HistoryManager = umlFrame.getHistory()
        historyManager.addCommandGroup(cmdGroup)

        cmd.execute()

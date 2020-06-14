
from typing import Dict
from typing import List

from logging import Logger
from logging import getLogger

from org.pyut.plugins.iopythonsupport.pyantlrparser.Python3Parser import Python3Parser
from org.pyut.plugins.iopythonsupport.pyantlrparser.Python3Visitor import Python3Visitor


class PyutPythonVisitor(Python3Visitor):

    PYTHON_SELF:       str = 'self'
    PYTHON_SELF_COMMA: str = f'{PYTHON_SELF},'

    MethodName     = str
    ClassName      = str
    ParameterNames = str                # comma separated parameter names
    MethodCode     = List[str]

    MethodNames    = List[MethodName]
    ParameterNames = List[ParameterNames]

    Methods    = Dict[ClassName, MethodNames]
    Parameters = Dict[MethodName, ParameterNames]
    MethodCode = Dict[MethodName, MethodCode]

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self.classMethods: PyutPythonVisitor.Methods    = {}
        self.parameters:   PyutPythonVisitor.Parameters = {}
        self.methodCode:   PyutPythonVisitor.MethodCode = {}

    def visitFuncdef(self, ctx: Python3Parser.FuncdefContext):

        className = self._checkIfMethodBelongsToClass(ctx, Python3Parser.ClassdefContext)
        if className:
            methodName = ctx.getChild(1).getText()
            self.logger.debug(f'visitFuncdef: methodName: {methodName}')
            if className not in self.classMethods:
                self.classMethods[className] = [methodName]
            else:
                self.classMethods[className].append(methodName)

            self.__getMethodCode(methodName, ctx)

        return super().visitChildren(ctx)

    def visitClassdef(self, ctx: Python3Parser.ClassdefContext):

        className: str = ctx.getChild(1).getText()
        self.logger.debug(f'visitClassdef: Visited class: {className}')

        return super().visitClassdef(ctx)

    def visitParameters(self, ctx: Python3Parser.ParametersContext):

        if len(ctx.children) > 1:
            parameterNames: PyutPythonVisitor.ParameterNames = ctx.getChild(1).getText()
            methodName:     PyutPythonVisitor.MethodName     = self._getParametersMethodName(ctx.parentCtx)
            self.logger.debug(f'visitParameters: Visited parameterNames: {parameterNames} in method {methodName}')

            if parameterNames != PyutPythonVisitor.PYTHON_SELF:
                strippedParameterNames: PyutPythonVisitor.ParameterNames = parameterNames.replace(PyutPythonVisitor.PYTHON_SELF_COMMA, "")
                if strippedParameterNames not in self.parameters:
                    self.parameters[methodName] = [strippedParameterNames]
                else:
                    self.parameters[methodName].append(strippedParameterNames)

        return super().visitChildren(ctx)

    def _checkIfMethodBelongsToClass(self, node: Python3Parser.FuncdefContext, classType):

        while node.parentCtx:
            if isinstance(node, classType):
                return node.getChild(1).getText()
            node = node.parentCtx
        return None

    def _getParametersMethodName(self, parentCtx: Python3Parser.FuncdefContext) -> MethodName:

        methodName: PyutPythonVisitor.MethodName = parentCtx.getChild(1).getText()
        return methodName

    def __getMethodCode(self, methodName: MethodName, ctx: Python3Parser.FuncdefContext):

        methodText:     str       = ctx.getText()
        splitText:      List[str] = methodText.split('\n')
        justMethodCode: List[str] = splitText[1:len(splitText)]

        self.logger.debug(f'justMethodCode: {justMethodCode}')

        self.methodCode[methodName] = justMethodCode

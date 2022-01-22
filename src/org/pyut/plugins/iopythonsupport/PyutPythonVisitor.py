
from typing import Dict
from typing import List
from typing import NewType
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from antlr4 import ParserRuleContext

from org.pyut.plugins.iopythonsupport.pyantlrparser.Python3Parser import Python3Parser
from org.pyut.plugins.iopythonsupport.pyantlrparser.Python3Visitor import Python3Visitor

MethodName          = NewType('MethodName', str)
PropertyName        = NewType('PropertyName', str)
ClassName           = NewType('ClassName', str)
ParentName          = str
ChildName           = str
MultiParameterNames = NewType('MultiParameterNames', str)  # comma separated parameter names
Field               = NewType('Field', str)
ExpressionText      = NewType('ExpressionText', str)
DataClassProperty   = NewType('DataClassProperty', Tuple[ClassName, ExpressionText])

ClassNames     = List[ClassName]
MethodNames    = List[MethodName]
ParameterNames = List[MultiParameterNames]
Fields         = List[Field]
Children       = List[ChildName]

Methods    = NewType('Methods', Dict[ClassName, MethodNames])
Parameters = NewType('Parameters', Dict[MethodName, ParameterNames])
MethodCode = NewType('MethodCode', Dict[MethodName, str])
Parents    = Dict[ParentName, Children]

PropertyNames      = Dict[PropertyName, ClassName]
PropertyParameters = Dict[PropertyName, ParameterNames]

DataClassProperties = List[DataClassProperty]


class PyutPythonVisitor(Python3Visitor):

    PYTHON_SELF:         str = 'self'
    PYTHON_SELF_COMMA:   str = f'{PYTHON_SELF},'
    FIELD_IDENTIFIER:    str = f'{PYTHON_SELF}.'
    PYTHON_CONSTRUCTOR:  str = '__init__'
    PROPERTY_DECORATOR:  str = '@property'
    DATACLASS_DECORATOR: str = '@dataclass'

    NON_PROPERTY_INDICATOR: str = '\n'

    PYTHON_EQUALITY_TOKEN: str = '='

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self.classNames:   ClassNames = []
        self.classMethods: Methods    = Methods({})
        self.parameters:   Parameters = Parameters({})
        self.methodCode:   MethodCode = MethodCode({})
        self.fields:       Fields     = []
        self._parents:     Parents    = {}

        self.propertyNames:    PropertyNames = {}
        self.setterProperties: Parameters    = Parameters({})
        self.getterProperties: Parameters    = Parameters({})

        self.dataClassNames:      ClassNames          = []
        self.dataClassProperties: DataClassProperties = []

    @property
    def parents(self) -> Parents:
        return self._parents

    @parents.setter
    def parents(self, additionalParents: Parents):
        self._parents = additionalParents

    def visitFuncdef(self, ctx: Python3Parser.FuncdefContext):

        className = self._checkIfMethodBelongsToClass(ctx, Python3Parser.ClassdefContext)
        if className:
            methodName = ctx.getChild(1).getText()
            if not self.__isProperty(methodName):
                self.logger.debug(f'visitFuncdef: {methodName=}')
                if className not in self.classMethods:
                    self.classMethods[className] = [methodName]
                else:
                    self.classMethods[className].append(methodName)

                self.__getMethodCode(methodName, ctx)

        return super().visitChildren(ctx)

    def visitDecorated(self, ctx: Python3Parser.DecoratedContext):

        funcDef  = ctx.funcdef()
        decorator: str = ctx.getChild(0).getText()
        #
        # Take care of data classes
        #
        if funcDef is not None:
            propName:  PropertyName = funcDef.getChild(1).getText()
            propCode:  str = ctx.getChild(1).getText()
            if self.__isPropertyDecorator(nameToCheck=decorator) is True:
                self.logger.info(f'visitDecorated - {decorator=} {propName=} {propCode=}')

                className: ClassName = self._checkIfMethodBelongsToClass(ctx, Python3Parser.ClassdefContext)

                self.logger.info(f'Update property names - {propName}')
                self.propertyNames[propName] = className
        elif self.__isDataClassDecorator(nameToCheck=decorator):
            className = ctx.classdef().getChild(1).getText()
            self.logger.info(f'visitDecorated -- We found dataclass: {className}')
            self.dataClassNames.append(className)

        return self.visitChildren(ctx)

    def visitClassdef(self, ctx: Python3Parser.ClassdefContext):

        className: ClassName = ClassName(ctx.getChild(1).getText())
        self.classNames.append(className)
        self.logger.debug(f'visitClassdef: Visited class: {className}')

        argListCtx: Python3Parser.ArglistContext = self._findArgListContext(ctx)
        if argListCtx is not None:
            self._createParentChildEntry(argListCtx, className)

        return super().visitClassdef(ctx)

    def visitParameters(self, ctx: Python3Parser.ParametersContext):

        if len(ctx.children) > 1:
            parameterNames: MultiParameterNames = ctx.getChild(1).getText()
            methodName:     MethodName          = self._getParametersMethodName(ctx.parentCtx)
            self.logger.debug(f'visitParameters: method {methodName=} {parameterNames=} ')

            if self.__isProperty(methodName=methodName):
                if parameterNames == PyutPythonVisitor.PYTHON_SELF:
                    self.getterProperties[methodName] = ['']
                else:
                    strippedParameterNames: MultiParameterNames = MultiParameterNames(parameterNames.replace(PyutPythonVisitor.PYTHON_SELF_COMMA, ""))
                    self.setterProperties[methodName] = [strippedParameterNames]
            else:
                if parameterNames != PyutPythonVisitor.PYTHON_SELF:
                    strippedParameterNames: MultiParameterNames = MultiParameterNames(parameterNames.replace(PyutPythonVisitor.PYTHON_SELF_COMMA, ""))
                    if strippedParameterNames not in self.parameters:
                        self.parameters[methodName] = [strippedParameterNames]
                    else:
                        self.parameters[methodName].append(strippedParameterNames)    # TODO this is does not execute; what was I thinking

        return super().visitChildren(ctx)

    def visitExpr_stmt(self, ctx: Python3Parser.Expr_stmtContext):

        exprText: str = ctx.getText()

        if exprText.startswith(PyutPythonVisitor.FIELD_IDENTIFIER) is True:
            areWeInInitMethod: bool = self.__isThisInitMethod(ctx)
            areWeAnAssignment: bool = self.__isThisAFieldAssignment(exprText)
            if areWeInInitMethod is True and areWeAnAssignment is True:
                self.logger.debug(f'Field expression: {exprText}')
                self.fields.append(Field(exprText.replace(PyutPythonVisitor.FIELD_IDENTIFIER, '')))
        else:
            isDataClass, dataClassName = self.__isThisADataClassProperty(ctx)
            if isDataClass is True:
                self.logger.info(f'Non-init:  {exprText=}')
                if PyutPythonVisitor.NON_PROPERTY_INDICATOR in exprText:
                    pass
                else:
                    dataClassProperty: DataClassProperty = DataClassProperty((dataClassName, exprText))
                    self.dataClassProperties.append(dataClassProperty)

        return super().visitChildren(ctx)

    def _checkIfMethodBelongsToClass(self, node: ParserRuleContext, classType) -> ClassName:

        while node.parentCtx:
            if isinstance(node, classType):
                return node.getChild(1).getText()
            node = node.parentCtx
        return cast(ClassName, None)

    def _getParametersMethodName(self, parentCtx: Python3Parser.FuncdefContext) -> MethodName:

        methodName: MethodName = parentCtx.getChild(1).getText()
        return methodName

    def _createParentChildEntry(self, parentCtx: Python3Parser.ArglistContext, childName: str):

        parentName: str = parentCtx.getText()
        self.logger.debug(f'Class: {childName} is subclass of {parentName}')

        if parentName in self._parents:
            children: Children = self._parents[parentName]
            children.append(childName)
        else:
            children = [childName]

        self._parents[parentName] = children

    def __getMethodCode(self, methodName: MethodName, ctx: Python3Parser.FuncdefContext):

        methodText:     str       = ctx.getText()
        splitText:      List[str] = methodText.split('\n')
        justMethodCode: List[str] = splitText[1:len(splitText)]

        self.logger.debug(f'justMethodCode: {justMethodCode}')

        self.methodCode[methodName] = justMethodCode

    def _findArgListContext(self, ctx: Python3Parser.ClassdefContext) -> Python3Parser.ArglistContext:

        argListCtx: Python3Parser.ArglistContext = cast(Python3Parser.ArglistContext, None)
        for childCtx in ctx.children:
            if isinstance(childCtx, Python3Parser.ArglistContext):
                argListCtx = childCtx
                break

        return argListCtx

    def __isThisInitMethod(self, ctx: Python3Parser.Expr_stmtContext) -> bool:

        ans: bool = False

        methodCtx: Python3Parser.FuncdefContext = self.__findMethodContext(ctx)
        if methodCtx is not None:
            methodName: str = methodCtx.getChild(1).getText()
            if methodName == PyutPythonVisitor.PYTHON_CONSTRUCTOR:
                ans = True

        return ans

    def __isThisAFieldAssignment(self, exprText: str):

        ans: bool = False
        if PyutPythonVisitor.PYTHON_EQUALITY_TOKEN in exprText:
            ans = True

        return ans

    def __findMethodContext(self, ctx: Python3Parser.Expr_stmtContext) -> Python3Parser.FuncdefContext:

        currentCtx: ParserRuleContext = ctx

        while isinstance(currentCtx, Python3Parser.FuncdefContext) is False:
            currentCtx = currentCtx.parentCtx
            if currentCtx is None:
                break

        if currentCtx is not None:
            self.logger.debug(f'Found method: {currentCtx.getChild(1).getText()}')

        return cast(Python3Parser.FuncdefContext, currentCtx)

    def __isProperty(self, methodName: MethodName) -> bool:
        """
        Used by the function definition visitor to determine if the method name that is being
        visited has been marked as a property.

        Args:
            methodName:  The method name to check

        Returns: True if its is in our know list of property names
        """
        ans: bool = False

        if methodName in self.propertyNames:
            ans = True

        return ans

    def __isPropertyDecorator(self, nameToCheck: str) -> bool:

        ans: bool = False

        if nameToCheck.startswith(PyutPythonVisitor.PROPERTY_DECORATOR):
            ans = True
        else:
            strippedText: str = nameToCheck.lstrip('@')
            splitText: List[str] = strippedText.split('.')
            propName: str = splitText[0]
            if propName in self.propertyNames:
                ans = True

        return ans

    def __isDataClassDecorator(self, nameToCheck: str) -> bool:

        ans: bool = False

        if nameToCheck.startswith(PyutPythonVisitor.DATACLASS_DECORATOR):
            ans = True

        return ans

    def __isThisADataClassProperty(self, startCtx: ParserRuleContext) -> Tuple[bool, str]:
        """

        Args:
            startCtx:

        Returns:
            A Tuple that a boolean answering the question.  If the answer is true
            then the 2nd value of the tuple is the data class name
        """

        dataClassName: str = self.__getPotentialDataClassName(startCtx)

        ans: bool = False
        if dataClassName in self.dataClassNames:
            ans = True

        self.logger.info(f'isDataClass: {ans} - {dataClassName=}')

        return ans, dataClassName

    def __getPotentialDataClassName(self, startCtx: ParserRuleContext):

        potentialDataClassName: str               = ''
        parentCtx:              ParserRuleContext = startCtx

        while parentCtx is not None:
            # self.logger.info(f'{parentCtx=}')
            if isinstance(parentCtx, Python3Parser.ClassdefContext):
                potentialDataClassName = parentCtx.getChild(1).getText()
                self.logger.info(f'{potentialDataClassName=}')

            if isinstance(parentCtx, Python3Parser.DecoratedContext):
                decorator: str = parentCtx.getChild(0).getText()
                self.logger.info(f'visitSimple_stmt - {decorator=}  {potentialDataClassName=}')
            parentCtx = parentCtx.parentCtx

        return potentialDataClassName

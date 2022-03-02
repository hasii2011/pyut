from typing import List
from typing import Tuple

from org.pyut.history.HistoryUtils import deTokenize
from org.pyut.history.HistoryUtils import tokenizeValue

from org.pyut.model.PyutClassCommon import PyutClassCommon
from org.pyut.model.PyutMethod import PyutMethod
from org.pyut.model.PyutParameter import PyutParameter
from org.pyut.model.PyutType import PyutType
from org.pyut.model.PyutVisibilityEnum import PyutVisibilityEnum


class MethodInformation:
    """
    Can deserialize the common shared information shared
    """

    @classmethod
    def serialize(cls, pyutClassCommon: PyutClassCommon) -> str:

        serializedInfo: str = ''

        methods = []
        for method in pyutClassCommon.methods:
            methodName:       str = method.name
            methodVisibility: str = method.visibility.__str__()
            methodReturns:    str = method.getReturns().__str__()

            params = []
            for param in method.parameters:
                paramName: str = param.name
                paramType: str = param.type.__str__()
                paramDefaultValue: str = param.defaultValue

                params.append((paramName, paramType, paramDefaultValue))

            modifiers = []
            for modifier in method.modifiers:
                modifierName = modifier.name
                modifiers.append(modifierName)

            methodProfile: Tuple[str, str, str, str, str] = (methodName, methodVisibility, methodReturns, repr(params), repr(modifiers))

            methods.append(methodProfile)

        classDescription:    str = pyutClassCommon.description

        serializedInfo += tokenizeValue("classDescription", classDescription)
        serializedInfo += tokenizeValue("methods", repr(methods))

        return serializedInfo

    @classmethod
    def deserialize(cls, serializedData: str, pyutObject: PyutClassCommon) -> PyutClassCommon:
        """

        Args:
            serializedData:
            pyutObject:

        Returns:  The updated PyutClass or PyutInterface

        """

        classDescription  = deTokenize("classDescription", serializedData)

        pyutObject.description = classDescription

        methods = eval(deTokenize("methods", serializedData))

        pyutMethods: List[PyutMethod] = []

        for methodProfile in methods:

            # construction of a method
            methodName:       str = methodProfile[0]
            methodVisibility: PyutVisibilityEnum = PyutVisibilityEnum.toEnum(methodProfile[1])
            methodReturns:    PyutType            = PyutType(value=methodProfile[2])

            pyutMethod: PyutMethod = PyutMethod(name=methodName, visibility=methodVisibility, returnType=methodReturns)

            # deserialize method's parameters;  Get the tuple (name, Type, defaultValue)
            params = eval(methodProfile[3])
            for param in params:
                paramName:         str      = param[0]
                paramType:         PyutType = PyutType(param[1])
                paramDefaultValue: str      = param[2]

                # creates and add the param to the method
                pyutParam: PyutParameter = PyutParameter(name=paramName, parameterType=paramType, defaultValue=paramDefaultValue)
                pyutMethod.addParameter(pyutParam)

            pyutMethods.append(pyutMethod)

        pyutObject.methods = pyutMethods
        return pyutObject

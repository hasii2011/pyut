
from typing import Tuple

from org.pyut.history.HistoryUtils import makeValuatedToken

from org.pyut.model.PyutClassCommon import PyutClassCommon


class MethodInformation:
    """
    Can deserializes the common information shared by an
    """

    @classmethod
    def serialize(cls, pyutClassCommon: PyutClassCommon) -> str:

        serializedInfo: str = ''

        methods = []
        for method in pyutClassCommon.methods:
            methodName:       str = method.getName()
            methodVisibility: str = method.getVisibility().__str__()
            methodReturns:    str = method.getReturns().__str__()

            params = []
            for param in method.getParams():
                paramName: str = param.getName()
                paramType: str = param.getType().__str__()
                paramDefaultValue: str = param.getDefaultValue()

                params.append((paramName, paramType, paramDefaultValue))

            modifiers = []
            for modifier in method.getModifiers():
                modifierName = modifier.getName()
                modifiers.append(modifierName)

            methodProfile: Tuple[str, str, str, str, str] = (methodName, methodVisibility, methodReturns, repr(params), repr(modifiers))

            methods.append(methodProfile)

        classDescription:    str = pyutClassCommon.description

        serializedInfo += makeValuatedToken("classDescription", classDescription)
        serializedInfo += makeValuatedToken("methods",          repr(methods))

        return serializedInfo

    @classmethod
    def deserialize(cls, serializedData: str, pyutObject: PyutClassCommon) -> PyutClassCommon:
        """

        Args:
            serializedData:
            pyutObject:

        Returns:  The updated PyutClass or PyutInterface

        """

        return pyutObject

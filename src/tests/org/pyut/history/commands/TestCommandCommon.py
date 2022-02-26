
from org.pyut.model.PyutMethod import PyutMethod
from org.pyut.model.PyutParam import PyutParam
from org.pyut.model.PyutType import PyutType

from org.pyut.model.PyutVisibilityEnum import PyutVisibilityEnum


class TestCommandCommon:

    methodParamNumber: int = 1
    methodTypeNumber:  int = 1

    @classmethod
    def createTestMethod(cls, name: str, visibility: PyutVisibilityEnum, returnType: PyutType) -> PyutMethod:

        pyutMethod: PyutMethod = PyutMethod()

        pyutMethod.name       = name
        pyutMethod.visibility = visibility
        pyutMethod.returnType = returnType

        pyutParam: PyutParam = PyutParam(name=f'param{TestCommandCommon.methodParamNumber}',
                                         parameterType=PyutType(f'Type{TestCommandCommon.methodTypeNumber}'),
                                         defaultValue='')

        pyutMethod.addParam(pyutParam)

        TestCommandCommon.methodParamNumber += 1
        TestCommandCommon.methodTypeNumber  += 1

        return pyutMethod

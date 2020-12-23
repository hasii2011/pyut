from inspect import getfullargspec

from typing import List
from typing import Callable
from typing import cast

from logging import Logger
from logging import getLogger

from org.pyut.model.PyutClass import PyutClass
from org.pyut.model.PyutMethod import PyutMethod
from org.pyut.model.PyutParam import PyutParam
from org.pyut.model.PyutType import PyutType
from org.pyut.model.PyutVisibilityEnum import PyutVisibilityEnum


class PythonMetaClassDataHandler:
    """

    """
    def __init__(self):

        self.logger: Logger = getLogger(__name__)

    def getClassListFromNames(self, classNames: List[str]) -> List[type]:
        """
        Get a list of classes info for classes in the name list

        Args:
            classNames:  This list of non-FQ class names

        Returns:

        """
        import org.pyut.experimental.PyutDataClasses as pdc

        self.logger.debug(f'pdc value {pdc.__dict__.values()}')

        classes: List[type] = []
        for clsType in pdc.__dict__.values():

            self.logger.debug(f"clsType: '{clsType}' isinstance(clsType, type): '{isinstance(clsType, type)}' type(clsType): '{type(clsType)}'")
            if isinstance(clsType, type) or type(clsType) == 'module':
                if clsType.__name__ in classNames:
                    self.logger.debug(f'clsType.__name__: `{clsType.__name__}`')
                    classes.append(clsType)
        return classes

    def getMethodsFromClass(self, clsType) -> List[classmethod]:

        clsMethods: List[classmethod] = cast(List[classmethod], [])
        for aMethod in clsType.__dict__.values():
            try:
                if isinstance(aMethod, Callable):
                    methName: str = aMethod.__name__
                    self.logger.debug(f'methName: {methName}')
                    if methName != '__str__' and methName != '__repr__':
                        clsMethods.append(aMethod)
            except AttributeError as e:
                self.logger.warning(f'Attribute Error: {e}')

        return clsMethods

    def generatePyutMethods(self, clsMethods: List[classmethod]) -> List[PyutMethod]:

        methods: List[PyutMethod] = []
        for me in clsMethods:
            funcName: str        = me.__name__
            meth:     PyutMethod = PyutMethod(funcName)

            if me is not None:
                args = getfullargspec(me)
                if args[3] is None:
                    firstDefVal = len(args[0])
                else:
                    firstDefVal = len(args[0]) - len(args[3])
                for arg, i in zip(args[0], range(len(args[0]))):
                    # don't add self, it's implied
                    if arg != "self":
                        if i >= firstDefVal:
                            defVal = args[3][i - firstDefVal]
                            if isinstance(defVal, str):
                                defVal = f'"{defVal}"'
                            param = PyutParam(arg, PyutType(""), str(defVal))
                        else:
                            param = PyutParam(arg)
                        meth.addParam(param)
            methods.append(meth)
            # set the visibility according to naming conventions
            func_name = funcName
            if func_name[-2:] != "__":
                if func_name[0:2] == "__":
                    meth.visibility = PyutVisibilityEnum.PRIVATE
                elif func_name[0] == "_":
                    meth.visibility = PyutVisibilityEnum.PROTECTED

        return methods

    def getParentClassNames(self, classes, pyutClassDef: PyutClass) -> List[str]:

        import org.pyut.experimental.PyutDataClasses as pdc

        currentClass = pdc.__dict__.get(pyutClassDef.getName())
        parentClasses = [cl for cl in classes if cl.__name__ in map(lambda z: z.__name__, currentClass.__bases__)]

        self.logger.debug(f'parentClasses: `{parentClasses}`')

        def getClassesNames(theList):
            return [item.__name__ for item in theList]

        parentNames: List[str] = getClassesNames(parentClasses)
        return parentNames

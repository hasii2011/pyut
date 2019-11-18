from inspect import getfullargspec

from typing import List
from typing import Callable

from logging import Logger
from logging import getLogger

from org.pyut.PyutMethod import PyutMethod
from org.pyut.PyutParam import PyutParam


class ClassGenerator:
    """

    """
    def __init__(self):

        self.logger: Logger = getLogger(__name__)

    def getClassListFromNames(self, classNames: List[str]):
        """
        Get a list of classes info for classes in the name list

        Args:
            classNames:  This list of non-FQ class names

        Returns:

        """
        import PyutDataClasses as pdc

        self.logger.debug(f'pdc value {pdc.__dict__.values()}')

        classes = []
        for clsType in pdc.__dict__.values():

            self.logger.debug(f"clsType: '{clsType}' isinstance(clsType, type): '{isinstance(clsType, type)}' type(clsType): '{type(clsType)}'")
            if isinstance(clsType, type) or type(clsType) == 'module':
                self.logger.debug(f'clsType.__name__: `{clsType.__name__}`')
                if clsType.__name__ in classNames:
                    classes.append(clsType)
        return classes

    def getMethodsFromClass(self, clsType):
        clmethods = []
        for methd in clsType.__dict__.values():
            if isinstance(methd, Callable):
                methName: str = methd.__name__
                self.logger.info(f'methName: {methName}')
                if methName != '__str__' and methName != '__repr__':
                    clmethods.append(methd)

        return clmethods

    def generatePyutMethods(self, clmethods) -> List[PyutMethod]:

        methods: List[PyutMethod] = []
        for me in clmethods:
            funcName: str = me.__name__
            meth = PyutMethod(funcName)

            if me is not None:
                args = getfullargspec(me)
                if args[3] is None:
                    firstDefVal = len(args[0])
                else:
                    firstDefVal = len(args[0]) - len(args[3])
                for arg, i in zip(args[0], range(len(args[0]))):
                    # don't add self, it's implied
                    # defVal = None
                    if arg != "self":
                        if i >= firstDefVal:
                            defVal = args[3][i - firstDefVal]
                            if isinstance(defVal, str):
                                defVal = f'"{defVal}"'
                            param = PyutParam(arg, "", str(defVal))
                        else:
                            param = PyutParam(arg)
                        meth.addParam(param)
            methods.append(meth)
            # set the visibility according to naming conventions
            func_name = funcName
            if func_name[-2:] != "__":
                if func_name[0:2] == "__":
                    meth.setVisibility("-")
                elif func_name[0] == "_":
                    meth.setVisibility("#")

            return methods

from types import FrameType
from types import ModuleType
from typing import List

from logging import Logger
from logging import getLogger

from inspect import FrameInfo

from inspect import getmodule
from inspect import stack

CLASS_IDENTIFIER:  str = 'self'
MODULE_IDENTIFIER: str = '<module>'


class Inspector:
    """
    Adapted from
        https://code.activestate.com/recipes/578352-get-full-caller-name-packagemodulefunction/

    TODO:  I am unsatisfied with the type hinting I managed to put in
    """
    def __init__(self):
        self.logger: Logger = getLogger(__name__)

    @classmethod
    def getCallerName(cls, skip: int = 2) -> str:
        """
        Get a name of a caller in the format module.class.method

        Args:
            skip: specifies how many levels of stack to skip while getting caller
                name. skip=1 means "who calls me", skip=2 "who calls my caller" etc.

        Returns:  An empty string is returned if skipped levels exceed stack height
        """
        stackList: List[FrameInfo] = stack()
        start:     int             = 0 + skip

        if len(stackList) < start + 1:
            return ''
        else:
            parentFrame: FrameType = stackList[start][0]
            name:        List[str] = []
            module:      ModuleType = getmodule(parentFrame)        # type: ignore

            # `module` can be None when frame is executed directly in console
            if module is not None:
                name.append(module.__name__)
            #
            # detect className
            #
            # noinspection PyUnresolvedReferences
            if CLASS_IDENTIFIER in parentFrame.f_locals:
                #
                # I don't know any way to detect call from the object method
                # There seems to be no way to detect static method call - it will be just a function call
                #

                # noinspection PyUnresolvedReferences
                clazz = parentFrame.f_locals[CLASS_IDENTIFIER]
                # fullyQualifiedClassName: str = parentFrame.f_locals[CLASS_IDENTIFIER].__class__.__name__
                fullyQualifiedClassName: str = clazz.__class__.__name__
                name.append(fullyQualifiedClassName)

            # noinspection PyUnresolvedReferences
            codeName: str = parentFrame.f_code.co_name
            if codeName != MODULE_IDENTIFIER:  # top level usually
                name.append(codeName)  # function or a method

            return ".".join(name)

    @classmethod
    def justClassMethodName(cls, fullyQualifiedName: str) -> str:

        parts: List[str] = fullyQualifiedName.split('.')

        partLen: int = len(parts)

        shortName: str = f'{parts[partLen-2]}.{parts[partLen-1]}'

        return shortName

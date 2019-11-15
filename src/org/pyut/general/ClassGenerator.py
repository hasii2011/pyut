
from typing import List
from typing import Callable

import types

from logging import Logger
from logging import getLogger


class ClassGenerator:

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
        for cl in pdc.__dict__.values():

            self.logger.debug(f"cl: '{cl}' isinstance(cl, type): '{isinstance(cl, type)}' type(cl): '{type(cl)}'")
            if isinstance(cl, type) or type(cl) == 'module':
                self.logger.debug(f'cl.__name__: `{cl.__name__}`')
                if cl.__name__ in classNames:
                    classes.append(cl)
        return classes

    def getMethodsFromClass(self, cl):
        clmethods = []
        for methd in cl.__dict__.values():
            if isinstance(methd, Callable):
                methName: str = methd.__name__
                self.logger.info(f'methName: {methName}')
                if methName != '__str__' and methName != '__repr__':
                    clmethods.append(methd)

        return clmethods

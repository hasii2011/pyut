
from typing import List

from logging import Logger
from logging import getLogger

from org.pyut.PyutClass import PyutClass
from org.pyut.ogl.OglClass import OglClass


class ElementTreeData:

    def __init__(self, pyutClass: PyutClass, oglClass: OglClass):

        self.logger: Logger = getLogger(__name__)

        self.pyutClass:         PyutClass  = pyutClass
        self.oglClass:          OglClass   = oglClass
        self._childElementNames: List[str] = []

    def getChildElementNames(self) -> List[str]:
        return self._childElementNames

    def setChildElementNames(self, theNewValues: List[str]):
        self._childElementNames = theNewValues

    childElementNames = property(getChildElementNames, setChildElementNames)

    def __str__(self):
        retStr: str = f'ElementTreeData - ClassName: {self.pyutClass.getName()} oglClass position: {self.oglClass.GetPosition()}\n'

        for childName in self.childElementNames:
            retStr += f'\t\tchildName: {childName}\n'
        return retStr

    def __repr__(self):
        return self.__str__()

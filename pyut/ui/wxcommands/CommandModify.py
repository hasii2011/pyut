
from typing import Any
from typing import List
from typing import NewType

from logging import Logger
from logging import getLogger

from wx import Command

from pyut.general.Globals import apply
# from pyut.preferences.PyutPreferences import PyutPreferences

Parameters = NewType('Parameters', List[Any])


class CommandModify(Command):

    def __init__(self, canUndo: bool, name: str, anyObject: object):

        self.logger: Logger = getLogger(__name__)

        super().__init__(canUndo=canUndo, name=name)

        # self._preferences: PyutPreferences = PyutPreferences()

        self._object: object = anyObject

        self._methodName:       str       = ''
        self._methodIsProperty: bool      = False
        self._oldParameters:    Parameters = Parameters([])
        self._newParameters:    Parameters = Parameters([])

    def CanUndo(self) -> bool:
        """

        Returns true if the command can be undone, false otherwise.
        """
        return True

    def Do(self) -> bool:
        """
        """
        assert self._methodName != '', 'You must set a method name'
        assert len(self._newParameters) != 0, 'You have have not saved the new parameters'
        if self.methodIsProperty is True:
            assert len(self._newParameters) == 1, 'Properties can only have a single parameter'
            setattr(self._object, self._methodName, self._newParameters[0])
        else:
            method = getattr(self._object, self._methodName)
            apply(method, self._newParameters)

        return True

    def Undo(self) -> bool:
        """
        """
        assert self._methodName != '', 'You must set a method name'
        assert len(self._oldParameters) != 0, 'You have have not saved the old parameters'
        if self.methodIsProperty is True:
            assert len(self._oldParameters) == 1, 'Properties can only have a single parameter'
            setattr(self._object, self._methodName, self._oldParameters[0])
        else:
            method = getattr(self._object, self._methodName)
            apply(method, self._oldParameters)

        return True

    @property
    def methodName(self) -> str:
        """
        Get the name of the method that does the modification.
        """
        assert self._methodName != '', 'You must set a method name'
        return self._methodName

    @methodName.setter
    def methodName(self, newName: str):
        """
        Set the name of the method that does the modification
        Args:
            newName:  The new Name
        """
        self._methodName = newName

    @property
    def methodIsProperty(self) -> bool:
        return self._methodIsProperty

    @methodIsProperty.setter
    def methodIsProperty(self, newValue: bool):
        self._methodIsProperty = newValue

    @property
    def oldParameters(self) -> Parameters:
        assert len(self._oldParameters) != 0, 'You have have not saved the old parameters'
        return self._oldParameters

    @oldParameters.setter
    def oldParameters(self, parameters: Parameters):
        """
        Set the parameters of the method that must be called to undo.
        Should be called before changes are performed.

        Args:
            parameters:  values that will be changed by the call of the method. Must be ordered as in the method profile.
        """
        self._oldParameters = parameters

    @property
    def newParameters(self) -> Parameters:
        assert len(self._newParameters) != 0, 'You have have not saved the new parameters'
        return self._newParameters

    @newParameters.setter
    def newParameters(self, parameters: Parameters):
        """
        Set the parameters of the method that must be called to redo.
        Should be called as soon as the parameters for change are known.

        Args:
            parameters: values that will be changed by calling the redo method. Must be ordered as in the method profile.
        """
        self._newParameters = parameters

    def _getModifiedObject(self, strObject, anObject):
        """
        @return the object that is represented by the string strObject. Used
        for deserialization.
        Notes : This method requires a lot of CPU resources and place on the
        stack. A refactoring must be proceeded in order to identify every
        object present in a frame more quickly.
        """
        pass
        # if cmp(repr(anObject), strObject) == 0:
        #     return anObject
        # else:
        #
        #     for anSubObject in anObject.__dict__.values():
        #         anSubObject = self._getModifiedObject(strObject, anSubObject)
        #     return anSubObject

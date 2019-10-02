
from Command1 import Command

from org.pyut.history.HistoryUtils import getTokenValue
from org.pyut.history.HistoryUtils import makeValuatedToken

from globals import cmp


class ModifyCommand(Command):
    """
    @author P. Dabrowski <przemek.dabrowski@destroy-display.com> (15.11.2005)
    This class is a part of the history system of PyUt.
    This command undo/redo every
    """

    def __init__(self, anyObject = None):

        super().__init__()

        self._object = anyObject

        # name of the method that is called for modification
        self._methodName = ""
        # old and new params for modification
        self._oldParams = []
        self._newParams = []

    def serialize(self):

        serialCmd = Command.serialize(self)

        serialCmd += makeValuatedToken("oldParams", repr(self._oldParams))
        serialCmd += makeValuatedToken("newParams", repr(self._newParams))
        serialCmd += makeValuatedToken("methodName", self._methodName)
        serialCmd += makeValuatedToken("object", repr(self._object))

        return serialCmd

    def unserialize(self, serializedInfos):

        Command.unserialize(self, serializedInfos)

        self._oldParams = eval(getTokenValue("oldParams", serializedInfos))
        self._newParams = eval(getTokenValue("newParams", serializedInfos))
        self._methodName = getTokenValue("methodName", serializedInfos)
        strObject = getTokenValue("object", serializedInfos)

        for anObject in self.getGroup().getHistory().getFrame().getUmlObjects():
            self._object = self._getModifiedObject(strObject, anObject)

    def undo(self):
        method = getattr(self._object, self._methodName)
        apply(method, self._oldParams)
        self.getGroup().getHistory().getFrame().Refresh()

    def redo(self):
        method = getattr(self._object, self._methodName)
        apply(method, self._newParams)
        self.getGroup().getHistory().getFrame().Refresh()

    def execute(self):
        """
        call of execute should do nothing, because the method that have
        modified the object has been already performed. (No call from history)
        """
        pass

    def setMethod(self, methodName):
        """
        set the name of the method that will performed a modification.
        @param methodName     :   name of the method
        """
        self._methodName = methodName

    def setOldParams(self, params):
        """
        Set the parameters of the method that must be called to undo.
        Should be called before changes are performed.
        @param params :   values that will be changed by the call
                                    of the method. Must be ordered as in the
                                    method profile.
        """
        self._oldParams = params

    def setNewParams(self, params):
        """
        Set the parameters of the method that must be called to redo.
        Should be called as soon as the parameters for change are known.
        @param params     :   values that will be changed by calling
                                    the redo method. Must be ordered as in the
                                    method profile.
        """
        self._newParams = params

    def _getModifiedObject(self, strObject, anObject):
        """
        @return the object that is represented by the string strObject. Used
        for unserialization.
        Notes : This methods requires a lot of CPU ressources and place on the
        stack. A refactoring must be proceeded in order to identify every
        object present in a frame more quickly.
        """

        if cmp(repr(anObject), strObject) == 0:
            return anObject
        else:

            for anSubObject in anObject.__dict__.values():
                anSubObject = self._getModifiedObject(strObject, anSubObject)
            return anSubObject

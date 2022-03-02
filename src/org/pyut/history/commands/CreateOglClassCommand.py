
from typing import Optional
from typing import cast

from logging import Logger
from logging import getLogger

from org.pyut.ogl.OglClass import OglClass

from org.pyut.model.PyutClass import PyutClass

from org.pyut.history.commands.BaseOglClassCommand import BaseOglClassCommand

from org.pyut.PyutUtils import PyutUtils

from org.pyut.preferences.PyutPreferences import PyutPreferences


class CreateOglClassCommand(BaseOglClassCommand):
    """
    This class is a part of Pyut's history system.
    It creates an OglClass and allows undoing & redoing operations.
    """
    clsCounter: int = 1

    def __init__(self, x: int = 0, y: int = 0, oglClass: Optional[OglClass] = None):
        """
        If the caller provides a ready-made class this command uses it and does not
        invoke the class editor

        Args:
            x:  abscissa of the class to create
            y:  ordinate of the class to create

        """
        self._classX: int = x
        self._classY: int = y
        self.logger:  Logger          = getLogger(__name__)
        self._prefs:  PyutPreferences = PyutPreferences()

        if oglClass is None:
            shape:                  Optional[OglClass] = self._createNewClass()
            self._invokeEditDialog: bool               = True
        else:
            shape = oglClass
            self._invokeEditDialog = False

        super().__init__(shape=shape)

    def serialize(self) -> str:
        """
        Defer serialization
        """
        return super().serialize()

    def deserialize(self, serializedData):
        """
        Defer deserialization
        Args:
            serializedData:

        """
        super().deserialize(serializedData)

    def redo(self):
        """
        """
        self._shape = self._createNewClass()
        self._placeShapeOnFrame()

    def undo(self):
        """
        Goes all the way back to DeleteOglObjectCommand
        """
        super().redo()

    def execute(self):
        self._placeShapeOnFrame()

    def _createNewClass(self) -> OglClass:
        """
        Create a new class

        Returns: the newly created OglClass
        """
        className: str       = f'{self._prefs.className}{CreateOglClassCommand.clsCounter}'
        pyutClass: PyutClass = PyutClass(className)
        oglClass:  OglClass  = OglClass(pyutClass)

        CreateOglClassCommand.clsCounter += 1

        return oglClass

    def _placeShapeOnFrame(self, ):
        """
        Place self._shape on the UML frame

        """
        from org.pyut.ui.Mediator import Mediator

        med:       Mediator  = Mediator()
        oglClass:  OglClass  = self._shape
        pyutClass: PyutClass = cast(PyutClass, oglClass.pyutObject)
        umlFrame = med.getFileHandling().getCurrentFrame()
        if self._invokeEditDialog is True:
            med.classEditor(pyutClass)

        if self._prefs.snapToGrid is True:
            snappedX, snappedY = PyutUtils.snapCoordinatesToGrid(self._classX, self._classY, self._prefs.backgroundGridInterval)
            umlFrame.addShape(oglClass, snappedX, snappedY, withModelUpdate=True)
        else:
            umlFrame.addShape(oglClass, self._classX, self._classY, withModelUpdate=True)

        med.autoResize(pyutClass)
        umlFrame.Refresh()

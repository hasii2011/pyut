
from typing import cast

from logging import Logger
from logging import getLogger

from org.pyut.ogl.OglClass import OglClass

from org.pyut.model.PyutClass import PyutClass

from org.pyut.commands.BaseOglClassCommand import BaseOglClassCommand

from org.pyut.PyutUtils import PyutUtils

from org.pyut.preferences.PyutPreferences import PyutPreferences


class CreateOglClassCommand(BaseOglClassCommand):
    """
    This class is a part of Pyut's history system.
    It creates an OglClass and allows undo/redo operations.
    """
    clsCounter: int = 1

    def __init__(self, x: int = 0, y: int = 0):
        """

        Args:
            x:  abscissa of the class to create
            y:  ordinate of the class to create

        """
        self._classX: int = x
        self._classY: int = y
        self.logger: Logger          = getLogger(__name__)
        self._prefs: PyutPreferences = PyutPreferences()

        shape: OglClass = self._createNewClass()

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
        """
        self.logger.warning(f'Implement create class UNDO')
        frame = self.getGroup().getHistory().getFrame()
        frame.addShape(self._shape, 0, 0, withModelUpdate=False)
        self._shape.UpdateFromModel()
        frame.Refresh()

    def execute(self):
        self._placeShapeOnFrame()

    def _createNewClass(self) -> OglClass:
        """
        Create a new class

        Returns: the newly created OglClass
        """
        className: str       = f'{self._prefs.className}{CreateOglClassCommand.clsCounter}'
        pyutClass: PyutClass = PyutClass(className)
        oglClass:  OglClass = OglClass(pyutClass)

        CreateOglClassCommand.clsCounter += 1

        return oglClass

    def _placeShapeOnFrame(self, ):
        """
        Place self._shape on the UML frame

        """
        from org.pyut.ui.Mediator import Mediator

        med:       Mediator  = Mediator()
        oglClass:  OglClass  = self._shape
        pyutClass: PyutClass = cast(PyutClass, oglClass.getPyutObject())
        umlFrame = med.getFileHandling().getCurrentFrame()
        med.classEditor(pyutClass)

        if self._prefs.snapToGrid is True:
            snappedX, snappedY = PyutUtils.snapCoordinatesToGrid(self._classX, self._classY, self._prefs.backgroundGridInterval)
            umlFrame.addShape(oglClass, snappedX, snappedY, withModelUpdate=True)
        else:
            umlFrame.addShape(oglClass, self._classX, self._classY, withModelUpdate=True)

        med.autoResize(pyutClass)
        umlFrame.Refresh()


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

    def __init__(self, x: int = 0, y: int = 0, createNewClass: bool = False, shape=None):
        """

        Args:
            x:  abscissa of the class to create
            y:  ordinate of the class to create

            createNewClass: Create new class or create Delete OGL Class command
            TODO  This is a code smell; Do not execute code based on a flag

            shape:
        """
        self.logger: Logger          = getLogger(__name__)
        self._prefs: PyutPreferences = PyutPreferences()

        if createNewClass is True:
            assert shape is None, 'Either we create it or you give it to us'

            if self._prefs.snapToGrid is True:
                snappedX, snappedY = PyutUtils.snapCoordinatesToGrid(x, y, self._prefs.backgroundGridInterval)
                self._shape = self._createNewClass(snappedX, snappedY)
            else:
                self._shape = self._createNewClass(x, y)
        else:
            super().__init__(shape)

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
        super().redo()

    def undo(self):
        """
        """
        super().undo()

    def execute(self):
        pass

    def _createNewClass(self, x: int, y: int) -> OglClass:
        """
        Add a new class at (x, y).

        Args:
            x: abscissa of the class to create
            y: ordinate of the class to create

        Returns: the newly created OglClass
        """
        from org.pyut.ui.Mediator import Mediator

        self.logger.info(f'{x=},{y=}')
        med = Mediator()
        umlFrame = med.getFileHandling().getCurrentFrame()

        className: str = f'{self._prefs.className}{CreateOglClassCommand.clsCounter}'
        pyutClass = PyutClass(className)
        CreateOglClassCommand.clsCounter += 1

        oglClass = OglClass(pyutClass)
        med.classEditor(pyutClass)

        umlFrame.addShape(oglClass, x, y, withModelUpdate=True)
        med.autoResize(pyutClass)
        umlFrame.Refresh()

        return oglClass

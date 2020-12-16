
from logging import Logger
from logging import getLogger

from org.pyut.commands.DelOglClassCommand import DelOglClassCommand

from org.pyut.PyutUtils import PyutUtils

from org.pyut.general.Globals import _

from org.pyut.preferences.PyutPreferences import PyutPreferences


class CreateOglClassCommand(DelOglClassCommand):
    """
    @author P. Dabrowski <przemek.dabrowski@destroy-display.com> (15.11.2005)
    This class is a part of the history system of PyUt.
    It creates an OglClass and allows to undo/redo it.
    """

    def __init__(self, x: float = 0, y: float = 0, createNewClass: bool = False, shape=None):
        """

        Args:
            x:  abscissa of the class to create
            y:  ordinate of the class to create

            createNewClass: Create new class or create Delete OGL Class command
            TODO  This is a code smell; Don't do code based on flag

            shape:
        """
        self.logger: Logger          = getLogger(__name__)
        self._prefs: PyutPreferences = PyutPreferences()

        if createNewClass is True:
            if self._prefs.snapToGrid is True:
                snappedX, snappedY = PyutUtils.snapCoordinatesToGrid(x, y, self._prefs.backgroundGridInterval)
                self._shape = self._createNewClass(snappedX, snappedY)
            else:
                self._shape = self._createNewClass(x, y)
        else:
            DelOglClassCommand.__init__(self, shape)

    def serialize(self):
        """
        serialize the data needed by the command to undo/redo the created link
        """

        return DelOglClassCommand.serialize(self)

    def deserialize(self, serializedData):
        """
        deserialize the data needed by the command to undo/redo the created link
        @param serializedData    :   string representation of the data needed
                                            by the command to undo redo a link
        """

        DelOglClassCommand.deserialize(self, serializedData)

    def redo(self):
        """
        redo the creation of the link.
        """

        DelOglClassCommand.undo(self)

    def undo(self):
        """
        Undo the creation of link, what means that we destroy the link
        """

        DelOglClassCommand.redo(self)

    def execute(self):
        pass

    def _createNewClass(self, x: float, y: float):
        """
        Add a new class at (x, y).

        Args:
            x: abscissa of the class to create
            y: ordinate of the class to create

        Returns: the newly created OgClass
        """
        from org.pyut.general.Mediator import Mediator
        from org.pyut.model.PyutClass import PyutClass
        from org.pyut.ogl.OglClass import OglClass

        self.logger.info(f'{x=},{y=}')
        med = Mediator()
        umlFrame = med.getFileHandling().getCurrentFrame()

        pyutClass = PyutClass(_("NoName"))
        oglClass = OglClass(pyutClass)
        med.classEditor(pyutClass)

        umlFrame.addShape(oglClass, x, y, withModelUpdate=True)
        med.autoResize(pyutClass)
        umlFrame.Refresh()

        return oglClass

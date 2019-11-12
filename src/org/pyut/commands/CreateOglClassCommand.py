
from org.pyut.commands.DelOglClassCommand import DelOglClassCommand

from Globals import _


class CreateOglClassCommand(DelOglClassCommand):
    """
    @author P. Dabrowski <przemek.dabrowski@destroy-display.com> (15.11.2005)
    This class is a part of the history system of PyUt.
    It creates an OglClass and allowds to undo/redo it.
    """

    def __init__(self, x=0, y=0, forExecute=False, shape=None):
        """
        Constructor.
        @param x     :   abscissa of the class to create
        @param y     :   ordinate of the class to create
        """

        if forExecute:
            self._shape = self._createNewClass(x, y)
        else:
            DelOglClassCommand.__init__(self, shape)

    def serialize(self):
        """
        serialize the data needed by the command to undo/redo the created link
        """

        return DelOglClassCommand.serialize(self)

    def deserialize(self, serializedInfos):
        """
        unserialize the data needed by the command to undo/redo the created link
        @param serializedInfos    :   string representation of the data needed
                                            by the command to undo redo a link
        """

        DelOglClassCommand.deserialize(self, serializedInfos)

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

    def _createNewClass(self, x, y):
        """
        Add a new class at (x, y).

        @return PyutClass : the newly created PyutClass
        @since 1.4
        @author L. Burgbacher <lb@alawa.ch>
        """
        from Mediator import getMediator
        from org.pyut.PyutClass import PyutClass
        from org.pyut.ogl.OglClass import OglClass

        med = getMediator()
        umlFrame = med.getFileHandling().getCurrentFrame()

        pyutClass = PyutClass(_("NoName"))
        oglClass = OglClass(pyutClass)
        med.classEditor(pyutClass)
        # med.autoResize(pyutClass)

        umlFrame.addShape(oglClass, x, y, withModelUpdate=True)
        med.autoResize(pyutClass)
        umlFrame.Refresh()

        return oglClass

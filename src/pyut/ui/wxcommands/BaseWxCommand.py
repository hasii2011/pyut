
from typing import cast
from typing import TYPE_CHECKING

from logging import Logger
from logging import getLogger

from ogl.OglUtils import OglUtils
from pyutmodel.PyutLinkedObject import PyutLinkedObject

from ogl.OglClass import OglClass

from wx import Command

from pyut.preferences.PyutPreferences import PyutPreferences
from pyut.ui.wxcommands.Types import DoableObjectType

if TYPE_CHECKING:
    from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame


class BaseWxCommand(Command):
    """
    Created simply to supply a way to
        * Delete Ogl objects from a diagram frame
        * Add Ogl Class behavior
    """
    clsLogger: Logger = getLogger(__name__)

    def __init__(self, canUndo: bool, name: str):

        super().__init__(canUndo=canUndo, name=name)
        self._preferences: PyutPreferences = PyutPreferences()

    def _removeOglObjectFromFrame(self, umlFrame: 'UmlDiagramsFrame', oglObject: DoableObjectType, pyutClass: PyutLinkedObject | None = None):

        from pyut.ui.umlframes.UmlFrame import UmlObjects

        umlObjects: UmlObjects = umlFrame.getUmlObjects()
        for oglObject in umlObjects:
            if isinstance(oglObject, OglClass):
                oglClass: OglClass = cast(OglClass, oglObject)
                pyutLinkedObject: PyutLinkedObject = oglClass.pyutObject
                if pyutClass in pyutLinkedObject.getParents():
                    self.clsLogger.warning(f'Removing {pyutClass=} from {pyutLinkedObject=}')
                    pyutLinkedObject.getParents().remove(cast(PyutLinkedObject, pyutClass))
        oglObject.Detach()
        umlFrame.Refresh()

    def _addOglClassToFrame(self, umlFrame: 'UmlDiagramsFrame', oglClass: OglClass, x: int, y: int):

        if self._preferences.snapToGrid is True:
            snappedX, snappedY = OglUtils.snapCoordinatesToGrid(x, y, self._preferences.backgroundGridInterval)
            umlFrame.addShape(oglClass, snappedX, snappedY, withModelUpdate=True)
        else:
            umlFrame.addShape(oglClass, x, y, withModelUpdate=True)

        if self._preferences.autoResizeShapesOnEdit is True:
            oglClass.autoResize()

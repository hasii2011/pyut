
from typing import cast
from typing import TYPE_CHECKING

from logging import Logger
from logging import getLogger

from ogl.OglUtils import OglUtils
from ogl.preferences.OglPreferences import OglPreferences
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
        self._preferences:    PyutPreferences = PyutPreferences()
        self._oglPreferences: OglPreferences  = OglPreferences()

    def _removeOglObjectFromFrame(self, umlFrame: 'UmlDiagramsFrame', oglObject: DoableObjectType, pyutClass: PyutLinkedObject | None = None):

        from pyut.ui.umlframes.UmlFrame import UmlObjects

        umlObjects: UmlObjects = umlFrame.getUmlObjects()

        for obj in umlObjects:

            if isinstance(obj, OglClass):

                potentialObject: OglClass = cast(OglClass, obj)

                if self._isSameObject(objectToRemove=oglObject, potentialObject=potentialObject):

                    pyutLinkedObject: PyutLinkedObject = potentialObject.pyutObject

                    if pyutClass in pyutLinkedObject.getParents():
                        self.clsLogger.warning(f'Removing {pyutClass=} from {pyutLinkedObject=}')
                        pyutLinkedObject.getParents().remove(cast(PyutLinkedObject, pyutClass))
                    potentialObject.Detach()
                    umlFrame.Refresh()

    def _addOglClassToFrame(self, umlFrame: 'UmlDiagramsFrame', oglClass: OglClass, x: int, y: int):

        if self._oglPreferences.snapToGrid is True:
            snappedX, snappedY = OglUtils.snapCoordinatesToGrid(x, y, self._oglPreferences.backgroundGridInterval)
            umlFrame.addShape(oglClass, snappedX, snappedY, withModelUpdate=True)
        else:
            umlFrame.addShape(oglClass, x, y, withModelUpdate=True)

        if self._preferences.autoResizeShapesOnEdit is True:
            oglClass.autoResize()

    def _isSameObject(self, objectToRemove: DoableObjectType, potentialObject: DoableObjectType) -> bool:
        """
        This probably could be done by updating the OglObject with the __equ__ dunder method.
        Wait until the ogl project updates

        Args:
            objectToRemove:   Object we were told to remove
            potentialObject:  The one that is on the frame

        Returns:  `True` if they are one and the same, else `False`

        """
        ans: bool = False

        if objectToRemove.pyutObject.id == potentialObject.pyutObject.id:
            ans = True

        return ans


from typing import cast
from typing import TYPE_CHECKING

from logging import Logger
from logging import getLogger

from wx import Command

from pyutmodelv2.PyutLinkedObject import PyutLinkedObject

from ogl.OglUtils import OglUtils
from ogl.OglClass import OglClass
from ogl.OglActor import OglActor
from ogl.OglLink import OglLink
from ogl.OglNote import OglNote
from ogl.OglText import OglText
from ogl.OglUseCase import OglUseCase
from ogl.OglInterface2 import OglInterface2

from ogl.sd.OglSDInstance import OglSDInstance
from ogl.sd.OglSDMessage import OglSDMessage

from ogl.preferences.OglPreferences import OglPreferences

from pyut.preferences.PyutPreferences import PyutPreferences

from pyut.ui.wxcommands.Types import DoableObjectType

if TYPE_CHECKING:
    from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame


class BaseWxCommand(Command):
    """
    Created to supply a simple way to
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

        umlObjects: UmlObjects = umlFrame.umlObjects

        for obj in umlObjects:

            # if isinstance(obj, OglClass):
            # This is a duplicate of the UmlObject, since I cannot use NewType
            if isinstance(obj, (OglClass, OglLink, OglNote, OglText, OglSDMessage, OglSDInstance, OglActor, OglUseCase, OglInterface2)):

                potentialObject: OglClass = cast(OglClass, obj)

                if self._isSameObject(objectToRemove=oglObject, potentialObject=potentialObject):

                    pyutLinkedObject: PyutLinkedObject = potentialObject.pyutObject

                    if pyutClass in pyutLinkedObject.parents:
                        self.clsLogger.warning(f'Removing {pyutClass=} from {pyutLinkedObject=}')
                        pyutLinkedObject.parents.remove(cast(PyutLinkedObject, pyutClass))
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

        if isinstance(objectToRemove, OglSDInstance):
            nonOglObject: OglSDInstance = cast(OglSDInstance, objectToRemove)
            if nonOglObject.pyutSDInstance.id == nonOglObject.pyutSDInstance.id:
                ans = True
        else:
            if objectToRemove.pyutObject.id == potentialObject.pyutObject.id:   # type: ignore
                ans = True

        return ans

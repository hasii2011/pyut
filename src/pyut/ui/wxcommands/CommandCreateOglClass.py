
from typing import cast
from typing import TYPE_CHECKING

from logging import Logger
from logging import getLogger


from pyutmodel.PyutClass import PyutClass

from ogl.OglClass import OglClass

from ogl.OglUtils import OglUtils

from pyut.ui.wxcommands.BaseWxCommand import BaseWxCommand

from pyut.uiv2.eventengine.Events import EventType
from pyut.uiv2.eventengine.IEventEngine import IEventEngine

if TYPE_CHECKING:
    from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame


class CommandCreateOglClass(BaseWxCommand):
    """
    This is version 2 of the Pyut undo/redo capability.  This version
    is based on wxPython's CommandProcessor as opposed to the original
    homegrown infrastructure
    """

    clsCounter: int = 1

    def __init__(self, eventEngine: IEventEngine, x: int = 0, y: int = 0, oglClass: OglClass | None = None):
        """
        If the caller provides a ready-made class this command uses it and does not
        invoke the class editor

        Args:
            eventEngine
            x:  abscissa of the class to create
            y:  ordinate of the class to create
            oglClass:
        """
        super().__init__(canUndo=True, name='Create Class', eventEngine=eventEngine, x=x, y=y, oglObject=oglClass)

        self.logger: Logger = getLogger(__name__)

    def CanUndo(self):
        return True

    def Undo(self) -> bool:
        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._cbGetActiveUmlFrameForUndo)
        return True

    def _createNewObject(self) -> OglClass:
        """
        Implement required abstract method

        Create a new class

        Returns: the newly created OglClass
        """
        className: str       = f'{self._prefs.className}{CommandCreateOglClass.clsCounter}'
        pyutClass: PyutClass = PyutClass(className)
        oglClass:  OglClass  = OglClass(pyutClass)

        CommandCreateOglClass.clsCounter += 1

        return oglClass

    def _placeShapeOnFrame(self):
        """
        Place self._shape on the UML frame

        """
        oglClass:  OglClass  = cast(OglClass, self._shape)
        pyutClass: PyutClass = cast(PyutClass, oglClass.pyutObject)
        if self._invokeEditDialog is True:
            self._eventEngine.sendEvent(EventType.EditClass, pyutClass=pyutClass)

        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._cbGetActiveUmlFrameForAdd)

    def _cbGetActiveUmlFrameForUndo(self, frame: 'UmlDiagramsFrame'):

        from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame
        from pyut.ui.umlframes.UmlFrame import UmlObjects
        from pyutmodel.PyutLinkedObject import PyutLinkedObject

        umlFrame: UmlDiagramsFrame = frame
        self.logger.info(f'{umlFrame=}')
        pyutClass: PyutClass = cast(PyutClass, self._shape.pyutObject)
        # need to check if the class has children, and remove the
        # references in the children
        umlObjects: UmlObjects = umlFrame.getUmlObjects()
        for oglObject in umlObjects:
            if isinstance(oglObject, OglClass):
                oglClass: OglClass = cast(OglClass, oglObject)
                pyutLinkedObject: PyutLinkedObject = oglClass.pyutObject
                if pyutClass in pyutLinkedObject.getParents():
                    pyutLinkedObject.getParents().remove(cast(PyutLinkedObject, pyutClass))
        self._shape.Detach()
        umlFrame.Refresh()

    def _cbGetActiveUmlFrameForAdd(self, frame: 'UmlDiagramsFrame'):

        from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

        umlFrame: UmlDiagramsFrame = frame
        self.logger.info(f'{umlFrame=}')
        oglClass:  OglClass  = cast(OglClass, self._shape)

        if self._prefs.snapToGrid is True:
            snappedX, snappedY = OglUtils.snapCoordinatesToGrid(self._classX, self._classY, self._prefs.backgroundGridInterval)
            umlFrame.addShape(oglClass, snappedX, snappedY, withModelUpdate=True)
        else:
            umlFrame.addShape(oglClass, self._classX, self._classY, withModelUpdate=True)

        # med.autoResize(pyutClass)
        if self._prefs.autoResizeShapesOnEdit is True:
            oglClass.autoResize()

        umlFrame.Refresh()


from typing import cast
from typing import TYPE_CHECKING

from logging import Logger
from logging import getLogger


from pyutmodelv2.PyutClass import PyutClass

from ogl.OglClass import OglClass

from pyut.ui.wxcommands.BaseWxCreateCommand import BaseWxCreateCommand

from pyut.uiv2.eventengine.Events import EventType
from pyut.uiv2.eventengine.IEventEngine import IEventEngine

if TYPE_CHECKING:
    from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame


class CommandCreateOglClass(BaseWxCreateCommand):
    """
    This is version 2 of the Pyut undo/redo capability.  This version
    is based on wxPython's CommandProcessor as opposed to the original
    homegrown infrastructure
    """

    clsCounter: int = 1

    def __init__(self, x: int, y: int, eventEngine: IEventEngine):
        """
        If the caller provides a ready-made class this command uses it and does not
        invoke the class editor

        Args:
            eventEngine
            x:  abscissa of the class to create
            y:  ordinate of the class to create

        """
        super().__init__(canUndo=True, name='Create Class', x=x, y=y, eventEngine=eventEngine)

        self.logger: Logger = getLogger(__name__)

    def Undo(self) -> bool:
        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._cbGetActiveUmlFrameForUndo)
        return True

    def _createPrototypeInstance(self) -> OglClass:
        """
        Implement required abstract method

        Create a new class

        Returns: the newly created OglClass
        """
        className: str       = f'{self._oglPreferences.className}{CommandCreateOglClass.clsCounter}'
        pyutClass: PyutClass = PyutClass(name=className)
        oglClass:  OglClass  = OglClass(pyutClass)

        CommandCreateOglClass.clsCounter += 1

        return oglClass

    def _placeShapeOnFrame(self):
        """
        Place self._shape on the UML frame
        """
        oglClass:  OglClass  = cast(OglClass, self._shape)              # get old
        pyutClass: PyutClass = cast(PyutClass, oglClass.pyutObject)
        #
        # Yet another reason to re-write miniogl.  I don't understand the model
        # stuff that it is maintaining;  However, I understand I have to recreate
        # the visuals so Shape._views is correct
        self._oglObjWidth, self._oglObjHeight = oglClass.GetSize()
        self._shape = OglClass(pyutClass, w=self._oglObjWidth, h=self._oglObjHeight)        # create new

        self._eventEngine.sendEvent(EventType.EditClass, pyutClass=pyutClass)

        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._cbGetActiveUmlFrameForAdd)

    def _cbGetActiveUmlFrameForUndo(self, frame: 'UmlDiagramsFrame'):

        from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

        umlFrame: UmlDiagramsFrame = frame
        self.logger.info(f'{umlFrame=}')
        pyutClass: PyutClass = cast(PyutClass, self._shape.pyutObject)
        self._removeOglObjectFromFrame(umlFrame=umlFrame, oglObject=self._shape, pyutClass=pyutClass)

    def _cbGetActiveUmlFrameForAdd(self, frame: 'UmlDiagramsFrame'):

        from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

        umlFrame: UmlDiagramsFrame = frame
        self.logger.info(f'{umlFrame=}')
        oglClass:  OglClass  = cast(OglClass, self._shape)

        self._addOglClassToFrame(umlFrame=umlFrame, oglClass=oglClass, x=self._oglObjX, y=self._oglObjY)
        umlFrame.Refresh()

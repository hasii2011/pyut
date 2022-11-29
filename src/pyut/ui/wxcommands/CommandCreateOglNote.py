
from typing import TYPE_CHECKING
from typing import cast

from logging import Logger
from logging import getLogger

from pyutmodel.PyutNote import PyutNote

from ogl.OglNote import OglNote

from pyut.ui.wxcommands.BaseWxCommand import BaseWxCommand

from pyut.uiv2.eventengine.Events import EventType
from pyut.uiv2.eventengine.IEventEngine import IEventEngine

if TYPE_CHECKING:
    from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame


class CommandCreateOglNote(BaseWxCommand):

    def __init__(self, eventEngine: IEventEngine, x: int = 0, y: int = 0, oglNote: OglNote | None = None):

        super().__init__(canUndo=True, name='Create Note', eventEngine=eventEngine, x=x, y=y, oglObject=oglNote)

        self.logger: Logger = getLogger(__name__)

    def CanUndo(self):
        return True

    def Undo(self) -> bool:
        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._cbGetActiveUmlFrameForUndo)
        return True

    def _createNewObject(self) -> OglNote:
        """
        Implement required abstract method

        Create a new class

        Returns: the newly created OglNote
        """
        pyutNote: PyutNote = PyutNote(noteText=self._prefs.noteText)
        oglNote:  OglNote  = OglNote(pyutNote)

        return oglNote

    def _placeShapeOnFrame(self):
        """
        Place self._shape on the UML frame

        """
        oglNote:  OglNote  = cast(OglNote, self._shape)
        pyutNote: PyutNote = cast(PyutNote, oglNote.pyutObject)
        if self._invokeEditDialog is True:
            self._eventEngine.sendEvent(EventType.EditNote, pyutNote=pyutNote)

        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._cbGetActiveUmlFrameForAdd)

    def _cbGetActiveUmlFrameForAdd(self, frame: 'UmlDiagramsFrame'):

        from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

        umlFrame: UmlDiagramsFrame = frame
        self.logger.info(f'{umlFrame=}')
        oglNote:  OglNote  = cast(OglNote, self._shape)

        umlFrame.addShape(oglNote, self._classX, self._classY, withModelUpdate=True)

        umlFrame.Refresh()

    def _cbGetActiveUmlFrameForUndo(self, frame: 'UmlDiagramsFrame'):

        umlFrame: UmlDiagramsFrame = frame

        self._shape.Detach()
        umlFrame.Refresh()

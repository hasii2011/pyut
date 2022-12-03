
from typing import TYPE_CHECKING
from typing import cast

from logging import Logger
from logging import getLogger

from pyutmodel.PyutNote import PyutNote

from ogl.OglNote import OglNote

from pyut.ui.wxcommands.BaseWxCreateCommand import BaseWxCreateCommand

from pyut.uiv2.eventengine.Events import EventType
from pyut.uiv2.eventengine.IEventEngine import IEventEngine

if TYPE_CHECKING:
    from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame


class CommandCreateOglNote(BaseWxCreateCommand):

    def __init__(self, x: int, y: int, eventEngine: IEventEngine):

        super().__init__(canUndo=True, name='Create Note', x=x, y=y, eventEngine=eventEngine)

        self.logger: Logger = getLogger(__name__)

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
        # Yet another reason to re-write miniogl.  I don't understand the model
        # stuff that it is maintaining;  However, I understand I have to recreate
        # the visuals so Shape._views is correct
        oglNote:  OglNote  = cast(OglNote, self._shape)                 # get old
        pyutNote: PyutNote = cast(PyutNote, oglNote.pyutObject)
        #
        # Yet another reason to re-write miniogl.  I don't understand the model
        # stuff that it is maintaining;  However, I understand I have to recreate
        # the visuals so Shape._views is correct
        self._oglObjWidth, self._oglObjHeight = oglNote.GetSize()
        self._shape = OglNote(pyutNote, w=self._oglObjWidth, h=self._oglObjHeight)      # create new

        self._eventEngine.sendEvent(EventType.EditNote, pyutNote=pyutNote)

        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._cbGetActiveUmlFrameForAdd)

    def _cbGetActiveUmlFrameForAdd(self, frame: 'UmlDiagramsFrame'):

        from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

        umlFrame: UmlDiagramsFrame = frame
        self.logger.info(f'{umlFrame=}')
        oglNote:  OglNote  = cast(OglNote, self._shape)

        umlFrame.addShape(oglNote, self._oglObjX, self._oglObjY, withModelUpdate=True)

        umlFrame.Refresh()

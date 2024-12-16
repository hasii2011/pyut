
from typing import cast

from logging import Logger
from logging import getLogger

from pyutmodelv2.PyutNote import PyutNote

from ogl.OglNote import OglNote

from pyut.ui.wxcommands.BaseWxCreateCommand import BaseWxCreateCommand

from pyut.ui.eventengine.EventType import EventType
from pyut.ui.eventengine.IEventEngine import IEventEngine


class CommandCreateOglNote(BaseWxCreateCommand):

    def __init__(self, x: int, y: int, eventEngine: IEventEngine):

        super().__init__(canUndo=True, name='Create Note', x=x, y=y, eventEngine=eventEngine)

        self.logger: Logger = getLogger(__name__)

    def _createPrototypeInstance(self) -> OglNote:
        """
        Implement required abstract method

        Create a new Note

        Returns: the newly created OglNote
        """
        pyutNote: PyutNote = PyutNote(content=self._oglPreferences.noteText)
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

        self._oglObjWidth, self._oglObjHeight = oglNote.GetSize()
        self._shape = OglNote(pyutNote, w=self._oglObjWidth, h=self._oglObjHeight)      # create new

        self._eventEngine.sendEvent(EventType.EditNote, pyutNote=pyutNote)

        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._cbAddOglObjectToFrame)

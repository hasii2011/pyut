from typing import cast

from org.pyut.history.HistoryUtils import deTokenize
from org.pyut.history.HistoryUtils import tokenizeValue
from org.pyut.history.commands.DeleteOglObjectCommand import DeleteOglObjectCommand
from org.pyut.model.PyutNote import PyutNote
from org.pyut.ogl.OglNote import OglNote


class DeleteOglNoteCommand(DeleteOglObjectCommand):

    def __init__(self, oglNote: OglNote = None):
        """

        Args:
            oglNote:   The destroyed note
        """
        super().__init__(oglNote)

    def serialize(self) -> str:
        """
        Serialize the data needed by the destroyed OglLinkedObject.

        Returns: A string representation of the data needed by the command.
        """

        # serialize the common data
        serializedNote: str = DeleteOglObjectCommand.serialize(self)

        pyutNote: PyutNote = cast(PyutNote, self._shape.pyutObject)
        content:  str      = pyutNote.content

        serializedNote += tokenizeValue("content", content)

        return serializedNote

    def deserialize(self, serializedData: str):
        """
        deserialize the data needed by the destroyed OglLinkedObject.

        Args:
            serializedData:

        Returns:  deserialized data needed by the command.

        """
        # deserialize the data common to all OglObjects
        DeleteOglObjectCommand.deserialize(self, serializedData)

        content:  str      = deTokenize("content", serializedData)
        pyutNote: PyutNote = cast(PyutNote, self._shape.pyutObject)

        pyutNote.content = content
        self._shape.pyutObject = pyutNote

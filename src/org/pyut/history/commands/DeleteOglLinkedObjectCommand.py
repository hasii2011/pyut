
from org.pyut.history.commands.DeleteOglObjectCommand import DeleteOglObjectCommand

from org.pyut.history.HistoryUtils import deTokenize
from org.pyut.history.HistoryUtils import tokenizeValue


class DeleteOglLinkedObjectCommand(DeleteOglObjectCommand):
    """
    This class is a part of Pyut's history system.

    It executes /undo/redo deletion of an OglLinkedObject
    PyutLikedObjects do not exist as stand alone objects but they represent every OglObject that has a
    pyutLinkedObject as pyutObject
    """

    def __init__(self, shape=None) -> str:
        """

        Args:
            shape:   The destroyed object
        """
        super().__init__(shape)

    def serialize(self):
        """
        Serialize the data needed by the destroyed OglLinkedObject.

        Returns: A string representation of the data needed by the command.
        """

        # serialize the common data common
        serializedShape: str = DeleteOglObjectCommand.serialize(self)

        fileName: str = self._shape.getPyutObject().getFilename()

        serializedShape += tokenizeValue("fileName", fileName)

        return serializedShape

    def deserialize(self, serializedData: str):
        """
        deserialize the data needed by the destroyed OglLinkedObject.

        Args:
            serializedData:

        Returns:  deserialized data needed by the command.

        """
        # deserialize the data common to all OglObjects
        DeleteOglObjectCommand.deserialize(self, serializedData)

        fileName = deTokenize("fileName", serializedData)
        self._shape.getPyutObject().setFilename(fileName)

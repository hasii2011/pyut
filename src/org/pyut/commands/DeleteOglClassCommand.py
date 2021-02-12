
from org.pyut.commands.BaseOglClassCommand import BaseOglClassCommand


class DeleteOglClassCommand(BaseOglClassCommand):
    """
    This class is a part of Pyut's history system.
    It creates an OglClass and allows undo/redo operations.
    """

    def __init__(self, shape=None):
        """

        Args:
            shape: The shape to serialize/deserialize
        """
        super().__init__(shape)

    def serialize(self) -> str:
        """
        Serialize an OglClass

        Returns:  A string representation of the data needed by the command.
        """
        return super().serialize()

    def deserialize(self, serializedData):
        """
        Deserialize the data needed by the deleted OglCass

        Args:
            serializedData: serialized data needed by the command.
        """
        super().deserialize(serializedData=serializedData)

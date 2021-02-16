
from org.pyut.commands.Command import Command
from org.pyut.history.HistoryUtils import makeValuatedToken


class OglShapeCommand(Command):

    def __init__(self, shape=None):

        super().__init__()

        self._shape = shape

    def serialize(self) -> str:

        serializedShape: str = super().serialize()

        #
        # serialize the class and module of the ogl and pyut shape to get the
        # constructors for the deserialization
        #
        oglShapeModule:  str = self._shape.__module__
        oglShapeClass:   str = self._shape.__class__.__name__
        pyutShapeModule: str = self._shape.pyutObject.__module__
        pyutShapeClass:  str = self._shape.pyutObject.__class__.__name__

        serializedShape += makeValuatedToken("oglShapeModule", oglShapeModule)
        serializedShape += makeValuatedToken("oglShapeClass", oglShapeClass)
        serializedShape += makeValuatedToken("pyutShapeModule", pyutShapeModule)
        serializedShape += makeValuatedToken("pyutShapeClass", pyutShapeClass)

        return serializedShape

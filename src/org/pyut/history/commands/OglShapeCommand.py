
from org.pyut.history.commands.Command import Command
from org.pyut.history.commands.MethodInformation import MethodInformation
from org.pyut.history.HistoryUtils import deTokenize
from org.pyut.history.HistoryUtils import tokenizeValue


class OglShapeCommand(Command):

    def __init__(self, shape=None):

        super().__init__()

        self._oglShapeClassName:   str = ''
        self._oglShapeModuleName:  str = ''
        self._pyutShapeClassName:  str = ''
        self._pyutShapeModuleName: str = ''

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

        serializedShape += tokenizeValue("oglShapeModule", oglShapeModule)
        serializedShape += tokenizeValue("oglShapeClass", oglShapeClass)
        serializedShape += tokenizeValue("pyutShapeModule", pyutShapeModule)
        serializedShape += tokenizeValue("pyutShapeClass", pyutShapeClass)

        pyutObj = self._shape.pyutObject

        shapeId:   int = pyutObj.getId()
        serializedShape += tokenizeValue("shapeId", repr(shapeId))

        shapeName: str = pyutObj.getName()
        serializedShape += tokenizeValue("shapeName", shapeName)

        methodInformation: str = MethodInformation.serialize(pyutClassCommon=pyutObj)
        serializedShape += methodInformation

        return serializedShape

    def deserialize(self, serializedShape: str):

        self._oglShapeClassName   = deTokenize("oglShapeClass", serializedShape)
        self._oglShapeModuleName  = deTokenize("oglShapeModule", serializedShape)
        self._pyutShapeClassName  = deTokenize("pyutShapeClass", serializedShape)
        self._pyutShapeModuleName = deTokenize("pyutShapeModule", serializedShape)

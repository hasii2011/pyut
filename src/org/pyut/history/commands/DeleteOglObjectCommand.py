
from typing import Tuple

from importlib import import_module
from typing import cast

from org.pyut.history.commands.Command import Command

from org.pyut.history.HistoryUtils import deTokenize
from org.pyut.history.HistoryUtils import tokenizeValue
from org.pyut.model.PyutLinkedObject import PyutLinkedObject


class DeleteOglObjectCommand(Command):
    """
    @author P. Dabrowski <przemek.dabrowski@destroy-display.com> (15.11.2005)
    This class is a part of the history system of PyUt.
    It implements undo & redo of and OglObject deletion. Consider this
    an abstract class, because OglObject is abstract.
    """

    def __init__(self, shape=None):
        super().__init__()
        self._shape = shape

    def serialize(self) -> str:

        serialShape: str = super().serialize()
        #
        # serialize the class and module of the ogl and pyut shape to get the
        # constructors for the deserialization
        oglShapeModule:  str = self._shape.__module__
        oglShapeClass:   str = self._shape.__class__.__name__
        pyutShapeModule: str = self._shape.pyutObject.__module__
        pyutShapeClass:  str = self._shape.pyutObject.__class__.__name__

        serialShape += tokenizeValue("oglShapeModule", oglShapeModule)
        serialShape += tokenizeValue("oglShapeClass", oglShapeClass)
        serialShape += tokenizeValue("pyutShapeModule", pyutShapeModule)
        serialShape += tokenizeValue("pyutShapeClass", pyutShapeClass)
        # This is interesting:
        # serialize the shape's model size and position and NOT the Ogl(view)'s
        # ones because a zoom could be performed in between.
        #

        # TODO using the following causes 'Invalid or prematurely-freed autorelease pool 0x7fed3d8f3218.'
        # boo hoo;  no typing for me
        # from org.pyut.miniogl.RectangleShapeModel import RectangleShapeModel
        # model: RectangleShapeModel = self._shape.GetModel()
        model = self._shape.GetModel()
        pos:   Tuple[int, int]     = model.GetPosition()
        size:  Tuple[int, int]     = model.GetSize()
        serialShape += tokenizeValue("position", repr(pos))
        serialShape += tokenizeValue("size", repr(size))
        #
        # serialize the graphical links (Ogl) attached to the shape
        # and put it in the common data of the group. We have to do
        # so because the link can be rebuilt only after the
        # shape is rebuilt and so the command for link deletion
        # must be placed after this one.
        #
        from org.pyut.history.commands.DelOglLinkCommand import DelOglLinkCommand
        for link in self._shape.getLinks():
            if not link.IsSelected():
                cmd: DelOglLinkCommand = DelOglLinkCommand(link)
                self.getGroup().addCommand(cmd)

        # serialize data to initialize the associated pyutObject
        pyutObj = self._shape.pyutObject
        shapeId:   int = pyutObj.getId()
        shapeName: str = pyutObj.name
        serialShape += tokenizeValue("shapeId", repr(shapeId))
        serialShape += tokenizeValue("shapeName", shapeName)

        return serialShape

    def deserialize(self, serializedData: str):
        """
        Deserialize the data needed to undo/redo a delete command and create shape

        Args:
            serializedData:
        """

        oglShapeClassName:   str = deTokenize("oglShapeClass", serializedData)
        oglShapeModuleName:  str = deTokenize("oglShapeModule", serializedData)
        pyutShapeClassName:  str = deTokenize("pyutShapeClass", serializedData)
        pyutShapeModuleName: str = deTokenize("pyutShapeModule", serializedData)

        shapeName:     str = deTokenize("shapeName", serializedData)     # name of the pyutObject
        shapeId:       int = eval(deTokenize("shapeId", serializedData))

        shapePosition: Tuple[float, float] = eval(deTokenize("position", serializedData))
        shapeSize:     Tuple[float, float] = eval(deTokenize("size", serializedData))
        #
        # Construct the UML objects
        oglModule = import_module(oglShapeModuleName)
        oglShapeClass = getattr(oglModule, oglShapeClassName)

        pyutModule     = import_module(pyutShapeModuleName)
        pyutShapeClass = getattr(pyutModule, pyutShapeClassName)
        #
        # build the pyutObject : it assumes that every parameter of the
        # constructor has a default value
        # break up for testability
        #
        group   = self._group
        history = group.getHistory()
        frame   = history.getFrame()
        self._shape = frame.getUmlObjectById(shapeId)

        if self._shape is None:

            pyutShape = pyutShapeClass(shapeName)
            pyutShape.setId(shapeId)
            #
            # build the OglObject : it assumes that every parameter of the
            # constructor has a default value
            self._shape = oglShapeClass()
            self._shape.pyutObject = pyutShape
            self._shape.GetModel().SetPosition(shapePosition[0], shapePosition[1])
            self._shape.GetModel().SetSize(shapeSize[0], shapeSize[1])

    def redo(self):
        """
        Delete the shape for which this command has been created. You do not
        need to redefine it.
        """
        from org.pyut.ogl.OglClass import OglClass
        umlFrame = self.getGroup().getHistory().getFrame()
        shape = self._shape
        if isinstance(shape, OglClass):
            # need to check if the class has children, and remove the
            # refs in the children
            pyutClass = shape.getPyutObject()
            # TODO: Fix this inscrutable piece of code
            for klass in [s.pyutObject
                          for s in umlFrame.getUmlObjects()
                          if isinstance(s, OglClass)]:
                pyutLinkedObject: PyutLinkedObject = cast(PyutLinkedObject, klass)
                if pyutClass in pyutLinkedObject.getParents():
                    pyutLinkedObject.getParents().remove(cast(PyutLinkedObject, pyutClass))
        shape.Detach()
        umlFrame.Refresh()

    def undo(self):
        """
        Rebuild the OglObject with its associated PyutObject. You do not
        need to redefine it for subclasses.
        """
        # we have to set up the model after the view is attached to the diagram
        # because when it is attached, the model is set up from the view.
        frame = self.getGroup().getHistory().getFrame()
        frame.addShape(self._shape, 0, 0, withModelUpdate=False)
        self._shape.UpdateFromModel()
        frame.Refresh()

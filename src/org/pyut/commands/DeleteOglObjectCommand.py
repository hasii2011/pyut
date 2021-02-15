
from typing import Tuple

from importlib import import_module

from org.pyut.commands.Command import Command

from org.pyut.history.HistoryUtils import getTokenValue
from org.pyut.history.HistoryUtils import makeValuatedToken


class DeleteOglObjectCommand(Command):
    """
    @author P. Dabrowski <przemek.dabrowski@destroy-display.com> (15.11.2005)
    This class is a part of the history system of PyUt.
    It execute/undo/redo the deletion of an OglObject. It is to be considered
    as an abstract class, because OglObject is abstract.
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
        pyutShapeModule: str = self._shape.getPyutObject().__module__
        pyutShapeClass:  str = self._shape.getPyutObject().__class__.__name__

        serialShape += makeValuatedToken("oglShapeModule", oglShapeModule)
        serialShape += makeValuatedToken("oglShapeClass", oglShapeClass)
        serialShape += makeValuatedToken("pyutShapeModule", pyutShapeModule)
        serialShape += makeValuatedToken("pyutShapeClass", pyutShapeClass)
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
        serialShape += makeValuatedToken("position", repr(pos))
        serialShape += makeValuatedToken("size", repr(size))
        #
        # serialize the graphical links (Ogl) attached to the shape
        # and put it in the common data of the group. We have to do
        # so because the link can be rebuilt only after the
        # shape is rebuilt and so the command for link deletion
        # must be placed after this one.
        #
        from org.pyut.commands.DelOglLinkCommand import DelOglLinkCommand
        for link in self._shape.getLinks():
            if not link.IsSelected():
                cmd: DelOglLinkCommand = DelOglLinkCommand(link)
                self.getGroup().addCommand(cmd)

        # serialize data to initialize the associated pyutObject
        pyutObj = self._shape.getPyutObject()
        shapeId:   int = pyutObj.getId()
        shapeName: str = pyutObj.getName()
        serialShape += makeValuatedToken("shapeId", repr(shapeId))
        serialShape += makeValuatedToken("shapeName", shapeName)

        return serialShape

    def deserialize(self, serializedData: str):
        """
        Deserialize the data needed to undo/redo a delete command and create shape

        Args:
            serializedData:
        """

        oglShapeClassName:   str = getTokenValue("oglShapeClass", serializedData)
        oglShapeModuleName:  str = getTokenValue("oglShapeModule", serializedData)
        pyutShapeClassName:  str = getTokenValue("pyutShapeClass", serializedData)
        pyutShapeModuleName: str = getTokenValue("pyutShapeModule", serializedData)

        shapeName:     str = getTokenValue("shapeName", serializedData)     # name of the pyutObject
        shapeId:       int = eval(getTokenValue("shapeId", serializedData))

        shapePosition: Tuple[float, float] = eval(getTokenValue("position", serializedData))
        shapeSize:     Tuple[float, float] = eval(getTokenValue("size", serializedData))
        #
        # Construct the UML objects
        # import the module which contains the ogl and pyut shape classes and instantiate the classes
        # oglShapeClass = getattr(__import__(oglShapeModule), oglShapeClassName)
        # pyutShapeClass = getattr(__import__(pyutShapeModule), pyutShapeClassName)
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
            # build the OglObject : it suppose that every parameter of the
            # constructor has a default value
            self._shape = oglShapeClass()
            self._shape.setPyutObject(pyutShape)
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
            for klass in [s.getPyutObject()
                          for s in umlFrame.getUmlObjects()
                          if isinstance(s, OglClass)]:
                if pyutClass in klass.getParents():
                    klass.getParents().remove(pyutClass)
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

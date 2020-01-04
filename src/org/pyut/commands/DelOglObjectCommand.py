
from org.pyut.commands.Command import Command
from org.pyut.history.HistoryUtils import getTokenValue

from org.pyut.history.HistoryUtils import makeValuatedToken


class DelOglObjectCommand(Command):
    """
    @author P. Dabrowski <przemek.dabrowski@destroy-display.com> (15.11.2005)
    This class is a part of the history system of PyUt.
    It execute/undo/redo the deletion of an OglObject. It is to be considered
    as an abstract class, because OglObject is abstract.
    """

    def __init__(self, shape=None):
        super().__init__()
        self._shape = shape

    def serialize(self):

        serialShape = Command.serialize(self)

        # serialize the class and module of the ogl and pyut shape to get the
        # constructors for the unserialization.
        oglShapeModule = self._shape.__module__
        oglShapeClass = self._shape.__class__.__name__
        pyutShapeModule = self._shape.getPyutObject().__module__
        pyutShapeClass = self._shape.getPyutObject().__class__.__name__
        serialShape += makeValuatedToken("oglShapeModule", oglShapeModule)
        serialShape += makeValuatedToken("oglShapeClass", oglShapeClass)
        serialShape += makeValuatedToken("pyutShapeModule", pyutShapeModule)
        serialShape += makeValuatedToken("pyutShapeClass", pyutShapeClass)
        # serialize the shape's model size and position and NOT the Ogl(view)'s
        # ones because a zoom could be performed in between.
        model = self._shape.GetModel()
        pos = model.GetPosition()
        size = model.GetSize()
        serialShape += makeValuatedToken("position", repr(pos))
        serialShape += makeValuatedToken("size", repr(size))
        # serialize the graphical links (Ogl) attached to the shape
        # and put it in the common data of the group. We have to do
        # so because the link can be rebuild only after that the
        # shape is rebuild and so the command for link deletion
        # must be placed after this one.
        from org.pyut.commands.DelOglLinkCommand import DelOglLinkCommand
        for link in self._shape.getLinks():
            if not link.IsSelected():
                cmd = DelOglLinkCommand(link)
                self.getGroup().addCommand(cmd)

        # serialize data to init the associated pyutObject
        pyutObj = self._shape.getPyutObject()
        shapeId = pyutObj.getId()
        shapeName = pyutObj.getName()
        serialShape += makeValuatedToken("shapeId", repr(shapeId))
        serialShape += makeValuatedToken("shapeName", shapeName)

        return serialShape

    def deserialize(self, serializedInfos):
        """
        unserialize the data needed to undo/redo a delete command and create
        a shape
        """

        #UNSERIALIZATION OF THE DATA NEEDED BY THE COMMAND :
        #name of the oglObject's class to rebuild it
        oglShapeClassName = getTokenValue("oglShapeClass", serializedInfos)
        # name of the oglObject's module to rebuild it
        oglShapeModule = getTokenValue("oglShapeModule", serializedInfos)
        # name of the pyutObject's class to rebuild it
        pyutShapeClassName = getTokenValue("pyutShapeClass", serializedInfos)
        # name of the pyutObject's module to rebuild it
        pyutShapeModule = getTokenValue("pyutShapeModule", serializedInfos)
        # name of the pyutObject
        shapeName = getTokenValue("shapeName", serializedInfos)
        # id of the pyutObject
        shapeId = eval(getTokenValue("shapeId", serializedInfos))
        # oglObject's modelPosition (MVC : see miniOgl)
        shapePosition = eval(getTokenValue("position", serializedInfos))
        # oglObject's modelSize (MVC : see miniOgl)
        shapeSize = eval(getTokenValue("size", serializedInfos))

        # CONSTRUCTION OF THE UML OBJECT :
        # import the module which contains the ogl and pyut shape classes and
        # get that classes.
        oglShapeClass = getattr(__import__(oglShapeModule), oglShapeClassName)
        pyutShapeClass = getattr(__import__(pyutShapeModule), pyutShapeClassName)

        # build the pyutObject : it suppose that every parameter of the
        # constructor has a default value

        self._shape = self.getGroup().getHistory().getFrame().getUmlObjectById(shapeId)

        if self._shape is None:

            pyutShape = pyutShapeClass(shapeName)
            pyutShape.setId(shapeId)

            # build the OglObject : it suppose that every parameter of the
            # constructor has a default value
            self._shape = oglShapeClass()
            self._shape.setPyutObject(pyutShape)
            self._shape.GetModel().SetPosition(shapePosition[0], shapePosition[1])
            self._shape.GetModel().SetSize(shapeSize[0], shapeSize[1])

    def redo(self):
        """
        Delete the shape for which this command has been created. You DON't
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
            for klass in [s.getPyutObject() for s in umlFrame.getUmlObjects()
                if isinstance(s, OglClass)]:
                    if pyutClass in klass.getParents():
                        klass.getParents().remove(pyutClass)
        shape.Detach()
        umlFrame.Refresh()

    def undo(self):
        """
        Rebuild the OglObject with its associated PyutObject. You DON't
        need to redefine it for subclasses.
        """
        # we have to set up the model after the view is attached to the diagram
        # because when it is attached, the model is set up from the view.
        frame = self.getGroup().getHistory().getFrame()
        frame.addShape(self._shape, 0, 0, withModelUpdate=False)
        self._shape.UpdateFromModel()
        frame.Refresh()

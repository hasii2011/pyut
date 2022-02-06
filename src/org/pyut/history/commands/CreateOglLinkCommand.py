
from typing import Tuple
from typing import cast

from wx import Point

from org.pyut.model.PyutClass import PyutClass
from org.pyut.model.PyutSDMessage import PyutSDMessage
from org.pyut.model.PyutLink import PyutLink

from org.pyut.history.commands.Command import Command

from org.pyut.ogl.OglClass import OglClass
from org.pyut.ogl.OglLink import OglLink
from org.pyut.ogl.OglLinkFactory import getLinkType
from org.pyut.ogl.OglLinkFactory import getOglLinkFactory

from org.pyut.ogl.sd.OglSDInstance import OglSDInstance
from org.pyut.ogl.sd.OglSDMessage import OglSDMessage

from org.pyut.enums.LinkType import LinkType

from org.pyut.history.HistoryUtils import deTokenize
from org.pyut.history.HistoryUtils import tokenizeValue


class CreateOglLinkCommand(Command):
    """
    This class is a part of the PyUt history system.
    It creates every kind of OglLink and allows Pyut to undo and redo actions.
    """
    NO_NAME_MESSAGE: str = "testMessage()"

    def __init__(self, src=None, dst=None, linkType: LinkType = LinkType.INHERITANCE, srcPos=None, dstPos=None):
        """

        Args:
            src:        Object from which starts the link
            dst:        Object at which ends the link
            linkType:   Type of the link (see OglLinkFactory)
            srcPos:     Start position of the link
            dstPos:     End position of the link
        """
        super().__init__()

        # If the command is created from the history for the undo command or redo command
        # the constructor will have no parameters and so the link
        # will be created or retrieved in the deserialize method.
        if src is None or dst is None:
            self._link = None
        else:
            self._link = self._createLink(src, dst, linkType, srcPos, dstPos)

    def serialize(self):
        """
        serialize the data needed by the command to undo/redo the created link
        """
        # serialize the data common to all commands
        serialShape = Command.serialize(self)
        # get the pyutId of the source OglObject of the link
        srcId = self._link.getSourceShape().getPyutObject().getId()
        # get the pyutId of the destination OglObject of the link
        dstId = self._link.getDestinationShape().getPyutObject().getId()
        # get the model start position of the link
        srcPos = self._link.GetSource().GetModel().GetPosition()
        # get the model end position of the link
        dstPos = self._link.GetDestination().GetModel().GetPosition()
        # get the type of the link (see OglLinkFactory)
        linkType = getLinkType(self._link)
        # get the pyutId of the link
        linkId = self._link.getPyutObject().getId()
        # serialize required data needed to undo/redo the link
        serialShape += tokenizeValue("srcId", repr(srcId))
        serialShape += tokenizeValue("dstId", repr(dstId))
        serialShape += tokenizeValue("srcPos", repr(srcPos))
        serialShape += tokenizeValue("dstPos", repr(dstPos))
        serialShape += tokenizeValue("linkType", repr(linkType))
        serialShape += tokenizeValue("linkId", repr(linkId))

        return serialShape

    def deserialize(self, serializedInfo: str):
        """
        deserialize the data needed by the command to undo/redo the created link
        @param serializedInfo    :   string representation of the data needed by the command to undo redo a link
        """

        # deserialize the data common to all commands
        Command.deserialize(self, serializedInfo)
        # get the pyutId of the source OglObject of the link
        srcId = eval(deTokenize("srcId", serializedInfo))
        # get the pyutId of the destination OglObject of the link
        dstId = eval(deTokenize("dstId", serializedInfo))
        # get the model (MVC pattern) start position of the link
        srcPos = eval(deTokenize("srcPos", serializedInfo))
        # get the model (MVC pattern) end position of the link
        dstPos = eval(deTokenize("dstPos", serializedInfo))
        # get the type of the link (see OglLinkFactory)
        linkType = eval(deTokenize("linkType", serializedInfo))
        # get the pyutId of the link
        linkId = eval(deTokenize("linkId", serializedInfo))
        # get the frame to which belongs the link
        umlFrame = self.getGroup().getHistory().getFrame()

        # if the link has been created it already exists in the frame.
        # But if an undo command has been performed, we have to rebuild the link.
        self._link = umlFrame.getUmlObjectById(linkId)
        if self._link is None:

            # get the source and destination OglObjects of the link
            src = umlFrame.getUmlObjectById(srcId)
            dst = umlFrame.getUmlObjectById(dstId)
            # create the link, but do not add it to the frame.
            # the model position is assigned to a temporary to
            # view, but will be reassigned to the model, after
            # it has been added to the frame, because the zoom
            # could have changed, and we have to update from the
            # model (see redo() method).
            self._link = self._createLink(src, dst, linkType,
                                          srcPos, dstPos)
            # we set the pyutId that the link has at its first creation
            self._link.getPyutObject().setId(linkId)

    def redo(self):
        """
        redo the creation of the link.
        """

        # get the frame to which belongs the link
        umlFrame = self.getGroup().getHistory().getFrame()
        # add the link that was created in the deserialize method.
        umlFrame.GetDiagram().AddShape(self._link, withModelUpdate=False)

        # get the view start and end position and assign it to the
        # model position, then the view position is updated from
        # the model, in regard of the frame zoom level.
        srcPosX, srcPosY = self._link.GetSource().GetPosition()
        dstPosX, dstPosY = self._link.GetDestination().GetPosition()
        self._link.GetSource().GetModel().SetPosition(srcPosX, srcPosY)
        self._link.GetDestination().GetModel().SetPosition(dstPosX, dstPosY)
        self._link.UpdateFromModel()

        umlFrame.Refresh()

    def undo(self):
        """
        Undo the creation of link, what means that we destroy the link
        """
        # create the command to delete an oglLink without add it to the group, then
        # just execute the destruction of the link.
        from org.pyut.history.commands.DelOglLinkCommand import DelOglLinkCommand
        cmd = DelOglLinkCommand(self._link)
        cmd.setGroup(self.getGroup())
        cmd.execute()

    def execute(self):
        self.redo()

    def _createLink(self, src, dst, linkType: LinkType = LinkType.INHERITANCE, srcPos=None, dstPos=None):
        """
        Add a link between src and dst without adding it to the frame.

        Args:
            src:        Source of the link
            dst:        Destination of the link
            linkType:   Type of the link
            srcPos:     Position on source
            dstPos:     Position destination

        Returns:    The created link
        """
        if linkType == LinkType.INHERITANCE:
            return self._createInheritanceLink(src, dst)
        elif linkType == LinkType.SD_MESSAGE:
            return self._createSDMessage(src=src, dest=dst, srcPos=srcPos, destPos=dstPos)
        pyutLink = PyutLink("", linkType=linkType, source=src.getPyutObject(), destination=dst.getPyutObject())

        # Call the factory to create OGL Link
        oglLinkFactory = getOglLinkFactory()
        # oglLink = oglLinkFactory.getOglLink(src, pyutLink, dst, linkType)
        oglLink = oglLinkFactory.getOglLink(srcShape=src, pyutLink=pyutLink, destShape=dst, linkType=linkType)

        src.addLink(oglLink)  # add it to the source OglShape
        dst.addLink(oglLink)  # add it to the destination OglShape

        src.getPyutObject().addLink(pyutLink)   # add it to the PyutClass

        return oglLink

    def _createSDMessage(self, src: OglSDInstance, dest: OglSDInstance, srcPos: Point, destPos: Point) -> OglSDMessage:

        srcRelativeCoordinates:  Tuple[int, int] = src.ConvertCoordToRelative(0, srcPos[1])
        destRelativeCoordinates: Tuple[int, int] = dest.ConvertCoordToRelative(0, destPos[1])

        srcY  = srcRelativeCoordinates[1]
        destY = destRelativeCoordinates[1]

        pyutSDMessage = PyutSDMessage(CreateOglLinkCommand.NO_NAME_MESSAGE, src.getPyutObject(), srcY, dest.getPyutObject(), destY)

        oglLinkFactory = getOglLinkFactory()
        oglSdMessage: OglSDMessage = oglLinkFactory.getOglLink(srcShape=src, pyutLink=pyutSDMessage, destShape=dest,
                                                               linkType=LinkType.SD_MESSAGE, srcPos=srcPos, dstPos=destPos)

        return oglSdMessage

    def _createInheritanceLink(self, child: OglClass, parent: OglClass) -> OglLink:
        """
        Add a parent link between the child and parent objects.

        Args:
            child:  Child PyutClass
            parent: Parent PyutClass

        Returns:
            The inheritance OglLink
        """
        sourceClass:      PyutClass = cast(PyutClass, child.getPyutObject())
        destinationClass: PyutClass = cast(PyutClass, parent.getPyutObject())
        pyutLink:         PyutLink = PyutLink("", linkType=LinkType.INHERITANCE, source=sourceClass, destination=destinationClass)
        oglLink:          OglLink = getOglLinkFactory().getOglLink(child, pyutLink, parent, LinkType.INHERITANCE)

        child.addLink(oglLink)
        parent.addLink(oglLink)

        # add it to the PyutClass
        # child.getPyutObject().addParent(parent.getPyutObject())
        childPyutClass:  PyutClass = cast(PyutClass, child.getPyutObject())
        parentPyutClass: PyutClass = cast(PyutClass, parent.getPyutObject())

        childPyutClass.addParent(parentPyutClass)

        return oglLink


from org.pyut.commands.Command import Command

from org.pyut.ogl.OglLinkFactory import getLinkType
from org.pyut.ogl.OglLinkFactory import getOglLinkFactory

from PyutConsts import OGL_INHERITANCE
from PyutLink import PyutLink

from org.pyut.history.HistoryUtils import getTokenValue
from org.pyut.history.HistoryUtils import makeValuatedToken


class CreateOglLinkCommand(Command):
    """
    @author P. Dabrowski <przemek.dabrowski@destroy-display.com> (15.11.2005)
    This class is a part of the history system of PyUt.
    It creates every kind of OglLink and allowds to undo/redo it.
    """

    def __init__(self, src=None, dst=None, linkType=OGL_INHERITANCE, srcPos=None, dstPos=None):
        """
        Constructor.
        @param src      :   object from which starts the link
        @param dst      :   object at which ends the link
        @param linkType :   type of the link (see OglLinkFactory)
        @param srcPos   :   start position of the link
        @param dstPos   :   end position of the link
        """

        super().__init__()

        # if the command is created from the history for an undo redo
        # the constructor will have no parameters and so the link
        # will be created or got in the unserialise method.
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
        serialShape += makeValuatedToken("srcId", repr(srcId))
        serialShape += makeValuatedToken("dstId", repr(dstId))
        serialShape += makeValuatedToken("srcPos", repr(srcPos))
        serialShape += makeValuatedToken("dstPos", repr(dstPos))
        serialShape += makeValuatedToken("linkType", repr(linkType))
        serialShape += makeValuatedToken("linkId", repr(linkId))

        return serialShape

    def unserialize(self, serializedInfo: str):
        """
        unserialize the data needed by the command to undo/redo the created link
        @param serializedInfo    :   string representation of the data needed by the command to undo redo a link
        """

        # unserialize the data common to all commands
        Command.unserialize(self, serializedInfo)
        # get the pyutId of the source OglObject of the link
        srcId = eval(getTokenValue("srcId", serializedInfo))
        # get the pyutId of the destination OglObject of the link
        dstId = eval(getTokenValue("dstId", serializedInfo))
        # get the model (MVC pattern) start position of the link
        srcPos = eval(getTokenValue("srcPos", serializedInfo))
        # get the model (MVC pattern) end position of the link
        dstPos = eval(getTokenValue("dstPos", serializedInfo))
        # get the type of the link (see OglLinkFactory)
        linkType = eval(getTokenValue("linkType", serializedInfo))
        # get the pyutId of the link
        linkId = eval(getTokenValue("linkId", serializedInfo))
        # get the frame to which belongs the link
        umlFrame = self.getGroup().getHistory().getFrame()

        # if the link has been created it already exist on the frame.
        # But if an undo has been performed, we have to rebuild the link.
        self._link = umlFrame.getUmlObjectById(linkId)
        if self._link is None:

            # get the source and destination OglObjects of the link
            src = umlFrame.getUmlObjectById(srcId)
            dst = umlFrame.getUmlObjectById(dstId)
            # create the link, but don't add it to the frame.
            # the model position is assigned to temporary to
            # view, but will be reassigned to the model, after
            # it has been added to the frame, because the zoom
            # could have change and we have to update from the
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
        # add the link that was created in the unserialize method.
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
        from org.pyut.commands.DelOglLinkCommand import DelOglLinkCommand
        cmd = DelOglLinkCommand(self._link)
        cmd.setGroup(self.getGroup())
        cmd.execute()

    def execute(self):
        """
        Create the ogl graphicaly by adding to the frame the oglLink created in the
        constructor.
        """
        umlFrame = self.getGroup().getHistory().getFrame()
        umlFrame.GetDiagram().AddShape(self._link, withModelUpdate=False)
        umlFrame.Refresh()

    def _createLink(self, src, dst, linkType=OGL_INHERITANCE, srcPos=None, dstPos=None):
        """
        Add a link between src and dst without adding it the frame.

        @param OglClass src  : source of the link
        @param OglClass dst  : destination of the link
        @param int linkType : type of the link
        @param srcPos : position on source
        @param dstPos : position destination

        @return OglLink : the link created

        @author L. Burgbacher
        @modified C.Dutoit 20021125 : added srcPos and dstPos to be compatible with Sequence diagram
        @modified P.Dabrowski 20051202 : moved from umlframe to this command in order to be redone/undone. The
                                         link is not added to the frame anymore.
        """

        if linkType == OGL_INHERITANCE:
            return self._createInheritanceLink(src, dst)

        pyutLink = PyutLink("", linkType=linkType, source=src.getPyutObject(), destination=dst.getPyutObject())

        # Call the factory to create OGL Link
        oglLinkFactory = getOglLinkFactory()
        oglLink = oglLinkFactory.getOglLink(src, pyutLink, dst, linkType)

        src.addLink(oglLink)  # add it to the source OglShape
        dst.addLink(oglLink)  # add it to the destination OglShape

        src.getPyutObject().addLink(pyutLink)   # add it to the PyutClass

        return oglLink

    def _createInheritanceLink(self, child, father):
        """
        Add a paternity link between child and father.

        @param OglClass child : child
        @param OglClass father : father
        @since 1.4
        @author L. Burgbacher <lb@alawa.ch>
        @modified P.Dabrowski 20051202 : moved from umlframe to this command in order to be redone/undone. The
                                         link is not added to the frame anymore.
        """
        pyutLink = PyutLink("", linkType=OGL_INHERITANCE, source=child.getPyutObject(), destination=father.getPyutObject())
        oglLink = getOglLinkFactory().getOglLink(child, pyutLink, father, OGL_INHERITANCE)

        # Added by ND
        child.addLink(oglLink)
        father.addLink(oglLink)
        # add it to the PyutClass
        child.getPyutObject().addFather(father.getPyutObject())

        return oglLink

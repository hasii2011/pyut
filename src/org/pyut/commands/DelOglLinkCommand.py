
from typing import cast

from org.pyut.commands.Command import Command
from org.pyut.commands.DeleteOglObjectCommand import DeleteOglObjectCommand
from org.pyut.ogl.OglClass import OglClass

from org.pyut.ogl.OglLinkFactory import getLinkType

from org.pyut.enums.LinkType import LinkType

from org.pyut.history.HistoryUtils import deTokenize
from org.pyut.history.HistoryUtils import tokenizeValue
from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame


class DelOglLinkCommand(DeleteOglObjectCommand):
    """
    @author P. Dabrowski <przemek.dabrowski@destroy-display.com> (15.11.2005)
    This class is a part of the history system of PyUt.
    Every action that needs to be redone/undone should have an associated
    command. This class is to be considered as an abstract class.
    """

    def __init__(self, link=None):

        DeleteOglObjectCommand.__init__(self, link)

        self._srcPosition  = None
        self._destPosition = None
        self._linkType: LinkType = cast(LinkType, None)
        self._linkSrcId    = None
        self._linkDestId   = None
        self._linkId       = None

    def serialize(self):

        serialLink = Command.serialize(self)

        self._srcPosition  = self._shape.GetSource().GetModel().GetPosition()
        self._destPosition = self._shape.GetDestination().GetModel().GetPosition()
        self._linkType     = getLinkType(self._shape)
        self._linkSrcId    = self._shape.getSourceShape().getPyutObject().getId()
        self._linkDestId   = self._shape.getDestinationShape().getPyutObject().getId()
        self._linkId       = self._shape.getPyutObject().getId()

        serialLink += tokenizeValue("srcPosition", repr(self._srcPosition))
        serialLink += tokenizeValue("destPosition", repr(self._destPosition))
        serialLink += tokenizeValue("linkType", repr(self._linkType))
        serialLink += tokenizeValue("linkSrcId", repr(self._linkSrcId))
        serialLink += tokenizeValue("linkDestId", repr(self._linkDestId))
        serialLink += tokenizeValue("linkId", repr(self._linkId))

        return serialLink

    def deserialize(self, serializedInfos):

        umlFrame = self.getGroup().getHistory().getFrame()

        self._srcPosition  = eval(deTokenize("srcPosition", serializedInfos))
        self._destPosition = eval(deTokenize("destPosition", serializedInfos))

        linkTypeStr: str = deTokenize("linkType", serializedInfos)
        self._linkType   = LinkType.toEnum(linkTypeStr)

        self._linkSrcId    = eval(deTokenize("linkSrcId", serializedInfos))
        self._linkDestId   = eval(deTokenize("linkDestId", serializedInfos))
        self._linkId       = eval(deTokenize("linkId", serializedInfos))

        self._shape = umlFrame.getUmlObjectById(self._linkId)

    def undo(self):

        umlFrame: UmlClassDiagramsFrame = self.getGroup().getHistory().getFrame()
        src:      OglClass              = umlFrame.getUmlObjectById(self._linkSrcId)
        dest:     OglClass              = umlFrame.getUmlObjectById(self._linkDestId)

        if self._shape is None:
            self._shape = umlFrame.createLink(src=src, dst=dest, linkType=self._linkType)
            umlFrame.GetDiagram().AddShape(shape=self._shape, withModelUpdate=True)

        self._shape.getPyutObject().setId(self._linkId)
        self._shape.GetSource().GetModel().SetPosition(self._srcPosition[0], self._srcPosition[1])
        self._shape.GetDestination().GetModel().SetPosition(self._destPosition[0], self._destPosition[1])
        self._shape.GetSource().UpdateFromModel()
        self._shape.GetDestination().UpdateFromModel()
        umlFrame.Refresh()

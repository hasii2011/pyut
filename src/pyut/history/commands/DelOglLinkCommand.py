
from typing import Any
from typing import cast

from ogl.OglClass import OglClass
from ogl.OglLinkFactory import getLinkType

from pyutmodel.PyutLinkType import PyutLinkType

from pyut.history.HistoryUtils import deTokenize
from pyut.history.HistoryUtils import tokenizeValue
from pyut.history.commands.Command import Command
from pyut.history.commands.DeleteOglObjectCommand import DeleteOglObjectCommand

from pyut.ui.umlframes.UmlClassDiagramsFrame import UmlClassDiagramsFrame


class DelOglLinkCommand(DeleteOglObjectCommand):
    """
    This class is part of the Pyut history system
    Every action that needs to be redone/undone should have an
    associated command.
    TODO: This should be an abstract class
    """
    def __init__(self, link=None):

        DeleteOglObjectCommand.__init__(self, link)

        self._srcPosition  = None
        self._destPosition = None
        self._linkType: PyutLinkType = cast(PyutLinkType, None)
        self._linkSrcId    = None
        self._linkDestId   = None
        self._linkId       = None

        self._shape: Any = None     # what a cheat !!

    def serialize(self):

        serialLink = Command.serialize(self)

        self._srcPosition  = self._shape.GetSource().GetModel().GetPosition()
        self._destPosition = self._shape.GetDestination().GetModel().GetPosition()
        self._linkType     = getLinkType(self._shape)
        self._linkSrcId    = self._shape.getSourceShape().pyutObject.id
        self._linkDestId   = self._shape.getDestinationShape().pyutObject.id
        self._linkId       = self._shape.pyutObject.id

        serialLink += tokenizeValue("srcPosition", repr(self._srcPosition))
        serialLink += tokenizeValue("destPosition", repr(self._destPosition))
        serialLink += tokenizeValue("linkType", repr(self._linkType))
        serialLink += tokenizeValue("linkSrcId", repr(self._linkSrcId))
        serialLink += tokenizeValue("linkDestId", repr(self._linkDestId))
        serialLink += tokenizeValue("linkId", repr(self._linkId))

        return serialLink

    def deserialize(self, serializedInformation):

        umlFrame = self.getGroup().getHistory().getFrame()

        self._srcPosition  = eval(deTokenize("srcPosition", serializedInformation))
        self._destPosition = eval(deTokenize("destPosition", serializedInformation))

        linkTypeStr: str = deTokenize("linkType", serializedInformation)
        self._linkType   = PyutLinkType.toEnum(linkTypeStr)

        self._linkSrcId    = eval(deTokenize("linkSrcId", serializedInformation))
        self._linkDestId   = eval(deTokenize("linkDestId", serializedInformation))
        self._linkId       = eval(deTokenize("linkId", serializedInformation))

        self._shape = umlFrame.getUmlObjectById(self._linkId)

    def undo(self):
        """
        TODO:  Fix this unholy mess of untyped code;  Or better you redo Pyut's history system
        """

        umlFrame: UmlClassDiagramsFrame = self.getGroup().getHistory().getFrame()
        src:      OglClass              = umlFrame.getUmlObjectById(self._linkSrcId)    # type: ignore
        dest:     OglClass              = umlFrame.getUmlObjectById(self._linkDestId)   # type: ignore

        if self._shape is None:
            self._shape = umlFrame.createLink(src=src, dst=dest, linkType=self._linkType)
            umlFrame.GetDiagram().AddShape(shape=self._shape, withModelUpdate=True)

        self._shape.pyutObject.id = self._linkId

        self._shape.GetSource().GetModel().SetPosition(self._srcPosition[0], self._srcPosition[1])          # type: ignore
        self._shape.GetDestination().GetModel().SetPosition(self._destPosition[0], self._destPosition[1])   # type: ignore

        self._shape.GetSource().UpdateFromModel()
        self._shape.GetDestination().UpdateFromModel()
        umlFrame    .Refresh()

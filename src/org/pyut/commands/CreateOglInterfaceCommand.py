
from typing import Tuple

from logging import Logger
from logging import getLogger

from org.pyut.MiniOgl.SelectAnchorPoint import SelectAnchorPoint
from org.pyut.enums.PyutAttachmentPoint import PyutAttachmentPoint
from org.pyut.model.PyutInterface import PyutInterface

from org.pyut.ogl.OglClass import OglClass

from org.pyut.commands.Command import Command
from org.pyut.ogl.OglInterface2 import OglInterface2
from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame


class CreateOglInterfaceCommand(Command):

    def __init__(self,  destinationClass: OglClass, attachmentAnchor: SelectAnchorPoint):

        super().__init__()
        self.logger: Logger = getLogger(__name__)

        self._createLollipopInterface(destinationClass, attachmentAnchor)

    def execute(self):
        self.redo()

    def _createLollipopInterface(self, destinationClass: OglClass, attachmentAnchor: SelectAnchorPoint):

        from org.pyut.general.Mediator import getMediator
        from org.pyut.general.Mediator import Mediator

        pyutInterface: PyutInterface = PyutInterface(name='Sin Nombre')
        oglInterface:  OglInterface2 = OglInterface2(pyutInterface, attachmentAnchor)

        anchorPosition: Tuple[float, float] = attachmentAnchor.GetPosition()
        self.logger.info(f'anchorPosition: {anchorPosition}')
        x = anchorPosition[0]
        y = anchorPosition[1]

        med:      Mediator              = getMediator()
        umlFrame: UmlClassDiagramsFrame = med.getFileHandling().getCurrentFrame()

        umlFrame.addShape(oglInterface, x, y, withModelUpdate=True)
        umlFrame.Refresh()

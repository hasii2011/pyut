
from typing import Tuple

from logging import Logger
from logging import getLogger

from org.pyut.miniogl.SelectAnchorPoint import SelectAnchorPoint
from org.pyut.model.PyutInterface import PyutInterface

from org.pyut.commands.Command import Command
from org.pyut.ogl.OglInterface2 import OglInterface2
from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame


class CreateOglInterfaceCommand(Command):

    def __init__(self,  pyutInterface: PyutInterface, attachmentAnchor: SelectAnchorPoint):

        super().__init__()
        self.logger: Logger = getLogger(__name__)

        self._createLollipopInterface(pyutInterface, attachmentAnchor)

    def execute(self):
        self.redo()

    def _createLollipopInterface(self, pyutInterface: PyutInterface, attachmentAnchor: SelectAnchorPoint):

        from org.pyut.ui.Mediator import Mediator

        oglInterface:  OglInterface2 = OglInterface2(pyutInterface, attachmentAnchor)

        anchorPosition: Tuple[float, float] = attachmentAnchor.GetPosition()
        self.logger.info(f'anchorPosition: {anchorPosition}')
        x = anchorPosition[0]
        y = anchorPosition[1]

        med:      Mediator              = Mediator()
        umlFrame: UmlClassDiagramsFrame = med.getFileHandling().getCurrentFrame()

        umlFrame.addShape(oglInterface, x, y, withModelUpdate=True)
        umlFrame.Refresh()
